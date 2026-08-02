import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type YoungThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  mode: 'door' | 'vote' | 'check';
};

export const YOUNG_THUMBS: YoungThumbConcept[] = [
  {id: '01', headline: 'THE WRONG HOUSE', hero: 'young_dryrun/img/TH01_thumb_001.png', accentWord: 'WRONG', mode: 'door'},
  {id: '02', headline: '5-4 STILL A COMMAND', hero: 'young_dryrun/img/TH02_thumb_002.png', accentWord: '5-4', mode: 'vote'},
  {id: '03', headline: 'PAID. NOT ANSWERED.', hero: 'young_dryrun/img/TH03_thumb_003.png', accentWord: 'NOT', mode: 'check'},
];

const ACCENT = '#3B7DD8';
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

export const YoungThumbnail: React.FC<{concept: YoungThumbConcept}> = ({concept}) => {
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
          transform: concept.mode === 'door' ? 'translateX(180px) scale(1.08)' : 'scale(1.08)',
          filter: 'brightness(0.98) contrast(1.18) saturate(0.9)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.96) 0%, rgba(4,5,8,0.84) 36%, rgba(4,5,8,0.22) 68%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(42% 52% at 78% 45%, ${ACCENT}44 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      <div style={{position: 'absolute', left: 48, top: 74, width: 610}}>
        {lines.map((line) => (
          <StrokeText key={line} line={line} accentWord={concept.accentWord} />
        ))}
        <div style={{width: 360, height: 12, background: ACCENT, marginTop: 22, boxShadow: `0 0 24px ${ACCENT}`}} />
      </div>
      {concept.mode === 'vote' && (
        <div style={{position: 'absolute', right: 62, top: 134, fontFamily: BRAND.font.display, fontSize: 170, color: ACCENT, WebkitTextStroke: '16px #000', paintOrder: 'stroke', textShadow: '0 10px 30px #000'}}>
          5-4
        </div>
      )}
      <Grain opacity={0.11} />
    </AbsoluteFill>
  );
};
