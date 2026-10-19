import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type LechThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  mode: 'hole' | 'numbers' | 'nothing';
  verified?: boolean;
  valueA?: string;
  valueB?: string;
};

export const LECH_THUMBS: LechThumbConcept[] = [
  {id: 'T1', headline: 'YOUR HOUSE. THEIR CALL.', hero: 'lech_dryrun/img/TH01_thumb_001.png', mode: 'hole'},
  {id: 'T2', headline: 'STOLEN VS DESTROYED', hero: 'lech_dryrun/img/TH02_thumb_002.png', mode: 'numbers', verified: false},
  {id: 'T3', headline: 'THEY PAID NOTHING', hero: 'lech_dryrun/img/TH03_thumb_003.png', mode: 'nothing'},
];

const GOLD = '#E5B53A';
const WHITE = '#F5F7FA';
const INK = '#090806';

const splitHeadline = (text: string) => {
  if (text.includes('. ')) return text.split('. ').map((x, i, a) => (i < a.length - 1 ? `${x}.` : x));
  const w = text.split(/\s+/);
  if (w.length <= 2) return [text];
  return [w.slice(0, Math.ceil(w.length / 2)).join(' '), w.slice(Math.ceil(w.length / 2)).join(' ')];
};

const StrokeText: React.FC<{children: string; gold?: boolean}> = ({children, gold}) => (
  <div
    style={{
      fontFamily: BRAND.font.display,
      fontSize: children.length > 12 ? 92 : 112,
      lineHeight: 0.92,
      color: gold ? GOLD : WHITE,
      WebkitTextStroke: '14px #000',
      paintOrder: 'stroke',
      textShadow: '0 8px 28px #000',
      letterSpacing: 0,
    }}
  >
    {children}
  </div>
);

export const LechThumbnail: React.FC<{concept: LechThumbConcept}> = ({concept}) => {
  const lines = splitHeadline(concept.headline);
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <Img
        src={staticFile(concept.hero)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: concept.mode === 'hole' ? 'translateX(190px) scale(1.06)' : 'scale(1.08)',
          filter: 'brightness(1.02) contrast(1.12) saturate(0.92)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(6,6,8,0.96) 0%, rgba(6,6,8,0.86) 36%, rgba(6,6,8,0.22) 67%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(42% 52% at 78% 45%, ${GOLD}44 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      <div style={{position: 'absolute', left: 48, top: 74, width: 560}}>
        {lines.map((line, i) => (
          <StrokeText key={line} gold={concept.mode === 'nothing' && line.includes('NOTHING')}>
            {line}
          </StrokeText>
        ))}
        <div style={{width: 360, height: 12, background: GOLD, marginTop: 22, boxShadow: `0 0 24px ${GOLD}`}} />
      </div>
      {concept.mode === 'numbers' && concept.verified && concept.valueA && concept.valueB && (
        <div style={{position: 'absolute', right: 54, top: 130, display: 'flex', alignItems: 'center', gap: 26, fontFamily: BRAND.font.display, WebkitTextStroke: '10px #000', paintOrder: 'stroke'}}>
          <span style={{color: WHITE, fontSize: 68}}>{concept.valueA}</span>
          <span style={{width: 4, height: 230, background: GOLD}} />
          <span style={{color: GOLD, fontSize: 130}}>{concept.valueB}</span>
        </div>
      )}
      <Grain opacity={0.11} />
    </AbsoluteFill>
  );
};
