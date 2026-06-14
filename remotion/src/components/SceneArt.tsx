import React from 'react';
import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {MovingStage} from './Motion';

/**
 * Coded symbolic art for scenes whose real Midjourney still is not generated yet.
 * The art itself now *animates* (gavel strikes, scales tip, light sweeps, a pin
 * ripples) so the animatic reads as a moving film, not a slideshow. Pure SVG/CSS,
 * $0. Intentionally symbolic — never mistaken for real footage (invariant 11).
 */

const S = BRAND.color;

const Caption: React.FC<{lines: string[]}> = ({lines}) => {
  const f = useCurrentFrame();
  return lines.length ? (
    <div style={{marginTop: 26, textAlign: 'center'}}>
      {lines.map((t, i) => {
        const o = interpolate(f, [6 + i * 6, 18 + i * 6], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const y = interpolate(o, [0, 1], [14, 0]);
        return (
          <div
            key={i}
            style={{
              opacity: o,
              transform: `translateY(${y}px)`,
              color: S.white,
              fontFamily: BRAND.font.display,
              fontSize: 40,
              fontWeight: 900,
              textTransform: 'uppercase',
              letterSpacing: 1,
            }}
          >
            {t}
          </div>
        );
      })}
    </div>
  ) : null;
};

/** Gavel that lifts and strikes on a loop, with an impact ripple at the block. */
const Gavel: React.FC = () => {
  const f = useCurrentFrame();
  const period = 72;
  const t = (f % period) / period; // 0..1
  const lift = Math.sin(Math.min(t, 0.55) / 0.55 * (Math.PI / 2)); // raise during first 55%
  const strike = t > 0.55 ? Math.min((t - 0.55) / 0.18, 1) : 0; // quick strike
  const angle = -10 - lift * 22 + strike * 26; // -32 (raised) -> -6 (struck)
  const impact = t > 0.73 ? interpolate(t, [0.73, 1], [1, 0]) : 0;
  return (
    <svg width="360" height="260" viewBox="0 0 360 260">
      <g transform={`rotate(${angle} 180 130)`} style={{transformOrigin: '180px 130px'}}>
        <rect x="70" y="106" width="220" height="34" rx="10" fill={S.gold} />
        <rect x="150" y="70" width="60" height="60" rx="10" fill={S.gold} />
      </g>
      <rect x="120" y="196" width="120" height="16" rx="8" fill={S.silver} opacity="0.6" />
      <circle cx="180" cy="204" r={10 + impact * 60} fill="none" stroke={S.gold} strokeWidth="3" opacity={impact * 0.8} />
    </svg>
  );
};

/** Scales of justice that tip and slowly settle back and forth. */
const Scales: React.FC = () => {
  const f = useCurrentFrame();
  const tilt = Math.sin(f * 0.045) * 9; // degrees
  const lpan = Math.tan((tilt * Math.PI) / 180) * 90;
  return (
    <svg width="340" height="280" viewBox="0 0 340 280" stroke={S.gold} strokeWidth="5" fill="none">
      <line x1="170" y1="34" x2="170" y2="220" />
      <g transform={`rotate(${tilt} 170 80)`}>
        <line x1="80" y1="80" x2="260" y2="80" />
        <path d={`M80 80 l-34 ${60 - lpan} a34 20 0 0 0 68 0 z`} fill={`${S.electric}22`} />
        <path d={`M260 80 l-34 ${60 + lpan} a34 20 0 0 0 68 0 z`} fill={`${S.electric}22`} />
      </g>
      <rect x="130" y="220" width="80" height="14" rx="7" fill={S.gold} />
    </svg>
  );
};

/** Document whose lines draw in, then a seal stamps down and pulses. */
const Document: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = [60, 90, 120, 150, 180];
  const stamp = spring({frame: f - 26, fps, config: {damping: 12, stiffness: 180}});
  const sealScale = interpolate(stamp, [0, 1], [2.2, 1]);
  const sealO = interpolate(f, [22, 32], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const glow = 0.5 + 0.5 * Math.sin(f * 0.08);
  return (
    <svg width="280" height="320" viewBox="0 0 280 320">
      <rect x="40" y="20" width="200" height="270" rx="10" fill={`${S.silver}22`} stroke={S.silver} strokeWidth="3" />
      {lines.map((y, i) => {
        const w = interpolate(f, [4 + i * 4, 16 + i * 4], [0, 140], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        return <rect key={y} x="70" y={y} width={w} height="8" rx="4" fill={`${S.silver}88`} />;
      })}
      <g transform={`translate(200 250) scale(${sealScale})`} opacity={sealO} style={{transformOrigin: '200px 250px'}}>
        <circle cx="0" cy="0" r="34" fill={`${S.gold}${glow > 0.6 ? '44' : '33'}`} stroke={S.gold} strokeWidth="4" />
      </g>
    </svg>
  );
};

/** Interrogation room: a hard lamp that flickers and a light cone that breathes. */
const Room: React.FC = () => {
  const f = useCurrentFrame();
  const flicker = 0.7 + 0.3 * Math.abs(Math.sin(f * 0.5)) * (Math.sin(f * 1.7) > -0.6 ? 1 : 0.4);
  const cone = 0.1 + 0.06 * (0.5 + 0.5 * Math.sin(f * 0.06));
  return (
    <svg width="440" height="300" viewBox="0 0 440 300">
      <ellipse cx="220" cy="262" rx="160" ry="24" fill={`${S.electric}22`} opacity={flicker} />
      <line x1="220" y1="0" x2="220" y2="74" stroke={S.silver} strokeWidth="4" />
      <circle cx="220" cy="84" r="16" fill={S.gold} opacity={flicker} />
      <circle cx="220" cy="84" r={26} fill={S.gold} opacity={flicker * 0.25} />
      <polygon points="220,94 124,262 316,262" fill={S.gold} opacity={cone} />
      <rect x="158" y="210" width="124" height="42" rx="6" fill={`${S.silver}33`} stroke={S.silver} strokeWidth="3" />
    </svg>
  );
};

/** Empty courtroom with a shaft of light sweeping across the columns. */
const Courtroom: React.FC = () => {
  const f = useCurrentFrame();
  const sweep = 60 + 320 * (0.5 + 0.5 * Math.sin(f * 0.03));
  return (
    <svg width="480" height="300" viewBox="0 0 480 300">
      <g stroke={S.silver} strokeWidth="3" fill="none">
        {[60, 140, 220, 300, 380, 430].map((x) => (
          <line key={x} x1={x} y1="40" x2={x} y2="210" opacity="0.45" />
        ))}
        <rect x="160" y="150" width="170" height="62" rx="6" fill={`${S.gold}22`} stroke={S.gold} />
        <line x1="40" y1="214" x2="440" y2="214" stroke={S.gold} />
      </g>
      <polygon points={`${sweep - 40},40 ${sweep + 40},40 ${sweep + 90},214 ${sweep - 90},214`} fill={`${S.electric}14`} />
    </svg>
  );
};

/** US map with a pin that emits expanding ripple rings on a loop. */
const MapUS: React.FC = () => {
  const f = useCurrentFrame();
  const period = 60;
  const phase = (f % period) / period;
  const r = 9 + phase * 46;
  const o = interpolate(phase, [0, 1], [0.7, 0]);
  return (
    <svg width="480" height="300" viewBox="0 0 480 300">
      <path
        d="M40 130 q40 -50 120 -40 q60 -30 140 -10 q70 -10 120 30 q-20 60 -90 70 q-80 40 -180 20 q-90 0 -110 -90 z"
        fill={`${S.electric}1a`}
        stroke={S.electric}
        strokeWidth="3"
      />
      <circle cx="150" cy="180" r={r} fill="none" stroke={S.gold} strokeWidth="2" opacity={o} />
      <circle cx="150" cy="180" r="9" fill={S.gold} />
    </svg>
  );
};

/** Timeline with a marker that travels along the line, the centre node pulsing. */
const Timeline: React.FC = () => {
  const f = useCurrentFrame();
  const x = interpolate(Math.sin(f * 0.03), [-1, 1], [40, 460]);
  const pulse = 11 + 3 * Math.sin(f * 0.12);
  return (
    <svg width="500" height="150" viewBox="0 0 500 150" stroke={S.silver} strokeWidth="3">
      <line x1="40" y1="75" x2="460" y2="75" />
      {[110, 250, 390].map((cx) => (
        <circle key={cx} cx={cx} cy="75" r="7" fill={S.silver} />
      ))}
      <circle cx="250" cy="75" r={pulse} fill="none" stroke={S.gold} strokeWidth="2" />
      <circle cx={x} cy="75" r="9" fill={S.gold} />
    </svg>
  );
};

const ART: Record<string, React.FC> = {
  gavel: Gavel,
  scales: Scales,
  document: Document,
  room: Room,
  courtroom: Courtroom,
  map: MapUS,
  timeline: Timeline,
};

/** Pick art from the visual mode + motif hint (best effort), with a sensible default. */
export function pickArt(visualMode: string, motifHint: string): React.FC {
  const h = (motifHint || '').toLowerCase();
  if (h.includes('gavel')) return Gavel;
  if (h.includes('scales') || h.includes('justice')) return Scales;
  if (h.includes('document') || h.includes('warning-card') || h.includes('constitution') || h.includes('seal'))
    return Document;
  if (h.includes('interrogation') || h.includes('spotlight') || h.includes('jail')) return Room;
  if (h.includes('court')) return Courtroom;
  if (visualMode === 'map') return MapUS;
  if (visualMode === 'timeline') return Timeline;
  if (visualMode === 'reenactment') return Room;
  if (visualMode === 'archival_illustration') return Courtroom;
  if (visualMode === 'object') return Document;
  return ART.gavel;
}

/** Entrance: art rises and fades in, then the moving stage carries it. */
const ArtEntrance: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: f, fps, config: {damping: 200}});
  const y = interpolate(enter, [0, 1], [34, 0]);
  const sc = interpolate(enter, [0, 1], [0.92, 1]);
  return (
    <div style={{transform: `translateY(${y}px) scale(${sc})`, opacity: enter, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      {children}
    </div>
  );
};

export const SceneArt: React.FC<{
  visualMode: string;
  motifHint: string;
  onScreenText: string[];
  seed?: string;
}> = ({visualMode, motifHint, onScreenText, seed = 'art'}) => {
  const Art = pickArt(visualMode, motifHint);
  return (
    <MovingStage seed={`${seed}-${visualMode}`} intensity={0.9}>
      <div
        style={{
          width: '100%',
          height: '100%',
          background: `radial-gradient(120% 100% at 50% 38%, ${S.navy} 0%, ${S.ink} 82%)`,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <ArtEntrance>
          <Art />
          <Caption lines={onScreenText.slice(0, 3)} />
        </ArtEntrance>
      </div>
    </MovingStage>
  );
};
