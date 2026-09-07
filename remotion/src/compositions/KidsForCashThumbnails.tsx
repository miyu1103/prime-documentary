import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';

/**
 * EP38 "kidsforcash" — the Luzerne County "Kids for Cash" scandal (two Pennsylvania
 * judges took ~$2.8 million to funnel juveniles into for-profit detention centers).
 * 派手 (bold/loud) max-CTR thumbnail set.
 *
 * House style: identical construction to RolinThumbnails / CarsearchThumbnails
 * (deep-navy field, one bright hero still, ONE brand accent, huge second-person /
 * declarative UPPERCASE hook, extra-thick black stroke on every glyph, red urgency
 * burst behind the hero). Reuses that proven, gate-passing layout verbatim; only the
 * hero art + copy differ.
 *
 * Constraints honored:
 *  - Heroes are AI key-art only (symbolic reconstruction; no on-image text/logos and
 *    no real-person likeness — invariant 11 / no-real-face). S16's subject is shot
 *    from behind (no face). Headline is composited here in Remotion.
 *  - Fact-safe copy: only the confirmed total kickback figure "$2.8 MILLION" is shown,
 *    and only on the concept sourced to that claim; no fabricated per-child figure.
 *  - luma_mean kept up: hero graded bright, red burst + bright accent line add
 *    luminance; only the LEFT third is scrimmed for the headline.
 *  - ONE urgency red (#E5202A, the only hardcoded hex) + ONE brand accent per thumb.
 *
 * Pure, deterministic component. Rendered via <Still id="Thumb-kidsforcash-01".../>
 * in Root.tsx (see KIDSFORCASH_THUMBS below).
 */

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

/** The single 派手 CTR urgency accent (only hardcoded hex). */
const URGENCY_RED = '#E5202A';

export type ThumbAccent = 'blue' | 'gold';

export type ThumbConcept = {
  /** stable option id (thumb01..thumb03). */
  id: string;
  /** UPPERCASE, <= 4 words. Final line renders in the brand accent. */
  headline: string;
  /** small gold/blue kicker above the headline. */
  kicker: string;
  /** staticFile-relative path to the graded hero key-art (no on-image text). */
  hero: string;
  /** ONE brand accent per thumb (electric blue or gold). */
  accent: ThumbAccent;
};

/**
 * The 3 planned concepts. Hero stills are the episode's 4K key-arts:
 *   thumb01 -> S08  child-figurines tagged with gold price tags on a conveyor toward a
 *                   prison gate (the literal "kids for cash" metaphor). SELECTED.
 *   thumb02 -> S16  a handcuffed man (shot from behind, no face) perp-walked up
 *                   courthouse steps past press lights (the judge arrested).
 *   thumb03 -> S05  a floodlit detention facility behind razor wire at dusk.
 * Fact-safe: the amount "$2.8 MILLION" only appears on thumb03, whose source claim is
 * the confirmed total kickback sum; the others carry no figure.
 */
export const KIDSFORCASH_THUMBS: ThumbConcept[] = [
  {
    id: 'thumb01',
    headline: 'SOLD FOR CASH',
    kicker: 'THE KIDS-FOR-CASH SCANDAL',
    hero: 'kidsforcash/img/kfc_S08.png',
    accent: 'gold',
  },
  {
    id: 'thumb02',
    headline: 'JAILED FOR CASH',
    kicker: "A JUDGE'S SECRET DEAL",
    hero: 'kidsforcash/img/kfc_S16.png',
    accent: 'blue',
  },
  {
    id: 'thumb03',
    headline: '$2.8 MILLION',
    kicker: 'TO JAIL CHILDREN',
    hero: 'kidsforcash/img/kfc_S05.png',
    accent: 'gold',
  },
];

/** Break a short hook into 1-2 balanced lines; last line takes the accent color. */
const splitHeadline = (headline: string): string[] => {
  const words = headline.trim().split(/\s+/);
  if (words.length === 1) return words;
  if (words.length === 2) return headline.length <= 9 ? [headline] : words;
  if (words.length === 3) return [words.slice(0, 2).join(' '), words.slice(2).join(' ')];
  const midpoint = Math.ceil(words.length / 2);
  return [words.slice(0, midpoint).join(' '), words.slice(midpoint).join(' ')];
};

/**
 * Red urgency burst — radiating rays + a hot core behind the hero, on the right
 * (hero) side of the frame. Adds alarm and luminance; the 派手 CTR accent.
 */
const UrgencyBurst: React.FC = () => (
  <svg width="1280" height="720" viewBox="0 0 1280 720" style={{position: 'absolute', inset: 0}}>
    <defs>
      <radialGradient id="kfcBurstCore" cx="50%" cy="50%" r="50%">
        <stop offset="0" stopColor={URGENCY_RED} stopOpacity="0.85" />
        <stop offset="0.45" stopColor={URGENCY_RED} stopOpacity="0.34" />
        <stop offset="1" stopColor={URGENCY_RED} stopOpacity="0" />
      </radialGradient>
    </defs>
    <g transform="translate(998 346)" opacity="0.72">
      {Array.from({length: 16}, (_, i) => {
        const a = (i * Math.PI * 2) / 16;
        const inner = 70;
        const outer = 820;
        const spread = 0.13;
        const x1 = Math.cos(a) * inner;
        const y1 = Math.sin(a) * inner;
        const x2 = Math.cos(a - spread) * outer;
        const y2 = Math.sin(a - spread) * outer;
        const x3 = Math.cos(a + spread) * outer;
        const y3 = Math.sin(a + spread) * outer;
        return (
          <polygon
            key={i}
            points={`${x1},${y1} ${x2},${y2} ${x3},${y3}`}
            fill={URGENCY_RED}
            opacity={i % 2 === 0 ? 0.3 : 0.14}
          />
        );
      })}
    </g>
    <ellipse cx="998" cy="346" rx="470" ry="470" fill="url(#kfcBurstCore)" />
  </svg>
);

/**
 * Bright-line motif — the show's signature glowing diagonal blade of light in the
 * brand accent (the line the children never got to cross). On thumb01 it is the full
 * hero barrier; on the others a seeded accent along the lower edge.
 */
const BrightLine: React.FC<{accent: string; hero: boolean}> = ({accent, hero}) => (
  <svg width="1280" height="720" viewBox="0 0 1280 720" style={{position: 'absolute', inset: 0}}>
    <defs>
      <filter id="kfcLineGlow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation={hero ? 16 : 9} result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
    {hero ? (
      <g>
        <line x1="470" y1="726" x2="1180" y2="150" stroke={accent} strokeWidth="46" strokeLinecap="round" opacity="0.22" filter="url(#kfcLineGlow)" />
        <line x1="470" y1="726" x2="1180" y2="150" stroke={WHITE} strokeWidth="9" strokeLinecap="round" opacity="0.95" filter="url(#kfcLineGlow)" />
        <line x1="470" y1="726" x2="1180" y2="150" stroke={accent} strokeWidth="18" strokeLinecap="round" opacity="0.85" />
        <circle cx="822" cy="440" r="34" fill={WHITE} opacity="0.9" filter="url(#kfcLineGlow)" />
        <circle cx="822" cy="440" r="64" fill="none" stroke={accent} strokeWidth="6" opacity="0.6" />
      </g>
    ) : (
      <g opacity="0.85">
        <line x1="60" y1="686" x2="1220" y2="632" stroke={accent} strokeWidth="7" strokeLinecap="round" filter="url(#kfcLineGlow)" />
        <line x1="60" y1="686" x2="1220" y2="632" stroke={accent} strokeWidth="20" strokeLinecap="round" opacity="0.16" filter="url(#kfcLineGlow)" />
      </g>
    )}
  </svg>
);

/**
 * One headline line with the extra-thick black stroke (特大黒縁). The stroke is
 * painted under the fill (paintOrder: 'stroke') and reinforced with a stacked shadow
 * so the type survives on any hero at 320px width.
 */
const StrokedLine: React.FC<{text: string; color: string; size: number}> = ({text, color, size}) => (
  <div
    style={{
      fontFamily: BRAND.font.display,
      fontSize: size,
      lineHeight: 0.9,
      color,
      textTransform: 'uppercase',
      letterSpacing: 0,
      WebkitTextStroke: '16px #000',
      paintOrder: 'stroke',
      textShadow:
        '0 0 2px #000, 0 6px 22px #000, 0 3px 0 #000, 0 -3px 0 #000, 3px 0 0 #000, -3px 0 0 #000',
    }}
  >
    {text}
  </div>
);

export const KidsForCashThumbnail: React.FC<{concept: ThumbConcept}> = ({concept}) => {
  const accent = concept.accent === 'gold' ? GOLD : BLUE;
  const heroLine = concept.id === 'thumb01';
  const lines = splitHeadline(concept.headline);
  const longest = Math.max(...lines.map((l) => l.length));
  const primarySize = longest > 12 ? 108 : 132;

  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {/* Hero key-art — graded bright toward navy; kept luminous (luma_mean up). */}
      <Img
        src={staticFile(concept.hero)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: 'scale(1.08)',
          filter: 'brightness(1.12) contrast(1.14) saturate(1.4)',
        }}
      />
      {/* Navy grade + LEFT-only scrim for headline contrast (right/hero side stays bright). */}
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${NAVY}f2 0%, ${NAVY}cc 34%, #00000022 62%, #00000000 100%)`}} />
      <AbsoluteFill style={{background: 'linear-gradient(0deg, #00000066 0%, #00000000 34%)'}} />

      {/* Red urgency burst behind the hero, then the brand bright-line motif. */}
      <UrgencyBurst />
      <BrightLine accent={accent} hero={heroLine} />

      {/* 派手 accent glow pooled behind the headline so the type reads as lit, not flat. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `radial-gradient(46% 42% at 26% 40%, ${accent}3a 0%, ${accent}12 40%, transparent 72%)`,
          mixBlendMode: 'screen',
        }}
      />

      {/* Hook headline block, upper-left over the scrim. */}
      <div style={{position: 'absolute', left: 54, top: 58, width: 720}}>
        <div style={{fontFamily: BRAND.font.body, fontSize: 30, fontWeight: 900, color: accent, textShadow: '0 2px 8px #000', letterSpacing: 1}}>
          {concept.kicker}
        </div>
        <div style={{height: 8, width: 320, background: accent, marginTop: 16, marginBottom: 30, boxShadow: '0 2px 10px #000'}} />
        {lines.map((line, i) => (
          <StrokedLine
            key={`${concept.id}-${i}`}
            text={line}
            color={i === lines.length - 1 ? accent : WHITE}
            size={i === 0 ? primarySize : Math.max(96, primarySize - 12)}
          />
        ))}
      </div>

      {/* Honesty + brand footer (illustration / reconstruction, not authentic footage). */}
      <div style={{position: 'absolute', right: 34, top: 26, fontFamily: BRAND.font.body, fontSize: 15, color: SILVER, border: `1px solid ${GOLD}99`, background: '#000000aa', padding: '5px 9px', letterSpacing: 0}}>
        symbolic reconstruction
      </div>
      <div style={{position: 'absolute', left: 58, bottom: 40, fontFamily: BRAND.font.body, fontSize: 22, color: SILVER, fontWeight: 900, letterSpacing: 1, textShadow: '0 2px 8px #000'}}>
        PRIME DOCUMENTARY
      </div>

      <Vignette strength={0.8} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};
