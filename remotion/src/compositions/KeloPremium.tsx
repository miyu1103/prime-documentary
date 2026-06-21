import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  Video,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {BrandEndcard, BrandOpening, ENDCARD_SEC, OPENING_SEC} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {LightSweep, Particles, Vignette} from '../components/Motion';
import {KELO_CAPTIONS} from '../data/kelo_captions';
import {KELO_ROUGHCUT} from '../data/kelo_roughcut';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Mode =
  | 'parallax'
  | 'publicUse'
  | 'location'
  | 'labelHouse'
  | 'plan'
  | 'turn'
  | 'resistance'
  | 'question'
  | 'twoWords'
  | 'equation'
  | 'stakes'
  | 'ruling'
  | 'purposeMorph'
  | 'dissent'
  | 'kennedy'
  | 'backlash'
  | 'states'
  | 'emptyLot'
  | 'pfizer'
  | 'movingHouse'
  | 'ending'
  | 'next'
  | 'cta';

type PremiumScene = {
  spanId: string;
  start: number;
  dur: number;
  mode: Mode;
  kicker: string;
  title?: string;
  subtitle?: string;
  citation?: string;
  chapter: 'hook' | 'opening' | 'act1' | 'act2' | 'act3' | 'act4' | 'ending';
};

type RoughShot = (typeof KELO_ROUGHCUT.shots)[number];

const shotMap = new Map<string, RoughShot>(KELO_ROUGHCUT.shots.map((shot) => [shot.spanId, shot]));

const getShot = (spanId: string): RoughShot => {
  const shot = shotMap.get(spanId);
  if (!shot) throw new Error(`Missing Kelo roughcut shot ${spanId}`);
  return shot;
};

const bodyScenes: PremiumScene[] = [
  {spanId: 'SPN-0002', start: 31.5, dur: 40.8, mode: 'publicUse', kicker: 'THESIS', title: '5th Amendment', subtitle: 'takings only "for public use"', chapter: 'opening'},
  {spanId: 'SPN-0003', start: 72.3, dur: 13.6, mode: 'location', kicker: 'ACT I', title: 'Fort Trumbull', subtitle: 'New London, Connecticut', chapter: 'act1'},
  {spanId: 'SPN-0004', start: 85.9, dur: 19.6, mode: 'labelHouse', kicker: 'ACT I', title: 'Not blighted', subtitle: 'Owner did nothing wrong.', chapter: 'act1'},
  {spanId: 'SPN-0005', start: 105.5, dur: 18.8, mode: 'plan', kicker: 'ACT I', title: 'The plan', subtitle: 'offices, hotel, jobs, taxes', chapter: 'act1'},
  {spanId: 'SPN-0006', start: 124.3, dur: 21.6, mode: 'turn', kicker: 'ACT I', chapter: 'act1'},
  {spanId: 'SPN-0007', start: 145.9, dur: 24.8, mode: 'resistance', kicker: 'ACT I', title: 'They refuse', subtitle: 'not for more money - for home', chapter: 'act1'},
  {spanId: 'SPN-0008', start: 170.7, dur: 20.8, mode: 'question', kicker: 'THE QUESTION', title: 'Is that "public use"?', chapter: 'act1'},
  {spanId: 'SPN-0009', start: 191.5, dur: 28.0, mode: 'twoWords', kicker: 'ACT II', title: 'Narrow', subtitle: 'the public actually uses it', chapter: 'act2'},
  {spanId: 'SPN-0010', start: 219.5, dur: 21.2, mode: 'twoWords', kicker: 'ACT II', title: 'Broad', subtitle: 'any "public purpose"', chapter: 'act2'},
  {spanId: 'SPN-0011', start: 240.7, dur: 16.8, mode: 'equation', kicker: 'ACT II', title: 'Economic development', subtitle: '= public use?', chapter: 'act2'},
  {spanId: 'SPN-0012', start: 257.5, dur: 26.0, mode: 'stakes', kicker: 'ACT II', title: 'The stakes', subtitle: 'tax value becomes pressure', chapter: 'act2'},
  {spanId: 'SPN-0013', start: 283.5, dur: 13.6, mode: 'parallax', kicker: 'ACT II', title: 'The limit', subtitle: 'whose property can be transferred?', chapter: 'act2'},
  {spanId: 'SPN-0014', start: 297.1, dur: 15.2, mode: 'ruling', kicker: 'ACT III', title: '2005 - 5-4', subtitle: 'Kelo v. New London', citation: '545 U.S. 469 (2005)', chapter: 'act3'},
  {spanId: 'SPN-0015', start: 312.3, dur: 27.2, mode: 'purposeMorph', kicker: 'MAJORITY', title: '"Public use"', subtitle: '= "public purpose"', chapter: 'act3'},
  {spanId: 'SPN-0027', start: 339.5, dur: 19.6, mode: 'kennedy', kicker: 'CONCURRENCE', title: 'Pretext still barred', subtitle: 'a narrow door remains', chapter: 'act3'},
  {spanId: 'SPN-0016', start: 359.1, dur: 39.6, mode: 'dissent', kicker: 'DISSENT', title: '"for public use"', subtitle: 'erased?', chapter: 'act3'},
  {spanId: 'SPN-0017', start: 398.7, dur: 19.2, mode: 'parallax', kicker: 'ACT III', title: 'A split that did not split normally', chapter: 'act3'},
  {spanId: 'SPN-0018', start: 417.9, dur: 18.4, mode: 'backlash', kicker: 'ACT IV', title: 'Backlash', subtitle: 'bipartisan', chapter: 'act4'},
  {spanId: 'SPN-0019', start: 436.3, dur: 29.2, mode: 'states', kicker: 'ACT IV', title: '40+ states', subtitle: 'many reforms criticized as weak', chapter: 'act4'},
  {spanId: 'SPN-0020', start: 465.5, dur: 19.6, mode: 'emptyLot', kicker: 'ACT IV', title: 'The development was never built', chapter: 'act4'},
  {spanId: 'SPN-0021', start: 485.1, dur: 24.8, mode: 'pfizer', kicker: 'ACT IV', title: '2009', subtitle: 'Pfizer leaves New London', chapter: 'act4'},
  {spanId: 'SPN-0022', start: 509.9, dur: 18.4, mode: 'movingHouse', kicker: 'ACT IV', title: 'Moved, not destroyed', subtitle: 'the pink house survives elsewhere', chapter: 'act4'},
  {spanId: 'SPN-0028', start: 528.3, dur: 31.2, mode: 'parallax', kicker: 'ACT IV', title: 'Market value cannot buy back a place', chapter: 'act4'},
  {spanId: 'SPN-0023', start: 559.5, dur: 16.4, mode: 'ending', kicker: 'ENDING', title: 'Kelo is still good law', chapter: 'ending'},
  {spanId: 'SPN-0024', start: 575.9, dur: 17.6, mode: 'ending', kicker: 'ENDING', title: '"Public use" stopped doing much work', chapter: 'ending'},
  {spanId: 'SPN-0025', start: 593.5, dur: 36.4, mode: 'next', kicker: 'NEXT', title: 'Where does free speech end?', chapter: 'ending'},
  {spanId: 'SPN-0026', start: 629.9, dur: 1.6, mode: 'cta', kicker: 'SUBSCRIBE', title: 'Subscribe', chapter: 'ending'},
];

const TOTAL_SEC = 631.5 + ENDCARD_SEC;

const hookBeats = [
  {spanId: 'SPN-0001', label: 'Your home', at: 0, dur: 2.6},
  {spanId: 'SPN-0006', label: 'Condemned', at: 2.6, dur: 2.4},
  {spanId: 'SPN-0014', label: '2005', at: 5.0, dur: 2.4},
  {spanId: 'SPN-0016', label: 'Dissent', at: 7.4, dur: 2.4},
  {spanId: 'SPN-0020', label: 'Empty lot', at: 9.8, dur: 2.7},
  {spanId: 'SPN-0021', label: '2009', at: 12.5, dur: 2.5},
  {spanId: 'SPN-0008', label: 'Public use?', at: 15.0, dur: 2.6},
  {spanId: 'SPN-0027', label: 'Pretext', at: 17.6, dur: 2.5},
  {spanId: 'SPN-0028', label: 'Human cost', at: 20.1, dur: 2.6},
  {spanId: 'SPN-0025', label: 'Next power', at: 22.7, dur: 1.8},
];

const firstImage = (spanId: string): string | null => {
  const shot = getShot(spanId);
  return shot.images?.find((src) => /\.(png|jpe?g|webp)$/i.test(src)) ?? (shot.src && /\.(png|jpe?g|webp)$/i.test(shot.src) ? shot.src : null);
};

const fitTitle = (text: string): number => Math.min(82, Math.max(36, 1360 / Math.max(text.length, 14)));

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = KELO_CAPTIONS.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 210,
        right: 210,
        bottom: 38,
        minHeight: 82,
        padding: '16px 28px',
        background: '#000000D8',
        borderTop: `2px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontSize: cue.text.length > 96 ? 27 : 31,
        lineHeight: 1.18,
        textAlign: 'center',
        textShadow: '0 2px 10px #000',
      }}
    >
      {cue.text}
    </div>
  );
};

const ReconstructionLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 54,
      top: 48,
      fontFamily: BRAND.font.body,
      fontSize: 18,
      color: SILVER,
      padding: '7px 11px',
      border: `1px solid ${GOLD}88`,
      background: '#000000A8',
    }}
  >
    symbolic reconstruction / AI-assisted visuals
  </div>
);

const Lower: React.FC<{scene: PremiumScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 90}});
  if (!scene.title) return null;
  return (
    <div style={{position: 'absolute', left: 58, top: 46, opacity: Math.min(1, enter), maxWidth: 1240}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker}</div>
      <div style={{width: 300, height: 2, background: GOLD, marginTop: 9, marginBottom: 21}} />
      <div
        style={{
          fontFamily: BRAND.font.display,
          fontSize: fitTitle(scene.title),
          color: WHITE,
          textTransform: 'uppercase',
          lineHeight: 0.95,
          textShadow: '0 5px 30px #000',
        }}
      >
        {scene.title}
      </div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 10}}>{scene.subtitle}</div> : null}
      {scene.citation ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: GOLD, marginTop: 14, background: '#000000AA', padding: '7px 11px', display: 'inline-block'}}>
          {scene.citation}
        </div>
      ) : null}
    </div>
  );
};

const StillPlates: React.FC<{scene: PremiumScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const shot = getShot(scene.spanId);
  const images = (shot.images ?? []).filter((src) => /\.(png|jpe?g|webp)$/i.test(src));
  const localFrames = Math.max(1, Math.round(scene.dur * FPS));
  const cutFrames = Math.max(80, Math.round(4.5 * FPS));
  const idx = images.length ? Math.min(images.length - 1, Math.floor(frame / cutFrames) % images.length) : -1;
  const nextIdx = images.length ? (idx + 1) % images.length : -1;
  const slot = frame % cutFrames;
  const cross = images.length > 1 ? interpolate(slot, [cutFrames * 0.72, cutFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const seed = Number(scene.spanId.slice(-2));
  const render = (src: string, index: number, opacity: number, extra = 0) => {
    const p = interpolate(frame - index * 8, [0, localFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const dir = index % 2 === 0 ? 1 : -1;
    return (
      <Img
        src={staticFile(src)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: `${50 + Math.sin(seed + index) * 7}% ${48 + Math.cos(seed + index) * 6}%`,
          opacity,
          transform: `translate3d(${dir * interpolate(p, [0, 1], [-44, 44])}px, ${interpolate(p, [0, 1], [20, -20])}px, 0) scale(${1.055 + p * 0.08 + extra}) rotate(${dir * 0.14}deg)`,
          filter: 'brightness(0.82) contrast(1.17) saturate(1.08)',
        }}
      />
    );
  };
  if (idx < 0) return <AbsoluteFill style={{background: `radial-gradient(95% 80% at 55% 36%, #12365f 0%, ${NAVY} 38%, ${INK} 86%)`}} />;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      {render(images[idx], idx, 1)}
      {images.length > 1 ? render(images[nextIdx], nextIdx, cross, 0.02) : null}
    </AbsoluteFill>
  );
};

const ClipPlates: React.FC<{scene: PremiumScene}> = ({scene}) => {
  const shot = getShot(scene.spanId);
  const clips = shot.clips ?? [];
  if (!clips.length) return <StillPlates scene={scene} />;
  const frame = useCurrentFrame();
  const slotFrames = Math.max(60, Math.round((scene.dur * FPS) / clips.length));
  const idx = Math.min(clips.length - 1, Math.floor(frame / slotFrames));
  const startFrom = Math.round((frame % slotFrames) * 0.25);
  return (
    <Video
      src={staticFile(clips[idx].src)}
      startFrom={startFrom}
      muted
      style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.78) contrast(1.16) saturate(1.05)'}}
    />
  );
};

const SceneBase: React.FC<{scene: PremiumScene; children?: React.ReactNode}> = ({scene, children}) => {
  const shot = getShot(scene.spanId);
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {shot.assetType === 'stock_video' ? <ClipPlates scene={scene} /> : <StillPlates scene={scene} />}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}C8 0%, #00000016 45%, ${INK}D8 100%)`}} />
      <LightSweep seed={scene.spanId} color={scene.mode === 'ruling' || scene.mode === 'pfizer' ? GOLD : BLUE} />
      <Particles seed={scene.spanId} count={18} color={scene.mode === 'ruling' ? GOLD : BLUE} />
      {children}
      <Lower scene={scene} />
      <ReconstructionLabel />
      <Vignette strength={0.9} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string}> = ({left, right, leftSub, rightSub}) => (
  <div style={{position: 'absolute', left: 250, right: 250, top: 370, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 44}}>
    {[
      {title: left, sub: leftSub, color: BLUE},
      {title: right, sub: rightSub, color: GOLD},
    ].map((box) => (
      <div key={box.title} style={{minHeight: 250, border: `3px solid ${box.color}`, background: '#020409CC', padding: 34}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 62, color: box.color, textTransform: 'uppercase'}}>{box.title}</div>
        {box.sub ? <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: SILVER, marginTop: 20}}>{box.sub}</div> : null}
      </div>
    ))}
  </div>
);

const PlanDoors: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['offices', 'hotel', 'jobs', 'taxes'];
  return (
    <div style={{position: 'absolute', left: 220, right: 220, top: 385, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 26}}>
      {labels.map((label, i) => {
        const on = spring({frame: frame - i * 12, fps: FPS, config: {damping: 18, stiffness: 80}});
        return (
          <div key={label} style={{height: 250, border: `3px solid ${i % 2 ? GOLD : BLUE}`, background: '#05070AD8', opacity: Math.min(1, on), transform: `translateY(${interpolate(on, [0, 1], [36, 0])}px)`}}>
            <div style={{fontFamily: BRAND.font.display, color: i % 2 ? GOLD : WHITE, fontSize: 44, textTransform: 'uppercase', padding: 24}}>{label}</div>
            <div style={{position: 'absolute', left: 22, right: 22, bottom: 28, height: 5, background: i % 2 ? BLUE : GOLD}} />
          </div>
        );
      })}
    </div>
  );
};

const LocationMap: React.FC = () => {
  const frame = useCurrentFrame();
  const ripple = (frame % 54) / 54;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M620 350 q160 -85 370 -45 q200 -25 350 70 q-55 175 -250 210 q-230 86 -470 -18 q-150 -35 -160 -150 z" fill={`${BLUE}22`} stroke={BLUE} strokeWidth="4" />
      <circle cx="1000" cy="478" r={16 + ripple * 66} fill="none" stroke={GOLD} strokeWidth="4" opacity={0.7 - ripple * 0.7} />
      <circle cx="1000" cy="478" r="13" fill={GOLD} />
      <text x="1040" y="468" fill={WHITE} fontFamily={BRAND.font.display} fontSize="54">CT</text>
      <text x="1040" y="524" fill={SILVER} fontFamily={BRAND.font.body} fontSize="30">New London - Fort Trumbull</text>
    </svg>
  );
};

const PublicUseUnderline: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [20, 58], [0, 500], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 300, right: 300, top: 390, textAlign: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 94, color: WHITE, textTransform: 'uppercase', textShadow: '0 4px 32px #000'}}>for public use</div>
      <div style={{width: w, height: 7, background: GOLD, margin: '22px auto 0', boxShadow: `0 0 18px ${GOLD}`}} />
    </div>
  );
};

const QuestionMark: React.FC = () => {
  const frame = useCurrentFrame();
  const punch = spring({frame: frame - 8, fps: FPS, config: {damping: 9, stiffness: 140}});
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 250, color: GOLD, transform: `scale(${0.82 + punch * 0.18})`, textShadow: `0 0 46px ${GOLD}`}}>?</div>
    </div>
  );
};

const Equation: React.FC = () => (
  <div style={{position: 'absolute', left: 280, right: 280, top: 430, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 40}}>
    {['economic development', '=', 'public use'].map((text, i) => (
      <div key={text} style={{fontFamily: BRAND.font.display, fontSize: i === 1 ? 112 : 58, color: i === 1 ? GOLD : WHITE, textTransform: 'uppercase', textAlign: 'center'}}>{text}</div>
    ))}
  </div>
);

const Vote: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="360" y1="370" x2="1560" y2="370" stroke={SILVER} strokeWidth="4" opacity="0.35" />
      <circle cx="960" cy="370" r="16" fill={GOLD} />
      <text x="960" y="330" fill={GOLD} fontFamily={BRAND.font.display} fontSize="70" textAnchor="middle">2005</text>
      <g transform="translate(570 455)">
        {Array.from({length: 9}, (_, i) => {
          const on = spring({frame: frame - i * 5, fps: FPS, config: {damping: 16, stiffness: 95}});
          const yes = i < 5;
          return <rect key={i} x={(i % 5) * 145} y={Math.floor(i / 5) * 135} width="92" height="92" rx="10" fill={yes ? BLUE : '#333844'} stroke={yes ? GOLD : SILVER} strokeWidth="4" opacity={Math.min(1, on)} />;
        })}
        <text x="355" y="315" fill={WHITE} fontFamily={BRAND.font.display} fontSize="110" textAnchor="middle">5-4</text>
      </g>
      <rect x="680" y="820" width="560" height="72" fill="#000000AA" stroke={GOLD} strokeWidth="3" />
      <text x="960" y="868" fill={GOLD} fontFamily={BRAND.font.body} fontSize="32" textAnchor="middle">Kelo v. New London, 545 U.S. 469</text>
    </svg>
  );
};

const PurposeMorph: React.FC = () => {
  const frame = useCurrentFrame();
  const merge = interpolate(frame, [20, 92], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{position: 'absolute', left: interpolate(merge, [0, 1], [280, 540]), top: 440, fontFamily: BRAND.font.display, fontSize: 72, color: WHITE, textTransform: 'uppercase'}}>"public use"</div>
      <div style={{position: 'absolute', right: interpolate(merge, [0, 1], [250, 515]), top: 545, fontFamily: BRAND.font.display, fontSize: 72, color: GOLD, textTransform: 'uppercase'}}>"public purpose"</div>
      <div style={{position: 'absolute', left: 900, top: 505, fontFamily: BRAND.font.display, fontSize: 110, color: SILVER, opacity: merge}}>=</div>
    </div>
  );
};

const StrikeText: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [36, 78], [0, 640], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 520, top: 470}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 86, color: WHITE, textTransform: 'uppercase'}}>"for public use"</div>
      <div style={{height: 8, width: w, background: '#D43F2E', transform: 'translateY(-52px) rotate(-3deg)', boxShadow: '0 0 20px #D43F2E'}} />
    </div>
  );
};

const KennedyNote: React.FC = () => (
  <div style={{position: 'absolute', right: 210, top: 310, width: 480, minHeight: 430, borderLeft: `5px solid ${GOLD}`, background: '#020409D8', padding: 34}}>
    <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: GOLD, fontWeight: 800}}>NOTE COLUMN</div>
    <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: WHITE, textTransform: 'uppercase', marginTop: 18}}>Pretextual takings</div>
    <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: SILVER, marginTop: 18, lineHeight: 1.18}}>Still barred if the public purpose is merely a cover.</div>
  </div>
);

const BacklashArrows: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <path d="M400 560 C620 420 760 420 910 540" fill="none" stroke={BLUE} strokeWidth="12" strokeLinecap="round" />
    <path d="M1520 560 C1300 420 1160 420 1010 540" fill="none" stroke={GOLD} strokeWidth="12" strokeLinecap="round" />
    <circle cx="960" cy="560" r="58" fill="#000000AA" stroke={SILVER} strokeWidth="4" />
    <text x="960" y="578" fill={WHITE} fontFamily={BRAND.font.display} fontSize="42" textAnchor="middle">AGAINST</text>
  </svg>
);

const StatesCounter: React.FC = () => {
  const frame = useCurrentFrame();
  const count = Math.round(interpolate(frame, [20, 150], [0, 40], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M410 360 q180 -90 450 -55 q270 -40 530 80 q-65 190 -330 245 q-310 100 -650 -30 q-170 -40 -175 -165 z" fill={`${BLUE}22`} stroke={BLUE} strokeWidth="4" />
      {Array.from({length: 44}, (_, i) => {
        const on = i < count;
        const x = 470 + ((i * 97) % 940);
        const y = 410 + ((i * 53) % 250);
        return <circle key={i} cx={x} cy={y} r={on ? 8 : 4} fill={on ? GOLD : SILVER} opacity={on ? 0.95 : 0.18} />;
      })}
      <text x="960" y="790" fill={GOLD} fontFamily={BRAND.font.display} fontSize="150" textAnchor="middle">{count}+</text>
      <text x="960" y="842" fill={SILVER} fontFamily={BRAND.font.body} fontSize="30" textAnchor="middle">states with reforms or amendments</text>
    </svg>
  );
};

const PfizerTimeline: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <line x1="430" y1="560" x2="1490" y2="560" stroke={SILVER} strokeWidth="5" opacity="0.6" />
    <circle cx="760" cy="560" r="18" fill={BLUE} />
    <circle cx="1160" cy="560" r="22" fill={GOLD} />
    <text x="760" y="500" fill={WHITE} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">2005</text>
    <text x="1160" y="500" fill={GOLD} fontFamily={BRAND.font.display} fontSize="72" textAnchor="middle">2009</text>
    <text x="1160" y="635" fill={SILVER} fontFamily={BRAND.font.body} fontSize="32" textAnchor="middle">Pfizer leaves</text>
  </svg>
);

const MovingHouse: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [20, 140], [560, 1130], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="460" y1="705" x2="1450" y2="705" stroke={SILVER} strokeWidth="5" opacity="0.35" />
      <g transform={`translate(${x} 535)`}>
        <rect x="-110" y="80" width="220" height="120" fill="#eaa0aa" stroke={GOLD} strokeWidth="4" />
        <path d="M-130 82 L0 -28 L130 82 Z" fill="#5c1d28" stroke={GOLD} strokeWidth="4" />
        <rect x="-25" y="126" width="50" height="74" fill="#111" />
      </g>
    </svg>
  );
};

const SubscribeButton: React.FC = () => {
  const frame = useCurrentFrame();
  const pop = spring({frame, fps: FPS, config: {damping: 10, stiffness: 160}});
  return (
    <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 82, color: INK, background: GOLD, padding: '28px 58px', transform: `scale(${0.82 + pop * 0.18})`, boxShadow: `0 0 42px ${GOLD}`}}>SUBSCRIBE</div>
    </div>
  );
};

const SceneOverlay: React.FC<{scene: PremiumScene}> = ({scene}) => {
  if (scene.mode === 'publicUse') return <PublicUseUnderline />;
  if (scene.mode === 'location') return <LocationMap />;
  if (scene.mode === 'plan') return <PlanDoors />;
  if (scene.mode === 'question') return <QuestionMark />;
  if (scene.mode === 'twoWords') return <TwoColumn left="Narrow" right="Broad" leftSub="public actually uses it" rightSub="public purpose" />;
  if (scene.mode === 'equation') return <Equation />;
  if (scene.mode === 'ruling') return <Vote />;
  if (scene.mode === 'purposeMorph') return <PurposeMorph />;
  if (scene.mode === 'dissent') return <StrikeText />;
  if (scene.mode === 'kennedy') return <KennedyNote />;
  if (scene.mode === 'backlash') return <BacklashArrows />;
  if (scene.mode === 'states') return <StatesCounter />;
  if (scene.mode === 'pfizer') return <PfizerTimeline />;
  if (scene.mode === 'movingHouse') return <MovingHouse />;
  if (scene.mode === 'cta') return <SubscribeButton />;
  return null;
};

const HookBeat: React.FC<{spanId: string; label: string}> = ({spanId, label}) => {
  const image = firstImage(spanId);
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 75], [1.03, 1.11], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {image ? <Img src={staticFile(image)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.72) contrast(1.24) saturate(1.08)', transform: `scale(${zoom})`}} /> : null}
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}E8 0%, #00000033 58%, ${INK}96 100%)`}} />
      <div style={{position: 'absolute', left: 74, bottom: 170, fontFamily: BRAND.font.display, color: WHITE, fontSize: 76, textTransform: 'uppercase', textShadow: '0 5px 28px #000'}}>{label}</div>
      <div style={{position: 'absolute', left: 76, bottom: 144, width: 280, height: 4, background: GOLD}} />
      <Particles seed={`hook-${spanId}`} count={10} color={GOLD} />
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

const HookMontage: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    {hookBeats.map((beat) => (
      <Sequence key={beat.spanId} from={Math.round(beat.at * FPS)} durationInFrames={Math.round(beat.dur * FPS)}>
        <HookBeat spanId={beat.spanId} label={beat.label} />
      </Sequence>
    ))}
    <div style={{position: 'absolute', left: 58, top: 46, fontFamily: BRAND.font.body, color: GOLD, fontWeight: 800, fontSize: 18}}>HOOK</div>
    <div style={{position: 'absolute', left: 58, top: 78, width: 260, height: 2, background: GOLD}} />
  </AbsoluteFill>
);

const SceneView: React.FC<{scene: PremiumScene}> = ({scene}) => (
  <SceneBase scene={scene}>
    <SceneOverlay scene={scene} />
  </SceneBase>
);

export const KeloPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={Math.round(24.5 * FPS)} name="PART_1_HOOK">
      <HookMontage />
    </Sequence>
    <Sequence from={Math.round(24.5 * FPS)} durationInFrames={Math.round(OPENING_SEC * FPS)} name="PART_2_BRAND_OPENING">
      <BrandOpening seriesLabel="Landmark Rights Cases" title="Kelo v. New London" subtitle="Your home - for a private developer?" />
    </Sequence>
    {bodyScenes.map((scene) => (
      <Sequence key={scene.spanId} from={Math.round(scene.start * FPS)} durationInFrames={Math.round(scene.dur * FPS)} name={`${scene.chapter}_${scene.spanId}`}>
        <SceneView scene={scene} />
      </Sequence>
    ))}
    <Sequence from={Math.round(631.5 * FPS)} durationInFrames={Math.round(ENDCARD_SEC * FPS)} name="PART_4_BRAND_ENDCARD">
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile('kelo/audio/kelo_final_mix_v001.mp3')} />
    <CaptionBand />
  </AbsoluteFill>
);

export const keloPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
