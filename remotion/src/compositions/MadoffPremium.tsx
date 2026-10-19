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
import {BrandEndcard, BrandOpening, ENDCARD_SEC} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {Particles, Vignette, LightSweep} from '../components/Motion';
import {finalShotsFor} from './madoffFinalShots';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const BLUE = BRAND.color.electric;

type SceneKind =
  | 'hookLine'
  | 'openingTrust'
  | 'trust'
  | 'club'
  | 'noTrades'
  | 'ponzi'
  | 'numbers'
  | 'math'
  | 'warnings'
  | 'collapse'
  | 'court'
  | 'sentence'
  | 'recovery'
  | 'lesson';

type Scene = {
  id: string;
  kind: SceneKind;
  start: number;
  dur: number;
  title?: string;
  subtitle?: string;
  bg?: string;
};

const OPENING_AT = 14.2;
const MADOFF_OPENING_SEC = 5.34;

const scenes: Scene[] = [
  {id: 's01', kind: 'hookLine', start: 0, dur: 14.236, title: 'Look at this line'},
  {id: 'opening', kind: 'openingTrust', start: OPENING_AT, dur: MADOFF_OPENING_SEC},
  {id: 's02', kind: 'openingTrust', start: 19.924, dur: 53.488, title: 'A trusted name. A perfect chart.'},
  {id: 's03', kind: 'trust', start: 73.762, dur: 28.564, title: 'The name you could trust'},
  {id: 's04', kind: 'club', start: 102.676, dur: 43.657, title: 'Invite only'},
  {id: 's05', kind: 'trust', start: 146.683, dur: 41.059, title: 'The hard questions melted away'},
  {id: 's06', kind: 'noTrades', start: 188.092, dur: 24.038, title: 'No real trades'},
  {id: 's07', kind: 'ponzi', start: 212.48, dur: 51.019, title: 'The hidden loop'},
  {id: 's08', kind: 'numbers', start: 263.849, dur: 54.667, title: '$65B was paper'},
  {id: 's09', kind: 'ponzi', start: 318.866, dur: 21.805, title: 'The math could not stop'},
  {id: 's10', kind: 'math', start: 341.021, dur: 48.744, title: 'Too smooth to be real'},
  {id: 's11', kind: 'warnings', start: 390.115, dur: 78.654, title: 'Warnings ignored'},
  {id: 's12', kind: 'collapse', start: 469.119, dur: 44.986, title: '2008'},
  {id: 's13', kind: 'court', start: 514.455, dur: 11.053, title: 'Guilty'},
  {id: 's14', kind: 'sentence', start: 525.858, dur: 18.601, title: '150 years'},
  {id: 's15', kind: 'recovery', start: 544.809, dur: 24.938, title: 'Recovery'},
  {id: 's16', kind: 'lesson', start: 570.097, dur: 80.54, title: 'Too smooth is the warning'},
  {id: 's17', kind: 'lesson', start: 650.637, dur: 60.363},
  {id: 'end', kind: 'lesson', start: 711, dur: ENDCARD_SEC},
];

const shotsFor = finalShotsFor as unknown as Partial<Record<SceneKind, string[]>>;

const SoftBg: React.FC<{kind: SceneKind}> = ({kind}) => {
  const f = useCurrentFrame();
  const shots = shotsFor[kind] ?? [];
  const shotFrames = Math.round(FPS * 6);
  const fadeFrames = Math.round(FPS * 0.55);
  const idx = shots.length > 0 ? Math.floor(f / shotFrames) % shots.length : 0;
  const nextIdx = shots.length > 0 ? (idx + 1) % shots.length : 0;
  const local = f % shotFrames;
  const progress = local / shotFrames;
  const cross = interpolate(local, [shotFrames - fadeFrames, shotFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const scale = interpolate(progress, [0, 1], [1.025, 1.058]);
  const pan = idx % 2 === 0 ? -10 + progress * 20 : 10 - progress * 20;
  const current = shots[idx];
  const next = shots[nextIdx];
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {current ? (
        <>
          <Img
            src={staticFile(current)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              opacity: 1 - cross,
              transform: `translate3d(${pan}px, 0, 0) scale(${scale})`,
              filter: 'brightness(0.74) contrast(1.11) saturate(0.96)',
            }}
          />
          {next ? (
            <Img
              src={staticFile(next)}
              style={{
                position: 'absolute',
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                opacity: cross,
                transform: `translate3d(${-pan}px, 0, 0) scale(${1.025 + cross * 0.01})`,
                filter: 'brightness(0.74) contrast(1.11) saturate(0.96)',
              }}
            />
          ) : null}
        </>
      ) : (
        <AbsoluteFill style={{background: `radial-gradient(100% 90% at 55% 35%, #1b2230 0%, ${INK} 78%)`}} />
      )}
      <AbsoluteFill style={{background: `linear-gradient(to bottom, ${INK}BB 0%, #00000022 40%, ${INK}DD 100%)`}} />
      <Particles seed={kind} count={14} color={GOLD} />
      <Vignette strength={1} />
    </AbsoluteFill>
  );
};

const Label: React.FC<{title?: string; sub?: string}> = ({title, sub}) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 22, 120, 150], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (!title) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'flex-start', padding: '46px 58px', opacity}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 15, letterSpacing: 4, color: GOLD, fontWeight: 800}}>PRIME DOCUMENTARY</div>
      <div style={{width: 210, height: 2, background: GOLD, marginTop: 9}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: 44, color: WHITE, marginTop: 22, textTransform: 'uppercase', textShadow: '0 3px 20px #000', maxWidth: 760, lineHeight: 1.02}}>
        {title}
      </div>
      {sub ? <div style={{fontFamily: BRAND.font.body, fontSize: 21, color: SILVER, marginTop: 8}}>{sub}</div> : null}
    </AbsoluteFill>
  );
};

const ReturnLine: React.FC<{compare?: boolean; annotate?: boolean}> = ({compare, annotate}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = interpolate(frame, [8, 95], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const warn = spring({frame: frame - 95, fps, config: {damping: 14, stiffness: 70}});
  const points = Array.from({length: 80}).map((_, i) => {
    const t = i / 79;
    const x = 260 + t * 1400;
    const y = 760 - (0.16 + t * 0.69 + Math.sin(t * 5) * 0.012) * 420;
    return `${x},${y}`;
  });
  const jagged = Array.from({length: 80}).map((_, i) => {
    const t = i / 79;
    const x = 260 + t * 1400;
    const y = 760 - (0.24 + t * 0.52 + Math.sin(t * 35) * 0.08) * 420;
    return `${x},${y}`;
  });
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity={0.45}>
        {[0, 1, 2, 3, 4].map((i) => <line key={`h${i}`} x1="260" x2="1660" y1={340 + i * 105} y2={340 + i * 105} stroke="#6d654f" strokeWidth="2" />)}
        {[0, 1, 2, 3, 4, 5].map((i) => <line key={`v${i}`} x1={260 + i * 280} x2={260 + i * 280} y1="330" y2="780" stroke="#6d654f" strokeWidth="2" />)}
      </g>
      {compare ? (
        <polyline points={jagged.join(' ')} fill="none" stroke={BLUE} strokeWidth="6" opacity="0.85" />
      ) : null}
      <polyline
        points={points.slice(0, Math.max(2, Math.floor(points.length * draw))).join(' ')}
        fill="none"
        stroke={GOLD}
        strokeWidth="9"
        strokeLinecap="round"
        strokeLinejoin="round"
        filter="drop-shadow(0px 0px 12px #e5b53a)"
      />
      {annotate ? (
        <g opacity={Math.min(warn, 1)}>
          <circle cx="1180" cy="430" r="95" fill="none" stroke="#d43f2e" strokeWidth="7" />
          <text x="1260" y="360" fill="#f8d682" fontSize="42" fontFamily="Impact">TOO SMOOTH</text>
        </g>
      ) : null}
    </svg>
  );
};

const HookLine: React.FC = () => (
  <AbsoluteFill>
    <ReturnLine />
  </AbsoluteFill>
);

const PonziLoop: React.FC = () => {
  const f = useCurrentFrame();
  const spin = f * 0.35;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g transform={`translate(960 560) rotate(${spin})`}>
        {[0, 45, 90, 135, 180, 225, 270, 315].map((a) => {
          const r = 280;
          const x = Math.cos((a * Math.PI) / 180) * r;
          const y = Math.sin((a * Math.PI) / 180) * r;
          return <circle key={a} cx={x} cy={y} r="34" fill={GOLD} stroke="#fff0ad" strokeWidth="4" />;
        })}
        <circle cx="0" cy="0" r="285" fill="none" stroke={GOLD} strokeWidth="8" strokeDasharray="34 18" />
      </g>
    </svg>
  );
};

const NumberMorph: React.FC = () => {
  const f = useCurrentFrame();
  const t = interpolate(f, [20, 100], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const left = interpolate(t, [0, 1], [1, 0.55]);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 70}}>
        <div style={{transform: `scale(${left})`, opacity: interpolate(t, [0, 1], [1, 0.55])}}>
          <div style={{fontFamily: BRAND.font.display, fontSize: 150, color: GOLD}}>$65B</div>
          <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: SILVER, textAlign: 'center'}}>on statements</div>
        </div>
        <div style={{width: 280, height: 6, background: GOLD}} />
        <div style={{opacity: t}}>
          <div style={{fontFamily: BRAND.font.display, fontSize: 130, color: WHITE}}>$17.5B</div>
          <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: SILVER, textAlign: 'center'}}>real principal</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const WarningTimeline: React.FC = () => {
  const f = useCurrentFrame();
  const years = ['2000', '2001', '2005', '2007', '2008'];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="300" x2="1620" y1="590" y2="590" stroke={GOLD} strokeWidth="6" />
      {years.map((y, i) => {
        const on = interpolate(f, [i * 18, i * 18 + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const x = 300 + i * 330;
        return (
          <g key={y} opacity={on}>
            <circle cx={x} cy="590" r="24" fill={GOLD} />
            <text x={x} y="515" fill={WHITE} fontSize="48" fontFamily="Impact" textAnchor="middle">{y}</text>
            <text x={x} y="675" fill={SILVER} fontSize="28" fontFamily="Trebuchet MS" textAnchor="middle">warning</text>
          </g>
        );
      })}
    </svg>
  );
};

const SceneView: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.id === 'end') return <BrandEndcard />;
  if (scene.kind === 'openingTrust' && scene.id === 'opening') {
    return <BrandOpening seriesLabel="Prime Documentary" title="Madoff" subtitle="The Perfect Line" />;
  }
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <SoftBg kind={scene.kind} />
      <LightSweep seed={scene.id} />
      {scene.kind === 'hookLine' ? <HookLine /> : null}
      {scene.kind === 'ponzi' ? <PonziLoop /> : null}
      {scene.kind === 'numbers' || scene.kind === 'recovery' ? <NumberMorph /> : null}
      {scene.kind === 'math' || scene.kind === 'lesson' ? <ReturnLine compare annotate /> : null}
      {scene.kind === 'warnings' ? <WarningTimeline /> : null}
      {scene.kind === 'sentence' ? (
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
          <div style={{fontFamily: BRAND.font.display, fontSize: 190, color: GOLD, textShadow: '0 8px 30px #000'}}>150 YEARS</div>
        </AbsoluteFill>
      ) : null}
      <Label title={scene.title} sub={scene.subtitle} />
      <Grain opacity={0.035} />
    </AbsoluteFill>
  );
};

export const MadoffPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    {scenes.map((s) => (
      <Sequence key={s.id} from={Math.round(s.start * FPS)} durationInFrames={Math.round(s.dur * FPS)}>
        <SceneView scene={s} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const madoffPremiumDurationInFrames = (fps: number): number => Math.round(720 * fps);

