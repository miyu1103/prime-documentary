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
import {MAHANOY_CAPTIONS} from '../data/mahanoy_captions';
import {MAHANOY_ROUGHCUT} from '../data/mahanoy_roughcut';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#D9483B';
const TOTAL_SEC = 720;
const HOOK_SEC = 28;
const BODY_START = HOOK_SEC + OPENING_SEC;
const BODY_TARGET_SEC = TOTAL_SEC - BODY_START - ENDCARD_SEC;
const SOURCE_BODY_SEC = 576.8;
const BODY_SCALE = BODY_TARGET_SEC / SOURCE_BODY_SEC;

type Mode =
  | 'post'
  | 'gateQuote'
  | 'map'
  | 'disappointment'
  | 'snap'
  | 'vanish'
  | 'suspension'
  | 'conflict'
  | 'ordinary'
  | 'armband'
  | 'timeline'
  | 'standard'
  | 'place'
  | 'dissolveGate'
  | 'clock'
  | 'ruling'
  | 'breyer'
  | 'scales'
  | 'nursery'
  | 'exceptions'
  | 'dissent'
  | 'boundary'
  | 'doors'
  | 'theme'
  | 'recap'
  | 'series'
  | 'next'
  | 'cta';

type PremiumScene = {
  spanId: string;
  sourceSeconds: number;
  mode: Mode;
  kicker: string;
  title?: string;
  subtitle?: string;
  citation?: string;
  chapter: 'hook' | 'opening' | 'act1' | 'act2' | 'act3' | 'act4' | 'ending';
};

type TimedScene = PremiumScene & {start: number; dur: number};
type RoughShot = (typeof MAHANOY_ROUGHCUT.shots)[number];

const shotMap = new Map<string, RoughShot>(MAHANOY_ROUGHCUT.shots.map((shot) => [shot.spanId, shot]));
const getShot = (spanId: string): RoughShot => {
  const shot = shotMap.get(spanId);
  if (!shot) throw new Error(`Missing Mahanoy roughcut shot ${spanId}`);
  return shot;
};

const bodySceneDefs: PremiumScene[] = [
  {spanId: 'SPN-0002', sourceSeconds: 41.6, mode: 'gateQuote', kicker: 'OPENING', title: '"Schoolhouse gate"', subtitle: 'Tinker, 1969', citation: 'Tinker v. Des Moines, 393 U.S. 503 (1969)', chapter: 'opening'},
  {spanId: 'SPN-0003', sourceSeconds: 10.4, mode: 'map', kicker: 'ACT I', title: 'Mahanoy, PA - 2017', chapter: 'act1'},
  {spanId: 'SPN-0004', sourceSeconds: 14.8, mode: 'disappointment', kicker: 'ACT I', title: 'JV stays. Varsity moves.', subtitle: 'a small decision that stings', chapter: 'act1'},
  {spanId: 'SPN-0005', sourceSeconds: 30.0, mode: 'snap', kicker: 'ACT I', title: '[caption censored]', subtitle: 'off campus - weekend - own phone', chapter: 'act1'},
  {spanId: 'SPN-0006', sourceSeconds: 22.8, mode: 'vanish', kicker: 'TURN', title: 'Snaps disappear. Screenshots do not.', chapter: 'act1'},
  {spanId: 'SPN-0028', sourceSeconds: 17.6, mode: 'ordinary', kicker: 'ACT I', title: 'No threat. No target. No plan.', chapter: 'act1'},
  {spanId: 'SPN-0007', sourceSeconds: 12.8, mode: 'suspension', kicker: 'ACT I', title: 'Suspended from JV cheer', subtitle: 'one year', chapter: 'act1'},
  {spanId: 'SPN-0008', sourceSeconds: 25.2, mode: 'conflict', kicker: 'THE QUESTION', title: "School's order vs. a student's voice", chapter: 'act1'},
  {spanId: 'SPN-0026', sourceSeconds: 21.6, mode: 'armband', kicker: 'ACT II', title: '1965', subtitle: 'black armbands to mourn the war dead', chapter: 'act2'},
  {spanId: 'SPN-0009', sourceSeconds: 15.6, mode: 'timeline', kicker: 'ACT II', title: 'Tinker v. Des Moines', subtitle: '1969', citation: '393 U.S. 503 (1969)', chapter: 'act2'},
  {spanId: 'SPN-0010', sourceSeconds: 19.6, mode: 'standard', kicker: 'TEST', title: '"substantial disruption"', subtitle: 'not mere discomfort', chapter: 'act2'},
  {spanId: 'SPN-0011', sourceSeconds: 12.8, mode: 'place', kicker: 'ACT II', title: 'For fifty years, the test had a place', chapter: 'act2'},
  {spanId: 'SPN-0012', sourceSeconds: 27.6, mode: 'dissolveGate', kicker: 'CENTER METAPHOR', title: 'The phone erased the gate', chapter: 'act2'},
  {spanId: 'SPN-0013', sourceSeconds: 25.6, mode: 'clock', kicker: 'THE DANGER', title: '24 hours. Anywhere.', subtitle: 'no natural stopping point', chapter: 'act2'},
  {spanId: 'SPN-0014', sourceSeconds: 14.0, mode: 'ruling', kicker: 'RULING', title: '2021 - 8-1', subtitle: 'Mahanoy v. B.L.', citation: '594 U.S. 180 (2021)', chapter: 'act3'},
  {spanId: 'SPN-0015', sourceSeconds: 27.6, mode: 'breyer', kicker: 'MAJORITY', title: 'Off campus, school power is weaker', chapter: 'act3'},
  {spanId: 'SPN-0027', sourceSeconds: 22.4, mode: 'nursery', kicker: 'BREYER', title: '"nurseries of democracy"', chapter: 'act3'},
  {spanId: 'SPN-0016', sourceSeconds: 16.8, mode: 'scales', kicker: 'FACTS', title: 'A few minutes of class chatter', subtitle: 'not substantial disruption', chapter: 'act3'},
  {spanId: 'SPN-0017', sourceSeconds: 29.2, mode: 'exceptions', kicker: 'LIMITS', title: 'Still reachable', subtitle: 'bullying - threats - cheating', chapter: 'act3'},
  {spanId: 'SPN-0018', sourceSeconds: 27.2, mode: 'dissent', kicker: 'DISSENT', title: 'Thomas, J. alone', subtitle: 'one vote the other way', chapter: 'act3'},
  {spanId: 'SPN-0019', sourceSeconds: 20.0, mode: 'boundary', kicker: 'ACT IV', title: 'Real protection. Fuzzy line.', chapter: 'act4'},
  {spanId: 'SPN-0020', sourceSeconds: 20.4, mode: 'doors', kicker: 'ACT IV', title: 'Not a wall', subtitle: 'serious cases remain open', chapter: 'act4'},
  {spanId: 'SPN-0021', sourceSeconds: 24.8, mode: 'theme', kicker: 'THE POINT', title: 'Free speech is tested by speech we dislike', chapter: 'act4'},
  {spanId: 'SPN-0022', sourceSeconds: 19.6, mode: 'recap', kicker: 'ENDING', title: 'The school could reach a lot.', subtitle: 'It could not reach everything.', chapter: 'ending'},
  {spanId: 'SPN-0023', sourceSeconds: 32.0, mode: 'series', kicker: 'SERIES LINE', title: 'Search. Track. Take. Speak.', subtitle: 'the edge keeps moving', chapter: 'ending'},
  {spanId: 'SPN-0024', sourceSeconds: 23.2, mode: 'next', kicker: 'NEXT', title: 'The right you sign away', subtitle: 'contracts, clicks, arbitration', chapter: 'ending'},
  {spanId: 'SPN-0025', sourceSeconds: 1.6, mode: 'cta', kicker: 'SUBSCRIBE', title: 'Subscribe', chapter: 'ending'},
];

let cursor = BODY_START;
const bodyScenes: TimedScene[] = bodySceneDefs.map((scene) => {
  const dur = scene.sourceSeconds * BODY_SCALE;
  const timed = {...scene, start: cursor, dur};
  cursor += dur;
  return timed;
});

const hookBeats = [
  {spanId: 'SPN-0001', label: 'Weekend post', at: 0, dur: 2.8},
  {spanId: 'SPN-0006', label: 'Screenshot', at: 2.8, dur: 2.7},
  {spanId: 'SPN-0012', label: 'The gate dissolves', at: 5.5, dur: 2.8},
  {spanId: 'SPN-0014', label: '2021 - 8-1', at: 8.3, dur: 2.7},
  {spanId: 'SPN-0027', label: 'Democracy', at: 11.0, dur: 2.8},
  {spanId: 'SPN-0016', label: 'A few minutes', at: 13.8, dur: 2.6},
  {spanId: 'SPN-0017', label: 'Still reachable', at: 16.4, dur: 2.8},
  {spanId: 'SPN-0018', label: 'One dissent', at: 19.2, dur: 2.7},
  {spanId: 'SPN-0021', label: 'Speech we dislike', at: 21.9, dur: 2.9},
  {spanId: 'SPN-0024', label: 'Next: the right you sign away', at: 24.8, dur: 2.8},
];

const fitTitle = (text: string): number => Math.min(84, Math.max(38, 1280 / Math.max(text.length, 14)));
const imageFor = (spanId: string): string | null => {
  const shot = getShot(spanId);
  return shot.images?.find((src) => /\.(png|jpe?g|webp)$/i.test(src)) ?? (shot.src && /\.(png|jpe?g|webp)$/i.test(shot.src) ? shot.src : null);
};

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = MAHANOY_CAPTIONS.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <div style={{position: 'absolute', left: 190, right: 190, bottom: 38, minHeight: 104, padding: '18px 34px', background: '#000000D8', borderTop: `2px solid ${GOLD}`, color: WHITE, fontFamily: BRAND.font.body, fontWeight: 800, fontSize: cue.text.length > 82 ? 34 : 38, lineHeight: 1.2, textAlign: 'center', textShadow: '0 2px 10px #000', whiteSpace: 'pre-line'}}>
      {cue.text}
    </div>
  );
};

const ReconLabel: React.FC = () => (
  <div style={{position: 'absolute', right: 54, top: 48, fontFamily: BRAND.font.body, fontSize: 18, color: SILVER, padding: '7px 11px', border: `1px solid ${GOLD}88`, background: '#000000A8'}}>
    symbolic reconstruction / AI-assisted visuals
  </div>
);

const Lower: React.FC<{scene: PremiumScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 90}});
  if (!scene.title) return null;
  return (
    <div style={{position: 'absolute', left: 58, top: 46, opacity: Math.min(1, e), maxWidth: 1240}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker}</div>
      <div style={{width: 300, height: 2, background: GOLD, marginTop: 9, marginBottom: 21}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: fitTitle(scene.title), color: WHITE, textTransform: 'uppercase', lineHeight: 0.95, textShadow: '0 5px 30px #000'}}>{scene.title}</div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 10}}>{scene.subtitle}</div> : null}
      {scene.citation ? <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: GOLD, marginTop: 14, background: '#000000AA', padding: '7px 11px', display: 'inline-block'}}>{scene.citation}</div> : null}
    </div>
  );
};

const FactoryOverlay: React.FC<{seed: string; mode: Mode}> = ({seed, mode}) => {
  const frame = useCurrentFrame();
  const idx = Math.abs(seed.split('').reduce((s, c) => s + c.charCodeAt(0), 0));
  const light = `mahanoy/factory/light_assets/AF-LIGHT-${String((idx % 6) + 1).padStart(4, '0')}__light_leak_overlay.jpg`;
  const particle = `mahanoy/factory/particle_assets/AF-PART-${String((idx % 6) + 1).padStart(4, '0')}__dust_particles_floating.jpg`;
  const sweep = interpolate(frame, [0, 180], [-80, 80], {extrapolateLeft: 'clamp', extrapolateRight: 'extend'});
  return (
    <>
      <Img src={staticFile(light)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', mixBlendMode: 'screen', opacity: mode === 'ruling' || mode === 'vanish' ? 0.24 : 0.13, transform: `translateX(${sweep}px) scale(1.08)`}} />
      <Img src={staticFile(particle)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', mixBlendMode: 'screen', opacity: 0.12, filter: 'contrast(1.25)'}} />
    </>
  );
};

const StillPlates: React.FC<{scene: PremiumScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const shot = getShot(scene.spanId);
  const images = (shot.images ?? []).filter((src) => /\.(png|jpe?g|webp)$/i.test(src));
  const localFrames = Math.max(1, Math.round((scene.sourceSeconds * BODY_SCALE || HOOK_SEC) * FPS));
  const cutFrames = Math.max(90, Math.round(4.5 * FPS));
  const idx = images.length ? Math.floor(frame / cutFrames) % images.length : -1;
  const nextIdx = images.length ? (idx + 1) % images.length : -1;
  const slot = frame % cutFrames;
  const cross = images.length > 1 ? interpolate(slot, [cutFrames * 0.72, cutFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const render = (src: string, index: number, opacity: number, extra = 0) => {
    const p = interpolate(frame - index * 7, [0, localFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const dir = index % 2 === 0 ? 1 : -1;
    return <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${50 + Math.sin(index + scene.spanId.length) * 7}% ${48 + Math.cos(index) * 6}%`, opacity, transform: `translate3d(${dir * interpolate(p, [0, 1], [-46, 46])}px, ${interpolate(p, [0, 1], [22, -22])}px, 0) scale(${1.055 + p * 0.085 + extra}) rotate(${dir * 0.14}deg)`, filter: 'brightness(0.82) contrast(1.18) saturate(1.06)'}} />;
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
  const slotFrames = Math.max(72, Math.round((scene.sourceSeconds * BODY_SCALE * FPS) / Math.max(1, clips.length)));
  const idx = Math.floor(frame / slotFrames) % clips.length;
  return <Video src={staticFile(clips[idx].src)} startFrom={Math.round((frame % slotFrames) * 0.25)} muted style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.78) contrast(1.16) saturate(1.05)'}} />;
};

const SceneBase: React.FC<{scene: PremiumScene; children?: React.ReactNode}> = ({scene, children}) => {
  const shot = getShot(scene.spanId);
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {shot.assetType === 'stock_video' ? <ClipPlates scene={scene} /> : <StillPlates scene={scene} />}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}C8 0%, #00000012 45%, ${INK}D8 100%)`}} />
      <FactoryOverlay seed={scene.spanId} mode={scene.mode} />
      <LightSweep seed={scene.spanId} color={scene.mode === 'ruling' || scene.mode === 'nursery' ? GOLD : BLUE} />
      <Particles seed={scene.spanId} count={18} color={scene.mode === 'ruling' ? GOLD : BLUE} />
      {children}
      <Lower scene={scene} />
      <ReconLabel />
      <Vignette strength={0.92} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};

const GateSvg: React.FC<{dissolve?: boolean}> = ({dissolve}) => {
  const frame = useCurrentFrame();
  const melt = dissolve ? interpolate(frame, [34, 122], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity={1 - melt * 0.75} transform={`translate(${melt * 34} ${melt * 8})`}>
        <line x1="560" x2="1360" y1="710" y2="710" stroke={GOLD} strokeWidth="8" />
        {[620, 780, 940, 1100, 1260].map((x, i) => <line key={i} x1={x} x2={x + melt * 140} y1={350} y2={710 + melt * 60} stroke={i === 2 ? GOLD : SILVER} strokeWidth="7" strokeDasharray={dissolve ? `${18 - melt * 16} 18` : undefined} opacity={1 - melt * 0.85} />)}
        <path d="M560 350 Q960 190 1360 350" fill="none" stroke={GOLD} strokeWidth="8" strokeDasharray={dissolve ? `${26 - melt * 20} 24` : undefined} />
      </g>
      {dissolve ? <circle cx="960" cy="540" r={80 + melt * 620} fill="none" stroke={BLUE} strokeWidth="7" opacity={0.85 - melt * 0.75} /> : null}
    </svg>
  );
};

const CensoredPost: React.FC = () => {
  const frame = useCurrentFrame();
  const typed = Math.round(interpolate(frame, [10, 72], [0, 9], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}));
  const bars = Array.from({length: Math.max(1, typed)}, (_, i) => i);
  return (
    <div style={{position: 'absolute', right: 220, top: 265, width: 440, height: 570, borderRadius: 42, border: `4px solid ${SILVER}`, background: '#020409DD', boxShadow: '0 20px 90px #000'}}>
      <div style={{height: 70, borderBottom: `1px solid ${SILVER}55`, color: GOLD, fontFamily: BRAND.font.body, fontWeight: 800, fontSize: 22, padding: '22px 28px'}}>weekend story</div>
      <div style={{padding: 32}}>
        {bars.map((_, i) => <div key={i} style={{height: 18, width: 260 + (i % 3) * 42, background: i > 3 ? '#111' : SILVER, opacity: i > 3 ? 0.98 : 0.35, marginBottom: 19}} />)}
        <div style={{marginTop: 38, background: '#000', border: `3px solid ${RED}`, color: WHITE, fontFamily: BRAND.font.display, fontSize: 42, textAlign: 'center', padding: '14px 0'}}>CENSORED</div>
      </div>
    </div>
  );
};

const Vote81: React.FC<{dissent?: boolean}> = ({dissent}) => {
  const frame = useCurrentFrame();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="370" y1="345" x2="1550" y2="345" stroke={SILVER} strokeWidth="4" opacity="0.3" />
      <circle cx="960" cy="345" r="16" fill={GOLD} />
      <text x="960" y="305" fill={GOLD} fontFamily={BRAND.font.display} fontSize="66" textAnchor="middle">2021</text>
      <g transform="translate(540 450)">
        {Array.from({length: 9}, (_, i) => {
          const on = spring({frame: frame - i * 5, fps: FPS, config: {damping: 16, stiffness: 95}});
          const one = i === 8;
          return <rect key={i} x={(i % 5) * 145} y={Math.floor(i / 5) * 135} width="92" height="92" rx="10" fill={one ? (dissent ? RED : '#333844') : BLUE} stroke={one ? RED : GOLD} strokeWidth="4" opacity={Math.min(1, on)} />;
        })}
        <text x="355" y="315" fill={WHITE} fontFamily={BRAND.font.display} fontSize="116" textAnchor="middle">8-1</text>
      </g>
      <rect x="675" y="820" width="570" height="72" fill="#000000AA" stroke={GOLD} strokeWidth="3" />
      <text x="960" y="868" fill={GOLD} fontFamily={BRAND.font.body} fontSize="31" textAnchor="middle">Mahanoy Area School Dist. v. B.L., 594 U.S. 180</text>
    </svg>
  );
};

const MapLocator: React.FC = () => {
  const frame = useCurrentFrame();
  const ripple = (frame % 56) / 56;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M470 390 q190 -100 430 -56 q250 -30 520 88 q-74 190 -340 248 q-340 96 -674 -36 q-170 -52 -170 -190 z" fill={`${BLUE}22`} stroke={BLUE} strokeWidth="4" />
      <circle cx="1030" cy="505" r={16 + ripple * 70} fill="none" stroke={GOLD} strokeWidth="4" opacity={0.72 - ripple * 0.72} />
      <circle cx="1030" cy="505" r="14" fill={GOLD} />
      <text x="1070" y="495" fill={WHITE} fontFamily={BRAND.font.display} fontSize="58">PA</text>
      <text x="1070" y="550" fill={SILVER} fontFamily={BRAND.font.body} fontSize="31">Mahanoy Area High School - 2017</text>
    </svg>
  );
};

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string}> = ({left, right, leftSub, rightSub}) => (
  <div style={{position: 'absolute', left: 250, right: 250, top: 372, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 44}}>
    {[{title: left, sub: leftSub, color: BLUE}, {title: right, sub: rightSub, color: GOLD}].map((box) => (
      <div key={box.title} style={{minHeight: 250, border: `3px solid ${box.color}`, background: '#020409CC', padding: 34}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 60, color: box.color, textTransform: 'uppercase'}}>{box.title}</div>
        {box.sub ? <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: SILVER, marginTop: 20}}>{box.sub}</div> : null}
      </div>
    ))}
  </div>
);

const Timeline: React.FC<{year?: string; label?: string}> = ({year = '1969', label = 'Tinker v. Des Moines'}) => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [12, 72], [0, 980], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="470" y1="560" x2={470 + w} y2="560" stroke={GOLD} strokeWidth="7" strokeLinecap="round" />
      <circle cx={470 + w} cy="560" r="18" fill={GOLD} />
      <text x="960" y="485" fill={WHITE} fontFamily={BRAND.font.display} fontSize="88" textAnchor="middle">{year}</text>
      <text x="960" y="625" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">{label}</text>
    </svg>
  );
};

const StandardCard: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [30, 82], [0, 640], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 435, top: 404, width: 1050, minHeight: 270, background: '#E5E0D0', color: INK, padding: 44, boxShadow: '0 22px 80px #000', transform: 'rotate(-1.2deg)'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 74, textTransform: 'uppercase'}}>"substantial disruption"</div>
      <div style={{width: w, height: 8, background: GOLD, marginTop: 18}} />
      <div style={{fontFamily: BRAND.font.body, fontSize: 30, marginTop: 24}}>The line is disruption, not mere offense.</div>
    </div>
  );
};

const ClockRipples: React.FC = () => {
  const frame = useCurrentFrame();
  const r = (frame % 90) / 90;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {[0, 1, 2].map((i) => <circle key={i} cx="960" cy="545" r={120 + ((r + i / 3) % 1) * 420} fill="none" stroke={i === 1 ? GOLD : BLUE} strokeWidth="5" opacity={0.45 - ((r + i / 3) % 1) * 0.42} />)}
      <circle cx="960" cy="545" r="142" fill="#020409CC" stroke={GOLD} strokeWidth="6" />
      <text x="960" y="570" fill={WHITE} fontFamily={BRAND.font.display} fontSize="86" textAnchor="middle">24h</text>
    </svg>
  );
};

const Scales: React.FC = () => {
  const frame = useCurrentFrame();
  const tilt = Math.sin(frame * 0.045) * 1.7;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g transform={`rotate(${tilt} 960 500)`}>
        <line x1="690" y1="500" x2="1230" y2="500" stroke={GOLD} strokeWidth="8" />
        <line x1="960" y1="360" x2="960" y2="720" stroke={SILVER} strokeWidth="8" />
        {[760, 1160].map((x, i) => (
          <g key={x}>
            <line x1={x} y1="500" x2={x - 70} y2="650" stroke={SILVER} strokeWidth="3" />
            <line x1={x} y1="500" x2={x + 70} y2="650" stroke={SILVER} strokeWidth="3" />
            <ellipse cx={x} cy="668" rx="115" ry="28" fill={i === 0 ? `${BLUE}88` : `${GOLD}88`} />
          </g>
        ))}
      </g>
      <text x="960" y="790" fill={SILVER} fontFamily={BRAND.font.body} fontSize="32" textAnchor="middle">the scale barely moves</text>
    </svg>
  );
};

const Exceptions: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['bullying', 'threats', 'cheating'];
  return (
    <div style={{position: 'absolute', left: 270, right: 270, top: 390, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 30}}>
      {labels.map((label, i) => {
        const on = spring({frame: frame - 24 - i * 24, fps: FPS, config: {damping: 15, stiffness: 100}});
        return <div key={label} style={{height: 250, border: `3px solid ${i === 1 ? RED : GOLD}`, background: '#020409D8', padding: 28, boxShadow: `0 0 ${Math.round(on * 26)}px ${i === 1 ? RED : GOLD}`, opacity: 0.55 + on * 0.45}}>
          <div style={{fontFamily: BRAND.font.display, color: i === 1 ? RED : GOLD, fontSize: 54, textTransform: 'uppercase'}}>{label}</div>
          <div style={{position: 'absolute', left: 28, right: 28, bottom: 30, height: 5, background: i === 1 ? RED : GOLD}} />
        </div>;
      })}
    </div>
  );
};

const Boundary: React.FC = () => {
  const frame = useCurrentFrame();
  const wobble = Math.sin(frame * 0.05) * 22;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d={`M 310 715 C 580 ${385 + wobble}, 790 ${755 - wobble}, 960 540 C 1130 ${320 + wobble}, 1330 ${610 - wobble}, 1610 340`} fill="none" stroke={BLUE} strokeWidth="9" strokeDasharray="18 18" />
      <text x="960" y="618" fill={GOLD} fontSize="58" fontFamily={BRAND.font.display} textAnchor="middle">A LINE IN PENCIL</text>
    </svg>
  );
};

const Doors: React.FC = () => (
  <div style={{position: 'absolute', left: 260, right: 260, top: 374, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 30}}>
    {['threat', 'targeted harassment', 'cheating ring'].map((label, i) => <div key={label} style={{height: 275, border: `3px solid ${i === 0 ? GOLD : `${SILVER}88`}`, background: '#05070AD8', padding: 25}}>
      <div style={{fontFamily: BRAND.font.display, color: i === 0 ? GOLD : WHITE, fontSize: 42, textTransform: 'uppercase'}}>{label}</div>
      <div style={{position: 'absolute', left: 25, right: 25, bottom: 30, height: 5, background: i === 0 ? GOLD : `${SILVER}66`}} />
    </div>)}
  </div>
);

const SeriesLine: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['search', 'track', 'take', 'speak'];
  const w = interpolate(frame, [20, 115], [0, 960], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="480" y1="575" x2={480 + w} y2="575" stroke={GOLD} strokeWidth="7" strokeLinecap="round" />
      {labels.map((label, i) => {
        const x = 480 + i * 320;
        return <g key={label}>
          <circle cx={x} cy="575" r="22" fill={w >= i * 320 ? GOLD : SILVER} opacity={w >= i * 320 ? 1 : 0.3} />
          <text x={x} y="655" fill={WHITE} fontFamily={BRAND.font.display} fontSize="44" textAnchor="middle">{label}</text>
        </g>;
      })}
    </svg>
  );
};

const Nursery: React.FC = () => {
  const frame = useCurrentFrame();
  const grow = interpolate(frame, [20, 110], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="960" y1="720" x2="960" y2={720 - grow * 250} stroke={GOLD} strokeWidth="9" strokeLinecap="round" />
      <path d={`M960 ${575 - grow * 105} C850 ${520 - grow * 60}, 805 ${445 - grow * 70}, 760 ${390 - grow * 24}`} fill="none" stroke={BLUE} strokeWidth="7" opacity={grow} />
      <path d={`M960 ${575 - grow * 105} C1070 ${520 - grow * 60}, 1115 ${445 - grow * 70}, 1160 ${390 - grow * 24}`} fill="none" stroke={BLUE} strokeWidth="7" opacity={grow} />
      <text x="960" y="805" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">teaching tolerance for disliked speech</text>
    </svg>
  );
};

const SubscribeButton: React.FC = () => {
  const frame = useCurrentFrame();
  const pop = spring({frame, fps: FPS, config: {damping: 10, stiffness: 160}});
  return <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><div style={{fontFamily: BRAND.font.display, fontSize: 82, color: INK, background: GOLD, padding: '28px 58px', transform: `scale(${0.82 + pop * 0.18})`, boxShadow: `0 0 42px ${GOLD}`}}>SUBSCRIBE</div></div>;
};

const SceneOverlay: React.FC<{scene: PremiumScene}> = ({scene}) => {
  if (scene.mode === 'post') return <CensoredPost />;
  if (scene.mode === 'gateQuote') return <><GateSvg /><div style={{position: 'absolute', left: 510, right: 510, top: 300, fontFamily: BRAND.font.body, fontWeight: 800, fontSize: 31, color: WHITE, textAlign: 'center'}}>"Students do not shed their constitutional rights at the <span style={{color: GOLD}}>schoolhouse gate</span>."</div></>;
  if (scene.mode === 'map') return <MapLocator />;
  if (scene.mode === 'disappointment') return <TwoColumn left="JV" right="Varsity" leftSub="stays behind" rightSub="moves up" />;
  if (scene.mode === 'snap') return <CensoredPost />;
  if (scene.mode === 'vanish') return <CensoredPost />;
  if (scene.mode === 'suspension') return <TwoColumn left="Weekend post" right="1 year" leftSub="off campus" rightSub="suspended from JV cheer" />;
  if (scene.mode === 'conflict') return <TwoColumn left="School's order" right="Student's voice" leftSub="discipline" rightSub="off-campus speech" />;
  if (scene.mode === 'ordinary') return <TwoColumn left="No threat" right="No target" leftSub="no plan" rightSub="ordinary venting" />;
  if (scene.mode === 'armband') return <Timeline year="1965" label="black armbands - silent protest" />;
  if (scene.mode === 'timeline') return <Timeline year="1969" label="Tinker v. Des Moines" />;
  if (scene.mode === 'standard') return <StandardCard />;
  if (scene.mode === 'dissolveGate') return <GateSvg dissolve />;
  if (scene.mode === 'clock') return <ClockRipples />;
  if (scene.mode === 'ruling') return <Vote81 />;
  if (scene.mode === 'scales') return <Scales />;
  if (scene.mode === 'nursery') return <Nursery />;
  if (scene.mode === 'exceptions') return <Exceptions />;
  if (scene.mode === 'dissent') return <Vote81 dissent />;
  if (scene.mode === 'boundary') return <Boundary />;
  if (scene.mode === 'doors') return <Doors />;
  if (scene.mode === 'theme') return <div style={{position: 'absolute', left: 220, right: 220, top: 420, textAlign: 'center', fontFamily: BRAND.font.display, fontSize: 88, color: GOLD, textTransform: 'uppercase', textShadow: '0 5px 36px #000'}}>Speech we dislike</div>;
  if (scene.mode === 'series') return <SeriesLine />;
  if (scene.mode === 'next') return <TwoColumn left="You click" right="You waive" leftSub="seconds" rightSub="courtroom rights" />;
  if (scene.mode === 'cta') return <SubscribeButton />;
  return null;
};

const SceneView: React.FC<{scene: TimedScene}> = ({scene}) => <SceneBase scene={scene}><SceneOverlay scene={scene} /></SceneBase>;

const HookBeat: React.FC<{spanId: string; label: string}> = ({spanId, label}) => {
  const image = imageFor(spanId);
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 84], [1.03, 1.12], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pseudo: PremiumScene = {spanId, sourceSeconds: 4, mode: spanId === 'SPN-0014' ? 'ruling' : 'post', kicker: 'HOOK', title: label, chapter: 'hook'};
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {image ? <Img src={staticFile(image)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.72) contrast(1.24) saturate(1.08)', transform: `scale(${zoom})`}} /> : null}
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}E8 0%, #00000033 58%, ${INK}96 100%)`}} />
      <FactoryOverlay seed={`hook-${spanId}`} mode={pseudo.mode} />
      {spanId === 'SPN-0014' ? <Vote81 /> : null}
      {spanId === 'SPN-0017' ? <Exceptions /> : null}
      {spanId === 'SPN-0018' ? <Vote81 dissent /> : null}
      {spanId === 'SPN-0012' ? <GateSvg dissolve /> : null}
      <div style={{position: 'absolute', left: 74, bottom: 170, fontFamily: BRAND.font.display, color: WHITE, fontSize: 74, textTransform: 'uppercase', textShadow: '0 5px 28px #000'}}>{label}</div>
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

export const MahanoyPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={Math.round(HOOK_SEC * FPS)} name="PART_1_HOOK">
      <HookMontage />
    </Sequence>
    <Sequence from={Math.round(HOOK_SEC * FPS)} durationInFrames={Math.round(OPENING_SEC * FPS)} name="PART_2_BRAND_OPENING">
      <BrandOpening seriesLabel="Prime Documentary" title="Mahanoy" subtitle="The phone and the schoolhouse gate" />
    </Sequence>
    {bodyScenes.map((scene) => (
      <Sequence key={scene.spanId} from={Math.round(scene.start * FPS)} durationInFrames={Math.round(scene.dur * FPS)} name={`${scene.chapter}_${scene.spanId}`}>
        <SceneView scene={scene} />
      </Sequence>
    ))}
    <Sequence from={Math.round((TOTAL_SEC - ENDCARD_SEC) * FPS)} durationInFrames={Math.round(ENDCARD_SEC * FPS)} name="PART_4_BRAND_ENDCARD">
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile('mahanoy/audio/mahanoy_final_mix_v001.mp3')} />
    <CaptionBand />
  </AbsoluteFill>
);

export const mahanoyPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
