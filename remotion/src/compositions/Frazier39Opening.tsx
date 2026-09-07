import React from 'react';
import {Trail} from '@remotion/motion-blur';
import {AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

export type Frazier39OpeningProps = {
  title: string;
  subtitle: string;
  accent: string;
  hasLogo: boolean;
};

const T = {
  bgIn: 0,
  logoIn: 0.1,
  gridIn: 0.15,
  glowIn: 0.25,
  titleIn: 0.3,
  charStagger: 0.04,
  accentIn: 0.95,
  subIn: 1.1,
  flashAt: 1.6,
  pushAt: 2.7,
} as const;

const sec = (fps: number, seconds: number) => Math.round(fps * seconds);

export const frazier39OpeningDurationInFrames = (fps: number) => Math.round(fps * 3);

export const Frazier39Opening: React.FC<Frazier39OpeningProps> = ({title, subtitle, accent, hasLogo}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const duration = frazier39OpeningDurationInFrames(fps);
  const bgOpacity = interpolate(frame, [sec(fps, T.bgIn), sec(fps, 0.4)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const bgScale = interpolate(frame, [0, duration], [1.08, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const pushScale = interpolate(frame, [sec(fps, T.pushAt), duration], [1, 1.02], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const gridReveal = spring({
    frame: frame - sec(fps, T.gridIn),
    fps,
    config: {damping: 200, mass: 1},
    durationInFrames: sec(fps, 0.8),
  });
  const gridY = interpolate(frame, [0, duration], [0, 48], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  const glow = spring({frame: frame - sec(fps, T.glowIn), fps, config: {damping: 18, mass: 1.2}});
  const accentSpring = spring({frame: frame - sec(fps, T.accentIn), fps, config: {damping: 16, mass: 0.8}});
  const subSpring = spring({frame: frame - sec(fps, T.subIn), fps, config: {damping: 20, mass: 1}});
  const logoSpring = spring({frame: frame - sec(fps, T.logoIn), fps, config: {damping: 14, mass: 0.9}});
  const stagger = Math.max(1, Math.ceil(fps * T.charStagger));
  const flashStart = sec(fps, T.flashAt);
  const flashEnd = sec(fps, T.flashAt + 0.2);
  const flashOpacity = interpolate(
    frame,
    [flashStart, flashStart + Math.round((flashEnd - flashStart) / 2), flashEnd],
    [0, 0.1, 0],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  return (
    <AbsoluteFill style={{backgroundColor: '#05070d', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${pushScale})`}}>
        <AbsoluteFill
          style={{
            opacity: bgOpacity,
            transform: `scale(${bgScale})`,
            background: 'radial-gradient(120% 120% at 50% 35%, #0E1B33 0%, #0A1020 45%, #05070d 100%)',
          }}
        />
        <AbsoluteFill
          style={{
            opacity: gridReveal * 0.18,
            transform: `translateY(${gridY}px)`,
            backgroundImage: `repeating-linear-gradient(0deg, ${accent}22 0px 1px, transparent 1px 64px), repeating-linear-gradient(90deg, ${accent}22 0px 1px, transparent 1px 64px)`,
            maskImage: 'radial-gradient(120% 90% at 50% 45%, black 35%, transparent 80%)',
          }}
        />
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
        <AbsoluteFill style={{backgroundColor: '#0B1A2B', opacity: flashOpacity}} />
        {hasLogo ? (
          <div
            style={{
              position: 'absolute',
              top: 64,
              left: 72,
              width: 84,
              height: 84,
              borderRadius: 20,
              opacity: interpolate(logoSpring, [0, 1], [0, 1]),
              transform: `scale(${interpolate(logoSpring, [0, 1], [0.4, 1])})`,
              background: `linear-gradient(135deg, ${accent}, #ffffff22)`,
              border: `2px solid ${accent}`,
              boxShadow: `0 0 30px ${accent}66`,
            }}
          />
        ) : null}
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', transform: 'translateY(-70px)'}}>
          <Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
            <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
              <div
                style={{
                  display: 'flex',
                  fontFamily: '"Oswald", "Archivo", Impact, sans-serif',
                  fontWeight: 800,
                  fontSize: 132,
                  letterSpacing: 0,
                  color: '#F5F7FA',
                  lineHeight: 1.05,
                }}
              >
                {title.split('').map((character, index) => {
                  const reveal = spring({
                    frame: frame - sec(fps, T.titleIn) - index * stagger,
                    fps,
                    config: {damping: 16, mass: 1},
                  });
                  const y = interpolate(reveal, [0, 1], [110, 0]);
                  const opacity = interpolate(reveal, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
                  return (
                    <span key={`${character}-${index}`} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}>
                      <span style={{display: 'inline-block', transform: `translateY(${y}%)`, opacity, whiteSpace: 'pre'}}>
                        {character}
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
            <div
              style={{
                width: 240,
                height: 6,
                borderRadius: 3,
                backgroundColor: accent,
                boxShadow: `0 0 24px ${accent}aa`,
                transform: `scaleX(${accentSpring})`,
                transformOrigin: 'left center',
              }}
            />
            <div
              style={{
                fontFamily: '"Oswald", "Archivo", sans-serif',
                fontWeight: 500,
                fontSize: 38,
                letterSpacing: 0,
                textTransform: 'uppercase',
                color: '#C8CDD6',
                opacity: subSpring,
                transform: `translateY(${interpolate(subSpring, [0, 1], [24, 0])}px)`,
              }}
            >
              {subtitle}
            </div>
          </div>
        </AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
