import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type ThumbVariant = {
  id: string;
  headline: string;
  kicker: string;
  image: string;
  motif: 'search' | 'warrant' | 'police' | 'life' | 'locked';
  accent: 'blue' | 'gold';
};

export const rileyThumbnailVariants: ThumbVariant[] = [
  {
    id: 'thumb01',
    headline: 'SEARCHED?',
    kicker: 'YOUR PHONE',
    image: 'riley/PD-2026-007-S001-IMG-001.v001.png',
    motif: 'search',
    accent: 'gold',
  },
  {
    id: 'thumb02',
    headline: 'GET A WARRANT',
    kicker: 'PHONE SEARCH',
    image: 'riley/PD-2026-007-S025-IMG-001.v001.png',
    motif: 'warrant',
    accent: 'gold',
  },
  {
    id: 'thumb03',
    headline: 'NO WARRANT?',
    kicker: 'POLICE + PHONE',
    image: 'riley/PD-2026-007-S003-IMG-001.v001.png',
    motif: 'police',
    accent: 'blue',
  },
  {
    id: 'thumb04',
    headline: 'YOUR PHONE IS YOUR LIFE',
    kicker: 'RILEY v. CALIFORNIA',
    image: 'riley/PD-2026-007-S015-IMG-001.v001.png',
    motif: 'life',
    accent: 'gold',
  },
  {
    id: 'thumb05',
    headline: 'CAN POLICE OPEN THIS?',
    kicker: 'LOCKED PHONE',
    image: 'riley/PD-2026-007-S005-IMG-001.v001.png',
    motif: 'locked',
    accent: 'blue',
  },
];

const splitHeadline = (headline: string): string[] => {
  if (headline.length <= 13) return [headline];
  const words = headline.split(' ');
  if (words.length <= 3) return [words.slice(0, 1).join(' '), words.slice(1).join(' ')];
  const midpoint = Math.ceil(words.length / 2);
  return [words.slice(0, midpoint).join(' '), words.slice(midpoint).join(' ')];
};

const PhoneIcon: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <defs>
      <filter id="rileyThumbGlow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="12" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <radialGradient id="rileyPhoneGlow" cx="52%" cy="45%" r="58%">
        <stop offset="0" stopColor={BLUE} stopOpacity="0.92" />
        <stop offset="0.45" stopColor={BLUE} stopOpacity="0.22" />
        <stop offset="1" stopColor={BLUE} stopOpacity="0" />
      </radialGradient>
    </defs>
    <g transform="translate(790 112) rotate(-7 170 250)">
      <rect x="-34" y="36" width="405" height="548" rx="70" fill="#000" opacity="0.54" filter="url(#rileyThumbGlow)" />
      <rect x="0" y="0" width="330" height="560" rx="54" fill="#05070b" stroke="#d9e2ef" strokeOpacity="0.74" strokeWidth="6" />
      <rect x="24" y="30" width="282" height="504" rx="38" fill="#030711" stroke={`${BLUE}88`} strokeWidth="3" />
      <ellipse cx="165" cy="274" rx="128" ry="154" fill="url(#rileyPhoneGlow)" />
      <circle cx="165" cy="278" r="82" fill="none" stroke={accent} strokeWidth="12" />
      <line x1="223" y1="336" x2="288" y2="401" stroke={accent} strokeWidth="18" strokeLinecap="round" />
      <text x="165" y="310" textAnchor="middle" fill={accent} fontFamily={BRAND.font.display} fontSize="100">?</text>
    </g>
  </svg>
);

const WarrantStamp: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <g transform="translate(710 360) rotate(-10)">
      <rect x="0" y="0" width="430" height="108" fill="#00000099" stroke={accent} strokeWidth="8" />
      <text x="215" y="74" textAnchor="middle" fill={accent} fontFamily={BRAND.font.display} fontSize="58">WARRANT</text>
    </g>
    <g transform="translate(805 236) rotate(9)">
      <rect x="0" y="0" width="310" height="82" fill="#00000077" stroke={SILVER} strokeWidth="4" opacity="0.72" />
      <text x="155" y="56" textAnchor="middle" fill={SILVER} fontFamily={BRAND.font.display} fontSize="43">PHONE</text>
    </g>
  </svg>
);

const PoliceBeam: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <rect x="694" y="0" width="170" height="720" fill={BLUE} opacity="0.13" transform="skewX(-14)" />
    <rect x="760" y="0" width="42" height="720" fill={accent} opacity="0.45" transform="skewX(-14)" />
    <text x="840" y="470" fill={accent} fontFamily={BRAND.font.display} fontSize="70" transform="rotate(-8 840 470)">NO</text>
    <text x="930" y="535" fill={WHITE} fontFamily={BRAND.font.display} fontSize="64" transform="rotate(-8 930 535)">WARRANT</text>
  </svg>
);

const LifeGrid: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    {['BANK', 'MAPS', 'PHOTOS', 'HEALTH', 'TEXTS', 'SEARCH'].map((label, i) => {
      const x = 690 + (i % 2) * 190;
      const y = 205 + Math.floor(i / 2) * 100;
      return (
        <g key={label}>
          <rect x={x} y={y} width="158" height="66" rx="14" fill="#000000a8" stroke={i % 2 ? accent : BLUE} strokeWidth="3" />
          <text x={x + 79} y={y + 43} textAnchor="middle" fill={i % 2 ? accent : WHITE} fontFamily={BRAND.font.body} fontSize="22" fontWeight="900">{label}</text>
        </g>
      );
    })}
  </svg>
);

const LockedPhone: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <rect x="865" y="156" width="210" height="350" rx="42" fill="#030711" stroke={SILVER} strokeWidth="6" />
    <rect x="910" y="326" width="120" height="92" rx="12" fill="#000000cc" stroke={accent} strokeWidth="6" />
    <path d="M932 326 L932 292 C932 252 1008 252 1008 292 L1008 326" fill="none" stroke={accent} strokeWidth="12" strokeLinecap="round" />
    <circle cx="970" cy="372" r="13" fill={accent} />
    <line x1="970" x2="970" y1="385" y2="404" stroke={accent} strokeWidth="6" />
  </svg>
);

const Motif: React.FC<{variant: ThumbVariant; accent: string}> = ({variant, accent}) => {
  if (variant.motif === 'warrant') return <WarrantStamp accent={accent} />;
  if (variant.motif === 'police') return <PoliceBeam accent={accent} />;
  if (variant.motif === 'life') return <LifeGrid accent={accent} />;
  if (variant.motif === 'locked') return <LockedPhone accent={accent} />;
  return <PhoneIcon accent={accent} />;
};

export const RileyThumbnail: React.FC<{variantIndex?: number}> = ({variantIndex = 0}) => {
  const variant = rileyThumbnailVariants[variantIndex] ?? rileyThumbnailVariants[0];
  const accent = variant.accent === 'gold' ? GOLD : BLUE;
  const lines = splitHeadline(variant.headline);
  const primarySize = lines.some((line) => line.length > 15) ? 78 : 106;
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <Img
        src={staticFile(variant.image)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: 'scale(1.08)',
          filter: 'brightness(0.63) contrast(1.26) saturate(1.05)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, #000000f5 0%, #02050be8 45%, #00000022 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(56% 70% at 78% 46%, ${accent}3f 0%, #00000000 64%)`}} />
      <AbsoluteFill style={{background: `radial-gradient(48% 58% at 78% 48%, ${NAVY}88 0%, #00000000 72%)`}} />
      <Motif variant={variant} accent={accent} />
      <div style={{position: 'absolute', left: 52, top: 50, width: 700}}>
        <div style={{fontFamily: BRAND.font.body, fontSize: 30, fontWeight: 900, color: accent, letterSpacing: 0}}>
          {variant.kicker}
        </div>
        <div style={{height: 6, width: 332, background: accent, marginTop: 16, marginBottom: 34}} />
        {lines.map((line, i) => (
          <div
            key={`${variant.id}-${line}`}
            style={{
              fontFamily: BRAND.font.display,
              fontSize: i === 0 ? primarySize : Math.max(74, primarySize - 10),
              lineHeight: 0.9,
              color: i === lines.length - 1 ? accent : WHITE,
              textTransform: 'uppercase',
              textShadow: '0 6px 24px #000',
              letterSpacing: 0,
            }}
          >
            {line}
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', right: 38, top: 28, fontFamily: BRAND.font.body, fontSize: 15, color: SILVER, border: `1px solid ${GOLD}99`, background: '#00000099', padding: '5px 8px', letterSpacing: 0}}>
        symbolic reconstruction
      </div>
      <div style={{position: 'absolute', left: 56, bottom: 42, fontFamily: BRAND.font.body, fontSize: 22, color: SILVER, fontWeight: 800, letterSpacing: 0}}>
        PRIME DOCUMENTARY
      </div>
      <Vignette strength={0.84} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};
