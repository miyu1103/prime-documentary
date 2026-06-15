import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';

const S = BRAND.color;
const IMPACT = 'Impact, "Arial Black", Arial, sans-serif';

export const HookCard: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const bg = interpolate(f, [0, 20], [0, 1], {extrapolateRight: 'clamp'});

  const bar1w = interpolate(f, [8, 40], [0, 900], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  const l1 = spring({frame: f - 12, fps, config: {damping: 22, stiffness: 70, mass: 0.9}});
  const l2 = spring({frame: f - 30, fps, config: {damping: 22, stiffness: 70, mass: 0.9}});
  const sub1 = spring({frame: f - 55, fps, config: {damping: 18, stiffness: 60}});
  const sub2 = spring({frame: f - 72, fps, config: {damping: 18, stiffness: 60}});
  const brand = spring({frame: f - 80, fps, config: {damping: 18, stiffness: 50}});

  // pulse glow on "TO REMAIN SILENT."
  const pulse = 0.7 + 0.3 * Math.sin((f / fps) * Math.PI * 2.4);
  const glowOpacity = interpolate(f, [35, 55], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // vignette fade at end
  const fadeOut = interpolate(f, [durationInFrames - 18, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{background: S.ink, opacity: bg}}>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', flexDirection: 'column', gap: 10}}>

        {/* top line */}
        <div style={{width: bar1w, height: 2, background: S.electric, marginBottom: 24}} />

        {/* LINE 1: YOU HAVE THE RIGHT */}
        <div style={{
          transform: `translateY(${interpolate(l1, [0, 1], [-80, 0])}px)`,
          opacity: l1,
          color: S.white,
          fontFamily: IMPACT,
          fontSize: 104,
          letterSpacing: 6,
          textAlign: 'center',
          lineHeight: 1,
        }}>
          YOU HAVE THE RIGHT
        </div>

        {/* LINE 2: TO REMAIN SILENT. */}
        <div style={{
          transform: `translateY(${interpolate(l2, [0, 1], [80, 0])}px)`,
          opacity: l2,
          color: S.electric,
          fontFamily: IMPACT,
          fontSize: 104,
          letterSpacing: 6,
          textAlign: 'center',
          lineHeight: 1,
          textShadow: glowOpacity > 0
            ? `0 0 ${60 * pulse}px ${S.electric}cc, 0 0 ${120 * pulse}px ${S.electric}55`
            : 'none',
        }}>
          TO REMAIN SILENT.
        </div>

        {/* bottom line */}
        <div style={{width: bar1w, height: 2, background: S.electric, marginTop: 24, opacity: l2}} />

        {/* sub 1 */}
        <div style={{
          marginTop: 32,
          opacity: sub1,
          transform: `translateY(${interpolate(sub1, [0, 1], [20, 0])}px)`,
          color: S.silver,
          fontFamily: BRAND.font.body,
          fontSize: 26,
          letterSpacing: 4,
          textTransform: 'uppercase',
        }}>
          You have heard it in a thousand movies.
        </div>

        {/* sub 2 */}
        <div style={{
          opacity: sub2,
          transform: `translateY(${interpolate(sub2, [0, 1], [20, 0])}px)`,
          color: S.gold,
          fontFamily: BRAND.font.body,
          fontSize: 26,
          letterSpacing: 4,
          textTransform: 'uppercase',
        }}>
          But where does it actually come from?
        </div>
      </AbsoluteFill>

      {/* PRIME DOCUMENTARY brand stamp — bottom right */}
      <div style={{
        position: 'absolute', bottom: 48, right: 64,
        opacity: brand,
        color: S.gold,
        fontFamily: IMPACT,
        fontSize: 20,
        letterSpacing: 7,
        textTransform: 'uppercase',
      }}>
        PRIME DOCUMENTARY
      </div>

      {/* Vignette overlay fade-out */}
      <AbsoluteFill style={{background: S.ink, opacity: fadeOut, pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};
