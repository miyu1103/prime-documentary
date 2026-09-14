import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Trail} from '@remotion/motion-blur';

export type OpeningStrieffProps = {
  title: string;
  subtitle: string;
  accent: string;
  hasLogo: boolean;
};

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingStrieffDurationInFrames = (fps: number) => Math.round(fps * 3.0);

export const OpeningStrieff: React.FC<OpeningStrieffProps> = ({title, subtitle, accent, hasLogo}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const bg = interpolate(frame, [0, sec(fps, 0.35)], [0, 1], {extrapolateRight: 'clamp'});
  const push = interpolate(frame, [0, openingStrieffDurationInFrames(fps)], [1.1, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const grid = spring({frame: frame - sec(fps, 0.15), fps, config: {damping: 190, mass: 1}, durationInFrames: sec(fps, 0.85)});
  const slit = spring({frame: frame - sec(fps, 0.48), fps, config: {damping: 22, mass: 1}});
  const glow = spring({frame: frame - sec(fps, 0.22), fps, config: {damping: 18, mass: 1.1}});
  const sub = spring({frame: frame - sec(fps, 1.08), fps, config: {damping: 20, mass: 1}});
  const logo = spring({frame: frame - sec(fps, 0.08), fps, config: {damping: 14, mass: 0.9}});
  const stagger = Math.max(1, sec(fps, 2 / fps));

  return (
    <AbsoluteFill style={{backgroundColor: '#0A0A0C', overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          opacity: bg,
          transform: `scale(${push})`,
          background: `radial-gradient(90% 90% at 62% 38%, ${accent}44 0%, #17101C 32%, #0A0A0C 78%)`,
        }}
      />
      <AbsoluteFill
        style={{
          opacity: grid * 0.22,
          backgroundImage: `repeating-linear-gradient(0deg, ${accent}24 0 1px, transparent 1px 58px), repeating-linear-gradient(90deg, ${accent}20 0 1px, transparent 1px 58px)`,
          maskImage: 'radial-gradient(115% 88% at 50% 48%, black 32%, transparent 82%)',
        }}
      />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: width * 0.78,
            height: 8,
            transform: `scaleX(${slit})`,
            opacity: interpolate(slit, [0, 1], [0, 0.72]),
            background: `linear-gradient(90deg, transparent, ${accent}, transparent)`,
            filter: 'blur(0.5px)',
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: width * 0.58,
            height: height * 0.32,
            opacity: interpolate(glow, [0, 1], [0, 0.86]),
            filter: 'blur(30px)',
            background: `radial-gradient(closest-side, ${accent}88 0%, ${accent}22 48%, transparent 76%)`,
          }}
        />
      </AbsoluteFill>
      {hasLogo && (
        <div
          style={{
            position: 'absolute',
            top: 64,
            left: 72,
            width: 84,
            height: 84,
            opacity: interpolate(logo, [0, 1], [0, 1]),
            transform: `scale(${interpolate(logo, [0, 1], [0.42, 1])}) rotate(45deg)`,
            border: `2px solid ${accent}`,
            boxShadow: `0 0 30px ${accent}66`,
          }}
        />
      )}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(-70px)'}}>
        <Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
          <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
            <div style={{display: 'flex', fontFamily: '"Oswald", "Archivo", Impact, sans-serif', fontWeight: 800, fontSize: 132, letterSpacing: 0, color: '#F5F7FA', lineHeight: 1.02}}>
              {title.split('').map((ch, i) => {
                const s = spring({frame: frame - sec(fps, 0.3) - i * stagger, fps, config: {damping: 16, mass: 1}});
                return (
                  <span key={`${ch}-${i}`} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}>
                    <span style={{display: 'inline-block', transform: `translateY(${interpolate(s, [0, 1], [110, 0])}%)`, opacity: interpolate(s, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'}), whiteSpace: 'pre'}}>
                      {ch}
                    </span>
                  </span>
                );
              })}
            </div>
          </AbsoluteFill>
        </Trail>
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(58px)'}}>
        <div style={{display: 'flex', flexDirection: 'column', gap: 18, alignItems: 'center'}}>
          <div style={{width: 260, height: 6, background: accent, boxShadow: `0 0 24px ${accent}`, transform: `scaleX(${sub})`, transformOrigin: 'center'}} />
          <div style={{fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 600, fontSize: 36, letterSpacing: 0, textTransform: 'uppercase', color: '#C8CDD6', opacity: sub}}>
            {subtitle}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
