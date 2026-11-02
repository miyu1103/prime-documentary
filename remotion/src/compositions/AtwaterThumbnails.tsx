import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';

export type AtwaterThumbConcept = {
  id: string;
  headline: string;
  hero: string;
  accentWord?: string;
  badge?: string;
  mode: 'seatbelt' | 'cuffs' | 'court';
};

// EP47 Atwater v. Lago Vista — jailed over a $50 seatbelt fine; SCOTUS 5-4 (2001) upheld the
// warrantless arrest for a fine-only offense. CTR-max: HUGE <=4-word hooks, violet keyword pop.
// R2: symbolic stills only — a seatbelt buckle, isolated handcuffs, marble/dome — no faces, no people.
export const ATWATER_THUMBS: AtwaterThumbConcept[] = [
  {id: '01', headline: 'JAILED OVER A SEATBELT', hero: 'atwater/img/S53.png', accentWord: 'SEATBELT', badge: 'ATWATER v. LAGO VISTA', mode: 'seatbelt'},
  {id: '02', headline: 'HANDCUFFED FOR $50', hero: 'atwater/img/S54.png', accentWord: '$50', badge: 'A FINE-ONLY OFFENSE', mode: 'cuffs'},
  {id: '03', headline: "THE COURT SAID IT'S LEGAL", hero: 'atwater/img/S57.png', accentWord: "IT'S LEGAL", badge: 'SUPREME COURT · 5-4 · 2001', mode: 'court'},
];

const ACCENT = '#7A5CD0';
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

export const AtwaterThumbnail: React.FC<{concept: AtwaterThumbConcept}> = ({concept}) => {
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
          transform: concept.mode === 'cuffs' ? 'translateX(120px) scale(1.1)' : 'scale(1.08)',
          filter: 'brightness(0.95) contrast(1.2) saturate(0.9)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(4,5,8,0.98) 0%, rgba(4,5,8,0.88) 39%, rgba(4,5,8,0.25) 70%, transparent 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(42% 52% at 78% 45%, ${ACCENT}44 0%, transparent 70%)`, mixBlendMode: 'screen'}} />
      {concept.mode === 'court' && (
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
