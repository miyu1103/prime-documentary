import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {BrandEndcard, BrandOpening, ENDCARD_SEC, OPENING_SEC} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {LightSweep, Particles, Vignette} from '../components/Motion';

const FPS = BRAND.video.fps;
const TOTAL_SEC = 678;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Kind =
  | 'trail'
  | 'opening'
  | 'detroit'
  | 'tower'
  | 'points'
  | 'warrant'
  | 'doctrine'
  | 'thinList'
  | 'lifeMap'
  | 'collision'
  | 'ruling'
  | 'boundary'
  | 'dissent'
  | 'doors'
  | 'trilogy'
  | 'end';

type Scene = {
  id: string;
  kind: Kind;
  start: number;
  dur: number;
  title: string;
  subtitle?: string;
  kicker?: string;
  citation?: string;
  image?: string;
  images?: string[];
  text?: string[];
};

const sceneImages = (id: string): string[] =>
  Array.from({length: 10}, (_, i) => `carpenter/v007/${id}/${id}_${String(i + 1).padStart(3, '0')}.png`);

const scenes: Scene[] = [
  {id: 's01', kind: 'trail', start: 0, dur: 27, title: '127 days. No warrant.', subtitle: 'Your phone is already drawing the map.', kicker: 'HOOK', image: 'carpenter/carpenter_hook_phone_map_v006_seed948991.png', images: sceneImages('s01'), text: ['127 days', 'no warrant']},
  {id: 'open', kind: 'opening', start: 27, dur: OPENING_SEC, title: 'Carpenter', subtitle: 'The phone that tracks you'},
  {id: 's02', kind: 'trilogy', start: 30.5, dur: 32, title: 'Body. Phone. Location.', subtitle: 'The privacy line moves into the device.', kicker: 'OPENING', image: 'carpenter/carpenter_ordinary_phone_desk_v006_seed949982.png', images: sceneImages('s02')},
  {id: 's03', kind: 'detroit', start: 62.5, dur: 31, title: 'Detroit area — 2010–2011', subtitle: 'A case begins with phone numbers.', kicker: 'ACT I', image: 'carpenter/carpenter_detroit_store_symbolic_v006_seed950973.png', images: sceneImages('s03'), text: ['Detroit', '2010–2011']},
  {id: 's04', kind: 'tower', start: 93.5, dur: 37, title: 'Cell-site location information', subtitle: 'Pings become a path.', kicker: 'ACT I', image: 'carpenter/carpenter_cell_tower_city_v006_seed951964.png', images: sceneImages('s04'), text: ['CSLI']},
  {id: 's05', kind: 'points', start: 130.5, dur: 35, title: '~12,898 points', subtitle: '127 days of location records.', kicker: 'ACT I', image: 'carpenter/carpenter_cell_tower_city_v006_seed951964.png', images: sceneImages('s05'), citation: 'CLM-0006', text: ['~12,898', '127 days']},
  {id: 's06', kind: 'warrant', start: 165.5, dur: 28, title: 'No warrant', subtitle: 'A lower Stored Communications Act standard.', kicker: 'ACT I', image: 'carpenter/carpenter_blank_order_phone_v006_seed952955.png', images: sceneImages('s06'), citation: 'CLM-0005', text: ['probable cause', 'lower standard']},
  {id: 's07', kind: 'doctrine', start: 193.5, dur: 34, title: 'The third-party doctrine', subtitle: 'Share it with a company, lose privacy?', kicker: 'ACT II', images: sceneImages('s07'), text: ['Miller 1976', 'Smith 1979']},
  {id: 's08', kind: 'thinList', start: 227.5, dur: 34, title: 'A list is thin', subtitle: 'Dialed numbers are not a life map.', kicker: 'ACT II', image: 'carpenter/carpenter_doctrine_split_v006_seed953946.png', images: sceneImages('s08'), text: ['dialed numbers']},
  {id: 's09', kind: 'lifeMap', start: 261.5, dur: 50, title: 'Different in kind, not degree', subtitle: 'Continuous, automatic, unavoidable.', kicker: 'ACT II', image: 'carpenter/carpenter_hook_phone_map_v006_seed948991.png', images: sceneImages('s09'), text: ['home', 'work', 'faith', 'health']},
  {id: 's10', kind: 'collision', start: 311.5, dur: 34, title: 'The collision', subtitle: 'A 1970s rule meets an always-on phone.', kicker: 'ACT II', image: 'carpenter/carpenter_ordinary_phone_desk_v006_seed949982.png', images: sceneImages('s10'), text: ['share it, lose it?', 'constant tracking']},
  {id: 's11', kind: 'ruling', start: 345.5, dur: 36, title: '2018 — 5–4', subtitle: 'Carpenter v. United States, 585 U.S. 296', kicker: 'ACT III', image: 'carpenter/carpenter_supreme_columns_abstract_v006_seed954937.png', images: sceneImages('s11'), citation: 'CLM-0002 / CLM-0001', text: ['5', '4']},
  {id: 's12', kind: 'boundary', start: 381.5, dur: 42, title: 'Did not overrule. Refused to extend.', subtitle: 'The old doctrine stops at CSLI.', kicker: 'ACT III', images: sceneImages('s12'), citation: 'CLM-0003', text: ['not overruled', 'not extended']},
  {id: 's13', kind: 'lifeMap', start: 423.5, dur: 40, title: 'Depth + no real choice', subtitle: 'A record you cannot avoid creating.', kicker: 'ACT III', images: sceneImages('s13'), citation: 'CLM-0009', text: ['depth', 'no choice']},
  {id: 's14', kind: 'dissent', start: 463.5, dur: 40, title: 'Where is the line?', subtitle: 'The dissents warned the rule was blurry.', kicker: 'ACT III', images: sceneImages('s14'), citation: 'CLM-0010', text: ['Congress?', 'Courts?']},
  {id: 's15', kind: 'boundary', start: 503.5, dur: 26, title: 'Rich + unavoidable = still private', subtitle: 'The warrant remains the line.', kicker: 'ACT III', images: sceneImages('s15'), text: ['warrant generally required']},
  {id: 's16', kind: 'doors', start: 529.5, dur: 48, title: 'Location was just the first door', subtitle: 'Searches. Purchases. Messages. Sensors.', kicker: 'ACT IV', image: 'carpenter/carpenter_data_doors_corridor_v006_seed955928.png', images: sceneImages('s16'), citation: 'CLM-0003', text: ['search', 'purchases', 'messages', 'sensors']},
  {id: 's17', kind: 'trilogy', start: 577.5, dur: 38, title: 'Body · Phone · Location', subtitle: 'Terry. Riley. Carpenter.', kicker: 'ENDING', images: sceneImages('s17'), text: ['Terry', 'Riley', 'Carpenter']},
  {id: 's18', kind: 'trail', start: 615.5, dur: 53.5, title: 'The line runs through your phone.', subtitle: 'And it is still being redrawn.', kicker: 'ENDING', image: 'carpenter/carpenter_viewer_device_final_v006_seed956919.png', images: sceneImages('s18')},
  {id: 'end', kind: 'end', start: 669, dur: ENDCARD_SEC, title: ''},
];

const fit = (n: string): number => Math.min(92, Math.max(42, 1200 / Math.max(n.length, 12)));

const sceneSeed = (id: string): number => id.split('').reduce((sum, ch) => sum + ch.charCodeAt(0), 0);

const SceneShell: React.FC<{scene: Scene; children: React.ReactNode}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const localDuration = Math.max(1, Math.round(scene.dur * FPS));
  const p = interpolate(frame, [0, localDuration], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const eased = p * p * (3 - 2 * p);
  const seed = sceneSeed(scene.id);
  const xDir = seed % 2 === 0 ? 1 : -1;
  const yDir = seed % 3 === 0 ? 1 : -1;
  const imageSet = scene.images && scene.images.length > 0 ? scene.images : scene.image ? [scene.image] : [];
  const segment = Math.max(42, Math.round(localDuration / Math.max(1, imageSet.length)));
  const currentIndex = imageSet.length > 0 ? Math.floor(frame / segment) % imageSet.length : 0;
  const nextIndex = imageSet.length > 0 ? (currentIndex + 1) % imageSet.length : 0;
  const segmentFrame = frame % segment;
  const nextOpacity = imageSet.length > 1 ? interpolate(segmentFrame, [segment * 0.74, segment], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const currentPulse = interpolate(segmentFrame, [0, segment], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const imgScale = 1.1 + eased * 0.1 + currentPulse * 0.06;
  const imgX = xDir * interpolate(eased, [0, 1], [-58, 58]) + xDir * interpolate(currentPulse, [0, 1], [-18, 18]);
  const imgY = yDir * interpolate(eased, [0, 1], [-32, 32]) + yDir * interpolate(currentPulse, [0, 1], [14, -14]);
  const imgRot = xDir * interpolate(eased, [0, 1], [-0.45, 0.45]);
  const pulse = 0.5 + 0.5 * Math.sin(frame * 0.035 + seed);
  const renderImage = (src: string, opacity: number, offset: number) => (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        opacity,
        transform: `translate3d(${imgX + offset * 16}px, ${imgY - offset * 9}px, 0) scale(${imgScale + offset * 0.025}) rotate(${imgRot + offset * 0.08}deg)`,
        transformOrigin: `${seed % 2 === 0 ? 64 : 36}% ${seed % 3 === 0 ? 58 : 42}%`,
        filter: 'brightness(0.78) contrast(1.22) saturate(1.08)',
        willChange: 'transform, opacity',
      }}
    />
  );
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {imageSet.length > 0 ? (
        <AbsoluteFill style={{overflow: 'hidden'}}>
          {renderImage(imageSet[currentIndex], 1, 0)}
          {imageSet.length > 1 ? renderImage(imageSet[nextIndex], nextOpacity, 1) : null}
          <AbsoluteFill
            style={{
              background: `radial-gradient(60% 55% at ${58 + xDir * 12}% ${44 + yDir * 6}%, ${BLUE}${Math.round(22 + pulse * 22).toString(16).padStart(2, '0')} 0%, #00000000 66%)`,
              mixBlendMode: 'screen',
              opacity: 0.55,
            }}
          />
        </AbsoluteFill>
      ) : (
        <AbsoluteFill
          style={{
            background: `radial-gradient(85% 70% at 62% 38%, #14335c 0%, ${NAVY} 28%, ${INK} 82%)`,
          }}
        />
      )}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}C8 0%, #00000016 42%, ${INK}DE 100%)`}} />
      <AbsoluteFill
        style={{
          background: `linear-gradient(${82 + imgRot * 12}deg, #00000000 0%, #ffffff0E 45%, #00000000 58%)`,
          transform: `translateX(${interpolate(eased, [0, 1], [-760, 760])}px)`,
          mixBlendMode: 'screen',
          opacity: 0.42,
        }}
      />
      <LightSweep seed={scene.id} color={scene.kind === 'ruling' ? GOLD : BLUE} />
      <Particles seed={scene.id} count={22} color={scene.kind === 'ruling' ? GOLD : BLUE} />
      {children}
      <Lower scene={scene} />
      <ReconLabel />
      <Vignette strength={1} />
      <Grain opacity={0.04} />
    </AbsoluteFill>
  );
};

const ReconLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 56,
      top: 52,
      fontFamily: BRAND.font.body,
      fontSize: 19,
      color: SILVER,
      padding: '8px 12px',
      border: `1px solid ${GOLD}77`,
      background: '#00000088',
    }}
  >
    symbolic reconstruction
  </div>
);

const Lower: React.FC<{scene: Scene}> = ({scene}) => {
  if (!scene.title || scene.kind === 'end') return null;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - Math.round(0.15 * fps), fps, config: {damping: 18, stiffness: 95}});
  return (
    <div style={{position: 'absolute', left: 58, top: 46, opacity: Math.min(1, e)}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker ?? 'PRIME DOCUMENTARY'}</div>
      <div style={{width: 290, height: 2, background: GOLD, marginTop: 9, marginBottom: 22}} />
      <div
        style={{
          fontFamily: BRAND.font.display,
          fontSize: fit(scene.title),
          color: WHITE,
          textTransform: 'uppercase',
          maxWidth: 1150,
          textShadow: '0 4px 24px #000',
        }}
      >
        {scene.title}
      </div>
      {scene.subtitle ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 8, maxWidth: 980}}>
          {scene.subtitle}
        </div>
      ) : null}
      {scene.citation ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: GOLD, marginTop: 14, background: '#00000099', padding: '7px 11px', display: 'inline-block'}}>
          {scene.citation}
        </div>
      ) : null}
    </div>
  );
};

const MapGrid: React.FC<{dense?: boolean}> = ({dense}) => {
  const frame = useCurrentFrame();
  const dots = Array.from({length: dense ? 170 : 44}, (_, i) => {
    const x = 220 + ((i * 109) % 1480);
    const y = 250 + ((i * 71) % 520);
    const on = interpolate(frame, [i * 0.7, i * 0.7 + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    return {x, y, on};
  });
  const mainPath = [
    [230, 430],
    [420, 476],
    [605, 546],
    [792, 520],
    [985, 606],
    [1192, 468],
    [1396, 612],
    [1640, 524],
  ];
  const branchPath = [
    [985, 606],
    [1084, 520],
    [1192, 468],
    [1306, 388],
  ];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.26">
        {Array.from({length: 9}, (_, i) => <line key={`h${i}`} x1="180" x2="1740" y1={230 + i * 70} y2={230 + i * 70} stroke={SILVER} strokeWidth="1" />)}
        {Array.from({length: 13}, (_, i) => <line key={`v${i}`} x1={210 + i * 125} x2={210 + i * 125} y1="190" y2="830" stroke={SILVER} strokeWidth="1" />)}
      </g>
      <polyline points={branchPath.map((d) => `${d[0]},${d[1]}`).join(' ')} fill="none" stroke={GOLD} strokeWidth="4" opacity="0.34" strokeLinecap="round" strokeLinejoin="round" />
      <polyline points={mainPath.map((d) => `${d[0]},${d[1]}`).join(' ')} fill="none" stroke={`${GOLD}44`} strokeWidth="18" opacity="0.52" strokeLinecap="round" strokeLinejoin="round" />
      <polyline points={mainPath.map((d) => `${d[0]},${d[1]}`).join(' ')} fill="none" stroke={GOLD} strokeWidth="6" opacity="0.92" strokeLinecap="round" strokeLinejoin="round" />
      {mainPath.map(([x, y], i) => <circle key={`p${i}`} cx={x} cy={y} r={i === mainPath.length - 1 ? 13 : 8} fill={i === mainPath.length - 1 ? GOLD : BLUE} opacity="0.95" />)}
      {dots.map((d, i) => <circle key={i} cx={d.x} cy={d.y} r={dense ? 4 : 7} fill={i % 11 === 0 ? GOLD : BLUE} opacity={d.on * 0.9} />)}
    </svg>
  );
};

const Phone: React.FC<{large?: boolean}> = ({large}) => {
  const frame = useCurrentFrame();
  const w = large ? 320 : 230;
  const h = large ? 590 : 420;
  const x = large ? 800 : 1325;
  const y = large ? 245 : 335;
  const shimmer = interpolate((frame % 180), [0, 90, 180], [0.18, 0.55, 0.18]);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <defs>
        <linearGradient id="phoneGlass" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0" stopColor="#0d1729" />
          <stop offset="0.46" stopColor="#02050a" />
          <stop offset="1" stopColor="#0a1c35" />
        </linearGradient>
        <radialGradient id="phoneGlow" cx="50%" cy="42%" r="58%">
          <stop offset="0" stopColor={BLUE} stopOpacity="0.72" />
          <stop offset="0.36" stopColor={BLUE} stopOpacity="0.16" />
          <stop offset="1" stopColor={BLUE} stopOpacity="0" />
        </radialGradient>
        <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="12" result="blur" />
          <feMerge>
            <feMergeNode in="blur" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      <g transform={`translate(${x} ${y}) rotate(-3 ${w / 2} ${h / 2})`}>
        <rect x="-28" y="42" width={w + 56} height={h - 20} rx="64" fill="#000" opacity="0.34" filter="url(#softGlow)" />
        <rect x="0" y="0" width={w} height={h} rx="48" fill="#05070b" stroke="#d8e1ee" strokeOpacity="0.55" strokeWidth="4" />
        <rect x="17" y="21" width={w - 34} height={h - 42} rx="36" fill="url(#phoneGlass)" stroke={`${BLUE}70`} strokeWidth="2" />
        <rect x="58" y="16" width={w - 116} height="12" rx="6" fill="#0a0e15" stroke="#2f3d52" strokeWidth="1" />
        <ellipse cx={w / 2} cy={h * 0.45} rx={w * 0.38} ry={h * 0.25} fill="url(#phoneGlow)" opacity={0.75 + shimmer * 0.25} />
        <path d={`M ${w * 0.20} ${h * 0.70} C ${w * 0.40} ${h * 0.46}, ${w * 0.55} ${h * 0.80}, ${w * 0.80} ${h * 0.28}`} fill="none" stroke="#f5b740" strokeWidth="7" strokeLinecap="round" opacity="0.94" />
        <path d={`M ${w * 0.20} ${h * 0.70} C ${w * 0.40} ${h * 0.46}, ${w * 0.55} ${h * 0.80}, ${w * 0.80} ${h * 0.28}`} fill="none" stroke={GOLD} strokeWidth="16" strokeLinecap="round" opacity="0.14" filter="url(#softGlow)" />
        {[0.20, 0.38, 0.57, 0.80].map((t, i) => (
          <g key={t}>
            <circle cx={w * t} cy={h * (0.82 - t * 0.67)} r={i === 3 ? 11 : 8} fill={i === 3 ? GOLD : BLUE} />
            <circle cx={w * t} cy={h * (0.82 - t * 0.67)} r={i === 3 ? 24 : 18} fill="none" stroke={i === 3 ? GOLD : BLUE} strokeWidth="3" opacity="0.24" />
          </g>
        ))}
        <path d={`M ${w * 0.20} 56 L ${w * 0.74} ${h - 90}`} stroke="#ffffff" strokeWidth="2" opacity={shimmer} />
        <rect x="21" y="25" width={w - 42} height={h - 50} rx="34" fill="none" stroke="#ffffff" strokeOpacity="0.10" strokeWidth="2" />
      </g>
    </svg>
  );
};

const TowerViz: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 0.45 + 0.55 * Math.sin(frame * 0.12);
  const towers = [[430, 720], [960, 420], [1420, 730]];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {towers.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r={140 + pulse * 44 + i * 15} fill="none" stroke={BLUE} strokeWidth="3" opacity="0.32" />
          <circle cx={x} cy={y} r={8} fill={GOLD} />
          <line x1={x} x2={x} y1={y} y2={y - 130} stroke={SILVER} strokeWidth="5" />
          <path d={`M ${x - 38} ${y - 40} L ${x} ${y - 130} L ${x + 38} ${y - 40}`} fill="none" stroke={SILVER} strokeWidth="4" />
        </g>
      ))}
      <Phone />
    </svg>
  );
};

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string}> = ({left, right, leftSub, rightSub}) => (
  <div style={{position: 'absolute', left: 260, right: 260, top: 360, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 46}}>
    {[{t: left, s: leftSub, c: BLUE}, {t: right, s: rightSub, c: GOLD}].map((b) => (
      <div key={b.t} style={{border: `3px solid ${b.c}`, background: '#020409cc', minHeight: 250, padding: 34}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 58, color: b.c, textTransform: 'uppercase'}}>{b.t}</div>
        {b.s ? <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: SILVER, marginTop: 20}}>{b.s}</div> : null}
      </div>
    ))}
  </div>
);

const Vote: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <g transform="translate(520 430)">
      {Array.from({length: 9}, (_, i) => {
        const yes = i < 5;
        return <rect key={i} x={(i % 5) * 150} y={Math.floor(i / 5) * 150} width="95" height="95" rx="10" fill={yes ? BLUE : '#333844'} stroke={yes ? GOLD : SILVER} strokeWidth="4" />;
      })}
      <text x="365" y="360" fill={WHITE} fontFamily={BRAND.font.display} fontSize="110" textAnchor="middle">5–4</text>
    </g>
  </svg>
);

const CourtColumns: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute', opacity: 0.22}}>
    <g transform="translate(1110 235)">
      {Array.from({length: 5}, (_, i) => (
        <g key={i} transform={`translate(${i * 120} 0)`}>
          <rect x="20" y="92" width="54" height="455" fill="#d8e1ee" opacity="0.35" />
          <path d="M 0 88 L 94 88 L 72 44 L 22 44 Z" fill={GOLD} opacity="0.42" />
          <rect x="-6" y="548" width="106" height="28" fill={GOLD} opacity="0.28" />
        </g>
      ))}
    </g>
  </svg>
);

const Doors: React.FC<{labels: string[]}> = ({labels}) => (
  <div style={{position: 'absolute', left: 230, right: 230, top: 340, display: 'grid', gridTemplateColumns: `repeat(${labels.length}, 1fr)`, gap: 28}}>
    {labels.map((label, i) => (
      <div key={label} style={{height: 310, border: `3px solid ${i === 0 ? BLUE : `${SILVER}66`}`, background: i === 0 ? `${BLUE}1F` : '#05070acc', position: 'relative'}}>
        <div style={{position: 'absolute', left: 20, right: 20, bottom: 30, height: 5, background: i === 0 ? GOLD : `${SILVER}55`}} />
        <div style={{fontFamily: BRAND.font.display, color: i === 0 ? GOLD : SILVER, fontSize: 42, textTransform: 'uppercase', padding: 24}}>{label}</div>
      </div>
    ))}
  </div>
);

const Triptych: React.FC = () => (
  <div style={{position: 'absolute', left: 170, right: 170, top: 360, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26}}>
    {[
      ['Terry', 'body'],
      ['Riley', 'phone contents'],
      ['Carpenter', 'location'],
    ].map(([a, b], i) => (
      <div key={a} style={{height: 280, border: `3px solid ${i === 2 ? GOLD : BLUE}`, background: '#020409cc', padding: 28}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 60, color: i === 2 ? GOLD : WHITE, textTransform: 'uppercase'}}>{a}</div>
        <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: SILVER, marginTop: 15}}>{b}</div>
      </div>
    ))}
  </div>
);

const SceneContent: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'opening') return <BrandOpening seriesLabel="Prime Documentary" title="Carpenter" subtitle="The phone that tracks you" />;
  if (scene.kind === 'end') return <BrandEndcard />;
  return (
    <SceneShell scene={scene}>
      {scene.kind === 'trail' ? <><MapGrid dense /><Phone /></> : null}
      {scene.kind === 'detroit' ? <><MapGrid /><TwoColumn left="Detroit" right="Phone numbers" leftSub="2010–2011" rightSub="A case board, not a portrait." /></> : null}
      {scene.kind === 'tower' ? <TowerViz /> : null}
      {scene.kind === 'points' ? <><MapGrid dense /><BigNumber top="~12,898" bottom="location points" /></> : null}
      {scene.kind === 'warrant' ? <TwoColumn left="Warrant" right="SCA order" leftSub="probable cause" rightSub="lower standard" /> : null}
      {scene.kind === 'doctrine' ? <TwoColumn left="Miller" right="Smith" leftSub="bank records · 1976" rightSub="dialed numbers · 1979" /> : null}
      {scene.kind === 'thinList' ? <ThinList /> : null}
      {scene.kind === 'lifeMap' ? <><MapGrid dense /><Doors labels={scene.text ?? ['home', 'work', 'faith', 'health']} /></> : null}
      {scene.kind === 'collision' ? <TwoColumn left="1970s rule" right="Modern phone" leftSub="share it, lose it" rightSub="constant, automatic, unavoidable" /> : null}
      {scene.kind === 'ruling' ? <><CourtColumns /><Vote /></> : null}
      {scene.kind === 'boundary' ? <Boundary /> : null}
      {scene.kind === 'dissent' ? <TwoColumn left="Clear rule" right="Blurry line" leftSub="easy to apply" rightSub="maybe in the right place" /> : null}
      {scene.kind === 'doors' ? <Doors labels={scene.text ?? ['location', 'search', 'messages', 'sensors']} /> : null}
      {scene.kind === 'trilogy' ? <Triptych /> : null}
    </SceneShell>
  );
};

const BigNumber: React.FC<{top: string; bottom: string}> = ({top, bottom}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 420, textAlign: 'center'}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: 150, color: GOLD, textShadow: '0 6px 35px #000'}}>{top}</div>
    <div style={{fontFamily: BRAND.font.body, fontSize: 38, color: WHITE}}>{bottom}</div>
  </div>
);

const ThinList: React.FC = () => (
  <div style={{position: 'absolute', left: 520, top: 390, width: 880, height: 230, background: '#e6dcc3', transform: 'rotate(-2deg)', boxShadow: '0 18px 55px #000'}}>
    {Array.from({length: 6}, (_, i) => <div key={i} style={{height: 14, width: 620 - i * 40, background: '#1b1d22', opacity: 0.75, margin: '22px 0 0 80px'}} />)}
  </div>
);

const Boundary: React.FC = () => {
  const frame = useCurrentFrame();
  const wobble = Math.sin(frame * 0.05) * 20;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d={`M 310 720 C 580 ${390 + wobble}, 790 ${760 - wobble}, 960 540 C 1130 ${320 + wobble}, 1330 ${610 - wobble}, 1610 340`} fill="none" stroke={BLUE} strokeWidth="10" />
      <text x="960" y="610" fill={GOLD} fontSize="58" fontFamily={BRAND.font.display} textAnchor="middle">WARRANT LINE</text>
    </svg>
  );
};

export const CarpenterPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    {scenes.map((scene) => (
      <Sequence key={scene.id} from={Math.round(scene.start * FPS)} durationInFrames={Math.round(scene.dur * FPS)}>
        <SceneContent scene={scene} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const carpenterPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
