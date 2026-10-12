import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type StrieffThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  mode: 'door' | 'warrant' | 'vote';
};

export const STRIEFF_THUMBS: StrieffThumbConcept[] = [
  {id: '01', headline: 'THE SEARCH STILL COUNTED', hero: 'strieff/img/S01.png', accentWord: 'COUNTED', badge: 'UTAH v. STRIEFF', mode: 'door'},
  {id: '02', headline: 'THE WARRANT BROKE THE CHAIN', hero: 'strieff/img/S15.png', accentWord: 'WARRANT', badge: 'ATTENUATION', mode: 'warrant'},
  {id: '03', headline: '5 TO 3 AFTER AN ILLEGAL STOP', hero: 'strieff/thumbs/thumb03_court_empty_seat.v001.png', accentWord: '5 TO 3', badge: 'SCALIA SEAT EMPTY', mode: 'vote'},
];

const ACCENT = '#9C6BAA';
const WHITE = '#F5F7FA';
const INK = '#0A0A0C';

const split = (text: string) => {
  const words = text.split(/\s+/);
  if (text.includes('5 TO 3')) return ['5 TO 3', 'AFTER AN ILLEGAL STOP'];
  return [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')];
};

const StrokeText: React.FC<{line: string; accentWord?: string}> = ({line, accentWord}) => {
  const active = accentWord && line.includes(accentWord);
  return (
    <div
      style={{
        fontFamily: BRAND.font.display,
        fontSize: line.length > 17 ? 78 : 100,
        lineHeight: 0.92,
        color: active ? ACCENT : WHITE,
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

export const StrieffThumbnail: React.FC<{concept: StrieffThumbConcept}> = ({concept}) => {
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
          transform: concept.mode === 'door' ? 'translateX(120px) scale(1.12)' : concept.mode === 'vote' ? 'scale(1.16)' : 'translateX(80px) scale(1.13)',
          filter: 'brightness(1.02) contrast(1.2) saturate(0.86)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.99) 0%, rgba(4,5,8,0.88) 40%, rgba(4,5,8,0.24) 72%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(46% 56% at 78% 46%, ${ACCENT}66 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      <div style={{position: 'absolute', left: 48, top: 70, width: 650}}>
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
