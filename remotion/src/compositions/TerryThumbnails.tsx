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
  image?: string;
  motif: 'gap' | 'frisk' | 'scale' | 'street' | 'phone' | 'dense' | 'cinematic';
  accent: 'blue' | 'gold';
};

export const terryThumbnailVariants: ThumbVariant[] = [
  {
    id: 'thumb01',
    headline: 'NO WARRANT?',
    kicker: 'HERE IS THE CATCH',
    image: 'terry/PD-2026-006-terry-S004-IMG-001.v001.png',
    motif: 'gap',
    accent: 'gold',
  },
  {
    id: 'thumb02',
    headline: 'STOPPED. FRISKED. LEGAL?',
    kicker: 'TERRY v. OHIO',
    image: 'terry/PD-2026-006-terry-S018-IMG-001.v001.png',
    motif: 'frisk',
    accent: 'blue',
  },
  {
    id: 'thumb03',
    headline: 'SUSPICION IS ENOUGH?',
    kicker: 'THE 1968 RULE',
    motif: 'scale',
    accent: 'gold',
  },
  {
    id: 'thumb04',
    headline: 'THE 8-1 EXCEPTION',
    kicker: 'NO WARRANT · LOWER STANDARD',
    image: 'terry/PD-2026-006-terry-S003-IMG-001.v001.png',
    motif: 'street',
    accent: 'blue',
  },
  {
    id: 'thumb05',
    headline: 'THE LINE IS THIN',
    kicker: 'FROM YOUR BODY TO YOUR PHONE',
    motif: 'phone',
    accent: 'gold',
  },
  {
    id: 'thumb06',
    headline: 'NO WARRANT?',
    kicker: 'TERRY STOP · 1968 · 8-1',
    image: 'terry/PD-2026-006-terry-S004-IMG-001.v001.png',
    motif: 'dense',
    accent: 'gold',
  },
  {
    id: 'thumb07',
    headline: 'NO WARRANT?',
    kicker: 'TERRY STOP · 1968 · 8-1',
    image: 'terry/PD-2026-006-terry-S004-IMG-001.v001.png',
    motif: 'cinematic',
    accent: 'gold',
  },
];

const splitHeadline = (headline: string): string[] => {
  if (headline.length <= 16) return [headline];
  const words = headline.split(' ');
  const midpoint = Math.ceil(words.length / 2);
  return [words.slice(0, midpoint).join(' '), words.slice(midpoint).join(' ')];
};

const Motif: React.FC<{variant: ThumbVariant; accent: string}> = ({variant, accent}) => {
  if (variant.motif === 'cinematic') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        <defs>
          <filter id="cinematicGlow" x="-70%" y="-70%" width="240%" height="240%">
            <feGaussianBlur stdDeviation="12" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <linearGradient id="goldPanel" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor={GOLD} stopOpacity="0.96" />
            <stop offset="100%" stopColor="#8d6412" stopOpacity="0.86" />
          </linearGradient>
          <linearGradient id="bluePath" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0%" stopColor="#1e5bff" />
            <stop offset="55%" stopColor={BLUE} />
            <stop offset="100%" stopColor={GOLD} />
          </linearGradient>
        </defs>

        <g opacity="0.88">
          <rect x="704" y="112" width="472" height="420" fill="#02050dcc" stroke={GOLD} strokeWidth="2" opacity="0.54" />
          <rect x="730" y="136" width="102" height="286" fill={GOLD} opacity="0.12" />
          <rect x="854" y="128" width="132" height="352" fill={GOLD} opacity="0.18" />
          <rect x="1012" y="150" width="118" height="300" fill={GOLD} opacity="0.14" />
          <line x1="704" x2="1176" y1="230" y2="230" stroke={SILVER} strokeWidth="2" opacity="0.18" />
          <line x1="838" x2="838" y1="112" y2="532" stroke={SILVER} strokeWidth="2" opacity="0.16" />
          <line x1="1000" x2="1000" y1="112" y2="532" stroke={SILVER} strokeWidth="2" opacity="0.16" />
        </g>

        <g transform="translate(736 128)" filter="url(#cinematicGlow)">
          {Array.from({length: 9}, (_, i) => (
            <rect key={i} x={i * 34} y="0" width="24" height="24" fill={i === 8 ? GOLD : BLUE} opacity={i === 8 ? 0.96 : 0.88} />
          ))}
          <text x="0" y="76" fill={GOLD} fontFamily={BRAND.font.display} fontSize="54">8-1</text>
        </g>

        <g opacity="0.96">
          <path d="M642 493 C690 444 724 428 774 454 C830 485 858 400 910 426 C950 447 986 466 1028 406 C1058 364 1090 394 1126 418" fill="none" stroke="#001c5a" strokeWidth="31" strokeLinecap="round" opacity="0.5" />
          <path d="M642 493 C690 444 724 428 774 454 C830 485 858 400 910 426 C950 447 986 466 1028 406 C1058 364 1090 394 1126 418" fill="none" stroke="url(#bluePath)" strokeWidth="10" strokeLinecap="round" />
          {[642, 774, 910, 1028, 1126].map((x, i) => (
            <circle key={x} cx={x} cy={[493, 454, 426, 406, 418][i]} r={i === 3 ? 14 : 11} fill={i === 3 ? GOLD : BLUE} stroke="#06101f" strokeWidth="4" />
          ))}
        </g>

        <g transform="translate(724 290)">
          <rect x="0" y="0" width="368" height="116" rx="2" fill="#010409dd" stroke={GOLD} strokeWidth="4" />
          <text x="28" y="36" fill={SILVER} fontFamily={BRAND.font.body} fontSize="18" fontWeight="800">LOWER STANDARD</text>
          <line x1="28" x2="330" y1="70" y2="70" stroke={SILVER} strokeWidth="5" opacity="0.48" />
          <line x1="28" x2="174" y1="70" y2="70" stroke={GOLD} strokeWidth="10" strokeLinecap="round" />
          <circle cx="174" cy="70" r="18" fill={GOLD} />
          <text x="27" y="104" fill={SILVER} fontFamily={BRAND.font.body} fontSize="17">hunch</text>
          <text x="136" y="104" fill={GOLD} fontFamily={BRAND.font.body} fontSize="17" fontWeight="900">suspicion</text>
          <text x="285" y="104" fill={SILVER} fontFamily={BRAND.font.body} fontSize="17">proof</text>
        </g>

        <g transform="translate(890 448)">
          <rect x="0" y="0" width="84" height="118" fill="url(#goldPanel)" opacity="0.95" />
          <rect x="-56" y="78" width="196" height="44" fill="#03070dcc" />
          <text x="-42" y="113" fill={GOLD} fontFamily={BRAND.font.display} fontSize="44">GAP</text>
        </g>

        <g transform="translate(618 584)">
          <rect x="0" y="-44" width="234" height="62" fill="#03070de6" stroke={SILVER} strokeWidth="1" opacity="0.9" />
          <text x="20" y="0" fill={WHITE} fontFamily={BRAND.font.display} fontSize="48">~12 TRIPS</text>
        </g>
      </svg>
    );
  }
  if (variant.motif === 'dense') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        <defs>
          <filter id="denseGlow" x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="9" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
        <g opacity="0.78">
          <polyline points="650,484 720,438 792,474 858,422 935,460 1012,398 1100,432" fill="none" stroke={BLUE} strokeWidth="8" strokeLinecap="round" strokeLinejoin="round" />
          <polyline points="650,484 720,438 792,474 858,422 935,460 1012,398 1100,432" fill="none" stroke={BLUE} strokeWidth="24" strokeLinecap="round" strokeLinejoin="round" opacity="0.14" />
          {[650,720,792,858,935,1012,1100].map((x, i) => <circle key={x} cx={x} cy={[484,438,474,422,460,398,432][i]} r={i % 2 ? 10 : 8} fill={i === 5 ? GOLD : BLUE} />)}
        </g>
        <g transform="translate(740 166)" filter="url(#denseGlow)">
          {Array.from({length: 8}, (_, i) => <rect key={i} x={i * 36} y="0" width="25" height="25" fill={i === 7 ? GOLD : BLUE} opacity="0.94" />)}
          <text x="0" y="72" fill={GOLD} fontFamily={BRAND.font.display} fontSize="48">8-1</text>
        </g>
        <g transform="translate(742 288)">
          <rect x="0" y="0" width="330" height="112" fill="#00000099" stroke={GOLD} strokeWidth="4" />
          <line x1="24" x2="306" y1="62" y2="62" stroke={SILVER} strokeWidth="5" opacity="0.55" />
          <line x1="24" x2="156" y1="62" y2="62" stroke={GOLD} strokeWidth="9" strokeLinecap="round" />
          <circle cx="156" cy="62" r="17" fill={GOLD} />
          <text x="22" y="98" fill={SILVER} fontFamily={BRAND.font.body} fontSize="19">hunch</text>
          <text x="132" y="98" fill={GOLD} fontFamily={BRAND.font.body} fontSize="19">suspicion</text>
          <text x="250" y="98" fill={SILVER} fontFamily={BRAND.font.body} fontSize="19">proof</text>
        </g>
        <g transform="translate(894 438)">
          <rect x="0" y="0" width="82" height="170" fill={GOLD} opacity="0.92" />
          <text x="-8" y="216" fill={GOLD} fontFamily={BRAND.font.display} fontSize="55">GAP</text>
        </g>
        <g opacity="0.62">
          {[
            [1015,250,70,38,GOLD],
            [1095,306,54,34,SILVER],
            [700,246,64,36,SILVER],
            [654,336,48,32,GOLD],
            [1130,502,66,36,SILVER],
            [790,542,56,34,BLUE],
          ].map(([x,y,w,h,c], i) => <rect key={i} x={x as number} y={y as number} width={w as number} height={h as number} fill={c as string} opacity="0.55" />)}
        </g>
        <text x="638" y="622" fill={WHITE} fontFamily={BRAND.font.display} fontSize="48" opacity="0.92">~12 TRIPS</text>
      </svg>
    );
  }
  if (variant.motif === 'frisk') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        <rect x="754" y="158" width="288" height="340" fill="#00000088" stroke={BLUE} strokeWidth="4" />
        <line x1="898" x2="898" y1="158" y2="498" stroke={GOLD} strokeWidth="6" />
        <text x="790" y="314" fill={WHITE} fontFamily={BRAND.font.display} fontSize="44">OUTER</text>
        <text x="924" y="314" fill={SILVER} fontFamily={BRAND.font.display} fontSize="44">POCKET</text>
        <text x="790" y="374" fill={GOLD} fontFamily={BRAND.font.body} fontSize="25">weapons only</text>
      </svg>
    );
  }
  if (variant.motif === 'scale') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        <line x1="690" x2="1120" y1="400" y2="400" stroke={SILVER} strokeWidth="6" opacity="0.4" />
        <line x1="690" x2="895" y1="400" y2="400" stroke={accent} strokeWidth="12" strokeLinecap="round" />
        <circle cx="895" cy="400" r="23" fill={accent} />
        <text x="673" y="458" fill={SILVER} fontFamily={BRAND.font.body} fontSize="25">hunch</text>
        <text x="826" y="458" fill={GOLD} fontFamily={BRAND.font.body} fontSize="25">suspicion</text>
        <text x="1035" y="458" fill={SILVER} fontFamily={BRAND.font.body} fontSize="25">proof</text>
      </svg>
    );
  }
  if (variant.motif === 'street') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        {Array.from({length: 8}, (_, i) => <rect key={i} x={700 + i * 42} y="306" width="30" height="30" fill={i === 7 ? GOLD : BLUE} />)}
        <text x="700" y="394" fill={GOLD} fontFamily={BRAND.font.display} fontSize="54">1968</text>
      </svg>
    );
  }
  if (variant.motif === 'phone') {
    return (
      <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
        <line x1="650" x2="1100" y1="430" y2="430" stroke={GOLD} strokeWidth="7" />
        <line x1="885" x2="885" y1="190" y2="560" stroke={BLUE} strokeWidth="5" />
        <rect x="965" y="205" width="140" height="255" rx="28" fill="#04070d" stroke={SILVER} strokeWidth="5" />
        <rect x="986" y="242" width="98" height="5" fill={GOLD} />
        <rect x="986" y="286" width="98" height="5" fill={BLUE} />
        <rect x="986" y="330" width="98" height="5" fill={SILVER} opacity="0.7" />
      </svg>
    );
  }
  return (
    <svg width="1280" height="720" style={{position: 'absolute', inset: 0}}>
      {Array.from({length: 7}, (_, i) => (
        <rect key={i} x={690 + i * 58 + (i > 3 ? 95 : 0)} y={250 + (i % 2) * 62} width="48" height="48" fill={SILVER} opacity="0.28" />
      ))}
      <rect x="888" y="205" width="92" height="300" fill={accent} opacity="0.9" />
      <text x="880" y="568" fill={accent} fontFamily={BRAND.font.display} fontSize="58">GAP</text>
    </svg>
  );
};

export const TerryThumbnail: React.FC<{variantIndex?: number}> = ({variantIndex = 0}) => {
  const variant = terryThumbnailVariants[variantIndex] ?? terryThumbnailVariants[0];
  const accent = variant.accent === 'gold' ? GOLD : BLUE;
  const lines = splitHeadline(variant.headline);
  const isCinematic = variant.motif === 'cinematic';
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {variant.image ? (
        <Img
          src={staticFile(variant.image)}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: 'scale(1.08)',
            filter: isCinematic ? 'brightness(0.76) contrast(1.34) saturate(1.18)' : 'brightness(0.66) contrast(1.22) saturate(1.04)',
          }}
        />
      ) : (
        <AbsoluteFill style={{background: `radial-gradient(90% 74% at 70% 36%, #173d6f 0%, ${NAVY} 34%, ${INK} 82%)`}} />
      )}
      <AbsoluteFill style={{background: isCinematic ? 'linear-gradient(90deg, #000000f8 0%, #02050bec 45%, #00000036 100%)' : 'linear-gradient(90deg, #000000f4 0%, #02050be8 49%, #00000022 100%)'}} />
      <AbsoluteFill style={{background: `radial-gradient(54% 68% at 78% 45%, ${accent}${isCinematic ? '55' : '3f'} 0%, #00000000 64%)`}} />
      {isCinematic ? <AbsoluteFill style={{background: 'linear-gradient(180deg, #00000070 0%, #00000000 35%, #00000088 100%)'}} /> : null}
      <Motif variant={variant} accent={accent} />
      <div style={{position: 'absolute', left: 52, top: 48, width: 720}}>
        <div style={{fontFamily: BRAND.font.body, fontSize: 28, fontWeight: 900, color: accent, letterSpacing: 0}}>
          {variant.kicker}
        </div>
        <div style={{height: 5, width: 348, background: accent, marginTop: 16, marginBottom: 34}} />
        {lines.map((line, i) => (
          <div
            key={line}
            style={{
              fontFamily: BRAND.font.display,
              fontSize: line.length > 14 ? 84 : 104,
              lineHeight: 0.9,
              color: i === lines.length - 1 ? accent : WHITE,
              textTransform: 'uppercase',
              textShadow: '0 6px 24px #000',
            }}
          >
            {line}
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 56, bottom: 42, fontFamily: BRAND.font.body, fontSize: 22, color: SILVER, fontWeight: 800}}>
        PRIME DOCUMENTARY
      </div>
      <Vignette strength={0.84} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};
