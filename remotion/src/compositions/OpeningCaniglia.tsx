import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {Trail} from '@remotion/motion-blur';

export type OpeningCanigliaProps = {
  title: string;
  subtitle: string;
  accent: string;
  hasLogo: boolean;
};

const sec = (fps: number, s: number) => Math.round(fps * s);
export const openingCanigliaDurationInFrames = (fps: number) => Math.round(fps * 3.0);

export const OpeningCaniglia: React.FC<OpeningCanigliaProps> = ({title, subtitle, accent, hasLogo}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const bgOpacity = interpolate(frame, [0, sec(fps, 0.4)], [0, 1], {extrapolateRight: 'clamp'});
  const bgScale = interpolate(frame, [0, openingCanigliaDurationInFrames(fps)], [1.08, 1.0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const grid = spring({frame: frame - sec(fps, 0.15), fps, config: {damping: 200, mass: 1}, durationInFrames: sec(fps, 0.8)});
  const glow = spring({frame: frame - sec(fps, 0.25), fps, config: {damping: 18, mass: 1.2}});
  const slit = spring({frame: frame - sec(fps, 0.55), fps, config: {damping: 22, mass: 1.1}});
  const accentSpring = spring({frame: frame - sec(fps, 0.95), fps, config: {damping: 16, mass: 0.8}});
  const subSpring = spring({frame: frame - sec(fps, 1.1), fps, config: {damping: 20, mass: 1}});
  const logoSpring = spring({frame: frame - sec(fps, 0.1), fps, config: {damping: 14, mass: 0.9}});
  const stagger = Math.max(1, sec(fps, 2 / fps));

  return (
    <AbsoluteFill style={{backgroundColor: '#0A0A0C', overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          opacity: bgOpacity,
          transform: `scale(${bgScale})`,
          background: 'radial-gradient(120% 120% at 50% 35%, #14110E 0%, #0F0C0A 45%, #0A0A0C 100%)',
        }}
      />
      <AbsoluteFill
        style={{
          opacity: grid * 0.18,
          transform: `translateY(${interpolate(frame, [0, openingCanigliaDurationInFrames(fps)], [0, 48], {
            easing: Easing.inOut(Easing.sin),
            extrapolateRight: 'clamp',
          })}px)`,
          backgroundImage: `repeating-linear-gradient(0deg, ${accent}22 0px 1px, transparent 1px 62px), repeating-linear-gradient(90deg, ${accent}22 0px 1px, transparent 1px 62px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 45%, black 34%, transparent 80%)',
        }}
      />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: width * 0.78,
            height: height * 0.02,
            transform: `scaleX(${slit})`,
            opacity: interpolate(slit, [0, 1], [0, 0.55]),
            transformOrigin: 'center',
            background: `linear-gradient(90deg, transparent 0%, ${accent}00 8%, ${accent}dd 48%, ${accent}00 92%, transparent 100%)`,
            filter: 'blur(1px)',
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: width * 0.62,
            height: height * 0.36,
            transform: `scale(${interpolate(glow, [0, 1], [0.6, 1.15])})`,
            opacity: interpolate(glow, [0, 1], [0, 0.85]),
            filter: 'blur(28px)',
            background: `radial-gradient(closest-side, ${accent}88 0%, ${accent}22 45%, transparent 75%)`,
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
            opacity: interpolate(logoSpring, [0, 1], [0, 1]),
            transform: `scale(${interpolate(logoSpring, [0, 1], [0.4, 1])})`,
            background: `linear-gradient(135deg, ${accent}, #ffffff22)`,
            border: `2px solid ${accent}`,
            boxShadow: `0 0 30px ${accent}66`,
          }}
        />
      )}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(-70px)'}}>
        <Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
          <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
            <div style={{display: 'flex', fontFamily: '"Oswald", "Archivo", Impact, sans-serif', fontWeight: 800, fontSize: 144, letterSpacing: 0, color: '#fff', lineHeight: 1.05}}>
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
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(55px)'}}>
        <div style={{display: 'flex', flexDirection: 'column', gap: 18, alignItems: 'center'}}>
          <div style={{width: 240, height: 6, background: accent, boxShadow: `0 0 24px ${accent}aa`, transform: `scaleX(${accentSpring})`, transformOrigin: 'left center'}} />
          <div style={{fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 500, fontSize: 38, letterSpacing: 0, textTransform: 'uppercase', color: '#c8d2e6', opacity: subSpring, transform: `translateY(${interpolate(subSpring, [0, 1], [24, 0])}px)`}}>
            {subtitle}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

