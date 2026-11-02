import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export type OpeningGloverProps = {
  title: string;
  subtitle: string;
  accent: string;
  hasLogo: boolean;
};

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingGloverDurationInFrames = (fps: number) => Math.round(fps * 3.0);

export const OpeningGlover: React.FC<OpeningGloverProps> = ({title, subtitle, accent, hasLogo}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const p = frame / Math.max(1, openingGloverDurationInFrames(fps));
  const titleIn = spring({frame: frame - sec(fps, 0.25), fps, config: {damping: 18, mass: 0.9}});
  const lineIn = spring({frame: frame - sec(fps, 0.65), fps, config: {damping: 22, mass: 0.9}});
  const subIn = spring({frame: frame - sec(fps, 0.95), fps, config: {damping: 20, mass: 1}});
  return (
    <AbsoluteFill style={{backgroundColor: '#0A0A0C', overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          background: `radial-gradient(90% 90% at ${42 + p * 16}% ${38 + p * 8}%, ${accent}44 0%, transparent 56%), linear-gradient(180deg, #101922 0%, #0A0A0C 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.18,
          transform: `translateX(${interpolate(p, [0, 1], [-80, 80])}px)`,
          backgroundImage: `repeating-linear-gradient(90deg, ${accent}66 0 2px, transparent 2px 72px)`,
        }}
      />
      {hasLogo && (
        <div
          style={{
            position: 'absolute',
            top: 64,
            left: 72,
            width: 84,
            height: 84,
            border: `2px solid ${accent}`,
            boxShadow: `0 0 30px ${accent}88`,
          }}
        />
      )}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(-58px)'}}>
        <div
          style={{
            width: width * 0.72,
            textAlign: 'center',
            fontFamily: '"Oswald", "Archivo", Impact, sans-serif',
            fontSize: 136,
            lineHeight: 0.92,
            fontWeight: 900,
            letterSpacing: 0,
            color: '#F5F7FA',
            opacity: titleIn,
            transform: `translateY(${interpolate(titleIn, [0, 1], [48, 0])}px)`,
            textShadow: '0 12px 44px #000',
          }}
        >
          {title}
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(82px)'}}>
        <div style={{width: width * 0.38, height: 7, background: accent, transform: `scaleX(${lineIn})`, boxShadow: `0 0 24px ${accent}`}} />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(142px)'}}>
        <div
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontSize: 36,
            fontWeight: 600,
            textTransform: 'uppercase',
            color: '#C8D8E6',
            opacity: subIn,
            transform: `translateY(${interpolate(subIn, [0, 1], [28, 0], {easing: Easing.out(Easing.cubic)})}px)`,
          }}
        >
          {subtitle}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
