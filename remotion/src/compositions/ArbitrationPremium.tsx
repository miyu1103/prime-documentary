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
import {ARBITRATION_ROUGHCUT} from '../data/arbitration_roughcut';
import {ARBITRATION_CAPTIONS} from '../data/arbitration_captions';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#D9483B';
const TOTAL_SEC = 720;
const HOOK_SEC = 30;
const BODY_START = HOOK_SEC + OPENING_SEC;
const BODY_TARGET_SEC = TOTAL_SEC - BODY_START - ENDCARD_SEC;
const BLOCKED_ASSET_RE = /(rbg|roberts|portrait)/i;

type RoughShot = (typeof ARBITRATION_ROUGHCUT.shots)[number];
type TimedShot = RoughShot & {start: number; dur: number};

const sourceBodySec = ARBITRATION_ROUGHCUT.shots.slice(1).reduce((sum, shot) => sum + shot.seconds, 0);
const bodyScale = BODY_TARGET_SEC / sourceBodySec;

let bodyCursor = BODY_START;
const bodyShots: TimedShot[] = ARBITRATION_ROUGHCUT.shots.slice(1).map((shot) => {
  const dur = shot.seconds * bodyScale;
  const timed = {...shot, start: bodyCursor, dur};
  bodyCursor += dur;
  return timed;
});

const safeImages = (shot: RoughShot): string[] =>
  (shot.images ?? [])
    .filter((src) => /\.(png|jpe?g|webp)$/i.test(src))
    .filter((src) => !BLOCKED_ASSET_RE.test(src));

const safeClips = (shot: RoughShot): {src: string; clipSeconds: number}[] =>
  (shot.clips ?? []).filter((clip) => !BLOCKED_ASSET_RE.test(clip.src));

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = ARBITRATION_CAPTIONS.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  const longest = Math.max(...cue.text.split('\n').map((line) => line.length));
  const fontSize = longest > 49 ? 48 : longest > 40 ? 54 : 60;
  return (
    <div
      style={{
        position: 'absolute',
        left: 170,
        right: 170,
        bottom: 34,
        minHeight: 118,
        padding: '18px 36px 20px',
        background: '#000000D9',
        borderTop: `3px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize,
        lineHeight: 1.08,
        textAlign: 'center',
        textShadow: '0 3px 14px #000, 0 0 5px #000',
        WebkitTextStroke: '1.4px #000',
        whiteSpace: 'pre-line',
      }}
    >
      {cue.text}
    </div>
  );
};

const SafetyLabel: React.FC = () => (
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
    symbolic reconstruction / not case footage
  </div>
);

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
        transform: `translate3d(${dir * interpolate(p, [0, 1], [-38, 38])}px, ${interpolate(p, [0, 1], [18, -18])}px, 0) scale(${1.07 + p * 0.08})`,
        filter: 'brightness(0.76) contrast(1.2) saturate(1.06)',
      }}
    />
  );
};

const ImageSequence: React.FC<{shot: RoughShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const images = safeImages(shot);
  if (!images.length && shot.src && !BLOCKED_ASSET_RE.test(shot.src)) {
    images.push(shot.src);
  }
  if (!images.length) return <MotionCard shot={shot} />;
  const per = Math.max(90, Math.round(4.6 * fps));
  const segments: {src: string; frames: number; index: number}[] = [];
  let used = 0;
  let idx = 0;
  while (used < durationInFrames) {
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: images[idx % images.length], frames, index: idx});
    used += frames;
    idx += 1;
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
  const per = Math.max(90, Math.round(5.5 * fps));
  const segments: {src: string; startFrom: number; frames: number; index: number}[] = [];
  let used = 0;
  let idx = 0;
  while (used < durationInFrames) {
    const clip = clips[idx % clips.length];
    const frames = Math.min(per, durationInFrames - used);
    segments.push({src: clip.src, startFrom: Math.round(((idx * per) % Math.max(1, clip.clipSeconds * fps)) * 0.35), frames, index: idx});
    used += frames;
    idx += 1;
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
              filter: 'brightness(0.72) contrast(1.18) saturate(1.04)',
              transform: 'scale(1.045)',
            }}
          />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const Telop: React.FC<{shot: RoughShot}> = ({shot}) => {
  const text = shot.telop[0];
  if (!text) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 56,
        top: 56,
        maxWidth: 850,
        color: WHITE,
        background: '#000000A6',
        borderLeft: `5px solid ${GOLD}`,
        padding: '12px 18px',
        fontFamily: BRAND.font.body,
        fontWeight: 800,
        fontSize: 32,
        lineHeight: 1.15,
        textShadow: '0 2px 10px #000',
      }}
    >
      {text}
    </div>
  );
};

const MotionCard: React.FC<{shot: RoughShot}> = ({shot}) => {
  const frame = useCurrentFrame();
  const sweep = interpolate(frame, [0, 220], [-260, 260], {extrapolateRight: 'extend'});
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(90% 80% at 60% 40%, ${NAVY} 0%, ${INK} 82%)`,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          position: 'absolute',
          width: 820,
          height: 820,
          borderRadius: '50%',
          border: `2px solid ${BLUE}77`,
          left: 560 + sweep * 0.1,
          top: 120,
        }}
      />
      <div style={{position: 'absolute', left: 620, right: 160, top: 340, color: WHITE, fontFamily: BRAND.font.display, fontSize: 72, lineHeight: 0.96, textTransform: 'uppercase'}}>
        {shot.telop[0] ?? shot.spanId}
      </div>
      <div style={{position: 'absolute', left: 624, top: 520, width: 360, height: 4, background: GOLD}} />
    </AbsoluteFill>
  );
};

const DebateOverlay: React.FC = () => (
  <div style={{position: 'absolute', left: 220, right: 220, top: 315, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 42}}>
    <ArgumentCard label="Critics" headline={'"forced arbitration"'} sub="courthouse door closes / small harms lose remedy" color={RED} />
    <ArgumentCard label="Defenders" headline="faster, cheaper, agreed-to" sub="private forum / lower formality / individual claims" color={BLUE} />
  </div>
);

const ArgumentCard: React.FC<{label: string; headline: string; sub: string; color: string}> = ({label, headline, sub, color}) => (
  <div style={{minHeight: 275, border: `3px solid ${color}`, background: '#020409D9', padding: 30, boxShadow: `0 0 28px ${color}55`}}>
    <div style={{fontFamily: BRAND.font.body, color: GOLD, fontWeight: 900, fontSize: 24, textTransform: 'uppercase'}}>{label}</div>
    <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 60, lineHeight: 0.95, textTransform: 'uppercase', marginTop: 18}}>{headline}</div>
    <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 27, lineHeight: 1.2, marginTop: 18}}>{sub}</div>
  </div>
);

const VoteSplit: React.FC<{year: string; label: string}> = ({year, label}) => {
  const frame = useCurrentFrame();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="272" fill={GOLD} fontFamily={BRAND.font.display} fontSize="98" textAnchor="middle">{year}</text>
      <text x="960" y="330" fill={SILVER} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">{label}</text>
      <g transform="translate(545 418)">
        {Array.from({length: 9}, (_, i) => {
          const on = spring({frame: frame - i * 4, fps: FPS, config: {damping: 16, stiffness: 95}});
          const dissent = i >= 5;
          return <rect key={i} x={(i % 5) * 145} y={Math.floor(i / 5) * 132} width="92" height="92" rx="8" fill={dissent ? RED : BLUE} stroke={GOLD} strokeWidth="4" opacity={Math.min(1, on)} />;
        })}
        <text x="355" y="312" fill={WHITE} fontFamily={BRAND.font.display} fontSize="118" textAnchor="middle">5-4</text>
      </g>
    </svg>
  );
};

const ClassActionGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    {Array.from({length: 13}, (_, i) => {
      const x = 590 + (i % 5) * 170;
      const y = 342 + Math.floor(i / 5) * 128;
      return <circle key={i} cx={x} cy={y} r="32" fill={i === 6 ? GOLD : BLUE} opacity="0.9" />;
    })}
    <line x1="590" y1="600" x2="1270" y2="344" stroke={GOLD} strokeWidth="7" strokeDasharray="18 14" opacity="0.9" />
    <text x="960" y="760" fill={WHITE} fontFamily={BRAND.font.display} fontSize="74" textAnchor="middle">ONE CASE, MANY SMALL HARMS</text>
  </svg>
);

const WaiverGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <rect x="690" y="230" width="540" height="520" rx="8" fill="#E5E0D0" opacity="0.86" />
    {[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x="750" y={300 + i * 58} width={360 - (i % 2) * 80} height="18" fill="#1B2638" opacity="0.35" />)}
    <line x1="760" y1="615" x2="1160" y2="615" stroke={RED} strokeWidth="18" />
    <text x="960" y="655" fill={INK} fontFamily={BRAND.font.display} fontSize="72" textAnchor="middle">WAIVER</text>
  </svg>
);

const ClickWaiveGraphic: React.FC = () => (
  <div style={{position: 'absolute', left: 640, top: 260, width: 640, height: 360}}>
    <div style={{width: 420, height: 150, borderRadius: 36, border: `6px solid ${GOLD}`, background: `${BLUE}CC`, boxShadow: `0 0 60px ${BLUE}`}} />
    <div style={{position: 'absolute', left: 90, top: 190, fontFamily: BRAND.font.display, color: WHITE, fontSize: 72, textTransform: 'uppercase'}}>tap</div>
    <div style={{position: 'absolute', left: 300, top: 190, fontFamily: BRAND.font.display, color: GOLD, fontSize: 72, textTransform: 'uppercase'}}>waive</div>
    <div style={{position: 'absolute', left: 228, top: 118, width: 220, height: 8, background: GOLD, transform: 'rotate(28deg)'}} />
  </div>
);

const OverlayFor: React.FC<{shot: RoughShot}> = ({shot}) => {
  if (shot.spanId === 'SPN-0006') return <ClassActionGraphic />;
  if (shot.spanId === 'SPN-0010') return <WaiverGraphic />;
  if (shot.spanId === 'SPN-0011' || shot.spanId === 'SPN-0012') return <DebateOverlay />;
  if (shot.spanId === 'SPN-0013') return <VoteSplit year="2011" label="AT&T Mobility v. Concepcion" />;
  if (shot.spanId === 'SPN-0018') return <VoteSplit year="2018" label="Epic Systems v. Lewis" />;
  if (shot.spanId === 'SPN-0023') return <ClickWaiveGraphic />;
  return null;
};

const Scene: React.FC<{shot: TimedShot}> = ({shot}) => (
  <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
    {shot.assetType === 'stock_video' ? <VideoSequence shot={shot} /> : <ImageSequence shot={shot} />}
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}C5 0%, #00000022 42%, ${INK}D6 100%)`}} />
    <LightSweep seed={shot.spanId} color={shot.spanId === 'SPN-0011' || shot.spanId === 'SPN-0012' ? GOLD : BLUE} />
    <Particles seed={shot.spanId} count={18} color={shot.spanId === 'SPN-0013' || shot.spanId === 'SPN-0018' ? GOLD : BLUE} />
    <OverlayFor shot={shot} />
    <Telop shot={shot} />
    <SafetyLabel />
    <Vignette strength={0.96} />
    <Grain opacity={0.05} />
  </AbsoluteFill>
);

const Hook: React.FC = () => {
  const shot = ARBITRATION_ROUGHCUT.shots[0];
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <VideoSequence shot={shot} />
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}EA 0%, #00000055 58%, ${INK}90 100%)`}} />
      <ClickWaiveGraphic />
      <div style={{position: 'absolute', left: 70, bottom: 185, fontFamily: BRAND.font.display, color: WHITE, fontSize: 86, lineHeight: 0.95, textTransform: 'uppercase', maxWidth: 860, textShadow: '0 6px 30px #000'}}>
        The right you sign away
      </div>
      <div style={{position: 'absolute', left: 74, bottom: 154, width: 360, height: 5, background: GOLD}} />
      <Particles seed="arbitration-hook" count={22} color={GOLD} />
      <Vignette strength={1} />
      <Grain opacity={0.055} />
    </AbsoluteFill>
  );
};

export const ArbitrationPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={Math.round(HOOK_SEC * FPS)} name="PART_1_HOOK">
      <Hook />
    </Sequence>
    <Sequence from={Math.round(HOOK_SEC * FPS)} durationInFrames={Math.round(OPENING_SEC * FPS)} name="PART_2_BRAND_OPENING">
      <BrandOpening seriesLabel="Prime Documentary" title="Arbitration" subtitle="The right you sign away" />
    </Sequence>
    {bodyShots.map((shot) => (
      <Sequence key={shot.spanId} from={Math.round(shot.start * FPS)} durationInFrames={Math.round(shot.dur * FPS)} name={`${shot.chapterId ?? 'body'}_${shot.spanId}`}>
        <Scene shot={shot} />
      </Sequence>
    ))}
    <Sequence from={Math.round((TOTAL_SEC - ENDCARD_SEC) * FPS)} durationInFrames={Math.round(ENDCARD_SEC * FPS)} name="PART_4_BRAND_ENDCARD">
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile('arbitration/audio/arbitration_final_mix_v001.mp3')} />
    <CaptionBand />
  </AbsoluteFill>
);

export const arbitrationPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
