import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type ClevelandThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  mode: 'door' | 'ledger' | 'line';
};

export const CLEV_THUMBS: ClevelandThumbConcept[] = [
  {id: '01', headline: 'JAILED FOR BEING POOR', hero: 'cleveland/img/S68.png', accentWord: 'POOR', badge: 'NO ABILITY-TO-PAY HEARING', mode: 'door'},
  {id: '02', headline: 'THE $1,554 TRAP', hero: 'cleveland/img/S25.png', accentWord: '$1,554', badge: 'OR 31 DAYS - PER FFJC', mode: 'ledger'},
  {id: '03', headline: '1983 RULE IGNORED', hero: 'cleveland/img/S46.png', accentWord: '1983', badge: 'BEARDEN HELD; ENFORCEMENT FAILED', mode: 'line'},
];

const ACCENT = '#B43A3A';
const WHITE = '#F5F7FA';
const INK = '#0A0A0C';

const split = (text: string) => {
  const words = text.split(/\s+/);
  if (words.length <= 2) return [text];
  if (text.includes('. ')) return text.split('. ');
  return [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')];
};

const StrokeText: React.FC<{line: string; accentWord?: string}> = ({line, accentWord}) => {
  const color = accentWord && line.includes(accentWord) ? ACCENT : WHITE;
  return (
    <div
      style={{
        fontFamily: BRAND.font.display,
        fontSize: line.length > 13 ? 88 : 110,
        lineHeight: 0.92,
        color,
        WebkitTextStroke: '14px #000',
        paintOrder: 'stroke',
        textShadow: '0 8px 28px #000',
        letterSpacing: 0,
      }}
    >
      {line}
    </div>
  );
};

export const ClevelandThumbnail: React.FC<{concept: ClevelandThumbConcept}> = ({concept}) => {
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
          transform: concept.mode === 'door' ? 'translateX(120px) scale(1.1)' : 'scale(1.1)',
          filter: 'brightness(0.92) contrast(1.22) saturate(0.82)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.98) 0%, rgba(4,5,8,0.88) 39%, rgba(4,5,8,0.25) 70%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(42% 52% at 78% 45%, ${ACCENT}44 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      {concept.mode === 'ledger' && (
        <div
          style={{
            position: 'absolute',
            right: 82,
            bottom: 58,
            width: 320,
            height: 210,
            border: `5px solid ${ACCENT}`,
            boxShadow: '0 12px 38px #000',
            background: 'rgba(8,8,10,0.55)',
          }}
        />
      )}
      {concept.mode === 'line' && (
        <div
          style={{
            position: 'absolute',
            right: 92,
            top: 116,
            width: 6,
            height: 460,
            background: ACCENT,
            boxShadow: `0 0 28px ${ACCENT}`,
          }}
        />
      )}
      <div style={{position: 'absolute', left: 48, top: 74, width: 610}}>
        {lines.map((line) => (
          <StrokeText key={line} line={line} accentWord={concept.accentWord} />
        ))}
        <div style={{width: 360, height: 12, background: ACCENT, marginTop: 22, boxShadow: `0 0 24px ${ACCENT}`}} />
        {concept.badge && (
          <div style={{marginTop: 18, fontFamily: BRAND.font.body, fontSize: 30, color: '#C8CDD6', letterSpacing: 0, textTransform: 'uppercase'}}>
            {concept.badge}
          </div>
        )}
      </div>
      <Grain opacity={0.11} />
    </AbsoluteFill>
  );
};


