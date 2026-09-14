import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type GloverThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  mode: 'plate' | 'stop' | 'rule';
};

export const GLOVER_THUMBS: GloverThumbConcept[] = [
  {id: '01', headline: 'PULLED OVER WITHOUT A VIOLATION', hero: 'glover/img/S03.png', accentWord: 'WITHOUT', badge: 'KANSAS v. GLOVER', mode: 'plate'},
  {id: '02', headline: 'THE PLATE WAS ENOUGH', hero: 'glover/img/S06.png', accentWord: 'ENOUGH', badge: '8-1, BUT NARROW', mode: 'stop'},
  {id: '03', headline: 'WHO OWNS YOUR CAR?', hero: 'glover/img/S43.png', accentWord: 'YOUR', badge: 'REASONABLE SUSPICION', mode: 'rule'},
];

const ACCENT = '#5B8DB8';
const WHITE = '#F5F7FA';
const INK = '#0A0A0C';

const split = (text: string) => {
  const words = text.split(/\s+/);
  return [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')];
};

const StrokeText: React.FC<{line: string; accentWord?: string}> = ({line, accentWord}) => {
  const color = accentWord && line.includes(accentWord) ? ACCENT : WHITE;
  return (
    <div
      style={{
        fontFamily: BRAND.font.display,
        fontSize: line.length > 15 ? 80 : 104,
        lineHeight: 0.92,
        color,
        WebkitTextStroke: '13px #000',
        paintOrder: 'stroke',
        textShadow: '0 8px 30px #000',
        letterSpacing: 0,
      }}
    >
      {line}
    </div>
  );
};

export const GloverThumbnail: React.FC<{concept: GloverThumbConcept}> = ({concept}) => {
  const lines = split(concept.headline);
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
          transform: concept.mode === 'rule' ? 'scale(1.12)' : 'translateX(110px) scale(1.13)',
          filter: 'brightness(0.95) contrast(1.18) saturate(0.88)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.99) 0%, rgba(4,5,8,0.88) 42%, rgba(4,5,8,0.24) 72%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(46% 56% at 78% 46%, ${ACCENT}55 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      <div style={{position: 'absolute', left: 48, top: 66, width: 680}}>
        {lines.map((line) => (
          <StrokeText key={line} line={line} accentWord={concept.accentWord} />
        ))}
        <div style={{width: 360, height: 12, background: ACCENT, marginTop: 22, boxShadow: `0 0 24px ${ACCENT}`}} />
        {concept.badge && (
          <div style={{marginTop: 18, fontFamily: BRAND.font.body, fontSize: 30, color: '#D5DFEA', letterSpacing: 0, textTransform: 'uppercase'}}>
            {concept.badge}
          </div>
        )}
      </div>
      <Grain opacity={0.11} />
    </AbsoluteFill>
  );
};
