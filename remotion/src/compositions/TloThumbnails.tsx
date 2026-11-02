import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type TloThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  mode: 'door' | 'ledger' | 'line';
};

// EP46 New Jersey v. T.L.O. (1985, 6-3): the 4th Amendment applies at school, but a school
// official needs only "reasonable suspicion" -- no warrant -- to search a student's belongings.
// CTR-max: <=3-4 huge words, second-person / curiosity-gap hook, symbolic faceless stills.
export const TLO_THUMBS: TloThumbConcept[] = [
  {id: '01', headline: 'SEARCHED AT SCHOOL', hero: 'tlo/img/S06.png', accentWord: 'SCHOOL', badge: 'NO WARRANT NEEDED', mode: 'line'},
  {id: '02', headline: 'THEY SEARCHED HER BAG', hero: 'tlo/img/S15.png', accentWord: 'HER BAG', badge: 'SUPREME COURT · 6-3', mode: 'ledger'},
  {id: '03', headline: "YOUR LOCKER ISN'T SAFE", hero: 'tlo/img/S08.png', accentWord: "ISN'T SAFE", badge: 'NO WARRANT NEEDED', mode: 'door'},
];

const ACCENT = '#3F8F5F'; // EP46 tlo lane color (schoolhouse green)
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

export const TloThumbnail: React.FC<{concept: TloThumbConcept}> = ({concept}) => {
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
