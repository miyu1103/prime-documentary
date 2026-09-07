import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type CentralparkThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  align: 'chair' | 'rec' | 'dna';
};

export const CENTRALPARK_THUMBS: CentralparkThumbConcept[] = [
  {
    id: '01',
    headline: 'NO CAMERA. NO MATCH.',
    hero: 'centralpark/img/S001.png',
    accentWord: 'NO MATCH.',
    badge: 'THE EXONERATED FIVE',
    align: 'chair',
  },
  {
    id: '02',
    headline: 'THE CONFESSION WAS WRONG',
    hero: 'centralpark/img/S018.png',
    accentWord: 'WRONG',
    badge: 'DNA TOLD THE TRUTH',
    align: 'rec',
  },
  {
    id: '03',
    headline: 'FIVE CHILDREN. ZERO DNA.',
    hero: 'centralpark/img/S268.png',
    accentWord: 'ZERO DNA.',
    badge: '1989 TO 2002',
    align: 'dna',
  },
];

const ACCENT = '#2F9FC4';
const WHITE = '#F5F7FA';
const INK = '#0A0A0C';

const split = (text: string) => {
  const words = text.split(/\s+/);
  if (words.length <= 3) return [text];
  return [words.slice(0, Math.ceil(words.length / 2)).join(' '), words.slice(Math.ceil(words.length / 2)).join(' ')];
};

const StrokeText: React.FC<{line: string; accentWord?: string}> = ({line, accentWord}) => {
  const color = accentWord && line.includes(accentWord) ? ACCENT : WHITE;
  return (
    <div
      style={{
        fontFamily: BRAND.font.display,
        fontSize: line.length > 15 ? 82 : 102,
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

export const CentralparkThumbnail: React.FC<{concept: CentralparkThumbConcept}> = ({concept}) => {
  const lines = split(concept.headline);
  const transform =
    concept.align === 'dna'
      ? 'translateX(170px) scale(1.14)'
      : concept.align === 'rec'
        ? 'translateX(120px) scale(1.12)'
        : 'translateX(90px) scale(1.12)';
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
          transform,
          filter: 'brightness(0.82) contrast(1.26) saturate(0.9)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.99) 0%, rgba(4,5,8,0.9) 43%, rgba(4,5,8,0.34) 70%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(42% 52% at 78% 45%, ${ACCENT}55 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      <div style={{position: 'absolute', left: 44, top: 66, width: 700}}>
        {lines.map((line) => (
          <StrokeText key={line} line={line} accentWord={concept.accentWord} />
        ))}
        <div style={{width: 390, height: 12, background: ACCENT, marginTop: 22, boxShadow: `0 0 24px ${ACCENT}`}} />
        {concept.badge && (
          <div style={{marginTop: 18, fontFamily: BRAND.font.body, fontSize: 29, color: '#C8CDD6', letterSpacing: 0, textTransform: 'uppercase'}}>
            {concept.badge}
          </div>
        )}
      </div>
      <Grain opacity={0.12} />
    </AbsoluteFill>
  );
};
