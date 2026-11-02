import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  Series,
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
import {TITAN_CAPTIONS} from '../data/titan_captions';
import {TITAN_FACTORY} from '../data/titan_factory_assets';
import {TITAN_ROUGHCUT} from '../data/titan_roughcut';
import type {CaptionCue, RoughCutData, RoughShot} from './RoughCut';

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#C64747';
const SILENCE_SPAN_ID = 'SPN-0071';
const SILENCE_BLACKOUT_START_SEC = 2275.7;
const SILENCE_BLACKOUT_DURATION_SEC = 2.05;
const OPENING_AFTER_SPAN_ID = 'SPN-0005';
const TITAN_REVIEW_MIX_SRC = 'titan/audio/titan_final_mix_v001.wav';
const BAD_FACTORY_ASSETS = new Set(['titan/factory/AF-VFX-0211__ink_in_water.mp4']);

type TimedShot = RoughShot & {start: number; dur: number};

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));

const isVideo = (src: string): boolean => /\.(mp4|mov|webm)$/i.test(src);
const isImage = (src: string): boolean => /\.(png|jpe?g|webp)$/i.test(src);

const pick = (key: keyof typeof TITAN_FACTORY, seed: string, count = 1): string[] => {
  const pool = (TITAN_FACTORY[key] ?? []).filter((src) => !BAD_FACTORY_ASSETS.has(src));
  if (!pool.length) return [];
  const start = seed.split('').reduce((sum, ch) => sum + ch.charCodeAt(0), 0) % pool.length;
  return Array.from({length: Math.min(count, pool.length)}, (_, i) => pool[(start + i) % pool.length]);
};

const orderedWithOpening = (data: RoughCutData): TimedShot[] => {
  let cursor = 0;
  const timed: TimedShot[] = [];
  data.shots.forEach((shot) => {
    timed.push({...shot, start: cursor, dur: shot.seconds});
    cursor += shot.seconds;
    if (shot.spanId === OPENING_AFTER_SPAN_ID) {
      cursor += OPENING_SEC;
    }
  });
  return timed;
};

export const titanPremiumDurationInFrames = (fps: number = BRAND.video.fps): number => {
  const body = TITAN_ROUGHCUT.shots.reduce((sum, shot) => sum + shot.seconds, 0);
  return framesFor(body + OPENING_SEC + ENDCARD_SEC, fps);
};

const titanDurationSeconds = (): number => TITAN_ROUGHCUT.shots.reduce((sum, shot) => sum + shot.seconds, 0) + OPENING_SEC + ENDCARD_SEC;

const safeImages = (shot: RoughShot): string[] =>
  Array.from(new Set([...(shot.images ?? []), ...(shot.src && shot.assetType !== 'stock_video' ? [shot.src] : [])].filter(isImage)));

const FIRST_SPAN_BY_CHAPTER: Record<string, string> = {
  cold_open: 'SPN-0001',
  the_dream: 'SPN-0006',
  the_warnings: 'SPN-0029',
  the_dive: 'SPN-0058',
  the_search: 'SPN-0073',
  the_truth: 'SPN-0088',
  coda: 'SPN-0103',
};

const CHAPTER_TITLES: Record<string, {kicker: string; title: string}> = {
  cold_open: {kicker: 'Hook', title: 'The Last Dive'},
  the_dream: {kicker: 'Part I', title: 'The Dream'},
  the_warnings: {kicker: 'Part II', title: 'The Warnings'},
  the_dive: {kicker: 'Part III', title: 'The Dive'},
  the_search: {kicker: 'Part IV', title: 'The Search'},
  the_truth: {kicker: 'Part V', title: 'The Truth'},
  coda: {kicker: 'Coda', title: 'What Remains'},
};

const HOOK_BEATS: Record<string, {top: string; main: string; sub: string}> = {
  'SPN-0001': {top: 'Cold open', main: '17 BOLTS', sub: 'one hatch, one descent'},
  'SPN-0002': {top: 'The clock', main: '96:00:00', sub: 'a promise that would collapse'},
  'SPN-0003': {top: 'North Atlantic', main: 'MISSING', sub: 'the world waits for a signal'},
  'SPN-0004': {top: 'The phrase', main: 'PURE WASTE', sub: 'safety, treated as friction'},
  'SPN-0005': {top: 'Prime Documentary', main: 'THE LAST DIVE', sub: 'Titan, June 2023'},
};

const sceneFactory = (shot: RoughShot): string[] => {
  if (shot.spanId === SILENCE_SPAN_ID) return [];
  if (shot.chapterId === 'the_dive') return [...pick('ink_in_water', shot.spanId, 2), ...pick('caustics_water_light', shot.spanId, 1)];
  if (shot.chapterId === 'the_search') return [...pick('surveillance_tech', shot.spanId, 2), ...pick('clock_ticking_macro', shot.spanId, 1)];
  if (shot.chapterId === 'the_warnings') return [...pick('documents_paper', shot.spanId, 1), ...pick('old_paper_texture', shot.spanId, 1)];
  if (shot.chapterId === 'the_truth') return [...pick('documents_paper', shot.spanId, 1), ...pick('old_paper_texture', shot.spanId, 1)];
  if (shot.chapterId === 'coda') return [];
  if (shot.chapterId === 'the_dream') return [...pick('ocean_horizon_moody', shot.spanId, 1), ...pick('finance_money', shot.spanId, 1)];
  return pick('ocean_horizon_moody', shot.spanId, 1);
};

const MovingImage: React.FC<{src: string; seed: string; durationFrames: number; intensity?: number}> = ({
  src,
  seed,
  durationFrames,
  intensity = 1,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, Math.max(1, durationFrames - 1)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = seed.length % 2 === 0 ? 1 : -1;
  const push = spring({frame, fps: 30, config: {damping: 28, stiffness: 38}});
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        filter: 'brightness(0.72) contrast(1.22) saturate(0.95)',
        transform: `translate3d(${dir * interpolate(p, [0, 1], [-74, 74]) * intensity}px, ${interpolate(p, [0, 1], [34, -38]) * intensity}px, 0) scale(${1.075 + p * 0.12 + push * 0.015 * intensity})`,
      }}
    />
  );
};

const ImageSequence: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const images = safeImages(shot);
  if (!images.length) return <AtmosphereFallback shot={shot} />;
  const baseCut = shot.chapterId === 'cold_open' ? 3.1 : shot.assetType === 'motion_graphic' ? 3.8 : 4.6;
  const per = Math.max(framesFor(baseCut, fps), Math.round(durationInFrames / Math.min(7, images.length)));
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
          <MovingImage src={segment.src} seed={`${shot.spanId}-${segment.index}`} durationFrames={segment.frames} intensity={shot.chapterId === 'cold_open' ? 1.28 : 1} />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const TextureLayer: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const stills = sceneFactory(shot).filter(isImage);
  if (!stills.length) return null;
  const per = Math.max(framesFor(4.8, fps), Math.round(durationInFrames / Math.min(3, stills.length)));
  const segments: {src: string; frames: number; index: number}[] = [];
  let used = 0;
  let index = 0;
  while (used < durationInFrames) {
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: stills[index % stills.length], frames, index});
    used += frames;
    index += 1;
  }
  const blend = shot.chapterId === 'the_warnings' || shot.chapterId === 'the_truth' ? 'screen' : 'overlay';
  return (
    <AbsoluteFill style={{opacity: shot.assetType === 'motion_graphic' ? 0.26 : 0.16, mixBlendMode: blend}}>
      <Series>
        {segments.map((segment) => (
          <Series.Sequence key={`${segment.index}-${segment.src}`} durationInFrames={segment.frames}>
            <MovingImage src={segment.src} seed={`texture-${shot.spanId}-${segment.index}`} durationFrames={segment.frames} intensity={0.42} />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};

const FactoryLayer: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const clips = sceneFactory(shot).filter(isVideo);
  if (!clips.length) return null;
  const per = Math.max(framesFor(5.2, fps), Math.round(durationInFrames / Math.min(4, clips.length)));
  const segments: {src: string; frames: number; index: number}[] = [];
  let used = 0;
  let index = 0;
  while (used < durationInFrames) {
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: clips[index % clips.length], frames, index});
    used += frames;
    index += 1;
  }
  return (
    <AbsoluteFill
      style={{
        opacity: shot.chapterId === 'cold_open' ? 0.36 : shot.chapterId === 'the_dive' ? 0.44 : shot.chapterId === 'the_search' ? 0.38 : shot.assetType === 'motion_graphic' ? 0.5 : 0.24,
        mixBlendMode: shot.chapterId === 'the_dive' || shot.chapterId === 'cold_open' ? 'screen' : 'normal',
      }}
    >
      <Series>
        {segments.map((segment) => (
          <Series.Sequence key={`${segment.index}-${segment.src}`} durationInFrames={segment.frames}>
            <Video
              src={staticFile(segment.src)}
              muted
              loop
              playbackRate={0.82}
              delayRenderTimeoutInMilliseconds={120000}
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                filter: 'brightness(0.58) contrast(1.24) saturate(0.84)',
                transform: 'scale(1.05)',
              }}
            />
          </Series.Sequence>
        ))}
      </Series>
    </AbsoluteFill>
  );
};

const AtmosphereFallback: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 260], [-90, 90], {extrapolateRight: 'extend'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(95% 85% at 55% 38%, ${NAVY} 0%, ${INK} 82%)`}}>
      <FactoryLayer shot={shot} />
      <div style={{position: 'absolute', width: 920, height: 920, borderRadius: '50%', border: `2px solid ${BLUE}55`, left: 500 + drift * 0.16, top: 90}} />
      <div style={{position: 'absolute', left: 650, top: 540, width: 440, height: 3, background: GOLD, opacity: 0.48}} />
    </AbsoluteFill>
  );
};

const DepthGauge: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const depth = Math.round(interpolate(p, [0, 1], [0, 3800]));
  const y = interpolate(depth, [0, 3800], [170, 850]);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="960" y1="170" x2="960" y2="850" stroke={SILVER} strokeWidth="4" opacity="0.55" />
      {[0, 1000, 2000, 3000, 3800].map((d) => {
        const ty = interpolate(d, [0, 3800], [170, 850]);
        return (
          <g key={d}>
            <line x1="900" y1={ty} x2="1020" y2={ty} stroke={d === 3800 ? GOLD : SILVER} strokeWidth={d === 3800 ? 6 : 3} />
            <text x="1045" y={ty + 10} fill={d === 3800 ? GOLD : SILVER} fontFamily={BRAND.font.body} fontSize="32">
              {d.toLocaleString()} m
            </text>
          </g>
        );
      })}
      <circle cx="960" cy={y} r="26" fill={BLUE} stroke={GOLD} strokeWidth="5" />
      <text x="820" y="116" fill={WHITE} fontFamily={BRAND.font.display} fontSize="72">
        {depth.toLocaleString()} m
      </text>
      <text x="782" y="914" fill={GOLD} fontFamily={BRAND.font.body} fontSize="30">
        Titanic depth marker
      </text>
    </svg>
  );
};

const OxygenCountdown: React.FC<{reveal?: boolean}> = ({reveal}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const p = interpolate(frame, [0, Math.max(1, durationInFrames - fps)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const total = Math.max(0, Math.round(96 * 3600 * (1 - p)));
  const hh = Math.floor(total / 3600).toString().padStart(2, '0');
  const mm = Math.floor((total % 3600) / 60).toString().padStart(2, '0');
  const ss = (total % 60).toString().padStart(2, '0');
  const snap = reveal && frame > durationInFrames * 0.58;
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 144, color: snap ? RED : WHITE, textShadow: `0 0 40px ${BLUE}88`}}>
        {snap ? '00:00:00' : `${hh}:${mm}:${ss}`}
      </div>
      <div style={{marginTop: 16, color: snap ? GOLD : SILVER, fontFamily: BRAND.font.body, fontWeight: 900, fontSize: snap ? 48 : 32, textTransform: 'uppercase'}}>
        {snap ? 'Day 1 was already 0' : 'reported oxygen clock'}
      </div>
    </AbsoluteFill>
  );
};

const WarningTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const items = [
    ['2018-01', 'safety report'],
    ['2018-03-27', 'industry letter: minor to catastrophic'],
    ['2022-07', 'Dive 80 anomaly / delamination'],
    ['2023-06-18', 'contact lost'],
    ['2025-08-05', 'USCG: preventable'],
  ];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="250" y1="540" x2="1670" y2="540" stroke={SILVER} strokeWidth="4" opacity="0.5" />
      {items.map(([date, label], i) => {
        const x = 250 + i * 355;
        const e = spring({frame: frame - i * 14, fps: 30, config: {damping: 18, stiffness: 95}});
        return (
          <g key={date} opacity={Math.min(1, e)}>
            <circle cx={x} cy="540" r="22" fill={i === items.length - 1 ? RED : BLUE} stroke={GOLD} strokeWidth="5" />
            <text x={x} y={i % 2 ? 470 : 628} fill={GOLD} fontFamily={BRAND.font.display} fontSize="44" textAnchor="middle">
              {date}
            </text>
            <text x={x} y={i % 2 ? 508 : 668} fill={WHITE} fontFamily={BRAND.font.body} fontSize="28" textAnchor="middle">
              {label}
            </text>
          </g>
        );
      })}
    </svg>
  );
};

const FatigueDiagram: React.FC = () => {
  const frame = useCurrentFrame();
  const cracks = Array.from({length: 9}, (_, i) => spring({frame: frame - i * 7, fps: 30, config: {damping: 17, stiffness: 90}}));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <defs>
        <linearGradient id="titanWall" x1="0" x2="1">
          <stop offset="0%" stopColor="#101B26" />
          <stop offset="50%" stopColor="#263A4F" />
          <stop offset="100%" stopColor="#071018" />
        </linearGradient>
        <marker id="arrow" markerWidth="14" markerHeight="14" refX="12" refY="7" orient="auto" markerUnits="strokeWidth">
          <path d="M2,2 L12,7 L2,12 Z" fill={BLUE} />
        </marker>
      </defs>
      <rect x="650" y="250" width="620" height="580" rx="18" fill="url(#titanWall)" stroke={SILVER} strokeWidth="4" />
      {[0, 1, 2, 3, 4].map((i) => (
        <line key={i} x1="690" y1={330 + i * 90} x2="1230" y2={330 + i * 90} stroke={BLUE} strokeWidth="3" opacity="0.35" />
      ))}
      {cracks.map((e, i) => {
        const x = 745 + (i % 3) * 170;
        const y = 340 + Math.floor(i / 3) * 130;
        return <path key={i} d={`M${x} ${y} l${45 * e} ${30 * e} l${-22 * e} ${38 * e} l${54 * e} ${28 * e}`} fill="none" stroke={GOLD} strokeWidth="5" opacity={Math.min(1, e)} />;
      })}
      <text x="960" y="170" fill={WHITE} fontFamily={BRAND.font.display} fontSize="72" textAnchor="middle">
        Compression fatigue
      </text>
      <text x="960" y="910" fill={SILVER} fontFamily={BRAND.font.body} fontSize="32" textAnchor="middle">
        Layers do not heal between cycles.
      </text>
      <g opacity="0.75">
        {[-1, 1].map((dir) => (
          <g key={dir}>
            <line x1={960 + dir * 560} y1="540" x2={960 + dir * 330} y2="540" stroke={BLUE} strokeWidth="12" markerEnd="url(#arrow)" />
          </g>
        ))}
      </g>
    </svg>
  );
};

const BoltCount: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <circle cx="960" cy="540" r="260" fill="none" stroke={SILVER} strokeWidth="12" opacity="0.55" />
      {Array.from({length: 17}, (_, i) => {
        const angle = (Math.PI * 2 * i) / 17 - Math.PI / 2;
        const x = 960 + Math.cos(angle) * 260;
        const y = 540 + Math.sin(angle) * 260;
        const on = frame > i * 5 ? 1 : 0.22;
        return <circle key={i} cx={x} cy={y} r="20" fill={on === 1 ? GOLD : SILVER} opacity={on} />;
      })}
      <text x="960" y="552" fill={WHITE} fontFamily={BRAND.font.display} fontSize="110" textAnchor="middle">
        17
      </text>
    </svg>
  );
};

const GraphicFor: React.FC<{shot: RoughShot}> = ({shot}) => {
  if (shot.spanId === 'SPN-0002' || shot.spanId === 'SPN-0005') return <BoltCount />;
  if (['SPN-0007', 'SPN-0009', 'SPN-0062', 'SPN-0066'].includes(shot.spanId)) return <DepthGauge />;
  if (['SPN-0075', 'SPN-0076'].includes(shot.spanId)) return <OxygenCountdown />;
  if (['SPN-0080', 'SPN-0081'].includes(shot.spanId)) return <OxygenCountdown reveal />;
  if (['SPN-0030', 'SPN-0035', 'SPN-0089', 'SPN-0092', 'SPN-0098'].includes(shot.spanId)) return <WarningTimeline />;
  if (['SPN-0019', 'SPN-0034', 'SPN-0090', 'SPN-0091'].includes(shot.spanId)) return <FatigueDiagram />;
  return null;
};

const Lower: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const reveal = spring({frame: frame - Math.round(0.15 * fps), fps, config: {damping: 18, stiffness: 95}});
  const label = shot.chapterId?.replace(/_/g, ' ') ?? '';
  return (
    <div style={{position: 'absolute', left: 54, top: 42, opacity: Math.min(1, reveal), maxWidth: 1180}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 900, textTransform: 'uppercase'}}>
        {label} / {shot.spanId}
      </div>
      <div style={{width: 260, height: 2, background: GOLD, marginTop: 9}} />
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
    illustrative symbolic reconstruction
  </div>
);

const ChapterMarker: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (FIRST_SPAN_BY_CHAPTER[shot.chapterId ?? ''] !== shot.spanId || shot.chapterId === 'cold_open') return null;
  if (frame > fps * 4.2) return null;
  const meta = CHAPTER_TITLES[shot.chapterId ?? ''];
  if (!meta) return null;
  const reveal = spring({frame, fps, config: {damping: 18, stiffness: 70}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 140, paddingRight: 140, pointerEvents: 'none'}}>
      <div style={{opacity: Math.min(1, reveal), transform: `translateY(${(1 - reveal) * 30}px)`}}>
        <div style={{fontFamily: BRAND.font.body, color: GOLD, fontSize: 28, fontWeight: 900, textTransform: 'uppercase', marginBottom: 18}}>
          {meta.kicker}
        </div>
        <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 104, lineHeight: 0.94, textTransform: 'uppercase', textShadow: '0 12px 38px #000'}}>
          {meta.title}
        </div>
        <div style={{width: 420, height: 5, background: GOLD, marginTop: 30}} />
      </div>
    </AbsoluteFill>
  );
};

const HookOverlay: React.FC<{shot: RoughShot}> = ({shot}) => {
  const beat = HOOK_BEATS[shot.spanId];
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!beat) return null;
  const durationInFrames = framesFor(shot.seconds, fps);
  const enter = spring({frame: frame - 4, fps, config: {damping: 16, stiffness: 120}});
  const pulse = 1 + Math.sin(frame / 5) * 0.012;
  const fade = interpolate(frame, [Math.max(1, durationInFrames - fps * 1.2), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', paddingLeft: 110, paddingRight: 110, opacity: fade}}>
      <div style={{maxWidth: 1280, transform: `translateX(${(1 - enter) * -70}px) scale(${pulse})`}}>
        <div style={{fontFamily: BRAND.font.body, color: GOLD, fontWeight: 900, fontSize: 30, textTransform: 'uppercase', letterSpacing: 0, marginBottom: 12}}>
          {beat.top}
        </div>
        <div
          style={{
            fontFamily: BRAND.font.display,
            color: beat.main === 'PURE WASTE' ? GOLD : WHITE,
            fontSize: beat.main.length > 10 ? 110 : 144,
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

const ScanBars: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const active = shot.chapterId === 'the_search' || shot.chapterId === 'the_dive' || shot.chapterId === 'cold_open';
  if (!active) return null;
  const y = interpolate(frame % 170, [0, 169], [-80, 1160]);
  return (
    <AbsoluteFill style={{opacity: shot.chapterId === 'the_search' ? 0.34 : 0.22, mixBlendMode: 'screen'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: y, height: 4, background: BLUE, boxShadow: `0 0 30px ${BLUE}`}} />
      {Array.from({length: 9}, (_, i) => (
        <div key={i} style={{position: 'absolute', left: 0, right: 0, top: i * 122 + ((frame * 0.2) % 40), height: 1, background: `${SILVER}22`}} />
      ))}
    </AbsoluteFill>
  );
};

const CaptionBand: React.FC<{captions: CaptionCue[]}> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = captions.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 170,
        right: 170,
        bottom: 34,
        minHeight: 106,
        padding: '17px 34px 19px',
        background: '#000000D8',
        borderTop: `3px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize: cue.text.length > 58 ? 38 : 48,
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

const SilenceBlackoutOverlay: React.FC = () => (
  <Sequence from={framesFor(SILENCE_BLACKOUT_START_SEC, BRAND.video.fps)} durationInFrames={framesFor(SILENCE_BLACKOUT_DURATION_SEC, BRAND.video.fps)} name="implosion_blackout">
    <AbsoluteFill style={{backgroundColor: '#000'}} />
  </Sequence>
);

const Scene: React.FC<{shot: RoughShot}> = ({shot}) => {
  if (shot.spanId === SILENCE_SPAN_ID) {
    return <AbsoluteFill style={{backgroundColor: '#000'}} />;
  }
  const graphic = <GraphicFor shot={shot} />;
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <ImageSequence shot={shot} />
      <FactoryLayer shot={shot} />
      <TextureLayer shot={shot} />
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}D0 0%, #00000010 44%, ${INK}E6 100%)`}} />
      <LightSweep seed={`titan-${shot.spanId}`} color={shot.chapterId === 'the_search' ? GOLD : BLUE} />
      <Particles seed={`titan-${shot.spanId}`} count={shot.assetType === 'motion_graphic' ? 24 : 14} color={shot.chapterId === 'the_search' ? GOLD : BLUE} />
      <ScanBars shot={shot} />
      {graphic}
      <HookOverlay shot={shot} />
      <ChapterMarker shot={shot} />
      <SafetyLabel />
      <Vignette strength={0.98} />
      <Grain opacity={0.055} />
    </AbsoluteFill>
  );
};

const TitanAudio: React.FC<{data: RoughCutData}> = ({data}) => {
  const {fps} = useVideoConfig();
  if (!data.narrationSrc && !data.bgmSrc) return null;
  const timed = orderedWithOpening(data);
  const silence = timed.find((shot) => shot.spanId === SILENCE_SPAN_ID);
  const sources = [data.narrationSrc, data.bgmSrc].filter(Boolean) as string[];
  if (!silence) {
    return <>{sources.map((src) => <Audio key={src} src={staticFile(src)} volume={src === data.bgmSrc ? 0.16 : 1} />)}</>;
  }
  const cutStart = framesFor(silence.start, fps);
  const cutEnd = framesFor(silence.start + silence.dur, fps);
  return (
    <>
      {sources.map((src) => (
        <React.Fragment key={src}>
          <Audio src={staticFile(src)} endAt={cutStart} volume={src === data.bgmSrc ? 0.16 : 1} />
          <Sequence from={cutEnd}>
            <Audio src={staticFile(src)} startFrom={cutEnd} volume={src === data.bgmSrc ? 0.16 : 1} />
          </Sequence>
        </React.Fragment>
      ))}
    </>
  );
};

export const TitanPremium: React.FC = () => {
  const {fps} = useVideoConfig();
  const captions: CaptionCue[] = TITAN_CAPTIONS.map((cue, index) => ({id: `titan-caption-${index + 1}`, ...cue}));
  const data: RoughCutData = {...TITAN_ROUGHCUT, narrationSrc: TITAN_REVIEW_MIX_SRC, bgmSrc: null, captions};
  const totalSec = titanDurationSeconds();
  const endFrom = framesFor(totalSec - ENDCARD_SEC, fps);
  let openingInserted = false;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <Series>
        {data.shots.flatMap((shot) => {
          const nodes = [
            <Series.Sequence key={shot.spanId} durationInFrames={framesFor(shot.seconds, fps)} name={`${shot.chapterId}_${shot.spanId}`}>
              <Scene shot={shot} />
            </Series.Sequence>,
          ];
          if (shot.spanId === OPENING_AFTER_SPAN_ID && !openingInserted) {
            openingInserted = true;
            nodes.push(
              <Series.Sequence key="brand-opening" durationInFrames={framesFor(OPENING_SEC, fps)} name="brand_opening">
                <BrandOpening seriesLabel="Prime Documentary" title="Pure Waste" subtitle="The Last Dive of the Titan" />
              </Series.Sequence>,
            );
          }
          return nodes;
        })}
      </Series>
      <Sequence from={endFrom} durationInFrames={framesFor(ENDCARD_SEC, fps)} name="brand_endcard">
        <BrandEndcard />
      </Sequence>
      <TitanAudio data={data} />
      <CaptionBand captions={data.captions ?? []} />
      <SilenceBlackoutOverlay />
    </AbsoluteFill>
  );
};
