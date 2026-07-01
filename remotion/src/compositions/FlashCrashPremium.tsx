import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
  Sequence,
  Series,
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
import {FLASHCRASH_CAPTIONS} from '../data/flashcrash_captions';
import {FLASHCRASH_FACTORY_ASSETS} from '../data/flashcrash_factory_assets';

const FPS = BRAND.video.fps;
const TOTAL_SEC = 28 * 60;
const HOOK_SEC = 29;
const OPENING_AT = HOOK_SEC;
const MAIN_START = HOOK_SEC + OPENING_SEC;
const MAIN_END = TOTAL_SEC - ENDCARD_SEC;
const MIX_SRC = 'flashcrash/audio/flashcrash_mix_v001.wav';

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#D84A3A';
const GREEN = '#58D68D';

type SceneKind =
  | 'valuation'
  | 'marketRoom'
  | 'question'
  | 'timeline'
  | 'home'
  | 'code'
  | 'orderbook'
  | 'ghostwall'
  | 'causal'
  | 'court'
  | 'money'
  | 'systems'
  | 'ending';

type Scene = {
  id: string;
  kind: SceneKind;
  title: string;
  subtitle: string;
  kicker: string;
  citation: string;
  act: string;
};

const SCENE_STARTS = [
  MAIN_START,
  61.411,
  91.605,
  167.664,
  232.124,
  331.159,
  373.653,
  438.58,
  515.393,
  590.442,
  641.621,
  712.401,
  768.687,
  827.806,
  879.913,
  959.19,
  986.846,
  1021.467,
  1062.451,
  1098.976,
  1191.317,
  1318.332,
  1415.882,
  1488.655,
  1575.558,
  1646.659,
];

const scenes: Scene[] = [
  {id: 'S01', kind: 'marketRoom', kicker: 'HOOK PAYOFF', act: 'opening', title: '2:32 PM', subtitle: 'The market begins to fall.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S02', kind: 'valuation', kicker: 'THE DROP', act: 'opening', title: '$1 TRILLION', subtitle: 'Briefly erased, then partly restored.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S03', kind: 'question', kicker: 'THE QUESTION', act: 'opening', title: 'Did one man break the market?', subtitle: 'Or did a stressed system reveal itself?', citation: 'Prime Documentary thesis'},
  {id: 'S04', kind: 'marketRoom', kicker: 'ACT I', act: 'act1', title: 'A normal afternoon', subtitle: 'Screens, liquidity, and pressure.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S05', kind: 'timeline', kicker: 'ACT I', act: 'act1', title: 'May 6, 2010', subtitle: 'The timeline compresses.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S06', kind: 'causal', kicker: 'ACT I', act: 'act1', title: 'Not one lever', subtitle: 'Large sell order, HFT pullback, market anxiety.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S07', kind: 'systems', kicker: 'ACT II', act: 'act2', title: 'The machine market', subtitle: 'Speed changes the shape of liquidity.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S08', kind: 'code', kicker: 'ACT II', act: 'act2', title: 'Spoofing', subtitle: 'Orders can signal size without a real intent to trade.', citation: 'United States v. Sarao'},
  {id: 'S09', kind: 'money', kicker: 'ACT II', act: 'act2', title: '$12.8M admitted', subtitle: 'More than $40M alleged by authorities.', citation: 'DOJ / CFTC case materials'},
  {id: 'S10', kind: 'orderbook', kicker: 'ACT III', act: 'act3', title: 'The wall appears', subtitle: 'A visible imbalance forms in the book.', citation: 'United States v. Sarao'},
  {id: 'S11', kind: 'ghostwall', kicker: 'ACT III', act: 'act3', title: 'A ghost wall', subtitle: 'Large displayed orders press on the market.', citation: 'United States v. Sarao'},
  {id: 'S12', kind: 'ghostwall', kicker: 'ACT III', act: 'act3', title: 'Then it disappears', subtitle: 'The signal vanishes before execution.', citation: 'United States v. Sarao'},
  {id: 'S13', kind: 'ghostwall', kicker: 'ACT III', act: 'act3', title: 'One real order remains', subtitle: 'The diagram is symbolic, not evidence footage.', citation: 'United States v. Sarao'},
  {id: 'S14', kind: 'marketRoom', kicker: 'ACT IV', act: 'act4', title: 'Greece in the background', subtitle: 'A nervous market was already listening for danger.', citation: 'Market context, May 2010'},
  {id: 'S15', kind: 'causal', kicker: 'ACT IV', act: 'act4', title: 'Two great weights', subtitle: 'Large sell pressure and a ghost wall press the same book.', citation: 'CFTC-SEC report / United States v. Sarao'},
  {id: 'S16', kind: 'systems', kicker: 'ACT IV', act: 'act4', title: 'Liquidity pulls back', subtitle: 'The machines step away when the floor is needed.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S17', kind: 'valuation', kicker: 'THE PLUNGE', act: 'climax', title: '998.5 points', subtitle: 'A fast fall, then a fast partial recovery.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S18', kind: 'valuation', kicker: 'THE PENNY', act: 'climax', title: '$0.01', subtitle: 'Some trades briefly printed at a penny.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S19', kind: 'timeline', kicker: 'ACT V', act: 'act5', title: 'The safeties trip', subtitle: 'Circuit breakers help the market find a floor.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S20', kind: 'systems', kicker: 'ACT V', act: 'act5', title: 'The autopsy', subtitle: 'The official report starts with the large sell program.', citation: 'CFTC-SEC report, May 6 2010'},
  {id: 'S21', kind: 'causal', kicker: 'ACT V', act: 'act5', title: 'Part of. Contributed to.', subtitle: 'Not a single-handed cause. A contribution inside a wider event.', citation: 'CFTC order / DOJ materials'},
  {id: 'S22', kind: 'court', kicker: 'ACT VI', act: 'act6', title: 'The law chooses someone', subtitle: '2015 arrest. 2016 plea: wire fraud and spoofing.', citation: 'United States v. Sarao'},
  {id: 'S23', kind: 'money', kicker: 'ACT VI', act: 'act6', title: '$12.9M forfeiture', subtitle: 'The legal ending is smaller than the market story.', citation: 'Court sentencing record'},
  {id: 'S24', kind: 'home', kicker: 'ACT VI', act: 'act6', title: '2020', subtitle: 'One year of home detention.', citation: 'Court sentencing record'},
  {id: 'S25', kind: 'question', kicker: 'ENDING', act: 'ending', title: 'Person or system?', subtitle: 'The honest answer is not a single villain.', citation: 'Prime Documentary conclusion'},
  {id: 'S26', kind: 'ending', kicker: 'ENDING', act: 'ending', title: 'What failed first?', subtitle: 'The order, the machine, or the trust between them?', citation: 'Prime Documentary conclusion'},
];

const framesFor = (seconds: number, fps: number = FPS): number => Math.max(1, Math.round(seconds * fps));
const sceneStart = (index: number): number => SCENE_STARTS[index] ?? MAIN_START;
const sceneEnd = (index: number): number => SCENE_STARTS[index + 1] ?? MAIN_END;
const sceneDuration = (index: number): number => Math.max(1, sceneEnd(index) - sceneStart(index));
const sceneImages = (id: string): string[] => [id, `${id}_02`, `${id}_03`].map((name) => `flashcrash/${name}.png`);

const fitTitle = (text: string): number => Math.min(112, Math.max(50, 1280 / Math.max(text.length, 12)));

const factoryByLayer = (layer: 'background' | 'light' | 'texture' | 'vfx') =>
  FLASHCRASH_FACTORY_ASSETS.filter((asset) => asset.layer === layer);

const FactoryLayer: React.FC<{scene: Scene}> = ({scene}) => {
  const {durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const light = factoryByLayer('light');
  const vfx = factoryByLayer('vfx');
  const textures = factoryByLayer('texture');
  const backgrounds = factoryByLayer('background');
  const assets = [...backgrounds, ...light, ...vfx, ...textures];
  if (!assets.length) return null;
  const pick = (offset: number) => assets[(scenes.findIndex((s) => s.id === scene.id) + offset) % assets.length];
  const selected = [pick(0), pick(7)].filter(Boolean);
  const p = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      {selected.map((asset, index) => {
        const opacity = asset.layer === 'background' ? 0.18 : asset.layer === 'texture' ? 0.14 : 0.25;
        const blend = asset.layer === 'texture' ? 'overlay' : asset.layer === 'background' ? 'normal' : 'screen';
        const common: React.CSSProperties = {
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          filter: 'brightness(0.72) contrast(1.18) saturate(0.82)',
          transform: `translate3d(${(index ? -1 : 1) * interpolate(p, [0, 1], [-35, 35])}px, 0, 0) scale(1.07)`,
        };
        return (
          <AbsoluteFill key={`${asset.id}-${index}`} style={{opacity, mixBlendMode: blend, pointerEvents: 'none'}}>
            {asset.kind === 'video' ? (
              <OffthreadVideo src={staticFile(asset.src)} muted playbackRate={0.85} style={common} />
            ) : (
              <Img src={staticFile(asset.src)} style={common} />
            )}
          </AbsoluteFill>
        );
      })}
    </>
  );
};

const MovingImageSet: React.FC<{scene: Scene}> = ({scene}) => {
  const {durationInFrames, fps} = useVideoConfig();
  const frame = useCurrentFrame();
  const images = sceneImages(scene.id);
  const per = Math.max(framesFor(4.4, fps), Math.round(durationInFrames / 11));
  const index = Math.floor(frame / per) % images.length;
  const next = (index + 1) % images.length;
  const local = frame % per;
  const cross = interpolate(local, [per * 0.78, per], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const sceneIndex = scenes.findIndex((s) => s.id === scene.id);
  const dir = sceneIndex % 2 === 0 ? 1 : -1;
  const progress = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const render = (src: string, opacity: number, offset: number) => (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        opacity,
        filter: 'brightness(0.68) contrast(1.28) saturate(0.9)',
        transform: `translate3d(${dir * (-62 + progress * 124 + offset * 20)}px, ${28 - progress * 56 - offset * 10}px, 0) scale(${1.08 + progress * 0.11 + offset * 0.025}) rotate(${dir * (-0.35 + progress * 0.7)}deg)`,
        transformOrigin: `${sceneIndex % 3 === 0 ? 42 : 58}% 46%`,
        willChange: 'transform, opacity',
      }}
    />
  );
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      {render(images[index], 1, 0)}
      {render(images[next], cross, 1)}
    </AbsoluteFill>
  );
};

const ReconLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 48,
      top: 44,
      fontFamily: BRAND.font.body,
      fontSize: 17,
      color: SILVER,
      background: '#00000099',
      border: `1px solid ${GOLD}88`,
      padding: '7px 11px',
      textTransform: 'uppercase',
    }}
  >
    symbolic reconstruction / AI-generated visual
  </div>
);

const SourceBug: React.FC<{scene: Scene}> = ({scene}) => (
  <div
    style={{
      position: 'absolute',
      right: 48,
      bottom: 178,
      maxWidth: 510,
      fontFamily: BRAND.font.body,
      fontSize: 18,
      lineHeight: 1.18,
      color: GOLD,
      background: '#000000B8',
      borderTop: `2px solid ${GOLD}`,
      padding: '8px 12px',
      textAlign: 'right',
    }}
  >
    {scene.citation}
  </div>
);

const Lower: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.15 * fps), fps, config: {damping: 18, stiffness: 92}});
  const titleSize = fitTitle(scene.title);
  return (
    <div style={{position: 'absolute', left: 58, top: 46, opacity: Math.min(1, enter), maxWidth: 1180}}>
      <div style={{fontFamily: BRAND.font.body, fontWeight: 900, color: scene.act === 'climax' ? RED : GOLD, fontSize: 18, textTransform: 'uppercase'}}>
        {scene.kicker} / {scene.id}
      </div>
      <div style={{width: 300, height: 2, background: scene.act === 'climax' ? RED : GOLD, marginTop: 9, marginBottom: 22}} />
      <div
        style={{
          fontFamily: BRAND.font.display,
          color: WHITE,
          fontSize: titleSize,
          lineHeight: 0.9,
          textTransform: 'uppercase',
          textShadow: '0 10px 35px #000',
        }}
      >
        {scene.title}
      </div>
      <div style={{fontFamily: BRAND.font.body, color: SILVER, fontWeight: 700, fontSize: 28, marginTop: 12, maxWidth: 980}}>
        {scene.subtitle}
      </div>
    </div>
  );
};

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = FLASHCRASH_CAPTIONS.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 160,
        right: 160,
        bottom: 34,
        minHeight: 102,
        padding: '16px 32px 18px',
        background: '#000000D8',
        borderTop: `3px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize: cue.text.length > 60 ? 38 : 46,
        lineHeight: 1.12,
        textAlign: 'center',
        textShadow: '0 3px 14px #000',
        whiteSpace: 'pre-line',
      }}
    >
      {cue.text}
    </div>
  );
};

const HookMontage: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const beats = [
    {id: 'S17', text: '998.5 POINTS'},
    {id: 'S18', text: '$0.01 PRINTS'},
    {id: 'S10', text: 'THE WALL'},
    {id: 'S19', text: '75,000 CONTRACTS'},
    {id: 'S06', text: 'NOT ONE LEVER'},
    {id: 'S15', text: 'WIRE FRAUD + SPOOFING'},
    {id: 'S25', text: 'PERSON OR SYSTEM?'},
  ];
  const per = framesFor(HOOK_SEC / beats.length, fps);
  const index = Math.min(beats.length - 1, Math.floor(frame / per));
  const beat = beats[index];
  const local = frame - index * per;
  const flash = interpolate(local, [0, 5, per - 5, per], [0.25, 0, 0, 0.22], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <MovingImageSet scene={{...scenes.find((s) => s.id === beat.id)!, id: beat.id}} />
      <AbsoluteFill style={{background: `linear-gradient(180deg, #000000CC 0%, #00000030 48%, ${INK}E8 100%)`}} />
      <FactoryLayer scene={scenes[index % scenes.length]} />
      <ValuationCollapse compact danger={beat.id === 'S17' || beat.id === 'S18'} />
      <div
        style={{
          position: 'absolute',
          left: 72,
          bottom: 170,
          fontFamily: BRAND.font.display,
          fontSize: beat.text.length > 16 ? 88 : 118,
          color: beat.id === 'S18' || beat.id === 'S17' ? RED : WHITE,
          textTransform: 'uppercase',
          textShadow: '0 10px 40px #000',
        }}
      >
        {beat.text}
      </div>
      <div style={{position: 'absolute', left: 76, bottom: 128, width: 440, height: 4, background: GOLD}} />
      <LightSweep seed={`hook-${beat.id}`} color={beat.id === 'S17' ? RED : GOLD} />
      <Particles seed={`hook-${beat.id}`} count={34} color={beat.id === 'S17' ? RED : GOLD} />
      <AbsoluteFill style={{background: WHITE, opacity: flash, mixBlendMode: 'screen'}} />
      <ReconLabel />
      <Vignette strength={1} />
      <Grain opacity={0.055} />
    </AbsoluteFill>
  );
};

const ValuationCollapse: React.FC<{compact?: boolean; danger?: boolean}> = ({compact, danger}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const crash = spring({frame: frame - 42, fps: FPS, config: {damping: 13, stiffness: 86}});
  const pts = Array.from({length: 44}, (_, i) => {
    const t = i / 43;
    const x = 250 + t * 1420;
    const base = 340 + Math.sin(t * 7.2) * 28 + t * 50;
    const drop = t > 0.55 ? (t - 0.55) * 760 * Math.min(1, crash) : 0;
    const rebound = t > 0.8 ? (t - 0.8) * 480 * Math.min(1, crash) : 0;
    return `${x},${base + drop - rebound}`;
  });
  const draw = Math.max(2, Math.floor(pts.length * interpolate(p, [0, 0.34], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})));
  const value = Math.round(interpolate(Math.min(1, crash), [0, 1], [1000, 0]));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute', opacity: compact ? 0.72 : 0.95}}>
      <g opacity="0.24">
        {Array.from({length: 6}, (_, i) => <line key={`h${i}`} x1="240" x2="1680" y1={260 + i * 92} y2={260 + i * 92} stroke={SILVER} strokeWidth="2" />)}
        {Array.from({length: 8}, (_, i) => <line key={`v${i}`} x1={250 + i * 205} x2={250 + i * 205} y1="230" y2="790" stroke={SILVER} strokeWidth="2" />)}
      </g>
      <polyline points={pts.slice(0, draw).join(' ')} fill="none" stroke={danger ? RED : GOLD} strokeWidth={compact ? 8 : 11} strokeLinecap="round" strokeLinejoin="round" filter={`drop-shadow(0 0 14px ${danger ? RED : GOLD})`} />
      <circle cx="1245" cy={430 + Math.min(1, crash) * 210} r={compact ? 13 : 20} fill={RED} opacity={Math.min(1, crash)} />
      {!compact ? (
        <>
          <text x="960" y="204" fill={GOLD} fontFamily={BRAND.font.display} fontSize="90" textAnchor="middle">$1T VALUE VANISHES</text>
          <text x="960" y="898" fill={WHITE} fontFamily={BRAND.font.display} fontSize="118" textAnchor="middle">{value === 0 ? '$0.01 PRINTS' : `$${value}B`}</text>
        </>
      ) : null}
    </svg>
  );
};

const OrderBook: React.FC = () => {
  const frame = useCurrentFrame();
  const rows = Array.from({length: 9}, (_, i) => i);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="225" fill={WHITE} fontFamily={BRAND.font.display} fontSize="78" textAnchor="middle">ORDER BOOK</text>
      <text x="655" y="308" fill={GREEN} fontFamily={BRAND.font.body} fontSize="34" fontWeight="900" textAnchor="middle">BUY</text>
      <text x="1265" y="308" fill={RED} fontFamily={BRAND.font.body} fontSize="34" fontWeight="900" textAnchor="middle">SELL</text>
      <line x1="960" x2="960" y1="320" y2="846" stroke={SILVER} strokeWidth="3" opacity="0.45" />
      {rows.map((i) => {
        const y = 358 + i * 54;
        const sellGrow = interpolate(frame - i * 8, [0, 38], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const buyGrow = interpolate(frame - i * 5, [0, 30], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const sellW = (180 + i * 48) * sellGrow;
        const buyW = (120 + (8 - i) * 22) * buyGrow;
        return (
          <g key={i}>
            <rect x={900 - buyW} y={y} width={buyW} height="34" fill={GREEN} opacity="0.78" />
            <rect x="1020" y={y} width={sellW} height="34" fill={i > 4 ? RED : GOLD} opacity={i > 4 ? 0.88 : 0.62} />
            <text x="930" y={y + 26} fill={SILVER} fontFamily={BRAND.font.body} fontSize="18" textAnchor="end">{(1100 - i).toLocaleString()}</text>
            <text x="990" y={y + 26} fill={SILVER} fontFamily={BRAND.font.body} fontSize="18">{(1101 + i).toLocaleString()}</text>
          </g>
        );
      })}
      <rect x="1012" y="612" width={interpolate(frame, [60, 118], [0, 520], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} height="96" fill={RED} opacity="0.22" stroke={RED} strokeWidth="5" />
      <text x="1220" y="764" fill={GOLD} fontFamily={BRAND.font.display} fontSize="54" textAnchor="middle">DISPLAYED WALL</text>
    </svg>
  );
};

const GhostWall: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const appear = spring({frame: frame - 18, fps: FPS, config: {damping: 14, stiffness: 74}});
  const vanish = interpolate(frame, [durationInFrames * 0.55, durationInFrames * 0.68], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const wallX = interpolate(Math.min(1, appear), [0, 1], [1700, 1050]);
  const wallOpacity = Math.max(0, Math.min(1, appear) * (1 - vanish));
  const realOrder = interpolate(frame, [durationInFrames * 0.68, durationInFrames * 0.82], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <defs>
        <linearGradient id="ghostWallFill" x1="0" x2="1">
          <stop offset="0" stopColor={RED} stopOpacity="0.05" />
          <stop offset="1" stopColor={RED} stopOpacity="0.48" />
        </linearGradient>
      </defs>
      <line x1="420" x2="1510" y1="540" y2="540" stroke={SILVER} strokeWidth="5" opacity="0.35" />
      <g opacity={wallOpacity}>
        <rect x={wallX} y="285" width="72" height="510" fill="url(#ghostWallFill)" stroke={RED} strokeWidth="5" />
        {Array.from({length: 8}, (_, i) => <rect key={i} x={wallX - i * 76} y={320 + i * 26} width="56" height={420 - i * 28} fill={RED} opacity={0.08 + i * 0.035} />)}
        <text x={wallX - 80} y="250" fill={RED} fontFamily={BRAND.font.display} fontSize="54" textAnchor="end">GHOST WALL</text>
      </g>
      <g opacity={realOrder}>
        <circle cx="960" cy="540" r="28" fill={GOLD} />
        <circle cx="960" cy="540" r="82" fill="none" stroke={GOLD} strokeWidth="5" opacity="0.38" />
        <text x="960" y="652" fill={WHITE} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">ONE REAL ORDER</text>
      </g>
      <text x="960" y="870" fill={SILVER} fontFamily={BRAND.font.body} fontSize="30" textAnchor="middle">symbolic diagram of alleged spoofing mechanics</text>
    </svg>
  );
};

const CausalBoard: React.FC = () => {
  const frame = useCurrentFrame();
  const items = [
    ['Large sell order', '75,000 E-mini contracts / about $4.1B', GOLD],
    ['Liquidity pullback', 'HFTs traded, then reduced available liquidity', BLUE],
    ['Spoofing allegation', 'contributed to order-book imbalance', RED],
    ['Market anxiety', 'Greek debt crisis pressure in the background', SILVER],
  ];
  return (
    <div style={{position: 'absolute', left: 240, right: 240, top: 328, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 28}}>
      {items.map(([title, sub, color], i) => {
        const enter = spring({frame: frame - i * 16, fps: FPS, config: {damping: 18, stiffness: 92}});
        return (
          <div key={title} style={{height: 196, border: `3px solid ${color}`, background: '#02060DCC', padding: 26, opacity: Math.min(1, enter), transform: `translateY(${(1 - enter) * 24}px)`}}>
            <div style={{fontFamily: BRAND.font.display, color, fontSize: 44, textTransform: 'uppercase'}}>{title}</div>
            <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 25, lineHeight: 1.16, marginTop: 14}}>{sub}</div>
          </div>
        );
      })}
    </div>
  );
};

const Timeline: React.FC = () => {
  const frame = useCurrentFrame();
  const nodes = [
    ['2009', 'activity period begins'],
    ['May 6 2010', 'flash crash'],
    ['2014', 'activity period ends'],
    ['2016', 'guilty plea'],
    ['2020', 'home detention'],
  ];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="270" x2="1650" y1="575" y2="575" stroke={GOLD} strokeWidth="7" />
      {nodes.map(([year, label], i) => {
        const x = 270 + i * 345;
        const on = spring({frame: frame - i * 18, fps: FPS, config: {damping: 16, stiffness: 100}});
        return (
          <g key={year} opacity={Math.min(1, on)} transform={`translate(0 ${(1 - on) * 30})`}>
            <circle cx={x} cy="575" r="25" fill={i === 1 ? RED : GOLD} />
            <text x={x} y="500" fill={WHITE} fontFamily={BRAND.font.display} fontSize="50" textAnchor="middle">{year}</text>
            <text x={x} y="656" fill={SILVER} fontFamily={BRAND.font.body} fontSize="24" textAnchor="middle">{label}</text>
          </g>
        );
      })}
    </svg>
  );
};

const MoneyCounter: React.FC = () => {
  const frame = useCurrentFrame();
  const admitted = interpolate(frame, [18, 86], [0, 12.8], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const alleged = interpolate(frame, [52, 132], [0, 40], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 255, right: 255, top: 380, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 48}}>
      <div style={{border: `4px solid ${GOLD}`, background: '#03070ECC', padding: 34, minHeight: 255}}>
        <div style={{fontFamily: BRAND.font.display, color: GOLD, fontSize: 94}}>${admitted.toFixed(1)}M</div>
        <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 28}}>admitted profits</div>
      </div>
      <div style={{border: `4px solid ${RED}`, background: '#03070ECC', padding: 34, minHeight: 255}}>
        <div style={{fontFamily: BRAND.font.display, color: RED, fontSize: 94}}>&gt;${Math.round(alleged)}M</div>
        <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 28}}>authorities' broader allegation</div>
      </div>
    </div>
  );
};

const CourtPlea: React.FC = () => (
  <div style={{position: 'absolute', left: 350, right: 350, top: 355, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 34}}>
    {[
      ['WIRE FRAUD', 'guilty plea'],
      ['SPOOFING', 'guilty plea'],
    ].map(([top, bottom]) => (
      <div key={top} style={{height: 250, border: `4px solid ${GOLD}`, background: '#05070DD8', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center'}}>
        <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 66, textTransform: 'uppercase'}}>{top}</div>
        <div style={{fontFamily: BRAND.font.body, color: GOLD, fontSize: 30, marginTop: 14}}>{bottom}</div>
      </div>
    ))}
  </div>
);

const SceneGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'valuation') return <ValuationCollapse danger={scene.act === 'climax'} />;
  if (scene.kind === 'orderbook') return <OrderBook />;
  if (scene.kind === 'ghostwall') return <GhostWall />;
  if (scene.kind === 'causal') return <CausalBoard />;
  if (scene.kind === 'timeline') return <Timeline />;
  if (scene.kind === 'money') return <MoneyCounter />;
  if (scene.kind === 'court') return <CourtPlea />;
  if (scene.kind === 'question' || scene.kind === 'ending') {
    return (
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{fontFamily: BRAND.font.display, color: scene.kind === 'ending' ? GOLD : WHITE, fontSize: 98, textAlign: 'center', maxWidth: 1180, lineHeight: 0.92, textTransform: 'uppercase', textShadow: '0 12px 42px #000'}}>
          {scene.title}
        </div>
        <div style={{width: 520, height: 5, background: GOLD, marginTop: 28}} />
      </AbsoluteFill>
    );
  }
  return null;
};

const SceneView: React.FC<{scene: Scene}> = ({scene}) => (
  <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
    <MovingImageSet scene={scene} />
    <FactoryLayer scene={scene} />
    <AbsoluteFill style={{background: scene.act === 'climax' ? `linear-gradient(180deg, #180202CC 0%, #00000033 43%, ${INK}F0 100%)` : `linear-gradient(180deg, ${INK}D6 0%, #00000025 43%, ${INK}F0 100%)`}} />
    <LightSweep seed={`flashcrash-${scene.id}`} color={scene.act === 'climax' ? RED : scene.kind === 'causal' ? GOLD : BLUE} />
    <Particles seed={`flashcrash-${scene.id}`} count={scene.act === 'climax' ? 38 : 22} color={scene.act === 'climax' ? RED : GOLD} />
    <SceneGraphic scene={scene} />
    <Lower scene={scene} />
    <SourceBug scene={scene} />
    <ReconLabel />
    <Vignette strength={1} />
    <Grain opacity={0.052} />
  </AbsoluteFill>
);

export const FlashCrashPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={framesFor(HOOK_SEC)} name="flash_forward_hook">
      <HookMontage />
    </Sequence>
    <Sequence from={framesFor(OPENING_AT)} durationInFrames={framesFor(OPENING_SEC)} name="brand_opening">
      <BrandOpening seriesLabel="Prime Documentary" title="Flash Crash" subtitle="Did one man break the market?" />
    </Sequence>
    {scenes.map((scene, index) => (
      <Sequence key={scene.id} from={framesFor(sceneStart(index))} durationInFrames={framesFor(sceneDuration(index))} name={`${scene.act}_${scene.id}`}>
        <SceneView scene={scene} />
      </Sequence>
    ))}
    <Sequence from={framesFor(MAIN_END)} durationInFrames={framesFor(ENDCARD_SEC)} name="brand_endcard">
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile(MIX_SRC)} />
    <CaptionBand />
  </AbsoluteFill>
);

export const flashCrashPremiumDurationInFrames = (fps: number = FPS): number => framesFor(TOTAL_SEC, fps);
