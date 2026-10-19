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
import {ONECOIN_CAPTIONS} from '../data/onecoin_captions';
import {ONECOIN_FACTORY, ONECOIN_FACTORY_LEDGER} from '../data/onecoin_factory_assets';
import {ONECOIN_ROUGHCUT} from '../data/onecoin_roughcut';
import type {CaptionCue, RoughCutData, RoughShot} from './RoughCut';

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#C94B4B';
const BLACK = '#000000';
const SILENCE_SPAN_ID = 'SPN-0043';
const OPENING_AFTER_SPAN_ID = 'SPN-0005';
const EDITORIAL_OPENING_AFTER_SPAN_ID = 'SPN-0003';
const TARGET_SECONDS = 30 * 60;
const INK_OVERLAY = 'onecoin/hero/T-IMG-014.png';

type ChapterId = 'cold_open' | 'the_promise' | 'the_crack' | 'the_void' | 'coda';
type TimedShot = RoughShot & {start: number; dur: number; sourceIndex: number};
type Schedule = {shots: TimedShot[]; totalSec: number; silence?: TimedShot; sourceOffset: number};

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));
const isImage = (src: string): boolean => /\.(png|jpe?g|webp)$/i.test(src);

const CHAPTER_META: Record<ChapterId, {kicker: string; title: string; grade: string; accent: string}> = {
  cold_open: {kicker: 'Hook', title: 'Nothing', grade: 'gold', accent: GOLD},
  the_promise: {kicker: 'Part I', title: 'The Promise', grade: 'gold', accent: GOLD},
  the_crack: {kicker: 'Part II', title: 'The Crack', grade: 'white', accent: SILVER},
  the_void: {kicker: 'Part III', title: 'The Void', grade: 'black', accent: WHITE},
  coda: {kicker: 'Coda', title: 'How Late?', grade: 'white', accent: SILVER},
};

const FIRST_SPAN_BY_CHAPTER: Record<ChapterId, string> = {
  cold_open: 'SPN-0001',
  the_promise: 'SPN-0006',
  the_crack: 'SPN-0020',
  the_void: 'SPN-0035',
  coda: 'SPN-0045',
};

const HOOK_BEATS: Record<string, {top: string; main: string; sub: string}> = {
  'SPN-0001': {top: 'London', main: 'YOU ARE NOT TOO LATE', sub: 'the room believes'},
  'SPN-0003': {top: 'Before we start', main: 'NO BLOCKCHAIN', sub: 'nothing to check'},
  'SPN-0005': {top: 'Prime Documentary', main: 'NOTHING', sub: 'a coin with a hole in it'},
};

const sourceSeconds = (shots = ONECOIN_ROUGHCUT.shots): number => shots.reduce((sum, shot) => sum + shot.seconds, 0);

const scheduledShots = (data: RoughCutData, chapterId?: ChapterId): Schedule => {
  if (chapterId) {
    const full = scheduledShots(data);
    const chapterShots = full.shots.filter((shot) => shot.chapterId === chapterId);
    const sourceOffset = chapterShots[0]?.start ?? 0;
    const localShots = chapterShots.map((shot) => ({...shot, start: shot.start - sourceOffset}));
    const shotEnd = localShots.reduce((end, shot) => Math.max(end, shot.start + shot.dur), 0);
    const includeOpening = data.timelineMode !== 'editorial';
    const totalSec = shotEnd + (includeOpening && chapterId === 'cold_open' ? OPENING_SEC : 0) + (chapterId === 'coda' ? ENDCARD_SEC : 0);
    return {shots: localShots, totalSec, silence: localShots.find((shot) => shot.spanId === SILENCE_SPAN_ID), sourceOffset};
  }
  const sourceShots = data.shots;
  const sourceTotal = sourceSeconds(sourceShots);
  const hasSilence = sourceShots.some((shot) => shot.spanId === SILENCE_SPAN_ID);
  const isEditorial = data.timelineMode === 'editorial';
  const includeOpening = !isEditorial;
  const openingAfterSpanId = isEditorial ? EDITORIAL_OPENING_AFTER_SPAN_ID : OPENING_AFTER_SPAN_ID;
  const target = isEditorial ? sourceTotal + (includeOpening ? OPENING_SEC : 0) + ENDCARD_SEC : TARGET_SECONDS;
  const fixed = (includeOpening ? OPENING_SEC : 0) + ENDCARD_SEC + (hasSilence ? 3 : 0);
  const sourceFixed = hasSilence ? 3 : 0;
  const scale = isEditorial ? 1 : Math.max(0.1, (target - fixed) / Math.max(1, sourceTotal - sourceFixed));
  let cursor = 0;
  const timed: TimedShot[] = [];
  sourceShots.forEach((shot) => {
    const dur = shot.spanId === SILENCE_SPAN_ID ? 3 : shot.seconds * scale;
    const timedShot = {...shot, start: cursor, dur, sourceIndex: data.shots.findIndex((candidate) => candidate.spanId === shot.spanId)};
    timed.push(timedShot);
    cursor += dur;
    if (!chapterId && includeOpening && shot.spanId === openingAfterSpanId) {
      cursor += OPENING_SEC;
    }
  });
  cursor += ENDCARD_SEC;
  return {shots: timed, totalSec: isEditorial ? cursor : TARGET_SECONDS, silence: timed.find((shot) => shot.spanId === SILENCE_SPAN_ID), sourceOffset: 0};
};

export const oneCoinPremiumDurationInFrames = (fps: number = BRAND.video.fps, chapterId?: ChapterId): number =>
  framesFor(scheduledShots(ONECOIN_ROUGHCUT, chapterId).totalSec, fps);

const chapter = (shot: RoughShot): ChapterId => (shot.chapterId as ChapterId) ?? 'the_promise';

const chapterTint = (shot: RoughShot): string => {
  const c = chapter(shot);
  if (c === 'the_promise' || c === 'cold_open') return `linear-gradient(180deg, #150D03DD 0%, #00000022 45%, #050302F0 100%)`;
  if (c === 'the_crack' || c === 'coda') return `linear-gradient(180deg, #DDE8F51A 0%, #00000020 42%, #02050BEE 100%)`;
  return `linear-gradient(180deg, #000000D8 0%, #00000055 44%, #000000F4 100%)`;
};

const pickFactory = (shot: TimedShot): string[] => {
  if (shot.spanId === SILENCE_SPAN_ID) return [];
  const primary = ONECOIN_FACTORY_LEDGER[shot.sourceIndex % ONECOIN_FACTORY_LEDGER.length]?.src;
  const c = chapter(shot);
  const group =
    c === 'the_promise' || c === 'cold_open'
      ? shot.sourceIndex % 2 === 0
        ? ONECOIN_FACTORY.stage
        : ONECOIN_FACTORY.finance
      : c === 'the_crack'
        ? shot.sourceIndex % 2 === 0
          ? ONECOIN_FACTORY.surveillance
          : ONECOIN_FACTORY.documents
        : c === 'coda'
          ? ONECOIN_FACTORY.vanishing
          : shot.assetRef === 'MG-BLACK'
            ? ONECOIN_FACTORY.void
            : ONECOIN_FACTORY.atmosphere;
  const secondary = group?.[shot.sourceIndex % Math.max(1, group.length)];
  return Array.from(new Set([primary, secondary].filter(Boolean) as string[]));
};

const safeImages = (shot: RoughShot): string[] => Array.from(new Set((shot.images ?? []).filter(isImage)));

const MovingImage: React.FC<{src: string; seed: string; durationFrames: number; intensity?: number}> = ({src, seed, durationFrames, intensity = 1}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, Math.max(1, durationFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = seed.length % 2 === 0 ? 1 : -1;
  const push = spring({frame, fps: 30, config: {damping: 28, stiffness: 36}});
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        filter: 'brightness(0.74) contrast(1.24) saturate(0.94)',
        transform: `translate3d(${dir * interpolate(p, [0, 1], [-78, 78]) * intensity}px, ${interpolate(p, [0, 1], [36, -38]) * intensity}px, 0) scale(${1.075 + p * 0.12 + push * 0.012 * intensity})`,
      }}
    />
  );
};

const ImageSequence: React.FC<{shot: TimedShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const images = safeImages(shot);
  if (!images.length || shot.assetType === 'motion_graphic') return <AtmosphereFallback shot={shot} />;
  const per = Math.max(framesFor(1.65, fps), Math.round(durationInFrames / Math.max(5, Math.min(14, images.length))));
  const segments: {src: string; frames: number; index: number}[] = [];
  let used = 0;
  let index = 0;
  while (used < durationInFrames) {
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: images[index % images.length], frames, index});
    used += frames;
    index += 1;
  }
  return (
    <Series>
      {segments.map((segment) => (
        <Series.Sequence key={`${segment.index}-${segment.src}`} durationInFrames={segment.frames}>
          <MovingImage src={segment.src} seed={`${shot.spanId}-${segment.index}`} durationFrames={segment.frames} intensity={chapter(shot) === 'cold_open' ? 1.28 : 1.08} />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const FactoryLayer: React.FC<{shot: TimedShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const clips = pickFactory(shot);
  if (!clips.length) return null;
  const per = Math.max(framesFor(2.2, fps), Math.round(durationInFrames / Math.max(5, clips.length * 2)));
  const segments: {src: string; frames: number; index: number}[] = [];
  let used = 0;
  let index = 0;
  while (used < durationInFrames) {
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: clips[index % clips.length], frames, index});
    used += frames;
    index += 1;
  }
  const c = chapter(shot);
  return (
    <AbsoluteFill
      style={{
        opacity: c === 'the_void' ? 0.46 : c === 'the_crack' ? 0.34 : c === 'coda' ? 0.26 : 0.3,
        mixBlendMode: c === 'the_void' || shot.assetType === 'motion_graphic' ? 'screen' : 'normal',
      }}
    >
      <Series>
        {segments.map((segment) => (
          <Series.Sequence key={`${segment.index}-${segment.src}`} durationInFrames={segment.frames}>
            <OffthreadVideo
              src={staticFile(segment.src)}
              muted
              playbackRate={1.08}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                filter: 'brightness(0.54) contrast(1.26) saturate(0.82)',
                transform: 'scale(1.055)',
              }}
            />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};

const InkOverlay: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  if (chapter(shot) !== 'the_void' && shot.assetRef !== 'MG-BLACK') return null;
  const opacity = 0.16 + 0.05 * Math.sin(frame * 0.025);
  return (
    <AbsoluteFill style={{opacity, mixBlendMode: 'screen'}}>
      <MovingImage src={INK_OVERLAY} seed={`ink-${shot.spanId}`} durationFrames={360} intensity={0.38} />
    </AbsoluteFill>
  );
};

const AtmosphereFallback: React.FC<{shot: TimedShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 260], [-90, 90], {extrapolateRight: 'extend'});
  const c = chapter(shot);
  const accent = CHAPTER_META[c].accent;
  return (
    <AbsoluteFill style={{background: `radial-gradient(95% 85% at 55% 38%, ${c === 'the_promise' ? '#2C1704' : NAVY} 0%, ${INK} 82%)`}}>
      <FactoryLayer shot={shot} />
      <div style={{position: 'absolute', width: 920, height: 920, borderRadius: '50%', border: `2px solid ${accent}55`, left: 500 + drift * 0.16, top: 90}} />
      <div style={{position: 'absolute', left: 650, top: 540, width: 440, height: 3, background: accent, opacity: 0.48}} />
    </AbsoluteFill>
  );
};

const EmptyLedger: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <defs>
        <linearGradient id="ledgerPage" x1="0" x2="1">
          <stop offset="0%" stopColor="#E9EEF6" stopOpacity="0.78" />
          <stop offset="100%" stopColor="#8EA4B9" stopOpacity="0.2" />
        </linearGradient>
      </defs>
      <path d="M420 260 C620 210 770 238 960 330 C1150 238 1300 210 1500 260 L1500 825 C1305 784 1155 802 960 892 C765 802 615 784 420 825 Z" fill="url(#ledgerPage)" stroke={SILVER} strokeWidth="4" opacity="0.82" />
      <line x1="960" y1="330" x2="960" y2="890" stroke={SILVER} strokeWidth="3" opacity="0.5" />
      {Array.from({length: 8}, (_, i) => {
        const y = 390 + i * 55;
        const leftFade = interpolate(frame - i * 10, [0, 24, 64], [0, 0.75, 0.08], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <g key={i}>
            <line x1="510" y1={y} x2="880" y2={y} stroke={BLUE} strokeWidth="3" opacity={0.16 + leftFade * 0.28} />
            <line x1="1040" y1={y} x2="1410" y2={y} stroke={BLUE} strokeWidth="3" opacity={0.16 + leftFade * 0.28} />
          </g>
        );
      })}
      {Array.from({length: 12}, (_, i) => {
        const x = 490 + i * 78;
        const y = 210 + Math.sin(i) * 28;
        const fall = interpolate(p, [0.25, 0.85], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return <rect key={i} x={x + fall * (i - 6) * 18} y={y + fall * 530} width="42" height="12" rx="6" fill="none" stroke={GOLD} strokeWidth="5" opacity={1 - fall * 0.82} transform={`rotate(${i * 9} ${x} ${y})`} />;
      })}
      <text x="960" y="175" fill={WHITE} fontFamily={BRAND.font.display} fontSize="78" textAnchor="middle">THE LEDGER NEVER FILLS</text>
      <text x="960" y="948" fill={SILVER} fontFamily={BRAND.font.body} fontSize="31" textAnchor="middle">rows appear, then empty themselves</text>
    </svg>
  );
};

const MlmTree: React.FC = () => {
  const frame = useCurrentFrame();
  const nodes = [
    [960, 230, 0],
    [780, 390, 14],
    [1140, 390, 18],
    [640, 560, 30],
    [840, 560, 36],
    [1080, 560, 42],
    [1280, 560, 48],
    [530, 745, 58],
    [720, 745, 64],
    [900, 745, 70],
    [1020, 745, 76],
    [1200, 745, 82],
    [1390, 745, 88],
  ];
  const collapse = interpolate(frame, [180, 290], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {nodes.slice(1).map(([x, y], i) => {
        const parent = i < 2 ? nodes[0] : nodes[1 + Math.floor((i - 2) / 2)];
        return <line key={`${x}-${y}`} x1={parent[0]} y1={parent[1]} x2={x} y2={y} stroke={GOLD} strokeWidth="4" opacity={0.5 * (1 - collapse)} />;
      })}
      {nodes.map(([x, y, delay], i) => {
        const on = spring({frame: frame - delay, fps: 30, config: {damping: 15, stiffness: 88}});
        const dx = (x - 960) * collapse * 0.18;
        const dy = collapse * 120;
        return <circle key={i} cx={x + dx} cy={y + dy} r={22 + on * 8} fill={collapse > 0.85 ? BLACK : GOLD} stroke={collapse > 0.6 ? RED : WHITE} strokeWidth="4" opacity={Math.max(0.06, Math.min(1, on) * (1 - collapse * 0.78))} />;
      })}
      <path d="M960 210 L520 800 L1400 800 Z" fill="none" stroke={collapse > 0.2 ? RED : BLUE} strokeWidth="7" strokeDasharray="18 14" opacity="0.68" />
      <text x="960" y="930" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">recruitment turns belief into a structure</text>
    </svg>
  );
};

const BarsGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const raised = interpolate(frame, [15, 130], [0, 880], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const pulse = 1 + Math.sin(frame * 0.07) * 0.015;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="190" fill={WHITE} fontFamily={BRAND.font.display} fontSize="76" textAnchor="middle">WHAT WAS RAISED</text>
      <text x="960" y="248" fill={SILVER} fontFamily={BRAND.font.body} fontSize="28" textAnchor="middle">according to U.S. prosecutors and OneCoin records</text>
      <text x="420" y="422" fill={GOLD} fontFamily={BRAND.font.display} fontSize="58">OVER $4B</text>
      <rect x="690" y="368" width="900" height="82" fill="#08101A" stroke={GOLD} strokeWidth="4" />
      <rect x="700" y="378" width={raised} height="62" fill={GOLD} />
      <text x="420" y="614" fill={SILVER} fontFamily={BRAND.font.display} fontSize="58">REAL COIN</text>
      <rect x="690" y="560" width="900" height="82" fill="#08101A" stroke={SILVER} strokeWidth="4" />
      <rect x="700" y="570" width="4" height="62" fill={RED} transform={`scale(${pulse} 1)`} />
      <text x="1140" y="620" fill={RED} fontFamily={BRAND.font.display} fontSize="72" textAnchor="middle">0</text>
      <text x="960" y="795" fill={WHITE} fontFamily={BRAND.font.body} fontSize="38" textAnchor="middle">the number on the screen was cheaper than the money behind it</text>
    </svg>
  );
};

const WantedPoster: React.FC = () => {
  const frame = useCurrentFrame();
  const enter = spring({frame, fps: 30, config: {damping: 20, stiffness: 58}});
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
      <div
        style={{
          width: 660,
          height: 840,
          background: '#E8E1D4',
          border: '10px solid #111',
          boxShadow: '0 28px 85px #000',
          transform: `translateY(${(1 - enter) * 30}px) rotate(${-1.3 + Math.sin(frame * 0.01) * 0.35}deg)`,
          padding: 34,
          color: '#111',
          fontFamily: BRAND.font.body,
        }}
      >
        <div style={{fontFamily: BRAND.font.display, fontSize: 82, textAlign: 'center', lineHeight: 0.9}}>WANTED</div>
        <div style={{margin: '20px auto 18px', width: 330, height: 330, background: '#111', borderRadius: '50% 50% 44% 44%', position: 'relative', overflow: 'hidden'}}>
          <div style={{position: 'absolute', left: 118, top: 68, width: 94, height: 116, borderRadius: '50%', background: '#E8E1D4', opacity: 0.96}} />
          <div style={{position: 'absolute', left: 70, top: 192, width: 190, height: 150, borderRadius: '70% 70% 0 0', background: '#E8E1D4', opacity: 0.96}} />
        </div>
        <div style={{fontFamily: BRAND.font.display, fontSize: 48, textAlign: 'center'}}>RUJA IGNATOVA</div>
        <div style={{height: 5, background: '#111', margin: '20px 0'}} />
        <div style={{fontSize: 34, fontWeight: 900, textAlign: 'center'}}>UP TO $5,000,000</div>
        <div style={{fontSize: 32, fontWeight: 900, color: '#7A1111', textAlign: 'center', marginTop: 13}}>VANISHED</div>
        <div style={{fontSize: 17, textAlign: 'center', marginTop: 26, lineHeight: 1.28}}>CHARGED AND WANTED. NOT CONVICTED. NO REAL-PERSON LIKENESS.</div>
      </div>
    </AbsoluteFill>
  );
};

const CoinVoid: React.FC = () => {
  const frame = useCurrentFrame();
  const spin = frame * 0.35;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <circle cx="960" cy="540" r="242" fill={GOLD} opacity="0.85" />
      <circle cx="960" cy="540" r="88" fill={BLACK} />
      <circle cx="960" cy="540" r="244" fill="none" stroke={WHITE} strokeWidth="4" opacity="0.45" strokeDasharray="20 18" transform={`rotate(${spin} 960 540)`} />
      <line x1="840" y1="540" x2="1080" y2="540" stroke={BLACK} strokeWidth="14" opacity="0.55" />
      <text x="960" y="880" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">light passes through the product</text>
    </svg>
  );
};

const GraphicFor: React.FC<{shot: TimedShot}> = ({shot}) => {
  if (shot.assetRef === 'MG-LEDGER') return <EmptyLedger />;
  if (shot.assetRef === 'MG-TREE') return <MlmTree />;
  if (shot.assetRef === 'MG-BARS') return <BarsGraphic />;
  if (shot.assetRef === 'T-IMG-003') return <CoinVoid />;
  if (shot.spanId === 'SPN-0041' || shot.spanId === 'SPN-0042') return <WantedPoster />;
  return null;
};

const Lower: React.FC<{shot: TimedShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const reveal = spring({frame: frame - Math.round(0.15 * fps), fps, config: {damping: 18, stiffness: 95}});
  const c = chapter(shot);
  const meta = CHAPTER_META[c];
  return (
    <div style={{position: 'absolute', left: 54, top: 42, opacity: Math.min(1, reveal), maxWidth: 1120}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: meta.accent, fontWeight: 900, textTransform: 'uppercase'}}>
        {meta.title} / {shot.spanId}
      </div>
      <div style={{width: 260, height: 2, background: meta.accent, marginTop: 9}} />
    </div>
  );
};

const SafetyLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 44,
      top: 42,
      fontFamily: BRAND.font.body,
      fontSize: 14,
      color: SILVER,
      padding: '6px 9px',
      border: `1px solid ${GOLD}88`,
      background: '#0000008C',
      opacity: 0.82,
    }}
  >
    symbolic reconstruction / no real-person likeness
  </div>
);

const ChapterMarker: React.FC<{shot: TimedShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const c = chapter(shot);
  if (FIRST_SPAN_BY_CHAPTER[c] !== shot.spanId || c === 'cold_open' || frame > fps * 4.2) return null;
  const meta = CHAPTER_META[c];
  const reveal = spring({frame, fps, config: {damping: 18, stiffness: 70}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 140, paddingRight: 140, pointerEvents: 'none'}}>
      <div style={{opacity: Math.min(1, reveal), transform: `translateY(${(1 - reveal) * 30}px)`}}>
        <div style={{fontFamily: BRAND.font.body, color: meta.accent, fontSize: 28, fontWeight: 900, textTransform: 'uppercase', marginBottom: 18}}>
          {meta.kicker}
        </div>
        <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 104, lineHeight: 0.94, textTransform: 'uppercase', textShadow: '0 12px 38px #000'}}>
          {meta.title}
        </div>
        <div style={{width: 420, height: 5, background: meta.accent, marginTop: 30}} />
      </div>
    </AbsoluteFill>
  );
};

const HookOverlay: React.FC<{shot: TimedShot}> = ({shot}) => {
  const beat = HOOK_BEATS[shot.spanId];
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!beat) return null;
  const durationInFrames = framesFor(shot.dur, fps);
  const enter = spring({frame: frame - 4, fps, config: {damping: 16, stiffness: 120}});
  const fade = interpolate(frame, [Math.max(1, durationInFrames - fps * 1.2), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 110, paddingRight: 110, opacity: fade}}>
      <div style={{maxWidth: 1320, transform: `translateX(${(1 - enter) * -70}px)`}}>
        <div style={{fontFamily: BRAND.font.body, color: GOLD, fontWeight: 900, fontSize: 30, textTransform: 'uppercase', letterSpacing: 0, marginBottom: 12}}>
          {beat.top}
        </div>
        <div
          style={{
            fontFamily: BRAND.font.display,
            color: beat.main === 'NOTHING' ? GOLD : WHITE,
            fontSize: beat.main.length > 13 ? 104 : 144,
            lineHeight: 0.86,
            textTransform: 'uppercase',
            textShadow: `0 14px 48px #000, 0 0 44px ${BLUE}88`,
          }}
        >
          {beat.main}
        </div>
        <div style={{fontFamily: BRAND.font.body, color: SILVER, fontWeight: 900, fontSize: 34, textTransform: 'uppercase', marginTop: 22}}>
          {beat.sub}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const CaptionBand: React.FC<{captions: CaptionCue[]; timeOffset: number; silence?: TimedShot}> = ({captions, timeOffset, silence}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const compositionT = frame / fps;
  if (silence && compositionT >= silence.start && compositionT < silence.start + silence.dur) return null;
  const t = compositionT + timeOffset;
  const cue = captions.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 50,
        right: 50,
        bottom: 42,
        minHeight: 56,
        maxWidth: 1180,
        margin: '0 auto',
        padding: '9px 24px 10px',
        background: '#0000008C',
        borderTop: `1px solid ${GOLD}88`,
        borderRadius: 3,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 700,
        fontSize: cue.text.length > 54 ? 30 : 34,
        lineHeight: 1.12,
        maxHeight: 76,
        overflow: 'hidden',
        textAlign: 'center',
        textShadow: '0 3px 12px #000, 0 0 2px #000',
        whiteSpace: 'pre-line',
        letterSpacing: 0,
      }}
    >
      {cue.text}
    </div>
  );
};

const Scene: React.FC<{shot: TimedShot}> = ({shot}) => {
  if (shot.spanId === SILENCE_SPAN_ID) return <AbsoluteFill style={{backgroundColor: BLACK}} />;
  const c = chapter(shot);
  return (
    <AbsoluteFill style={{backgroundColor: c === 'the_void' ? BLACK : INK, overflow: 'hidden'}}>
      {shot.assetType === 'motion_graphic' ? <AtmosphereFallback shot={shot} /> : <ImageSequence shot={shot} />}
      <FactoryLayer shot={shot} />
      <InkOverlay shot={shot} />
      <AbsoluteFill style={{background: chapterTint(shot)}} />
      <LightSweep seed={`onecoin-${shot.spanId}`} color={CHAPTER_META[c].accent} />
      <Particles seed={`onecoin-${shot.spanId}`} count={shot.assetType === 'motion_graphic' ? 24 : 16} color={CHAPTER_META[c].accent} />
      <GraphicFor shot={shot} />
      <HookOverlay shot={shot} />
      <ChapterMarker shot={shot} />
      <Lower shot={shot} />
      <SafetyLabel />
      <Vignette strength={0.98} />
      <Grain opacity={0.055} />
    </AbsoluteFill>
  );
};

const OneCoinAudio: React.FC<{data: RoughCutData; silence?: TimedShot; sourceOffset: number}> = ({data, silence, sourceOffset}) => {
  const {fps} = useVideoConfig();
  const sources = [data.narrationSrc, data.bgmSrc].filter(Boolean) as string[];
  if (!sources.length) return null;
  const sourceOffsetFrames = framesFor(sourceOffset, fps);
  if (!silence) return <>{sources.map((src) => <Audio key={src} src={staticFile(src)} startFrom={sourceOffsetFrames} volume={src === data.bgmSrc ? 0.16 : 1} />)}</>;
  const cutStart = framesFor(silence.start, fps);
  const cutEnd = framesFor(silence.start + silence.dur, fps);
  return (
    <>
      {sources.map((src) => (
        <React.Fragment key={src}>
          <Audio src={staticFile(src)} startFrom={sourceOffsetFrames} endAt={sourceOffsetFrames + cutStart} volume={src === data.bgmSrc ? 0.16 : 1} />
          <Sequence from={cutEnd}>
            <Audio src={staticFile(src)} startFrom={sourceOffsetFrames + cutEnd} volume={src === data.bgmSrc ? 0.16 : 1} />
          </Sequence>
        </React.Fragment>
      ))}
    </>
  );
};

export const OneCoinPremium: React.FC<{chapterId?: ChapterId}> = ({chapterId}) => {
  const {fps} = useVideoConfig();
  const data: RoughCutData = {...ONECOIN_ROUGHCUT, captions: ONECOIN_CAPTIONS};
  const schedule = scheduledShots(data, chapterId);
  const fullSchedule = chapterId ? scheduledShots(data) : schedule;
  const captionTimeOffset = chapterId ? fullSchedule.shots.find((shot) => shot.chapterId === chapterId)?.start ?? 0 : 0;
  const includeOpening = data.timelineMode !== 'editorial';
  const openingSpan = data.timelineMode === 'editorial' ? EDITORIAL_OPENING_AFTER_SPAN_ID : OPENING_AFTER_SPAN_ID;
  const openingShot = schedule.shots.find((shot) => shot.spanId === openingSpan);
  const endFrom = framesFor(schedule.totalSec - (!chapterId ? ENDCARD_SEC : 0), fps);
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {schedule.shots.map((shot) => (
        <Sequence key={shot.spanId} from={framesFor(shot.start, fps)} durationInFrames={framesFor(shot.dur, fps)} name={`${shot.chapterId}_${shot.spanId}`}>
          <Scene shot={shot} />
        </Sequence>
      ))}
      {includeOpening && (!chapterId || chapterId === 'cold_open') && openingShot ? (
        <Sequence from={framesFor(openingShot.start + openingShot.dur, fps)} durationInFrames={framesFor(OPENING_SEC, fps)} name="brand_opening">
          <BrandOpening seriesLabel="Prime Documentary" title="Nothing" subtitle="The Woman Who Sold a Coin That Did Not Exist" />
        </Sequence>
      ) : null}
      {(!chapterId || chapterId === 'coda') ? (
        <Sequence from={endFrom} durationInFrames={framesFor(ENDCARD_SEC, fps)} name="brand_endcard">
          <BrandEndcard />
        </Sequence>
      ) : null}
      <OneCoinAudio data={data} silence={schedule.silence} sourceOffset={schedule.sourceOffset} />
      <CaptionBand captions={data.captions ?? []} timeOffset={captionTimeOffset} silence={schedule.silence} />
    </AbsoluteFill>
  );
};
