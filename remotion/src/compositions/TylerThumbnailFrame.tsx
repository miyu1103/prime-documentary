import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {PdMonogram} from '../components/Brand';

/**
 * TylerThumbnailFrame — EP33 "The $2,300 That Took a House" (Tyler v. Hennepin County).
 * CTR-first thumbnail in the PD house style (cf. KeloThumbnailFrame): a background
 * hero image + dark left scrim + big left headline (white over gold) + kicker +
 * badge + gold border + PD monogram.
 *
 * The Codex hero image is not generated yet (05_visuals empty), so `backgroundSrc`
 * is OPTIONAL: when absent, a self-contained ABSTRACT fallback (a dusk window +
 * door + red SEIZED stamp, all vector/gradient) renders so concepts are reviewable
 * NOW. When the Codex still lands, pass `backgroundSrc` to composite the real photo.
 * No real-person likeness in the fallback (invariant 11).
 *
 * The "え？なにそれ？" hook is the DISPROPORTION: a tiny $2,300 debt took the whole
 * home, and the county kept the surplus — all legal until a 9–0 ruling.
 */

type Variant = 'disproportion' | 'surplus' | 'legal';

type Props = {
  backgroundSrc?: string;
  variant?: Variant;
  headlineTop?: string;
  headlineBottom?: string;
  kicker?: string;
  badge?: string;
  bigNumber?: string;
};

const PRESET: Record<Variant, Required<Omit<Props, 'backgroundSrc'>>> = {
  // A — the disproportion (tiny debt → whole home). Strongest "wait, WHAT?".
  disproportion: {
    variant: 'disproportion',
    kicker: 'PROPERTY SEIZED',
    headlineTop: 'SHE OWED $2,300',
    headlineBottom: 'THEY TOOK HER HOME',
    badge: 'AND IT WAS LEGAL',
    bigNumber: '$2,300',
  },
  // B — the surplus theft (kept the change).
  surplus: {
    variant: 'surplus',
    kicker: 'THE STATE SOLD HER HOME',
    headlineTop: 'AND KEPT',
    headlineBottom: '$25,000',
    badge: 'HER MONEY — GONE',
    bigNumber: '',
  },
  // C — "they did nothing wrong" series framing.
  legal: {
    variant: 'legal',
    kicker: 'THEY DID NOTHING WRONG',
    headlineTop: 'A TAX BILL TOOK',
    headlineBottom: 'HER WHOLE HOUSE',
    badge: 'PROPERTY RIGHTS · PART 1',
    bigNumber: '',
  },
};

const {ink, navy, electric, silver, gold, white} = BRAND.color;

// self-contained abstract background: warm dusk window + door silhouette.
const FallbackScene: React.FC = () => (
  <AbsoluteFill>
    <AbsoluteFill style={{background: `radial-gradient(120% 120% at 78% 42%, ${navy} 0%, ${ink} 78%)`}} />
    {/* door slab (right-center) */}
    <div
      style={{
        position: 'absolute',
        right: 210,
        top: 96,
        width: 300,
        height: 560,
        background: `linear-gradient(180deg, #14100c 0%, #0b0a09 100%)`,
        borderLeft: `4px solid #221a12`,
        borderRight: `4px solid #060505`,
        boxShadow: `0 40px 120px #000A`,
      }}
    />
    {/* warm window on the door — a life still lit inside */}
    <div
      style={{
        position: 'absolute',
        right: 250,
        top: 150,
        width: 220,
        height: 250,
        background: `radial-gradient(80% 80% at 50% 40%, #f6c66a 0%, #b5792a 60%, #5a3a12 100%)`,
        boxShadow: `0 0 90px 24px #e0a24855`,
      }}
    />
    {/* muntin bars (window cross) */}
    <div style={{position: 'absolute', right: 358, top: 150, width: 4, height: 250, background: '#2018108c'}} />
    <div style={{position: 'absolute', right: 250, top: 270, width: 220, height: 4, background: '#2018108c'}} />
    {/* cool rim light from the left (the institution's cold) */}
    <AbsoluteFill style={{background: `linear-gradient(90deg, ${electric}10 0%, transparent 30%)`, mixBlendMode: 'screen'}} />
    {/* corner vignette */}
    <AbsoluteFill style={{boxShadow: `inset 0 0 260px 60px ${ink}`}} />
  </AbsoluteFill>
);

// red SEIZED stamp (rotated, distressed border) — the payoff mark.
const SeizedStamp: React.FC<{right: number; top: number; rot: number}> = ({right, top, rot}) => (
  <div
    style={{
      position: 'absolute',
      right,
      top,
      transform: `rotate(${rot}deg)`,
      color: '#e23b34',
      border: '7px solid #e23b34',
      borderRadius: 8,
      padding: '8px 24px',
      fontFamily: BRAND.font.display,
      fontWeight: 900,
      fontSize: 76,
      letterSpacing: 6,
      textShadow: `3px 3px 0 #3a0a08`,
      boxShadow: `0 0 0 3px #3a0a0855, 6px 8px 24px #000A`,
      opacity: 0.96,
    }}
  >
    SEIZED
  </div>
);

export const TylerThumbnailFrame: React.FC<Props> = (props) => {
  const v = props.variant ?? 'disproportion';
  const p = {...PRESET[v], ...props};
  const bottomColor = v === 'surplus' ? gold : v === 'legal' ? white : gold;

  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      {p.backgroundSrc ? (
        <Img
          src={staticFile(p.backgroundSrc)}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: '63% 55%',
            transform: 'scale(1.22)',
            filter: 'brightness(1.18) contrast(1.12) saturate(1.12)',
          }}
        />
      ) : (
        <FallbackScene />
      )}

      {/* left scrim so the headline reads over any background */}
      <AbsoluteFill
        style={{
          background:
            `linear-gradient(90deg, ${ink}F4 0%, ${ink}DC 34%, ${ink}55 62%, transparent 100%), ` +
            `linear-gradient(0deg, ${ink}B8 0%, transparent 32%, transparent 100%)`,
        }}
      />

      {/* gold frame */}
      <div style={{position: 'absolute', inset: 0, border: `3px solid ${gold}`}} />

      {/* kicker (top-left, electric) + underline */}
      <div style={{position: 'absolute', left: 52, top: 50, fontFamily: BRAND.font.body, fontSize: 32, color: electric, fontWeight: 900, letterSpacing: 0.5, textTransform: 'uppercase'}}>
        {p.kicker}
      </div>
      <div style={{position: 'absolute', left: 52, top: 98, width: 330, height: 10, background: gold}} />

      {/* headline (white over accent), big display */}
      <div
        style={{
          position: 'absolute',
          left: 50,
          top: 156,
          width: 900,
          fontFamily: BRAND.font.display,
          fontWeight: 900,
          fontSize: 108,
          lineHeight: 0.92,
          letterSpacing: 0,
          textTransform: 'uppercase',
          textShadow: `7px 8px 0 ${ink}, 0 0 26px ${ink}`,
        }}
      >
        <div style={{color: white}}>{p.headlineTop}</div>
        <div style={{color: bottomColor}}>{p.headlineBottom}</div>
      </div>

      {/* badge */}
      <div
        style={{
          position: 'absolute',
          left: 54,
          top: 486,
          border: `2px solid ${gold}`,
          color: silver,
          background: `${ink}D8`,
          fontFamily: BRAND.font.body,
          fontSize: 31,
          fontWeight: 900,
          padding: '12px 20px',
          letterSpacing: 0.5,
        }}
      >
        {p.badge}
      </div>

      {/* SEIZED stamp over the door, BELOW the headline so key words stay legible */}
      {v !== 'surplus' && <SeizedStamp right={170} top={402} rot={-13} />}

      {/* footer + monogram */}
      <div style={{position: 'absolute', left: 56, bottom: 44, fontFamily: BRAND.font.body, color: silver, fontSize: 24, fontWeight: 900, letterSpacing: 1}}>
        PRIME DOCUMENTARY
      </div>
      <div style={{position: 'absolute', right: 40, bottom: 30}}>
        <PdMonogram size={84} />
      </div>
    </AbsoluteFill>
  );
};
