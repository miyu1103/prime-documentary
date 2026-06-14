import React from 'react';
import {AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

const MJ_IMAGE_MAP: Record<string, string> = {
  'MJ-EP:constitution-fifth-amendment': 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  'MJ-EP:interrogation-room-symbolic':  'approved/s004_interrogation_room_01_primary.png',
  'MJ-EP:courtroom-1960s-symbolic':     'approved/s007_courtroom_1960s_01_primary.png',
  'MJ-EP:miranda-warning-card':         'approved/s016_miranda_warning_card_01_primary.png',
  'MJ-EP:retrial-symbolic':             'approved/s018_retrial_symbolic_01_primary.png',
};

/**
 * Coded symbolic art for scenes whose real Midjourney still is not generated yet.
 * Gives the animatic a "video" feel ($0, pure SVG/CSS) instead of a placeholder box.
 * These are intentionally symbolic — never mistaken for real footage (invariant 11).
 */

const S = BRAND.color;

const Frame: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  // slow breathing drift so it feels alive
  const k = interpolate(f, [0, durationInFrames], [0, 1]);
  const dy = Math.sin(k * Math.PI) * -10;
  return (
    <AbsoluteFill
      style={{background: `radial-gradient(120% 100% at 50% 38%, ${S.navy} 0%, ${S.ink} 82%)`,
        justifyContent: 'center', alignItems: 'center'}}
    >
      <div style={{transform: `translateY(${dy}px)`}}>{children}</div>
    </AbsoluteFill>
  );
};

const Caption: React.FC<{lines: string[]}> = ({lines}) =>
  lines.length ? (
    <div style={{marginTop: 26, textAlign: 'center', color: S.white, fontFamily: BRAND.font.display,
      fontSize: 40, fontWeight: 900, textTransform: 'uppercase', letterSpacing: 1}}>
      {lines.map((t, i) => <div key={i}>{t}</div>)}
    </div>
  ) : null;

const Gavel: React.FC = () => (
  <svg width="360" height="240" viewBox="0 0 360 240">
    <g transform="rotate(-18 180 120)">
      <rect x="70" y="96" width="220" height="34" rx="10" fill={S.gold} />
      <rect x="150" y="60" width="60" height="60" rx="10" fill={S.gold} />
    </g>
    <rect x="120" y="180" width="120" height="16" rx="8" fill={S.silver} opacity="0.6" />
  </svg>
);

const Scales: React.FC = () => (
  <svg width="320" height="260" viewBox="0 0 320 260" stroke={S.gold} strokeWidth="5" fill="none">
    <line x1="160" y1="30" x2="160" y2="210" />
    <line x1="70" y1="70" x2="250" y2="70" />
    <path d="M70 70 l-34 60 a34 20 0 0 0 68 0 z" fill={`${S.electric}22`} />
    <path d="M250 70 l-34 60 a34 20 0 0 0 68 0 z" fill={`${S.electric}22`} />
    <rect x="120" y="210" width="80" height="14" rx="7" fill={S.gold} />
  </svg>
);

const Document: React.FC = () => (
  <svg width="280" height="320" viewBox="0 0 280 320">
    <rect x="40" y="20" width="200" height="270" rx="10" fill={`${S.silver}22`} stroke={S.silver} strokeWidth="3" />
    {[60, 90, 120, 150, 180].map((y) => <rect key={y} x="70" y={y} width="140" height="8" rx="4" fill={`${S.silver}88`} />)}
    <circle cx="200" cy="250" r="34" fill={`${S.gold}33`} stroke={S.gold} strokeWidth="4" />
  </svg>
);

const Room: React.FC = () => (
  <svg width="420" height="280" viewBox="0 0 420 280">
    <ellipse cx="210" cy="250" rx="150" ry="22" fill={`${S.electric}22`} />
    <line x1="210" y1="0" x2="210" y2="70" stroke={S.silver} strokeWidth="4" />
    <circle cx="210" cy="80" r="16" fill={S.gold} />
    <polygon points="210,90 120,250 300,250" fill={`${S.gold}18`} />
    <rect x="150" y="200" width="120" height="40" rx="6" fill={`${S.silver}33`} stroke={S.silver} strokeWidth="3" />
  </svg>
);

const Courtroom: React.FC = () => (
  <svg width="460" height="280" viewBox="0 0 460 280" stroke={S.silver} strokeWidth="3" fill="none">
    {[60, 130, 200, 270, 340, 400].map((x) => <line key={x} x1={x} y1="40" x2={x} y2="200" opacity="0.5" />)}
    <rect x="150" y="150" width="160" height="60" rx="6" fill={`${S.gold}22`} stroke={S.gold} />
    <line x1="40" y1="210" x2="420" y2="210" stroke={S.gold} />
  </svg>
);

const MapUS: React.FC = () => (
  <svg width="460" height="280" viewBox="0 0 460 280">
    <path d="M40 120 q40 -50 120 -40 q60 -30 140 -10 q70 -10 120 30 q-20 60 -90 70 q-80 40 -180 20 q-90 0 -110 -90 z"
      fill={`${S.electric}1a`} stroke={S.electric} strokeWidth="3" />
    <circle cx="150" cy="170" r="9" fill={S.gold} />
    <circle cx="150" cy="170" r="20" fill="none" stroke={S.gold} strokeWidth="2" opacity="0.6" />
  </svg>
);

const Timeline: React.FC = () => (
  <svg width="500" height="140" viewBox="0 0 500 140" stroke={S.silver} strokeWidth="3">
    <line x1="30" y1="70" x2="470" y2="70" />
    {[110, 250, 390].map((x) => <circle key={x} cx={x} cy="70" r="7" fill={S.silver} />)}
    <circle cx="250" cy="70" r="13" fill={S.gold} stroke={S.gold} />
  </svg>
);

const ART: Record<string, React.FC> = {
  gavel: Gavel, scales: Scales, document: Document, room: Room, courtroom: Courtroom, map: MapUS, timeline: Timeline,
};

/** Pick art from the visual mode + motif hint (best effort), with a sensible default. */
export function pickArt(visualMode: string, motifHint: string): React.FC {
  const h = (motifHint || '').toLowerCase();
  if (h.includes('gavel')) return Gavel;
  if (h.includes('scales') || h.includes('justice')) return Scales;
  if (h.includes('document') || h.includes('warning-card') || h.includes('constitution') || h.includes('seal')) return Document;
  if (h.includes('interrogation') || h.includes('spotlight') || h.includes('jail')) return Room;
  if (h.includes('court')) return Courtroom;
  if (visualMode === 'map') return MapUS;
  if (visualMode === 'timeline') return Timeline;
  if (visualMode === 'reenactment') return Room;
  if (visualMode === 'archival_illustration') return Courtroom;
  if (visualMode === 'object') return Document;
  return ART.gavel;
}

function panDirection(motifHint: string): 1 | -1 {
  let sum = 0;
  for (let i = 0; i < motifHint.length; i++) sum += motifHint.charCodeAt(i);
  return sum % 2 === 0 ? 1 : -1;
}

const PhotoFrame: React.FC<{src: string; motifHint: string}> = ({src, motifHint}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const t = f / durationInFrames;
  const dir = panDirection(motifHint);
  const scale = interpolate(t, [0, 1], [1.0, 1.14]);
  const tx    = interpolate(t, [0, 1], [0, dir * 55]);
  const ty    = interpolate(t, [0, 1], [0, -18]);
  return (
    <AbsoluteFill style={{background: BRAND.color.ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{
        transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
        transformOrigin: '50% 50%',
        willChange: 'transform',
      }}>
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{
        background: 'linear-gradient(to top, rgba(10,10,12,0.75) 0%, rgba(10,10,12,0.10) 40%, rgba(10,10,12,0.40) 100%)',
      }} />
    </AbsoluteFill>
  );
};

export const SceneArt: React.FC<{visualMode: string; motifHint: string; onScreenText: string[]}> = ({
  visualMode, motifHint, onScreenText,
}) => {
  const imgSrc = MJ_IMAGE_MAP[motifHint];
  if (imgSrc) {
    return <PhotoFrame src={imgSrc} motifHint={motifHint} />;
  }
  const Art = pickArt(visualMode, motifHint);
  return (
    <Frame>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <Art />
        <Caption lines={onScreenText.slice(0, 3)} />
      </div>
    </Frame>
  );
};
