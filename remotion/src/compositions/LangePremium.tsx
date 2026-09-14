import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Series,
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
import {LightSweep, MovingStage, Particles, Vignette} from '../components/Motion';
import {SceneArt} from '../components/SceneArt';
import {LANGE_BODY_AUDIO_SEC} from '../data/lange_audio_timing';
import {LANGE_CAPTIONS} from '../data/lange_captions';
import {LANGE_ROUGHCUT} from '../data/lange_roughcut';

const FPS = BRAND.video.fps;
const TOTAL_FRAME_RATE = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Chapter = 'hook' | 'opening' | 'act1' | 'act2' | 'act3' | 'act4' | 'ending';
type SceneKind =
  | 'video'
  | 'image'
  | 'map'
  | 'distance'
  | 'entry'
  | 'equation'
  | 'exigency'
  | 'twoColumns'
  | 'vote'
  | 'factor'
  | 'split'
  | 'vacate'
  | 'boundary'
  | 'frontDoor'
  | 'series'
  | 'tease'
  | 'plain';

type ClipInfo = {
  src: string;
  clipSeconds?: number;
};

type RoughShot = (typeof LANGE_ROUGHCUT.shots)[number];

type PremiumScene = {
  spanId: string;
  start: number;
  dur: number;
  chapter: Chapter;
  kind: SceneKind;
  kicker: string;
  title: string;
  subtitle?: string;
  citation?: string;
  note?: string;
  visualMode?: 'map' | 'timeline';
  motifHint?: string;
  telopOn?: boolean;
  citationLeft?: string;
};

type HookBeat = {
  spanId: string;
  label: string;
  dur: number;
  subtitle?: string;
  kind?: 'video' | 'image';
};

const shotMap = new Map<string, RoughShot>(LANGE_ROUGHCUT.shots.map((shot) => [shot.spanId, shot]));
const imageExt = /\.(png|jpe?g|webp|avif)$/i;
const getShot = (spanId: string): RoughShot => {
  const shot = shotMap.get(spanId);
  if (!shot) {
    throw new Error(`Missing Lange shot ${spanId}`);
  }
  return shot;
};
const shotImages = (shot: RoughShot): string[] =>
  shot.images && shot.images.length ? shot.images.filter((s) => imageExt.test(s)) : shot.src && imageExt.test(shot.src) ? [shot.src] : [];
const shotClips = (shot: RoughShot): ClipInfo[] => shot.clips ?? [];
const seedOffset = (seed: string, modulo: number): number =>
  modulo <= 1 ? 0 : Array.from(seed).reduce((sum, char) => sum + char.charCodeAt(0), 0) % modulo;
const fitTitle = (text: string): number => Math.min(78, Math.max(28, 1240 / Math.max(10, text.length)));
const fitSub = (text: string): number => Math.min(34, Math.max(20, 620 / Math.max(10, text.length)));

const HOOK_SEC = 10;
const CONTENT_START = HOOK_SEC + OPENING_SEC;
const BODY_TOTAL_SEC = 619.6;
const FINAL_AUDIO_SEC = Math.max(1, LANGE_BODY_AUDIO_SEC);
const CONTENT_SEC = Math.max(1, FINAL_AUDIO_SEC - CONTENT_START);
const BODY_SCALE = CONTENT_SEC / BODY_TOTAL_SEC;

const BODY_SCENES: PremiumScene[] = [
  {spanId: 'SPN-0001', start: 0.0, dur: 37.6, chapter: 'hook', kind: 'video', kicker: 'HOOK', title: 'Can a cop follow you into your home?'},
  {spanId: 'SPN-0002', start: 37.6, dur: 46.8, chapter: 'opening', kind: 'image', kicker: 'OPENING', title: 'The home: warrant required', subtitle: '(with narrow exceptions)'},
  {spanId: 'SPN-0003', start: 84.4, dur: 18.8, chapter: 'act1', kind: 'map', kicker: 'ACT I', title: 'Sonoma County, CA', subtitle: 'loud music & honking', visualMode: 'map', motifHint: 'map'},
  {spanId: 'SPN-0004', start: 103.2, dur: 13.2, chapter: 'act1', kind: 'distance', kicker: 'ACT I', title: '~100 feet from home', visualMode: 'map', motifHint: 'object'},
  {spanId: 'SPN-0005', start: 116.4, dur: 23.6, chapter: 'act1', kind: 'video', kicker: 'ACT I', title: 'Foot under the door — entry', subtitle: 'The line was crossed the moment the door stopped'},
  {spanId: 'SPN-0006', start: 140, dur: 32.8, chapter: 'act1', kind: 'entry', kicker: 'ACT I', title: 'The question: the ENTRY, not the DUI', subtitle: 'The legal fight was not about DUI itself'},
  {spanId: 'SPN-0007', start: 172.8, dur: 18.4, chapter: 'act1', kind: 'equation', kicker: 'ACT I', title: 'California: any flight = automatic entry'},
  {spanId: 'SPN-0008', start: 191.2, dur: 7.6, chapter: 'act2', kind: 'image', kicker: 'ACT II', title: ''},
  {spanId: 'SPN-0009', start: 198.8, dur: 38.4, chapter: 'act2', kind: 'exigency', kicker: 'ACT II', title: 'Exigent circumstances', subtitle: 'danger · evidence · escape'},
  {spanId: 'SPN-0010', start: 237.2, dur: 21.6, chapter: 'act2', kind: 'image', kicker: 'ACT II', title: 'What level of danger changes the rule?', visualMode: 'timeline', motifHint: 'legal'},
  {spanId: 'SPN-0011', start: 258.8, dur: 38, chapter: 'act2', kind: 'twoColumns', kicker: 'ACT II', title: "Don't let suspects escape", subtitle: "don't gut the home"},
  {spanId: 'SPN-0012', start: 296.8, dur: 13.6, chapter: 'act2', kind: 'video', kicker: 'ACT II', title: ''},
  {spanId: 'SPN-0013', start: 310.4, dur: 18.4, chapter: 'act3', kind: 'vote', kicker: 'ACT III', title: '2021 — 9–0 (in judgment)', subtitle: 'Lange v. California, 594 U.S. 295', citation: 'Lange v. California, 594 U.S. 295 (2021)', visualMode: 'timeline', motifHint: 'seal', citationLeft: 'LANGE'},
  {spanId: 'SPN-0014', start: 328.8, dur: 32.8, chapter: 'act3', kind: 'factor', kicker: 'ACT III', title: 'A FACTOR, not a TRIGGER', subtitle: 'Flight can support probable judgment, not decide it alone'},
  {spanId: 'SPN-0015', start: 361.6, dur: 50.0, chapter: 'act3', kind: 'split', kicker: 'ACT III', title: 'Result unanimity, reasoning split', subtitle: 'Roberts + Alito concur in result, want a broader rule', note: 'concur in result; reasons differ'},
  {spanId: 'SPN-0016', start: 411.6, dur: 16.8, chapter: 'act3', kind: 'vacate', kicker: 'ACT III', title: 'Vacated & remanded', subtitle: 'the judgment goes back to lower courts'},
  {spanId: 'SPN-0017', start: 428.4, dur: 33.6, chapter: 'act4', kind: 'plain', kicker: 'ACT IV', title: 'What warrants and true emergencies are still required'},
  {spanId: 'SPN-0018', start: 462, dur: 29.6, chapter: 'act4', kind: 'boundary', kicker: 'ACT IV', title: 'The line is not always bright', subtitle: 'case-by-case applies to each real-world chase'},
  {spanId: 'SPN-0019', start: 491.6, dur: 18.0, chapter: 'ending', kind: 'frontDoor', kicker: 'ENDING', title: 'The line at your front door'},
  {spanId: 'SPN-0020', start: 509.6, dur: 28.0, chapter: 'ending', kind: 'series', kicker: 'ENDING', title: 'Series trajectory', subtitle: 'Terry → Riley → Carpenter → Lange'},
  {spanId: 'SPN-0021', start: 537.6, dur: 28.8, chapter: 'ending', kind: 'tease', kicker: 'NEXT', title: 'Finale: when does a bold promise become a crime?'},
  {spanId: 'SPN-0022', start: 566.4, dur: 25.6, chapter: 'act2', kind: 'image', kicker: 'ACT II', title: 'Misdemeanor spectrum', subtitle: 'from assault to noise complaint'},
  {spanId: 'SPN-0023', start: 592, dur: 27.6, chapter: 'act3', kind: 'image', kicker: 'ACT III', title: 'No automatic rule at common law', subtitle: 'historical baseline remains', visualMode: 'timeline', motifHint: 'document'},
];

const HOOK_BEATS: HookBeat[] = [
  {spanId: 'SPN-0001', label: 'Door under pressure is the trigger moment', dur: 3.0, kind: 'video'},
  {spanId: 'SPN-0005', label: 'ENTRY starts the legal fight', dur: 2.9, kind: 'video'},
  {spanId: 'SPN-0013', label: 'The ruling was 9–0, in judgment', dur: 3.0, kind: 'image'},
  {spanId: 'SPN-0014', label: 'Flight is only one factor', dur: 2.8, kind: 'image'},
  {spanId: 'SPN-0015', label: 'The result can be unanimous, reasons can split', dur: 2.8, kind: 'image'},
  {spanId: 'SPN-0016', label: 'A remand means the case goes back', dur: 2.4, kind: 'video'},
  {spanId: 'SPN-0022', label: 'What counts as a misdemeanor is not one thing', dur: 2.5, kind: 'video'},
  {spanId: 'SPN-0020', label: 'Series path: Terry to Riley to Carpenter to Lange', dur: 2.6, kind: 'image'},
  {spanId: 'SPN-0023', label: 'No automatic rule at common law', dur: 2.5, kind: 'image'},
  {spanId: 'SPN-0021', label: 'Next: when does a bold claim become a crime?', dur: 2.5, kind: 'image'},
];

const sceneCutStyle = (sceneId: string) => {
  const base = sceneId.replace(/[^0-9]/g, '');
  const pick = Number(base) % 360;
  return `${20 + (pick % 16)}%`;
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
      padding: '8px 11px',
      border: `1px solid ${GOLD}88`,
      background: '#000000A8',
    }}
  >
    symbolic reconstruction
  </div>
);

const UpperTelop: React.FC<{scene: PremiumScene}> = ({scene}) => {
  if (!scene.title) return null;
  return (
    <div style={{position: 'absolute', left: 74, top: 58, maxWidth: 1340, opacity: 1}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker}</div>
      <div style={{width: 280, height: 2, background: GOLD, marginTop: 8, marginBottom: 16}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: fitTitle(scene.title), color: WHITE, textTransform: 'uppercase', lineHeight: 0.96, textShadow: '0 4px 30px #000'}}>
        {scene.title}
      </div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: fitSub(scene.subtitle), color: SILVER, marginTop: 12, maxWidth: 1270}}>{scene.subtitle}</div> : null}
    </div>
  );
};

const CitationBadge: React.FC<{text: string; side?: 'left' | 'right'}> = ({text, side = 'right'}) => (
  <div
    style={{
      position: 'absolute',
      [side]: 54,
      bottom: 156,
      maxWidth: 520,
      background: '#000000CC',
      borderLeft: `4px solid ${GOLD}`,
      color: GOLD,
      fontFamily: BRAND.font.body,
      fontSize: 21,
      fontWeight: 800,
      padding: '7px 10px',
      textAlign: 'left',
    }}
  >
    {text}
  </div>
);

const ImagePlate: React.FC<{spanId: string; duration: number; seed: string; scaleFloor?: number}> = ({spanId, duration, seed, scaleFloor = 1.05}) => {
  const frame = useCurrentFrame();
  const shot = getShot(spanId);
  const images = shotImages(shot);
  const offset = seedOffset(seed, images.length);
  const localFrames = Math.max(1, Math.round(duration * FPS));
  const slot = images.length > 1 ? Math.max(Math.round(3.4 * FPS), Math.floor(localFrames / images.length)) : Math.max(1, localFrames);
  const rawIdx = images.length > 0 ? Math.min(images.length - 1, Math.floor(frame / slot)) : 0;
  const idx = images.length > 0 ? (rawIdx + offset) % images.length : 0;
  const next = images.length > 1 ? (idx + 1) % images.length : idx;
  const segment = frame - rawIdx * slot;
  const nextOpacity = images.length > 1 ? interpolate(segment, [Math.max(0, slot - 18), slot], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const t = idx % 2 === 0 ? 1 : -1;
  const draw = (src: string, opacity: number, dx: number) => (
    <Img
      key={src}
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        objectPosition: `${50 + 4 * Math.sin(Number(seed.slice(-1) || 1) + idx)}% ${50 + 4 * Math.cos(Number(seed.charCodeAt(0)))}%`,
        opacity,
        transform: `scale(${scaleFloor + 0.08 * Math.sin((frame + idx * 20) / 28)})
                   translate3d(${t * 18}px, ${-t * 12}px, 0)`,
        filter: 'brightness(0.82) contrast(1.16) saturate(1.09)',
      }}
    />
  );
  if (!images.length) {
    return <AbsoluteFill style={{background: `radial-gradient(95% 80% at 58% 36%, ${BLUE}22 0%, ${NAVY} 40%, ${INK} 100%)`}} />;
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      {draw(images[idx], 1 - nextOpacity, 0)}
      {images.length > 1 ? draw(images[next], nextOpacity, 16) : null}
    </AbsoluteFill>
  );
};

const VideoPlate: React.FC<{spanId: string; duration: number; seed: string; muted?: boolean}> = ({spanId, duration, seed, muted = true}) => {
  const shot = getShot(spanId);
  const clips = shotClips(shot);
  if (!clips.length) {
    return <ImagePlate spanId={spanId} duration={duration} seed={seed} />;
  }
  const totalFrames = Math.max(1, Math.round(duration * FPS));
  const segments: {src: string; frames: number; startFrom: number; idx: number}[] = [];
  let used = 0;
  let idx = 0;
  const offset = seedOffset(seed, clips.length);
  while (used < totalFrames) {
    const clip = clips[(idx + offset) % clips.length];
    const clipFrames = Math.max(18, Math.floor((clip.clipSeconds ?? 4) * FPS) - 6);
    const frames = Math.max(1, Math.min(Math.round(2.7 * FPS), clipFrames, totalFrames - used));
    const maxStart = Math.max(0, clipFrames - frames - 2);
    const startFrom = maxStart > 0 ? Math.round(((idx + offset + 1) * 53) % maxStart) : 0;
    segments.push({src: clip.src, frames, startFrom, idx});
    used += frames;
    idx += 1;
  }
  return (
    <Series>
      {segments.map((segment) => (
        <Series.Sequence key={`${segment.idx}-${segment.src}-${segment.startFrom}`} durationInFrames={segment.frames}>
          <Video
            src={staticFile(segment.src)}
            muted={muted}
            startFrom={segment.startFrom}
            delayRenderTimeoutInMilliseconds={120000}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: 'brightness(0.78) contrast(1.2) saturate(1.06)',
              transform: 'scale(1.035)',
            }}
          />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string}> = ({left, right, leftSub, rightSub}) => (
  <div style={{position: 'absolute', left: 210, right: 210, top: 360, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 46}}>
    {[
      {title: left, sub: leftSub, color: BLUE},
      {title: right, sub: rightSub, color: GOLD},
    ].map((panel) => (
      <div key={panel.title} style={{minHeight: 250, border: `3px solid ${panel.color}`, background: '#020409CC', padding: 34}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: panel.color, textTransform: 'uppercase'}}>{panel.title}</div>
        {panel.sub ? <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: SILVER, marginTop: 18}}>{panel.sub}</div> : null}
      </div>
    ))}
  </div>
);

const Doors: React.FC<{labels: string[]}> = ({labels}) => (
  <div style={{position: 'absolute', left: 190, right: 190, top: 360, display: 'grid', gridTemplateColumns: `repeat(${labels.length}, 1fr)`, gap: 22}}>
    {labels.map((label, i) => (
      <div key={label} style={{height: 300, border: `3px solid ${i === 0 ? GOLD : `${SILVER}66`}`, background: i === 0 ? `${GOLD}18` : '#05070acc', position: 'relative'}}>
        <div style={{position: 'absolute', left: 18, right: 18, bottom: 24, height: 4, background: i === 0 ? BLUE : `${SILVER}55`}} />
        <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: i === 0 ? GOLD : SILVER, margin: 24, lineHeight: 1.18}}>{label}</div>
      </div>
    ))}
  </div>
);

const WarrantUnderline: React.FC = () => {
  const frame = useCurrentFrame();
  const w = interpolate(frame, [14, 50], [150, 640], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 210, top: 410}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 80, color: WHITE, textTransform: 'uppercase', textShadow: '0 4px 24px #000'}}>warrant required</div>
      <div style={{height: 6, width: w, background: GOLD, marginTop: 10, boxShadow: `0 0 22px ${GOLD}`}} />
      <div style={{marginTop: 12, fontFamily: BRAND.font.body, fontSize: 30, color: SILVER}}>with narrow exceptions</div>
    </div>
  );
};

const DistanceLabel: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 120], [0.9, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M280 730 C470 640 680 510 920 500 C1160 492 1285 560 1500 470" fill="none" stroke={GOLD} strokeWidth="7" strokeLinecap="round" opacity="0.76" />
      <circle cx={250 + p * 140} cy="744" r="9" fill={BLUE} />
      <text x="980" y="440" fill={WHITE} fontFamily={BRAND.font.body} fontSize="30">~100 feet</text>
      <text x="1500" y="446" fill={SILVER} fontFamily={BRAND.font.body} fontSize="22">entry threshold</text>
    </svg>
  );
};

const EntryStrike: React.FC = () => {
  const frame = useCurrentFrame();
  const sweep = interpolate(frame, [0, 40], [0, 1]);
  const strike = interpolate(frame, [12, 50], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 240, top: 360}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 112, color: GOLD, textTransform: 'uppercase', letterSpacing: '0.03em'}}>ENTRY</div>
      <div style={{height: 3, width: Math.round(660 * sweep), background: GOLD, marginTop: -12, transform: 'translateX(6px)'}} />
      <div style={{marginTop: 14, fontFamily: BRAND.font.body, fontSize: 38, color: `${SILVER}CC`}}>
        the DUI
        <span style={{display: 'inline-block', position: 'relative', marginLeft: 12}}>
          <span style={{position: 'absolute', left: 0, right: `${Math.round(100 - 100 * strike)}%`, top: '48%', height: 4, background: '#c0392b', opacity: strike, transform: 'rotate(-10deg)'}} />
          is not the issue
        </span>
      </div>
    </div>
  );
};

const EquationBars: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 230, right: 230, top: 350, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 46}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: GOLD, textTransform: 'uppercase'}}>any flight</div>
      <div style={{width: 95, height: 5, background: GOLD, transform: `scaleX(${p})`, transformOrigin: 'left'}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: GOLD, textTransform: 'uppercase'}}>=</div>
      <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: WHITE, textTransform: 'uppercase'}}>automatic entry</div>
    </div>
  );
};

const ExigencyCards: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['danger', 'evidence destruction', 'escape'];
  return (
    <div style={{position: 'absolute', left: 200, right: 200, top: 360, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 30}}>
      {labels.map((label, i) => {
        const on = spring({frame: frame - i * 18, fps: FPS, config: {damping: 18, stiffness: 75}});
        return (
          <div
            key={label}
            style={{
              border: `3px solid ${i % 2 ? BLUE : GOLD}`,
              background: '#05070ACC',
              minHeight: 190,
              opacity: Math.min(1, on),
              transform: `translateY(${interpolate(on, [0, 1], [44, 0])}px)`,
              boxShadow: `0 0 18px ${i % 2 ? `${BLUE}55` : `${GOLD}55`}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <div style={{fontFamily: BRAND.font.display, fontSize: 38, color: WHITE, textTransform: 'uppercase'}}>{label}</div>
          </div>
        );
      })}
    </div>
  );
};

const VoteUnanimous: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = interpolate(frame, [0, 16], [0.6, 1]);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g transform="translate(560 430)">
        {Array.from({length: 9}, (_, i) => {
          const on = spring({frame: frame - i * 3, fps: FPS, config: {damping: 15, stiffness: 85}});
          const col = i % 3;
          const row = Math.floor(i / 3);
          return (
            <rect
              key={i}
              x={col * 145}
              y={row * 145}
              width="94"
              height="94"
              rx="9"
              fill={BLUE}
              stroke={GOLD}
              strokeWidth="4"
              opacity={0.42 + on * 0.58}
              style={{transform: `scale(${0.96 + 0.06 * Math.min(1, on * pulse)})`}}
            />
          );
        })}
        <text x="216" y="336" fill={WHITE} fontFamily={BRAND.font.display} fontSize="122" textAnchor="middle">9–0</text>
        <text x="216" y="380" fill={GOLD} fontFamily={BRAND.font.body} fontSize="31" fontWeight={700} textAnchor="middle">in judgment</text>
      </g>
    </svg>
  );
};

const SplitReason: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, 65], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 220, right: 220, top: 330}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 70, color: WHITE, textTransform: 'uppercase', textAlign: 'center'}}>same result</div>
      <div style={{position: 'relative', marginTop: 24, height: 300}}>
        <svg width="1480" height="300" style={{position: 'absolute', left: 0, top: 0}}>
          <path d={`M 0 ${160 * (1 - drift)} C 360 ${130 - drift * 30}, 620 ${150 + drift * 30}, 740 160 S 980 190, 1480 160`} fill="none" stroke={BLUE} strokeWidth="7" />
          <path d={`M 0 ${160} C 410 ${160 + drift * 30}, 660 ${140 - drift * 22}, 740 160 S 990 190, 1480 ${180 + drift * 22}`} fill="none" stroke={GOLD} strokeWidth="7" />
          <text x="520" y="112" fill={BLUE} fontSize="38" fontFamily={BRAND.font.body} letterSpacing="0.04em">concurs in result</text>
          <text x="900" y="112" fill={GOLD} fontSize="38" fontFamily={BRAND.font.body} letterSpacing="0.04em">different rationale</text>
        </svg>
        <div style={{position: 'absolute', left: 250, top: 170, right: 900, color: WHITE, fontFamily: BRAND.font.body, fontSize: 32}}>Roberts + Alito</div>
        <div style={{position: 'absolute', left: 900, top: 170, right: 250, color: WHITE, fontFamily: BRAND.font.body, fontSize: 32}}>Broader pursuit rule</div>
      </div>
    </div>
  );
};

const Boundary: React.FC = () => {
  const frame = useCurrentFrame();
  const jitter = Math.sin(frame * 0.07) * 14;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path
        d={`M 280 ${675 + jitter} C 620 ${420 + jitter * 0.4} 840 ${810 - jitter * 0.2} 960 ${600} C 1080 ${390 - jitter * 0.5} 1300 ${700 - jitter * 0.4} 1640 ${430 + jitter * 0.1}`}
        fill="none"
        stroke={BLUE}
        strokeWidth="10"
      />
      <text x="960" y="720" fill={GOLD} fontFamily={BRAND.font.display} fontSize="74" textAnchor="middle">CASE-BY-CASE</text>
    </svg>
  );
};

const TrailSeries: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 180], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const points = ['Terry', 'Riley', 'Carpenter', 'Lange'];
  return (
    <div style={{position: 'absolute', left: 210, right: 210, top: 360}}>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24}}>
        {points.map((name, i) => {
          const isActive = p * 100 >= i * 26;
          return (
            <div
              key={name}
              style={{
                border: `3px solid ${isActive ? GOLD : `${SILVER}55`}`,
                background: isActive ? '#020409CC' : '#05070AD8',
                padding: 20,
                minHeight: 170,
              }}
            >
              <div style={{fontFamily: BRAND.font.display, fontSize: 48, color: isActive ? GOLD : SILVER, textTransform: 'uppercase'}}>{name}</div>
              <div style={{height: 5, background: isActive ? GOLD : `${SILVER}44`, marginTop: 16, opacity: isActive ? 1 : 0.4}} />
            </div>
          );
        })}
      </div>
      <svg width="1480" height="120" style={{position: 'absolute', left: 0, top: 205}}>
        <line x1="8" y1="60" x2="1472" y2="60" stroke={SILVER} strokeWidth="4" opacity="0.45" />
        {points.map((_, i) => <circle key={i} cx={20 + i * 494} cy="60" r="8" fill={i <= Math.floor(p * 100 / 25) ? GOLD : SILVER} />)}
      </svg>
    </div>
  );
};

const FrontDoor: React.FC = () => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 0}}>
    <div style={{position: 'absolute', left: 700, top: 410, width: 520, height: 520, border: `8px solid ${GOLD}`, borderRadius: 10, boxShadow: `0 0 36px ${GOLD}66`}} />
    <div style={{position: 'absolute', left: 920, top: 468, width: 78, height: 78, border: `4px solid ${BLUE}`, borderRadius: '50%', background: `radial-gradient(circle, ${GOLD}99, ${INK})`}} />
    <div style={{position: 'absolute', left: 930, top: 620, width: 60, height: 4, background: GOLD}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: 950, textAlign: 'center', color: GOLD, fontFamily: BRAND.font.body, fontSize: 32, letterSpacing: '0.08em'}}>THE LINE AT YOUR DOOR</div>
  </div>
);

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = LANGE_CAPTIONS.find((item) => t >= item.start && t < item.end);
  if (!cue) return null;
  const longest = Math.max(...cue.text.split('\n').map((line) => line.length));
  const fontSize = longest > 38 ? 44 : longest > 30 ? 50 : 56;
  return (
    <div
      style={{
        position: 'absolute',
        left: 190,
        right: 190,
        bottom: 40,
        minHeight: 86,
        padding: '16px 32px 18px',
        background: '#000000DB',
        borderTop: `3px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize,
        lineHeight: 1.06,
        textAlign: 'center',
        textShadow: '0 3px 14px #000, 0 0 5px #000',
        WebkitTextStroke: '1.1px #000',
        whiteSpace: 'pre-line',
        zIndex: 100,
      }}
    >
      {cue.text}
    </div>
  );
};

const SceneShell: React.FC<{scene: PremiumScene; children?: React.ReactNode}> = ({scene, children}) => (
  <AbsoluteFill>
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>{children}</AbsoluteFill>
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}B8 0%, #00000010 45%, ${INK}D2 100%)`}} />
    <LightSweep seed={scene.spanId} color={scene.chapter === 'act3' ? GOLD : BLUE} />
    <Particles seed={scene.spanId} color={scene.chapter === 'act3' ? GOLD : BLUE} count={18} />
    {scene.telopOn !== false ? <UpperTelop scene={scene} /> : null}
    {scene.citation ? <CitationBadge text={scene.citation} /> : null}
    <ReconstructionLabel />
    <Vignette strength={1} />
    <Grain opacity={0.045} />
  </AbsoluteFill>
);

const SceneContent: React.FC<{scene: PremiumScene}> = ({scene}) => {
  switch (scene.kind) {
    case 'video':
      return <SceneShell scene={scene}><VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} /></SceneShell>;
    case 'image':
      if (scene.spanId === 'SPN-0002') {
        return (
          <SceneShell scene={scene}>
            <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
            <AbsoluteFill style={{background: '#00000055'}} />
            <WarrantUnderline />
          </SceneShell>
        );
      }
      if (scene.spanId === 'SPN-0011') {
        return (
          <SceneShell scene={scene}>
            <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
            <TwoColumn left="Don't let suspects escape" right="Don't gut the home" leftSub="public safety" rightSub="privacy baseline" />
            <SceneArt visualMode="timeline" motifHint="scales" onScreenText={['ESCAPE', 'PRIVACY']} seed="scales-scene-0011" />
          </SceneShell>
        );
      }
      if (scene.spanId === 'SPN-0014') {
        return (
          <SceneShell scene={scene}>
            <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
            <TwoColumn left="A FACTOR" right="NOT A TRIGGER" leftSub="important signal" rightSub="too broad to auto decide" />
            <div style={{position: 'absolute', left: 170, right: 170, top: 690}}>
              <div style={{textAlign: 'center', fontFamily: BRAND.font.display, fontSize: 86, color: GOLD, textTransform: 'uppercase'}}>flight</div>
              <div style={{position: 'relative', margin: '10px auto 0', width: 420, height: 5, background: `${GOLD}`}}>
                <div style={{position: 'absolute', left: 0, right: 0, top: -2, height: 2, background: '#c0392b'}} />
              </div>
            </div>
          </SceneShell>
        );
      }
      if (scene.spanId === 'SPN-0023') {
        return (
          <SceneShell scene={scene}>
            <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
            <SceneArt visualMode="timeline" motifHint="document" onScreenText={['common law', 'no automatic pursuit exception']} seed="common-law-2023" />
          </SceneShell>
        );
      }
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
        </SceneShell>
      );
    case 'map':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <SceneArt visualMode="map" motifHint={scene.motifHint || 'map'} onScreenText={[scene.title, scene.subtitle || '']} seed={scene.spanId} />
          {scene.spanId === 'SPN-0003' ? <SceneArt visualMode="timeline" motifHint="document" onScreenText={['Sonoma County']} seed={`${scene.spanId}-ripple`} /> : null}
        </SceneShell>
      );
    case 'distance':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <DistanceLabel />
        </SceneShell>
      );
    case 'entry':
      return (
        <SceneShell scene={scene}>
          <VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <EntryStrike />
        </SceneShell>
      );
    case 'equation':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <EquationBars />
        </SceneShell>
      );
    case 'exigency':
      return (
        <SceneShell scene={scene}>
          <VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <ExigencyCards />
        </SceneShell>
      );
    case 'twoColumns':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <TwoColumn left="don't let suspects escape" right="don't gut the home" leftSub="public safety" rightSub="home sanctity" />
        </SceneShell>
      );
    case 'vote':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <SceneArt visualMode={scene.visualMode || 'timeline'} motifHint={scene.motifHint || 'seal'} onScreenText={['The Court in 2021']} seed="scene-0013" />
          <VoteUnanimous />
          <CitationBadge text={scene.citation || ''} />
        </SceneShell>
      );
    case 'factor':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <TwoColumn left="A FACTOR" right="NOT A TRIGGER" leftSub="consider" rightSub="decide separately" />
          <Doors labels={['assault', 'noise complaint', 'risk level']} />
        </SceneShell>
      );
    case 'split':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <SplitReason />
        </SceneShell>
      );
    case 'vacate':
      return (
        <SceneShell scene={scene}>
          <VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <div style={{position: 'absolute', left: 240, top: 420, width: 560, border: `4px solid ${GOLD}`, color: GOLD, fontFamily: BRAND.font.display, fontSize: 72, textAlign: 'center', textTransform: 'uppercase', letterSpacing: '0.03em', padding: '20px'}}>vacated</div>
          <div style={{position: 'absolute', left: 920, top: 420, width: 560, border: `4px solid ${GOLD}`, color: WHITE, fontFamily: BRAND.font.display, fontSize: 72, textAlign: 'center', textTransform: 'uppercase', letterSpacing: '0.03em', padding: '20px'}}>remanded</div>
          <div style={{position: 'absolute', left: 800, top: 540, width: 0, height: 0, borderLeft: '16px solid transparent', borderRight: '16px solid transparent', borderTop: `28px solid ${GOLD}`}} />
        </SceneShell>
      );
    case 'boundary':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <Boundary />
        </SceneShell>
      );
    case 'frontDoor':
      return (
        <SceneShell scene={scene}>
          <VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <FrontDoor />
        </SceneShell>
      );
    case 'series':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <TrailSeries />
        </SceneShell>
      );
    case 'tease':
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
          <div style={{position: 'absolute', left: 190, top: 360}}>
            <div style={{fontFamily: BRAND.font.display, fontSize: 82, color: GOLD, textTransform: 'uppercase', textShadow: '0 5px 30px #000'}}>next episode</div>
            <div style={{fontFamily: BRAND.font.body, fontSize: 38, color: WHITE, marginTop: 14}}>{scene.subtitle}</div>
          </div>
        </SceneShell>
      );
    case 'plain':
    default:
      return (
        <SceneShell scene={scene}>
          <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />
        </SceneShell>
      );
  }
};

const HookBeatCard: React.FC<{beat: HookBeat; from: number}> = ({beat}) => {
  const shot = getShot(beat.spanId);
  const media = (beat.kind === 'video' || shot.assetType === 'stock_video') ? (
    <VideoPlate spanId={beat.spanId} duration={beat.dur} seed={beat.spanId} muted />
  ) : (
    <ImagePlate spanId={beat.spanId} duration={beat.dur} seed={beat.spanId} />
  );
  const pulse = spring({frame: useCurrentFrame(), fps: FPS, config: {damping: 18, stiffness: 130}});
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {media}
      <AbsoluteFill style={{background: `linear-gradient(95% 75% at 54% 38%, ${INK}9E 0%, ${INK}F8 58%, ${INK}AA 100%)`}} />
      <div
        style={{
          position: 'absolute',
          left: 74,
          bottom: 130,
          color: WHITE,
          fontFamily: BRAND.font.display,
          fontSize: 62,
          textTransform: 'uppercase',
          textShadow: '0 4px 25px #000',
          maxWidth: 1180,
          opacity: Math.min(1, pulse),
          transform: `translateY(${interpolate(pulse, [0, 1], [14, 0])}px)`,
        }}
      >
        {beat.label}
      </div>
      {beat.subtitle ? (
        <div
          style={{
            position: 'absolute',
            left: 82,
            bottom: 80,
            color: GOLD,
            fontFamily: BRAND.font.body,
            fontSize: 28,
          }}
        >
          {beat.subtitle}
        </div>
      ) : null}
      <Particles seed={`hook-${beat.spanId}`} count={14} color={GOLD} />
    </AbsoluteFill>
  );
};

const HookMontage: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <ImagePlate spanId="SPN-0002" duration={HOOK_SEC} seed="lange-hook-spn0002" scaleFloor={1.02} />
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}F5 0%, ${INK}99 42%, #00000030 100%)`}} />
      <LightSweep seed="lange-hook" color={GOLD} />
      <Particles seed="lange-hook" color={BLUE} count={22} />
      <div style={{position: 'absolute', left: 80, top: 60, color: GOLD, fontFamily: BRAND.font.body, fontWeight: 900, fontSize: 18, letterSpacing: '0.09em'}}>HOOK</div>
      <div style={{position: 'absolute', left: 80, top: 92, width: 260, height: 3, background: GOLD}} />
      <div style={{position: 'absolute', left: 82, top: 280, maxWidth: 1120}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 88, lineHeight: 0.94, color: WHITE, textTransform: 'uppercase', textShadow: '0 6px 30px #000'}}>
          Can a cop follow you into your home?
        </div>
        <div style={{marginTop: 22, fontFamily: BRAND.font.body, fontSize: 34, color: SILVER, maxWidth: 900, textShadow: '0 3px 14px #000'}}>
          A garage door, a foot under the threshold, and the Fourth Amendment line around your front door.
        </div>
      </div>
      <Vignette strength={1} />
      <Grain opacity={0.04} />
    </AbsoluteFill>
  );
};

export const LangePremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={Math.round(HOOK_SEC * FPS)} name="PART_HOOK">
      <HookMontage />
    </Sequence>
    <Sequence from={Math.round(HOOK_SEC * FPS)} durationInFrames={Math.round(OPENING_SEC * FPS)} name="PART_OPENING">
      <BrandOpening seriesLabel="Landmark Rights Cases" title="Lange v. California" subtitle="Can a cop follow you into your home?" />
    </Sequence>
    {BODY_SCENES.map((scene) => {
      const scaledScene = {...scene, start: scene.start * BODY_SCALE, dur: scene.dur * BODY_SCALE};
      return (
        <Sequence
          key={scene.spanId}
          from={Math.round((CONTENT_START + scaledScene.start) * FPS)}
          durationInFrames={Math.round(scaledScene.dur * FPS)}
          name={`${scene.chapter}_${scene.spanId}`}
        >
          <SceneContent scene={scaledScene} />
        </Sequence>
      );
    })}
    <Sequence
      from={Math.round(FINAL_AUDIO_SEC * FPS)}
      durationInFrames={Math.round(ENDCARD_SEC * FPS)}
      name="PART_ENDCARD"
    >
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile('lange/audio/lange_final_mix_v010_suno_balanced_full_length.mp3')} />
    <CaptionBand />
  </AbsoluteFill>
);

export const langePremiumDurationInFrames = (fps: number): number =>
  Math.round((FINAL_AUDIO_SEC + ENDCARD_SEC) * fps);


