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
import type {RoughCutData, RoughShot} from './RoughCut';

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#D84B4B';
const BLOCKED_ASSET_RE = /(rbg|roberts|portrait|holmes|balwani|stockton|rush|us_dollar_bill|smartphone|phone_scroll|money_handover)/i;

type OverlayKind = 'generic' | 'lange' | 'theranos';

type TimedShot = RoughShot & {start: number; dur: number};

export type CasePremiumProps = {
  data: RoughCutData;
  shortTitle: string;
  subtitle: string;
  overlayKind: OverlayKind;
  totalSec?: number;
  shotOrder?: string[];
};

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));

export const casePremiumDurationInFrames = (data: RoughCutData, fps: number, totalSec?: number): number =>
  Math.round((totalSec ?? data.shots.slice(1).reduce((sum, shot) => sum + shot.seconds, 0) + data.shots[0].seconds + OPENING_SEC + ENDCARD_SEC) * fps);

const isImage = (src: string): boolean => /\.(png|jpe?g|webp)$/i.test(src);

const safeImages = (shot: RoughShot): string[] => {
  const candidates = [...(shot.images ?? []), ...(shot.src && shot.assetType !== 'stock_video' ? [shot.src] : [])];
  return Array.from(new Set(candidates.filter((src) => isImage(src) && !BLOCKED_ASSET_RE.test(src))));
};

const safeClips = (shot: RoughShot): {src: string; clipSeconds: number}[] => {
  const clips = shot.clips ?? (shot.src && shot.assetType === 'stock_video' ? [{src: shot.src, clipSeconds: shot.clipSeconds ?? shot.seconds}] : []);
  return clips.filter((clip) => !BLOCKED_ASSET_RE.test(clip.src));
};

const fitTitle = (text: string): number => Math.min(78, Math.max(38, 1360 / Math.max(text.length, 14)));

const MovingImage: React.FC<{src: string; seed: string}> = ({src, seed}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = seed.length % 2 === 0 ? 1 : -1;
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        objectPosition: `${50 + Math.sin(seed.length) * 6}% ${48 + Math.cos(seed.length) * 5}%`,
        filter: 'brightness(0.78) contrast(1.2) saturate(1.05)',
        transform: `translate3d(${dir * interpolate(p, [0, 1], [-44, 44])}px, ${interpolate(p, [0, 1], [22, -22])}px, 0) scale(${1.06 + p * 0.08})`,
      }}
    />
  );
};

const ImageSequence: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const images = safeImages(shot);
  if (!images.length) return <MotionCard shot={shot} />;
  const per = Math.max(framesFor(4.4, fps), Math.round(durationInFrames / Math.min(5, images.length)));
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
          <MovingImage src={segment.src} seed={`${shot.spanId}-${segment.index}`} />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const VideoSequence: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const clips = safeClips(shot);
  if (!clips.length) return <ImageSequence shot={shot} />;
  const per = Math.max(framesFor(4.8, fps), Math.round(durationInFrames / Math.min(4, clips.length)));
  const segments: {src: string; frames: number; startFrom: number; index: number}[] = [];
  let used = 0;
  let index = 0;
  while (used < durationInFrames) {
    const clip = clips[index % clips.length];
    const frames = Math.min(per, durationInFrames - used);
    const maxStart = Math.max(1, Math.round((clip.clipSeconds ?? 1) * fps) - frames - 1);
    segments.push({src: clip.src, frames, startFrom: Math.max(0, Math.round((index * 47) % maxStart)), index});
    used += frames;
    index += 1;
  }
  return (
    <Series>
      {segments.map((segment) => (
        <Series.Sequence key={`${segment.index}-${segment.src}`} durationInFrames={segment.frames}>
          <Video
            src={staticFile(segment.src)}
            muted
            startFrom={segment.startFrom}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: 'brightness(0.74) contrast(1.18) saturate(1.03)',
              transform: 'scale(1.045)',
            }}
          />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const SafetyLabel: React.FC<{kind: OverlayKind}> = ({kind}) => (
  <div
    style={{
      position: 'absolute',
      right: 52,
      top: 44,
      fontFamily: BRAND.font.body,
      fontSize: 18,
      color: SILVER,
      padding: '7px 11px',
      border: `1px solid ${GOLD}88`,
      background: '#000000A8',
    }}
  >
    {kind === 'theranos' ? 'symbolic reconstruction / no real-person likeness' : 'symbolic reconstruction / not case footage'}
  </div>
);

const Lower: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const line = shot.telop[0];
  const reveal = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 95}});
  if (!line) return null;
  return (
    <div style={{position: 'absolute', left: 58, top: 46, opacity: Math.min(1, reveal), maxWidth: 1260}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800, textTransform: 'uppercase'}}>{shot.chapterId ?? shot.spanId}</div>
      <div style={{width: 300, height: 2, background: GOLD, marginTop: 9, marginBottom: 20}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: fitTitle(line), color: WHITE, textTransform: 'uppercase', lineHeight: 0.96, textShadow: '0 5px 30px #000'}}>
        {line}
      </div>
    </div>
  );
};

const MotionCard: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const sweep = interpolate(frame, [0, 220], [-300, 300], {extrapolateRight: 'extend'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(90% 80% at 58% 38%, ${NAVY} 0%, ${INK} 82%)`, overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 900, height: 900, borderRadius: '50%', border: `2px solid ${BLUE}77`, left: 500 + sweep * 0.1, top: 96}} />
      <div style={{position: 'absolute', left: 614, top: 536, width: 360, height: 4, background: GOLD, opacity: 0.45}} />
    </AbsoluteFill>
  );
};

const CaptionBand: React.FC<{captions: RoughCutData['captions']}> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!captions || captions.length === 0) return null;
  const t = frame / fps;
  const cue = captions.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  const longest = Math.max(...cue.text.split('\n').map((line) => line.length));
  const fontSize = longest > 58 ? 34 : longest > 46 ? 38 : 42;
  return (
    <div
      style={{
        position: 'absolute',
        left: 260,
        right: 260,
        bottom: 58,
        minHeight: 82,
        padding: '15px 30px 17px',
        background: '#050505E8',
        borderLeft: `5px solid ${GOLD}`,
        borderRadius: 6,
        boxShadow: '0 18px 44px #000000A8',
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize,
        lineHeight: 1.18,
        textAlign: 'center',
        textShadow: '0 2px 10px #000, 0 0 4px #000',
        WebkitTextStroke: '0.7px #000',
        whiteSpace: 'pre-line',
        letterSpacing: 0,
      }}
    >
      {cue.text}
    </div>
  );
};

const VoteGrid: React.FC<{label: string; sub: string; dissent?: boolean}> = ({label, sub, dissent}) => {
  const frame = useCurrentFrame();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="292" fill={GOLD} fontFamily={BRAND.font.display} fontSize="104" textAnchor="middle">{label}</text>
      <text x="960" y="348" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">{sub}</text>
      <g transform="translate(596 430)">
        {Array.from({length: 9}, (_, i) => {
          const on = spring({frame: frame - i * 4, fps: 30, config: {damping: 16, stiffness: 95}});
          const color = dissent && i === 8 ? RED : BLUE;
          return <rect key={i} x={(i % 5) * 142} y={Math.floor(i / 5) * 128} width="94" height="94" rx="8" fill={color} stroke={GOLD} strokeWidth="4" opacity={Math.min(1, on)} />;
        })}
      </g>
    </svg>
  );
};

const Threshold: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 120], [550, 1370], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <rect x="720" y="250" width="480" height="580" fill="none" stroke={GOLD} strokeWidth="9" />
      <line x1="720" y1="830" x2="1200" y2="830" stroke={WHITE} strokeWidth="5" />
      <circle cx={x} cy="830" r="28" fill={BLUE} stroke={GOLD} strokeWidth="5" />
      <text x="960" y="905" fill={SILVER} fontFamily={BRAND.font.body} fontSize="32" textAnchor="middle">threshold</text>
    </svg>
  );
};

const Boundary: React.FC<{left: string; right: string}> = ({left, right}) => {
  const frame = useCurrentFrame();
  const wobble = Math.sin(frame * 0.06) * 24;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d={`M960 240 C${890 + wobble} 390, ${1030 - wobble} 520, 960 840`} fill="none" stroke={GOLD} strokeWidth="8" strokeDasharray="22 16" />
      <text x="650" y="570" fill={WHITE} fontFamily={BRAND.font.display} fontSize="64" textAnchor="middle">{left}</text>
      <text x="1270" y="570" fill={WHITE} fontFamily={BRAND.font.display} fontSize="64" textAnchor="middle">{right}</text>
    </svg>
  );
};

const BloodDrop: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 1 + 0.04 * Math.sin(frame * 0.09);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M960 255 C1075 420 1135 518 1135 645 C1135 762 1054 846 960 846 C866 846 785 762 785 645 C785 518 845 420 960 255Z" fill={RED} opacity="0.82" transform={`translate(${960 - 960 * pulse} ${560 - 560 * pulse}) scale(${pulse})`} />
      <circle cx="930" cy="520" r="74" fill="#FFFFFF" opacity="0.16" />
    </svg>
  );
};

const MoneySignal: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [16, 110], [0, 780], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="415" fill={GOLD} fontFamily={BRAND.font.display} fontSize="148" textAnchor="middle">$9B</text>
      <rect x="570" y="505" width={w} height="18" fill={BLUE} />
      <text x="960" y="586" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">valuation is not verification</text>
    </svg>
  );
};

const VerdictBoard: React.FC = () => (
  <div style={{position: 'absolute', left: 300, right: 300, top: 330, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 46}}>
    <VerdictCard title="Investors" result="guilty" color={GOLD} />
    <VerdictCard title="Patients" result="not guilty / no verdict" color={SILVER} />
  </div>
);

const VerdictCard: React.FC<{title: string; result: string; color: string}> = ({title, result, color}) => (
  <div style={{minHeight: 260, border: `3px solid ${color}`, background: '#020409D9', padding: 30, boxShadow: `0 0 28px ${color}55`}}>
    <div style={{fontFamily: BRAND.font.body, color, fontWeight: 900, fontSize: 26, textTransform: 'uppercase'}}>{title}</div>
    <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 68, lineHeight: 0.95, textTransform: 'uppercase', marginTop: 28}}>{result}</div>
  </div>
);

const OverlayFor: React.FC<{shot: RoughShot; kind: OverlayKind}> = ({shot, kind}) => {
  if (kind === 'lange') {
    if (shot.spanId === 'SPN-0001' || shot.spanId === 'SPN-0002') return <Threshold />;
    if (shot.spanId === 'SPN-0013') return <VoteGrid label="9-0" sub="Lange v. California — in judgment" />;
    if (shot.spanId === 'SPN-0018') return <Boundary left="WARRANT" right="EXCEPTION" />;
    if (shot.spanId === 'SPN-0020' || shot.spanId === 'SPN-0021') return <Boundary left="HOME" right="CHASE" />;
  }
  if (kind === 'theranos') {
    if (shot.spanId === 'SPN-0001' || shot.spanId === 'SPN-0002') return <BloodDrop />;
    if (shot.spanId === 'SPN-0005' || shot.spanId === 'SPN-0008') return <MoneySignal />;
    if (shot.spanId === 'SPN-0013' || shot.spanId === 'SPN-0014') return <VerdictBoard />;
    if (shot.spanId === 'SPN-0017' || shot.spanId === 'SPN-0023') return <Boundary left="DREAM" right="CRIME" />;
  }
  return null;
};

const Scene: React.FC<{shot: RoughShot; kind: OverlayKind}> = ({shot, kind}) => (
  <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
    {safeClips(shot).length ? <VideoSequence shot={shot} /> : <ImageSequence shot={shot} />}
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}C8 0%, #00000022 42%, ${INK}DC 100%)`}} />
    <LightSweep seed={`${kind}-${shot.spanId}`} color={shot.spanId === 'SPN-0013' ? GOLD : BLUE} />
    <Particles seed={`${kind}-${shot.spanId}`} count={18} color={shot.spanId === 'SPN-0013' ? GOLD : BLUE} />
    <OverlayFor shot={shot} kind={kind} />
    <Lower shot={shot} />
    <SafetyLabel kind={kind} />
    <Vignette strength={0.96} />
    <Grain opacity={0.05} />
  </AbsoluteFill>
);

const Hook: React.FC<{shot: RoughShot; kind: OverlayKind; title: string}> = ({shot, kind, title}) => (
  <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
    {safeClips(shot).length ? <VideoSequence shot={shot} /> : <ImageSequence shot={shot} />}
    <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}EA 0%, #00000044 58%, ${INK}A0 100%)`}} />
    <OverlayFor shot={shot} kind={kind} />
    <div style={{position: 'absolute', left: 74, bottom: 178, fontFamily: BRAND.font.display, color: WHITE, fontSize: 86, lineHeight: 0.95, textTransform: 'uppercase', maxWidth: 930, textShadow: '0 6px 30px #000'}}>
      {title}
    </div>
    <div style={{position: 'absolute', left: 76, bottom: 148, width: 360, height: 5, background: GOLD}} />
    <SafetyLabel kind={kind} />
    <Particles seed={`${kind}-hook`} count={22} color={GOLD} />
    <Vignette strength={1} />
    <Grain opacity={0.055} />
  </AbsoluteFill>
);

export const CasePremiumFromRoughCut: React.FC<CasePremiumProps> = ({data, shortTitle, subtitle, overlayKind, totalSec, shotOrder}) => {
  const {fps} = useVideoConfig();
  const orderedShots = shotOrder
    ? shotOrder.map((id) => {
        const shot = data.shots.find((candidate) => candidate.spanId === id);
        if (!shot) throw new Error(`Missing shot ${id}`);
        return shot;
      })
    : data.shots;
  const hook = orderedShots[0];
  const hookSec = hook.seconds;
  const bodyStart = hookSec + OPENING_SEC;
  const sourceBodySec = orderedShots.slice(1).reduce((sum, shot) => sum + shot.seconds, 0);
  const resolvedTotalSec = totalSec ?? hookSec + OPENING_SEC + sourceBodySec + ENDCARD_SEC;
  const availableBodySec = Math.max(1, resolvedTotalSec - bodyStart - ENDCARD_SEC);
  const scale = availableBodySec / sourceBodySec;
  let cursor = bodyStart;
  const bodyShots: TimedShot[] = orderedShots.slice(1).map((shot) => {
    const dur = shot.seconds * scale;
    const timed = {...shot, start: cursor, dur};
    cursor += dur;
    return timed;
  });
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <Sequence from={0} durationInFrames={framesFor(hookSec, fps)} name="PART_1_HOOK">
        <Hook shot={hook} kind={overlayKind} title={hook.telop[0] ?? data.title} />
      </Sequence>
      <Sequence from={framesFor(hookSec, fps)} durationInFrames={framesFor(OPENING_SEC, fps)} name="PART_2_BRAND_OPENING">
        <BrandOpening seriesLabel="Prime Documentary" title={shortTitle} subtitle={subtitle} />
      </Sequence>
      {bodyShots.map((shot) => (
        <Sequence key={shot.spanId} from={framesFor(shot.start, fps)} durationInFrames={framesFor(shot.dur, fps)} name={`${shot.chapterId ?? 'body'}_${shot.spanId}`}>
          <Scene shot={shot} kind={overlayKind} />
        </Sequence>
      ))}
      <Sequence from={framesFor(resolvedTotalSec - ENDCARD_SEC, fps)} durationInFrames={framesFor(ENDCARD_SEC, fps)} name="PART_4_BRAND_ENDCARD">
        <BrandEndcard />
      </Sequence>
      {data.narrationSrc ? <Audio src={staticFile(data.narrationSrc)} /> : null}
      {data.bgmSrc ? <Audio src={staticFile(data.bgmSrc)} volume={0.16} /> : null}
      <CaptionBand captions={data.captions} />
    </AbsoluteFill>
  );
};
