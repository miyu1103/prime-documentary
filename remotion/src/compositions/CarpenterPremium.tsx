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
  text?: string[];
};

const scenes: Scene[] = [
  {id: 's01', kind: 'trail', start: 0, dur: 27, title: '127 days. No warrant.', subtitle: 'Your phone is already drawing the map.', kicker: 'HOOK', image: 'carpenter/CARP_H01_phone_map_hand_c04_seed826548.png', text: ['127 days', 'no warrant']},
  {id: 'open', kind: 'opening', start: 27, dur: OPENING_SEC, title: 'Carpenter', subtitle: 'The phone that tracks you'},
  {id: 's02', kind: 'trilogy', start: 30.5, dur: 32, title: 'Body. Phone. Location.', subtitle: 'The privacy line moves into the device.', kicker: 'OPENING'},
  {id: 's03', kind: 'detroit', start: 62.5, dur: 31, title: 'Detroit area — 2010–2011', subtitle: 'A case begins with phone numbers.', kicker: 'ACT I', text: ['Detroit', '2010–2011']},
  {id: 's04', kind: 'tower', start: 93.5, dur: 37, title: 'Cell-site location information', subtitle: 'Pings become a path.', kicker: 'ACT I', text: ['CSLI']},
  {id: 's05', kind: 'points', start: 130.5, dur: 35, title: '~12,898 points', subtitle: '127 days of location records.', kicker: 'ACT I', citation: 'CLM-0006', text: ['~12,898', '127 days']},
  {id: 's06', kind: 'warrant', start: 165.5, dur: 28, title: 'No warrant', subtitle: 'A lower Stored Communications Act standard.', kicker: 'ACT I', citation: 'CLM-0005', text: ['probable cause', 'lower standard']},
  {id: 's07', kind: 'doctrine', start: 193.5, dur: 34, title: 'The third-party doctrine', subtitle: 'Share it with a company, lose privacy?', kicker: 'ACT II', text: ['Miller 1976', 'Smith 1979']},
  {id: 's08', kind: 'thinList', start: 227.5, dur: 34, title: 'A list is thin', subtitle: 'Dialed numbers are not a life map.', kicker: 'ACT II', image: 'carpenter/CARP_H02_dark_location_bloom_c01_seed826959.png', text: ['dialed numbers']},
  {id: 's09', kind: 'lifeMap', start: 261.5, dur: 50, title: 'Different in kind, not degree', subtitle: 'Continuous, automatic, unavoidable.', kicker: 'ACT II', text: ['home', 'work', 'faith', 'health']},
  {id: 's10', kind: 'collision', start: 311.5, dur: 34, title: 'The collision', subtitle: 'A 1970s rule meets an always-on phone.', kicker: 'ACT II', text: ['share it, lose it?', 'constant tracking']},
  {id: 's11', kind: 'ruling', start: 345.5, dur: 36, title: '2018 — 5–4', subtitle: 'Carpenter v. United States, 585 U.S. 296', kicker: 'ACT III', citation: 'CLM-0002 / CLM-0001', text: ['5', '4']},
  {id: 's12', kind: 'boundary', start: 381.5, dur: 42, title: 'Did not overrule. Refused to extend.', subtitle: 'The old doctrine stops at CSLI.', kicker: 'ACT III', citation: 'CLM-0003', text: ['not overruled', 'not extended']},
  {id: 's13', kind: 'lifeMap', start: 423.5, dur: 40, title: 'Depth + no real choice', subtitle: 'A record you cannot avoid creating.', kicker: 'ACT III', citation: 'CLM-0009', text: ['depth', 'no choice']},
  {id: 's14', kind: 'dissent', start: 463.5, dur: 40, title: 'Where is the line?', subtitle: 'The dissents warned the rule was blurry.', kicker: 'ACT III', citation: 'CLM-0010', text: ['Congress?', 'Courts?']},
  {id: 's15', kind: 'boundary', start: 503.5, dur: 26, title: 'Rich + unavoidable = still private', subtitle: 'The warrant remains the line.', kicker: 'ACT III', text: ['warrant generally required']},
  {id: 's16', kind: 'doors', start: 529.5, dur: 48, title: 'Location was just the first door', subtitle: 'Searches. Purchases. Messages. Sensors.', kicker: 'ACT IV', citation: 'CLM-0003', text: ['search', 'purchases', 'messages', 'sensors']},
  {id: 's17', kind: 'trilogy', start: 577.5, dur: 38, title: 'Body · Phone · Location', subtitle: 'Terry. Riley. Carpenter.', kicker: 'ENDING', text: ['Terry', 'Riley', 'Carpenter']},
  {id: 's18', kind: 'trail', start: 615.5, dur: 53.5, title: 'The line runs through your phone.', subtitle: 'And it is still being redrawn.', kicker: 'ENDING', image: 'carpenter/CARP_H01_phone_map_hand_c02_seed826274.png'},
  {id: 'end', kind: 'end', start: 669, dur: ENDCARD_SEC, title: ''},
];

const fit = (n: string): number => Math.min(92, Math.max(42, 1200 / Math.max(n.length, 12)));

const SceneShell: React.FC<{scene: Scene; children: React.ReactNode}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const imgScale = 1.04 + p * 0.05;
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {scene.image ? (
        <AbsoluteFill style={{overflow: 'hidden'}}>
          <Img
            src={staticFile(scene.image)}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              transform: `scale(${imgScale})`,
              filter: 'brightness(0.72) contrast(1.12) saturate(0.95)',
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
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}D9 0%, #00000022 40%, ${INK}E8 100%)`}} />
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
  const path = dots.filter((_, i) => i % 13 === 0 || i % 17 === 0).slice(0, 18);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.26">
        {Array.from({length: 9}, (_, i) => <line key={`h${i}`} x1="180" x2="1740" y1={230 + i * 70} y2={230 + i * 70} stroke={SILVER} strokeWidth="1" />)}
        {Array.from({length: 13}, (_, i) => <line key={`v${i}`} x1={210 + i * 125} x2={210 + i * 125} y1="190" y2="830" stroke={SILVER} strokeWidth="1" />)}
      </g>
      {path.length > 1 ? <polyline points={path.map((d) => `${d.x},${d.y}`).join(' ')} fill="none" stroke={GOLD} strokeWidth="5" opacity="0.9" /> : null}
      {dots.map((d, i) => <circle key={i} cx={d.x} cy={d.y} r={dense ? 4 : 7} fill={i % 11 === 0 ? GOLD : BLUE} opacity={d.on * 0.9} />)}
    </svg>
  );
};

const Phone: React.FC<{large?: boolean}> = ({large}) => {
  const w = large ? 310 : 210;
  const h = large ? 580 : 390;
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g transform={`translate(${large ? 805 : 1340} ${large ? 250 : 350})`}>
        <rect x="0" y="0" width={w} height={h} rx="44" fill="#06080c" stroke={SILVER} strokeWidth="5" />
        <rect x="26" y="42" width={w - 52} height={h - 84} rx="22" fill="#07101f" stroke={`${BLUE}66`} strokeWidth="2" />
        <circle cx={w / 2} cy={h - 28} r="8" fill={SILVER} opacity="0.5" />
        <path d={`M ${w * 0.24} ${h * 0.68} C ${w * 0.45} ${h * 0.42}, ${w * 0.52} ${h * 0.8}, ${w * 0.78} ${h * 0.25}`} fill="none" stroke={GOLD} strokeWidth="7" />
        {[0.25, 0.42, 0.58, 0.77].map((t) => <circle key={t} cx={w * t} cy={h * (0.75 - t * 0.55)} r="8" fill={BLUE} />)}
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
      {scene.kind === 'ruling' ? <Vote /> : null}
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

