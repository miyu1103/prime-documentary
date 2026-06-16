import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';

/**
 * Click-first thumbnail concepts for the Miranda episode: one bold curiosity-gap
 * line, a single symbol, brand colours, mobile-legible. Rendered as a <Still>;
 * A/B/C concepts are produced by overriding props. Title text stays *complementary*
 * to the video title (the thumbnail carries the surprise, the title the recognition).
 */

const S = BRAND.color;

const Bars: React.FC = () => (
  <svg width="520" height="520" viewBox="0 0 400 400">
    <polygon points="120,0 280,0 372,400 28,400" fill={S.gold} opacity="0.14" />
    {[70, 130, 190, 250, 310].map((x) => (
      <rect key={x} x={x} y="30" width="16" height="350" rx="6" fill={S.silver} opacity="0.85" />
    ))}
    {[70, 130, 190, 250, 310].map((x) => (
      <rect key={`g${x}`} x={x} y="30" width="16" height="350" rx="6" fill={S.electric} opacity="0.18" />
    ))}
  </svg>
);

const Gavel: React.FC = () => (
  <svg width="540" height="420" viewBox="0 0 400 300">
    <g transform="rotate(-22 200 150)">
      <rect x="60" y="120" width="280" height="44" rx="14" fill={S.gold} />
      <rect x="170" y="70" width="78" height="78" rx="14" fill={S.gold} />
    </g>
    <rect x="120" y="240" width="160" height="22" rx="11" fill={S.silver} opacity="0.6" />
    <circle cx="200" cy="252" r="64" fill="none" stroke={S.gold} strokeWidth="4" opacity="0.5" />
  </svg>
);

const Scales: React.FC = () => (
  <svg width="520" height="460" viewBox="0 0 360 320" stroke={S.gold} strokeWidth="7" fill="none">
    <line x1="180" y1="36" x2="180" y2="250" />
    <g transform="rotate(10 180 90)">
      <line x1="70" y1="90" x2="290" y2="90" />
      <path d="M70 90 l-40 76 a40 22 0 0 0 80 0 z" fill={`${S.electric}33`} />
      <path d="M290 90 l-40 92 a40 22 0 0 0 80 0 z" fill={`${S.electric}33`} />
    </g>
    <rect x="130" y="250" width="100" height="18" rx="9" fill={S.gold} />
  </svg>
);

/** A handwritten letter sheet with a pencil — the icon of the Gideon story. */
const Letter: React.FC = () => (
  <svg width="520" height="520" viewBox="0 0 420 420">
    <g transform="rotate(-8 210 210)">
      <rect x="90" y="60" width="240" height="300" rx="8" fill={`${S.silver}1a`} stroke={S.silver} strokeWidth="4" />
      {[110, 145, 180, 215, 250, 285].map((y) => (
        <rect key={y} x="120" y={y} width={y % 2 ? 150 : 180} height="7" rx="3" fill={`${S.silver}99`} />
      ))}
    </g>
    {/* pencil */}
    <g transform="rotate(38 300 300)">
      <rect x="285" y="120" width="26" height="240" fill={S.gold} />
      <polygon points="285,360 311,360 298,400" fill={S.silver} />
      <polygon points="290,392 306,392 298,408" fill={S.ink} />
      <rect x="285" y="120" width="26" height="26" fill={`${S.electric}`} />
    </g>
  </svg>
);

const SYM: Record<string, React.FC> = {gavel: Gavel, bars: Bars, scales: Scales, letter: Letter};

export type ThumbConceptProps = {
  kicker?: string;
  line1: string;
  line2: string;
  sub?: string;
  symbol: 'gavel' | 'bars' | 'scales' | 'letter';
  /** Optional real background still (Midjourney) — static path or http; falls back to gradient.
   *  When supplied, the coded symbol is hidden by default (the photo is the visual). */
  backgroundSrc?: string | null;
  showSymbol?: boolean;
};

export const ThumbConcept: React.FC<ThumbConceptProps> = ({
  kicker,
  line1,
  line2,
  sub,
  symbol,
  backgroundSrc = null,
  showSymbol,
}) => {
  const Sym = SYM[symbol] ?? Gavel;
  const symbolVisible = showSymbol ?? !backgroundSrc;
  return (
    <AbsoluteFill style={{backgroundColor: S.ink}}>
      {backgroundSrc ? (
        <Img
          src={backgroundSrc.startsWith('http') ? backgroundSrc : staticFile(backgroundSrc)}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      ) : (
        <AbsoluteFill
          style={{background: `radial-gradient(120% 100% at 78% 38%, ${S.navy} 0%, ${S.ink} 78%)`}}
        />
      )}
      {/* symbol, right side (hidden when a real background is provided) */}
      {symbolVisible ? (
        <div style={{position: 'absolute', right: 24, top: '50%', transform: 'translateY(-50%)', opacity: 0.92}}>
          <Sym />
        </div>
      ) : null}
      {/* left scrim for text legibility */}
      <AbsoluteFill
        style={{background: `linear-gradient(90deg, ${S.ink}F2 0%, ${S.ink}C0 46%, transparent 72%)`}}
      />
      {/* gold horizon line */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 92, height: 5, background: S.gold, opacity: 0.85}} />
      {/* text block */}
      <AbsoluteFill style={{padding: 64, justifyContent: 'center', alignItems: 'flex-start'}}>
        {kicker ? (
          <div
            style={{
              color: S.silver,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 30,
              letterSpacing: 3,
              textTransform: 'uppercase',
              marginBottom: 14,
            }}
          >
            {kicker}
          </div>
        ) : null}
        <div
          style={{
            color: S.white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 118,
            lineHeight: 0.96,
            letterSpacing: -2,
            textTransform: 'uppercase',
            textShadow: `0 6px 28px ${S.ink}`,
            maxWidth: '74%',
          }}
        >
          {line1}
        </div>
        <div
          style={{
            color: S.gold,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 118,
            lineHeight: 0.96,
            letterSpacing: -2,
            textTransform: 'uppercase',
            textShadow: `0 6px 28px ${S.ink}`,
            maxWidth: '76%',
          }}
        >
          {line2}
        </div>
        {sub ? (
          <div
            style={{
              color: S.white,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 34,
              marginTop: 18,
              opacity: 0.9,
              maxWidth: '70%',
            }}
          >
            {sub}
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
