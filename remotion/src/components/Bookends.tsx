import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from './Brand';
import {LightSweep, Particles, Vignette} from './Motion';

/**
 * Reusable channel BOOKENDS — the SAME opening + ending every episode (brand consistency,
 * decisions/0002 §G). Only the opening's episode title/subtitle changes; the end-card is fixed
 * (identical every episode). EP3+ import these as-is.
 */

const INK = BRAND.color.ink;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

export const OPENING_SEC = 3.5;
export const ENDCARD_SEC = 9;

/** Standard cinematic title opening: PD monogram + gold rule + series label / TITLE / subtitle. */
export const BrandOpening: React.FC<{seriesLabel: string; title: string; subtitle?: string}> = ({
  seriesLabel,
  title,
  subtitle,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const zoom = interpolate(frame, [0, durationInFrames], [1.04, 1.12]);
  const monoS = spring({frame: frame - Math.round(0.2 * fps), fps, config: {stiffness: 48, damping: 13, mass: 1.1}});
  const ruleW = interpolate(frame, [Math.round(0.9 * fps), Math.round(1.5 * fps)], [0, 520], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fadeIn = interpolate(frame, [0, Math.round(0.4 * fps)], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - Math.round(0.5 * fps), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const titleE = spring({frame: frame - Math.round(1.0 * fps), fps, config: {damping: 18, stiffness: 110}});
  return (
    <AbsoluteFill style={{backgroundColor: INK, opacity: Math.min(fadeIn, fadeOut)}}>
      <AbsoluteFill style={{overflow: 'hidden'}}>
        <Img src={staticFile('banner_sunrise.png')} style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 42%', transform: `scale(${zoom})`, transformOrigin: '50% 55%', filter: 'brightness(0.5) contrast(1.15) saturate(0.85)'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(to bottom, ${INK}B0 0%, ${INK}40 42%, ${INK}E6 100%)`}} />
      <LightSweep seed="opening" />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{transform: `translateY(${interpolate(monoS, [0, 1], [60, 0])}px)`, opacity: monoS, marginBottom: 8}}>
          <PdMonogram size={150} />
        </div>
        <div style={{width: ruleW, height: 2, background: GOLD, boxShadow: `0 0 16px 3px ${GOLD}99`, margin: '8px 0 22px'}} />
        <div style={{opacity: Math.min(titleE * 1.4, 1), transform: `translateY(${interpolate(titleE, [0, 1], [22, 0])}px)`, textAlign: 'center'}}>
          <div style={{color: SILVER, fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 24, letterSpacing: 6, textTransform: 'uppercase'}}>{seriesLabel}</div>
          <div style={{color: WHITE, fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 92, letterSpacing: -1, textTransform: 'uppercase', textShadow: `0 0 40px ${GOLD}55`, marginTop: 8}}>{title}</div>
          {subtitle ? <div style={{color: GOLD, fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 30, marginTop: 10}}>{subtitle}</div> : null}
        </div>
      </AbsoluteFill>
      <Particles count={16} seed="opening" color={GOLD} />
      <Vignette strength={1} />
    </AbsoluteFill>
  );
};

const Reveal: React.FC<{at: number; children: React.ReactNode; style?: React.CSSProperties}> = ({at, children, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - at, fps, config: {damping: 18, stiffness: 110, mass: 0.7}});
  return <div style={{transform: `translateY(${interpolate(e, [0, 1], [24, 0])}px)`, opacity: Math.min(e * 1.4, 1), ...style}}>{children}</div>;
};

/** Standard channel END-CARD — IDENTICAL every episode (brand sign-off + subscribe). */
export const BrandEndcard: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const out = interpolate(frame, [durationInFrames - 18, durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const monoS = spring({frame: frame - Math.round(0.2 * fps), fps, config: {stiffness: 48, damping: 13, mass: 1.1}});
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${BRAND.color.navy} 0%, ${INK} 82%)`, opacity: out}}>
      <Particles seed="endcard" count={18} color={GOLD} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{opacity: monoS, transform: `translateY(${interpolate(monoS, [0, 1], [40, 0])}px)`}}>
          <PdMonogram size={170} />
        </div>
        <Reveal at={Math.round(1.0 * fps)} style={{color: WHITE, fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 64, letterSpacing: 2, textTransform: 'uppercase', marginTop: 18, textShadow: `0 0 38px ${GOLD}55`}}>
          Prime Documentary
        </Reveal>
        <Reveal at={Math.round(1.8 * fps)} style={{color: GOLD, fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 32, marginTop: 14}}>
          ▶ Subscribe — Landmark Rights Cases
        </Reveal>
        <Reveal at={Math.round(2.5 * fps)} style={{color: SILVER, fontFamily: BRAND.font.body, fontSize: 26, marginTop: 8}}>
          New episodes every week
        </Reveal>
      </AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: '24%', height: 3, background: GOLD, opacity: 0.85, boxShadow: `0 0 16px 3px ${GOLD}77`}} />
      <Vignette strength={1} />
    </AbsoluteFill>
  );
};
