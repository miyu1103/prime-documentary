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
import {Grain} from '../components/Grain';
import {LightSweep, Particles, Vignette} from '../components/Motion';

const TOTAL_SEC = 678;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Kind =
  | 'pov'
  | 'wall'
  | 'image'
  | 'counter'
  | 'observer'
  | 'type'
  | 'risk'
  | 'charge'
  | 'scale'
  | 'question'
  | 'ruling'
  | 'facts'
  | 'frisk'
  | 'boundary'
  | 'equation'
  | 'dissent'
  | 'modern'
  | 'pressure'
  | 'line'
  | 'objects'
  | 'phone'
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
  recon?: boolean;
};

const scenes: Scene[] = [
  {id: 'S001', kind: 'pov', start: 0, dur: 30, title: 'No warrant. No crime seen.', subtitle: 'A street stop before the legal line is named.', kicker: 'HOOK', text: ['No warrant', 'No crime seen'], recon: true},
  {id: 'S002', kind: 'wall', start: 30, dur: 47, title: 'Suspicion, not proof', subtitle: 'The Fourth Amendment wall has a gap.', kicker: 'OPENING', text: ['warrant', 'solid evidence', 'suspicion']},
  {id: 'S003', kind: 'image', start: 77, dur: 18, title: 'Cleveland, Ohio - 1963', subtitle: 'The case begins on a downtown street.', kicker: 'ACT I', image: 'terry/PD-2026-006-terry-S003-IMG-001.v001.png', citation: 'CLM-0005', recon: true},
  {id: 'S004', kind: 'counter', start: 95, dur: 25, title: '~12 trips', subtitle: 'Two men, one store window, a repeated path.', kicker: 'ACT I', image: 'terry/PD-2026-006-terry-S004-IMG-001.v001.png', citation: 'CLM-0006', text: ['~12 trips'], recon: true},
  {id: 'S005', kind: 'observer', start: 120, dur: 18, title: 'A pattern forms', subtitle: 'Experience turns ordinary motion into suspicion.', kicker: 'ACT I', text: ['window', 'return', 'heads together']},
  {id: 'S006', kind: 'type', start: 138, dur: 14, title: 'Suspicion != proof', subtitle: 'Under the ordinary rule, that is not enough.', kicker: 'ACT I'},
  {id: 'S007', kind: 'risk', start: 152, dur: 22, title: 'The decision point', subtitle: 'Officer safety on one side. Innocent contact on the other.', kicker: 'ACT I', text: ['officer safety', 'innocent contact']},
  {id: 'S008', kind: 'frisk', start: 174, dur: 16, title: 'Outer clothing', subtitle: 'The weapon question is shown as a boundary, not a spectacle.', kicker: 'ACT I', image: 'terry/PD-2026-006-terry-S018-IMG-001.v001.png', citation: 'CLM-0006', recon: true},
  {id: 'S009', kind: 'charge', start: 190, dur: 12, title: 'Carrying a concealed weapon', subtitle: 'The street encounter becomes a constitutional case.', kicker: 'ACT II', citation: 'CLM-0007'},
  {id: 'S010', kind: 'scale', start: 202, dur: 24, title: 'Probable cause + warrant', subtitle: 'The ordinary Fourth Amendment baseline.', kicker: 'ACT II', text: ['reasonable suspicion', 'probable cause', 'warrant']},
  {id: 'S011', kind: 'scale', start: 226, dur: 22, title: 'Threshold not met', subtitle: 'A window pattern is less than full probable cause.', kicker: 'ACT II'},
  {id: 'S012', kind: 'risk', start: 248, dur: 24, title: 'The unknown moment', subtitle: 'Before proof exists, the safety risk can still be real.', kicker: 'ACT II'},
  {id: 'S013', kind: 'question', start: 272, dur: 30, title: 'Below arrest?', subtitle: 'Can a brief stop sit below probable cause?', kicker: 'ACT II', text: ['encounter', 'stop', 'arrest']},
  {id: 'S014', kind: 'wall', start: 302, dur: 24, title: 'Two truths at once', subtitle: 'Real streets. Real abuse risk.', kicker: 'ACT II'},
  {id: 'S015', kind: 'ruling', start: 326, dur: 26, title: '1968 - 8-1', subtitle: 'Terry v. Ohio, 392 U.S. 1', kicker: 'ACT III', citation: 'CLM-0002', text: ['8', '1']},
  {id: 'S016', kind: 'facts', start: 352, dur: 24, title: 'Specific, articulable facts', subtitle: 'Reasonable suspicion must be describable.', kicker: 'ACT III', citation: 'CLM-0004'},
  {id: 'S017', kind: 'facts', start: 376, dur: 34, title: '"specific and articulable facts"', subtitle: 'Two men. Same window. A dozen trips. Heads together.', kicker: 'ACT III', citation: 'CLM-0004', text: ['two men', 'same window', 'a dozen trips', 'heads together']},
  {id: 'S018', kind: 'frisk', start: 410, dur: 20, title: 'Weapons only', subtitle: 'Outer clothing, and only for weapons.', kicker: 'ACT III', image: 'terry/PD-2026-006-terry-S018-IMG-001.v001.png', citation: 'CLM-0001', recon: true},
  {id: 'S019', kind: 'boundary', start: 430, dur: 29, title: 'Outer clothing - weapons only', subtitle: 'Not pockets. Not evidence. Not one inch more.', kicker: 'ACT III', citation: 'CLM-0003'},
  {id: 'S020', kind: 'equation', start: 459, dur: 32, title: 'Stop = seizure. Frisk = search.', subtitle: 'Still reasonable on a lower standard.', kicker: 'ACT III', citation: 'CLM-0003 / CLM-0004'},
  {id: 'S021', kind: 'dissent', start: 491, dur: 22, title: 'Dissent: Douglas, J. (alone)', subtitle: 'A warning about lowering the probable-cause line.', kicker: 'ACT III', citation: 'CLM-0008'},
  {id: 'S022', kind: 'modern', start: 513, dur: 16, title: '"Terry stop"', subtitle: 'One of the most common police-public encounters.', kicker: 'ACT IV', citation: 'CLM-0009', recon: true},
  {id: 'S023', kind: 'pressure', start: 529, dur: 22, title: 'Judgment can bend', subtitle: 'Training can sharpen it. Bias can distort it.', kicker: 'ACT IV', citation: 'CLM-0009'},
  {id: 'S024', kind: 'modern', start: 551, dur: 27, title: 'Facts, later put into words', subtitle: 'A low bar can be careful work - or weather.', kicker: 'ACT IV', citation: 'CLM-0009', recon: true},
  {id: 'S025', kind: 'pressure', start: 578, dur: 20, title: 'Careful rule. Pressured street.', subtitle: 'The risk is application under pressure.', kicker: 'ACT IV'},
  {id: 'S026', kind: 'line', start: 598, dur: 20, title: 'The line is thin', subtitle: 'Redrawn on sidewalks every day.', kicker: 'ACT IV'},
  {id: 'S027', kind: 'equation', start: 618, dur: 18, title: 'Street. Body. Less than proof.', subtitle: 'A real suspicion, and the gun was allowed to stand.', kicker: 'ENDING', citation: 'CLM-0001 / CLM-0007'},
  {id: 'S028', kind: 'objects', start: 636, dur: 18, title: 'Physical things', subtitle: 'House. Pockets. The ground you stand on.', kicker: 'ENDING'},
  {id: 'S029', kind: 'phone', start: 654, dur: 18, title: 'Next: can they search your phone?', subtitle: 'The device inside the pocket changes the question.', kicker: 'NEXT'},
  {id: 'S030', kind: 'end', start: 672, dur: 6, title: 'Prime Documentary', subtitle: 'Subscribe', kicker: 'END'},
];

const fit = (text: string): number => Math.min(86, Math.max(42, 1240 / Math.max(text.length, 14)));

const ReconLabel: React.FC = () => (
  <div style={{
    position: 'absolute',
    right: 54,
    top: 48,
    fontFamily: BRAND.font.body,
    fontSize: 18,
    color: SILVER,
    padding: '7px 11px',
    border: `1px solid ${GOLD}88`,
    background: '#00000099',
  }}>
    symbolic reconstruction
  </div>
);

const Lower: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'end') return null;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 90}});
  return (
    <div style={{position: 'absolute', left: 58, top: 48, opacity: Math.min(1, e), maxWidth: 1260}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker ?? 'PRIME DOCUMENTARY'}</div>
      <div style={{width: 300, height: 2, background: GOLD, marginTop: 9, marginBottom: 21}} />
      <div style={{
        fontFamily: BRAND.font.display,
        fontSize: fit(scene.title),
        color: WHITE,
        textTransform: 'uppercase',
        lineHeight: 0.95,
        textShadow: '0 4px 28px #000',
      }}>{scene.title}</div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 12, maxWidth: 1030}}>{scene.subtitle}</div> : null}
      {scene.citation ? <div style={{fontFamily: BRAND.font.body, fontSize: 19, color: GOLD, marginTop: 15, background: '#000000AA', padding: '7px 11px', display: 'inline-block'}}>{scene.citation}</div> : null}
    </div>
  );
};

const SceneShell: React.FC<{scene: Scene; children: React.ReactNode}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const scale = 1.035 + p * 0.035;
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
              transform: `scale(${scale})`,
              filter: 'brightness(0.66) contrast(1.18) saturate(0.93)',
            }}
          />
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{background: `radial-gradient(90% 74% at 60% 34%, #14335c 0%, ${NAVY} 34%, ${INK} 82%)`}} />
      )}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}E6 0%, #00000011 42%, ${INK}F0 100%)`}} />
      <LightSweep seed={scene.id} color={scene.kind === 'ruling' || scene.kind === 'dissent' ? GOLD : BLUE} />
      <Particles seed={scene.id} count={scene.image ? 18 : 26} color={scene.kind === 'ruling' ? GOLD : BLUE} />
      {children}
      <Lower scene={scene} />
      {scene.recon ? <ReconLabel /> : null}
      <Vignette strength={1} />
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

const Pairs: React.FC<{left: string; right: string}> = ({left, right}) => (
  <div style={{position: 'absolute', left: 380, right: 160, top: 390, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 44}}>
    {[left, right].map((label, i) => (
      <div key={label} style={{height: 210, border: `2px solid ${i === 0 ? BLUE : GOLD}`, background: '#00000088', padding: 30}}>
        <div style={{fontFamily: BRAND.font.display, color: i === 0 ? BLUE : GOLD, fontSize: 54, textTransform: 'uppercase'}}>{label}</div>
        <div style={{height: 2, width: 220, background: i === 0 ? BLUE : GOLD, marginTop: 18}} />
      </div>
    ))}
  </div>
);

const PovGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const hand = interpolate(frame, [20, 90, 160], [240, 0, 40], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <div style={{position: 'absolute', left: 780, top: 305, width: 340, height: 460, border: `3px solid ${SILVER}55`, borderRadius: 170, opacity: 0.44}} />
      <div style={{position: 'absolute', left: 600 - hand, top: 560, width: 320, height: 60, background: `${GOLD}DD`, transform: 'rotate(-10deg)', boxShadow: `0 0 36px ${GOLD}88`}} />
      <div style={{position: 'absolute', right: 480 - hand, top: 585, width: 320, height: 60, background: `${BLUE}CC`, transform: 'rotate(8deg)', boxShadow: `0 0 36px ${BLUE}88`}} />
      <div style={{position: 'absolute', left: 820, top: 805, width: 280, height: 4, background: GOLD}} />
    </>
  );
};

const WallGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const gap = interpolate(frame, [10, 80], [8, 132], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {Array.from({length: 9}, (_, i) => (
        <rect key={i} x={310 + i * 150 + (i > 4 ? gap : 0)} y={380 + (i % 2) * 68} width="132" height="62" fill={SILVER} opacity="0.22" />
      ))}
      <rect x="882" y="330" width={gap} height="360" fill={BLUE} opacity="0.78" />
      <text x="905" y="735" fill={GOLD} fontFamily={BRAND.font.display} fontSize="42">GAP</text>
    </svg>
  );
};

const CounterPath: React.FC = () => {
  const frame = useCurrentFrame();
  const trips = Math.min(12, Math.floor(interpolate(frame, [5, 650], [0, 12], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})));
  return (
    <>
      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        <polyline points="420,720 680,650 940,710 1200,640 1460,705" fill="none" stroke={`${BLUE}88`} strokeWidth="14" strokeLinecap="round" strokeLinejoin="round" />
        {Array.from({length: trips}, (_, i) => (
          <circle key={i} cx={420 + (i % 6) * 208} cy={i % 2 ? 650 : 720} r="11" fill={i % 2 ? GOLD : BLUE} opacity="0.92" />
        ))}
      </svg>
      <div style={{position: 'absolute', right: 170, bottom: 140, fontFamily: BRAND.font.display, fontSize: 124, color: GOLD, textShadow: '0 4px 28px #000'}}>~{trips}</div>
    </>
  );
};

const ScaleGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const pos = scene.id === 'S011' ? 0.38 : scene.id === 'S016' ? 0.56 : 0.82;
  const x = interpolate(frame, [0, 70], [420, 420 + pos * 880], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="420" x2="1300" y1="612" y2="612" stroke={SILVER} strokeWidth="6" opacity="0.45" />
      <line x1="420" x2={x} y1="612" y2="612" stroke={GOLD} strokeWidth="10" strokeLinecap="round" />
      <circle cx={x} cy="612" r="24" fill={GOLD} />
      <text x="405" y="670" fill={SILVER} fontFamily={BRAND.font.body} fontSize="24">hunch</text>
      <text x="845" y="670" fill={BLUE} fontFamily={BRAND.font.body} fontSize="24">reasonable suspicion</text>
      <text x="1190" y="670" fill={GOLD} fontFamily={BRAND.font.body} fontSize="24">probable cause</text>
      <line x1="1185" x2="1185" y1="560" y2="664" stroke={GOLD} strokeWidth="3" opacity="0.75" />
    </svg>
  );
};

const RulingGraphic: React.FC = () => (
  <div style={{position: 'absolute', left: 520, right: 190, top: 385, display: 'flex', alignItems: 'center', gap: 24}}>
    {Array.from({length: 8}, (_, i) => <div key={i} style={{width: 82, height: 82, background: BLUE, boxShadow: `0 0 24px ${BLUE}99`}} />)}
    <div style={{fontFamily: BRAND.font.display, fontSize: 92, color: GOLD, padding: '0 18px'}}>:</div>
    <div style={{width: 82, height: 82, background: GOLD, boxShadow: `0 0 24px ${GOLD}99`}} />
  </div>
);

const FactsGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const facts = scene.text ?? ['specific', 'describable', 'testable'];
  return (
    <div style={{position: 'absolute', left: 430, top: 405, display: 'flex', flexWrap: 'wrap', gap: 18, width: 1040}}>
      {facts.map((fact, i) => (
        <div key={fact} style={{fontFamily: BRAND.font.body, fontSize: 34, color: i % 2 ? GOLD : WHITE, border: `2px solid ${i % 2 ? GOLD : BLUE}`, padding: '18px 22px', background: '#00000099'}}>
          {fact}
        </div>
      ))}
    </div>
  );
};

const BoundaryGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <rect x="560" y="350" width="640" height="330" fill="#00000088" stroke={BLUE} strokeWidth="4" />
    <line x1="880" x2="880" y1="350" y2="680" stroke={GOLD} strokeWidth="5" />
    <text x="610" y="465" fill={WHITE} fontFamily={BRAND.font.display} fontSize="50">OUTER</text>
    <text x="930" y="465" fill={SILVER} fontFamily={BRAND.font.display} fontSize="50">POCKETS</text>
    <text x="610" y="555" fill={GOLD} fontFamily={BRAND.font.body} fontSize="32">weapons check</text>
    <text x="930" y="555" fill={SILVER} fontFamily={BRAND.font.body} fontSize="32">requires more</text>
  </svg>
);

const EquationGraphic: React.FC<{scene: Scene}> = ({scene}) => (
  <div style={{position: 'absolute', left: 390, top: 402, display: 'grid', gap: 20}}>
    {(scene.id === 'S027' ? ['street', 'body', 'less than proof'] : ['stop = seizure', 'frisk = search', 'reasonable suspicion']).map((line, i) => (
      <div key={line} style={{fontFamily: BRAND.font.display, fontSize: 62, color: i === 2 ? GOLD : WHITE, borderLeft: `5px solid ${i === 2 ? GOLD : BLUE}`, paddingLeft: 22, textTransform: 'uppercase'}}>
        {line}
      </div>
    ))}
  </div>
);

const DissentGraphic: React.FC = () => (
  <div style={{position: 'absolute', left: 510, top: 420, display: 'flex', gap: 20, alignItems: 'center'}}>
    {Array.from({length: 8}, (_, i) => <div key={i} style={{width: 58, height: 58, background: `${BLUE}88`}} />)}
    <div style={{width: 58, height: 58, background: GOLD, boxShadow: `0 0 26px ${GOLD}`}} />
  </div>
);

const ModernGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <line x1="260" x2="1640" y1="760" y2="760" stroke={SILVER} strokeWidth="3" opacity="0.32" />
    {Array.from({length: 5}, (_, i) => {
      const x = 520 + i * 210;
      return <rect key={i} x={x} y={500 + (i % 2) * 38} width="58" height="210" fill={i === 2 ? GOLD : BLUE} opacity="0.34" />;
    })}
    <path d="M420 760 C640 640, 880 820, 1140 650 S1480 710, 1620 620" fill="none" stroke={GOLD} strokeWidth="5" opacity="0.72" />
  </svg>
);

const LineGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 560], [260, 1660], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <line x1="260" x2="1660" y1="645" y2="645" stroke={SILVER} strokeWidth="2" opacity="0.25" />
      <line x1="260" x2={x} y1="645" y2="645" stroke={GOLD} strokeWidth="5" />
      <line x1={x} x2={x + 110} y1="645" y2="645" stroke={BLUE} strokeWidth="5" />
    </svg>
  );
};

const ObjectsGraphic: React.FC = () => (
  <div style={{position: 'absolute', left: 460, top: 405, display: 'flex', gap: 56}}>
    {['house', 'pockets', 'sidewalk'].map((item, i) => (
      <div key={item} style={{width: 260, height: 190, border: `2px solid ${i === 1 ? GOLD : BLUE}`, background: '#00000088', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: BRAND.font.display, fontSize: 42, color: WHITE, textTransform: 'uppercase'}}>
        {item}
      </div>
    ))}
  </div>
);

const PhoneGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = interpolate(frame % 90, [0, 45, 90], [0.25, 0.8, 0.25]);
  return (
    <div style={{position: 'absolute', left: 860, top: 300, width: 230, height: 430, borderRadius: 34, border: `5px solid ${SILVER}`, background: '#05070A', boxShadow: `0 0 ${70 + glow * 70}px ${BLUE}`}}>
      <div style={{position: 'absolute', left: 30, right: 30, top: 70, height: 5, background: GOLD, opacity: 0.8}} />
      <div style={{position: 'absolute', left: 30, right: 30, top: 118, height: 5, background: BLUE, opacity: 0.8}} />
      <div style={{position: 'absolute', left: 30, right: 30, top: 166, height: 5, background: SILVER, opacity: 0.5}} />
    </div>
  );
};

const EndCard: React.FC = () => (
  <AbsoluteFill style={{background: INK, alignItems: 'center', justifyContent: 'center'}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: 84, color: WHITE, textTransform: 'uppercase'}}>Prime Documentary</div>
    <div style={{fontFamily: BRAND.font.body, fontSize: 30, color: GOLD, marginTop: 16}}>Subscribe</div>
    <Grain opacity={0.05} />
  </AbsoluteFill>
);

const SceneBody: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'end') return <EndCard />;
  let body: React.ReactNode;
  switch (scene.kind) {
    case 'pov':
      body = <PovGraphic />;
      break;
    case 'wall':
      body = <WallGraphic />;
      break;
    case 'counter':
      body = <CounterPath />;
      break;
    case 'observer':
      body = <FactsGraphic scene={{...scene, text: scene.text ?? ['window', 'return', 'pattern']}} />;
      break;
    case 'risk':
      body = <Pairs left={(scene.text?.[0] ?? 'officer safety')} right={(scene.text?.[1] ?? 'innocent contact')} />;
      break;
    case 'scale':
      body = <ScaleGraphic scene={scene} />;
      break;
    case 'question':
      body = <FactsGraphic scene={{...scene, text: scene.text ?? ['encounter', 'stop', 'arrest']}} />;
      break;
    case 'ruling':
      body = <RulingGraphic />;
      break;
    case 'facts':
      body = <FactsGraphic scene={scene} />;
      break;
    case 'frisk':
      body = <BoundaryGraphic />;
      break;
    case 'boundary':
      body = <BoundaryGraphic />;
      break;
    case 'equation':
      body = <EquationGraphic scene={scene} />;
      break;
    case 'dissent':
      body = <DissentGraphic />;
      break;
    case 'modern':
      body = <ModernGraphic />;
      break;
    case 'pressure':
      body = <Pairs left="careful rule" right="pressure" />;
      break;
    case 'line':
      body = <LineGraphic />;
      break;
    case 'objects':
      body = <ObjectsGraphic />;
      break;
    case 'phone':
      body = <PhoneGraphic />;
      break;
    case 'charge':
    case 'type':
    default:
      body = <EquationGraphic scene={{...scene, text: [scene.title]}} />;
  }
  return <SceneShell scene={scene}>{body}</SceneShell>;
};

export const TerryPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    {scenes.map((scene) => (
      <Sequence key={scene.id} from={Math.round(scene.start * BRAND.video.fps)} durationInFrames={Math.round(scene.dur * BRAND.video.fps)} name={scene.id}>
        <SceneBody scene={scene} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const terryPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
