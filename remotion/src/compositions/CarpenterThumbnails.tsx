import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';

const INK = BRAND.color.ink;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type ThumbVariant = {
  id: string;
  headline: string;
  kicker: string;
  image: string;
  accent: 'blue' | 'gold';
};

export const thumbnailVariants: ThumbVariant[] = [
  {
    id: 'thumb01',
    headline: 'YOUR PHONE IS A MAP',
    kicker: '127 DAYS · NO WARRANT',
    image: 'carpenter/CARP_H02_dark_location_bloom_c06_seed827644.png',
    accent: 'gold',
  },
  {
    id: 'thumb02',
    headline: '127 DAYS NO WARRANT',
    kicker: 'PHONE LOCATION RECORDS',
    image: 'carpenter/CARP_H02_dark_location_bloom_c02_seed827096.png',
    accent: 'gold',
  },
  {
    id: 'thumb03',
    headline: 'POLICE WANTED THIS MAP',
    kicker: 'CARPENTER v. UNITED STATES',
    image: 'carpenter/CARP_H02_dark_location_bloom_c01_seed826959.png',
    accent: 'blue',
  },
  {
    id: 'thumb04',
    headline: 'THE MAP IN YOUR PHONE',
    kicker: '5-4 · THE WARRANT LINE',
    image: 'carpenter/CARP_H02_dark_location_bloom_c04_seed827370.png',
    accent: 'blue',
  },
  {
    id: 'thumb05',
    headline: 'CAN POLICE MAP YOUR LIFE?',
    kicker: 'PHONE LOCATION PRIVACY',
    image: 'carpenter/CARP_H02_dark_location_bloom_c06_seed827644.png',
    accent: 'gold',
  },
];

const Phone: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <defs>
      <linearGradient id="thumbPhoneGlass" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0" stopColor="#0d1729" />
        <stop offset="0.5" stopColor="#02050a" />
        <stop offset="1" stopColor="#0a1c35" />
      </linearGradient>
      <radialGradient id="thumbPhoneGlow" cx="52%" cy="42%" r="58%">
        <stop offset="0" stopColor={BLUE} stopOpacity="0.9" />
        <stop offset="0.42" stopColor={BLUE} stopOpacity="0.24" />
        <stop offset="1" stopColor={BLUE} stopOpacity="0" />
      </radialGradient>
      <filter id="thumbGlow" x="-60%" y="-60%" width="220%" height="220%">
        <feGaussianBlur stdDeviation="14" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
    </defs>
    <g transform="translate(760 96) rotate(-7 180 270)">
      <rect x="-42" y="44" width="444" height="590" rx="74" fill="#000" opacity="0.52" filter="url(#thumbGlow)" />
      <rect x="0" y="0" width="356" height="608" rx="58" fill="#05070b" stroke="#d8e1ee" strokeOpacity="0.72" strokeWidth="7" />
      <rect x="24" y="28" width="308" height="552" rx="42" fill="url(#thumbPhoneGlass)" stroke={`${BLUE}88`} strokeWidth="3" />
      <rect x="82" y="18" width="166" height="14" rx="7" fill="#080c13" stroke="#344054" strokeWidth="1" />
      <ellipse cx="178" cy="270" rx="136" ry="172" fill="url(#thumbPhoneGlow)" />
      <path d="M 70 445 C 126 292, 194 426, 276 154" fill="none" stroke={accent} strokeWidth="17" strokeLinecap="round" />
      <path d="M 70 445 C 126 292, 194 426, 276 154" fill="none" stroke={accent} strokeWidth="38" strokeLinecap="round" opacity="0.17" filter="url(#thumbGlow)" />
      {[70, 142, 224, 276].map((x, i) => (
        <g key={x}>
          <circle cx={x} cy={[445, 360, 274, 154][i]} r={i === 3 ? 21 : 15} fill={i === 3 ? accent : BLUE} />
          <circle cx={x} cy={[445, 360, 274, 154][i]} r={i === 3 ? 42 : 31} fill="none" stroke={i === 3 ? accent : BLUE} strokeWidth="4" opacity="0.26" />
        </g>
      ))}
    </g>
  </svg>
);

const Trail: React.FC<{accent: string}> = ({accent}) => (
  <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
    <polyline
      points="80,482 208,416 332,456 450,386 588,430 712,324 872,374 1114,292"
      fill="none"
      stroke={accent}
      strokeWidth="9"
      strokeLinecap="round"
      strokeLinejoin="round"
      opacity="0.94"
    />
    <polyline
      points="80,482 208,416 332,456 450,386 588,430 712,324 872,374 1114,292"
      fill="none"
      stroke={accent}
      strokeWidth="28"
      strokeLinecap="round"
      strokeLinejoin="round"
      opacity="0.13"
    />
    {[80, 208, 332, 450, 588, 712, 872, 1114].map((x, i) => (
      <circle key={x} cx={x} cy={[482, 416, 456, 386, 430, 324, 374, 292][i]} r={i === 7 ? 18 : 10} fill={i === 7 ? accent : BLUE} />
    ))}
  </svg>
);

export const CarpenterThumbnail: React.FC<{variantIndex?: number}> = ({variantIndex = 0}) => {
  const variant = thumbnailVariants[variantIndex] ?? thumbnailVariants[0];
  const accent = variant.accent === 'gold' ? GOLD : BLUE;
  const words = variant.headline.split(' ');
  const lineA = words.slice(0, Math.ceil(words.length / 2)).join(' ');
  const lineB = words.slice(Math.ceil(words.length / 2)).join(' ');
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
          filter: 'brightness(0.72) contrast(1.18) saturate(1.08)',
        }}
      />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, #000000fa 0%, #02050bef 46%, #00000022 100%)'}} />
      <AbsoluteFill style={{background: 'radial-gradient(64% 76% at 80% 50%, #1f6bff4f 0%, #00000000 62%)'}} />
      <Trail accent={accent} />
      <Phone accent={accent} />
      <div style={{position: 'absolute', left: 46, top: 48, width: 700}}>
        <div style={{fontFamily: BRAND.font.body, fontSize: 28, fontWeight: 900, color: accent, letterSpacing: 0}}>
          {variant.kicker}
        </div>
        <div style={{height: 6, width: 336, background: accent, marginTop: 14, marginBottom: 28}} />
        <div style={{fontFamily: BRAND.font.display, fontSize: 104, lineHeight: 0.89, color: WHITE, textTransform: 'uppercase', textShadow: '0 8px 26px #000'}}>
          {lineA}
        </div>
        <div style={{fontFamily: BRAND.font.display, fontSize: 104, lineHeight: 0.89, color: accent, textTransform: 'uppercase', textShadow: '0 8px 26px #000'}}>
          {lineB}
        </div>
      </div>
      <div style={{position: 'absolute', left: 52, bottom: 42, display: 'flex', gap: 14, alignItems: 'center'}}>
        <div style={{fontFamily: BRAND.font.body, fontSize: 22, color: SILVER, fontWeight: 900}}>PRIME DOCUMENTARY</div>
        <div style={{width: 2, height: 24, background: `${SILVER}66`}} />
        <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: accent, fontWeight: 900}}>SYMBOLIC RECONSTRUCTION</div>
      </div>
      <Vignette strength={0.82} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};
