import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  Video,
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
import {SceneArt} from '../components/SceneArt';
import {THERANOS_CAPTIONS} from '../data/theranos_captions';
import {THERANOS_ROUGHCUT} from '../data/theranos_roughcut';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#C64A46';
const GREEN = '#4FD19B';

const HOOK_MONTAGE_SEC = 7;
const BRIDGE_SEC = 1.5;
const CONTENT_START_SEC = HOOK_MONTAGE_SEC + BRIDGE_SEC + OPENING_SEC;
const MIX_SRC = 'theranos/audio/theranos_mix_v001.mp3';

type SceneKind =
  | 'valuationCrash'
  | 'arrowFlip'
  | 'timeline2003'
  | 'needleBox'
  | 'valuationRise'
  | 'authority'
  | 'story'
  | 'timeline2015'
  | 'machineSwap'
  | 'diagnosisChain'
  | 'secCollapse'
  | 'failureFraud'
  | 'definition'
  | 'trialSplit'
  | 'verdictGuilty'
  | 'verdictSplit'
  | 'acquittalNuance'
  | 'sentence'
  | 'fakeIt'
  | 'boundaryEquation'
  | 'stakes'
  | 'seriesTriptych'
  | 'lineRedrawn'
  | 'subscribe';

type BodySceneInput = {
  spanId: string;
  dur: number;
  chapter: string;
  kind: SceneKind;
  kicker: string;
  title: string;
  subtitle?: string;
  citation?: string;
  ai?: boolean;
};

type BodyScene = BodySceneInput & {start: number};

const BODY_INPUT: BodySceneInput[] = [
  {spanId: 'SPN-0001', dur: 27.725 + 8, chapter: 'hook', kind: 'valuationCrash', kicker: 'HOOK', title: 'When does selling a dream become a crime?', subtitle: '$9B promise -> $0 collapse', citation: 'United States v. Holmes (N.D. Cal.) - verdict Jan 3, 2022'},
  {spanId: 'SPN-0002', dur: 36.27 + 11.5, chapter: 'opening', kind: 'arrowFlip', kicker: 'OPENING', title: 'Finale: one person vs. everyone', subtitle: 'The series camera turns around.', ai: true},
  {spanId: 'SPN-0003', dur: 9.381, chapter: 'act1', kind: 'timeline2003', kicker: 'ACT I', title: "2003 - a Stanford dropout's startup", subtitle: 'A symbolic origin, no likeness.', ai: true},
  {spanId: 'SPN-0004', dur: 25.542, chapter: 'act1', kind: 'needleBox', kicker: 'ACT I', title: 'The Edison: hundreds of tests, one drop', subtitle: 'A black box symbol, not the real device.'},
  {spanId: 'SPN-0005', dur: 24.381 + 8, chapter: 'act1', kind: 'valuationRise', kicker: 'ACT I', title: '~$9B - board prestige - Walgreens limited', subtitle: 'Limited rollout, not nationwide.', citation: 'SEC charges 2018 (settled, no admission)'},
  {spanId: 'SPN-0023', dur: 19.458, chapter: 'act1', kind: 'authority', kicker: 'ACT I', title: 'Prestige became a substitute for scrutiny', subtitle: 'Credentials grow; scrutiny shrinks.', ai: true},
  {spanId: 'SPN-0006', dur: 24.242 + 11.5, chapter: 'act1', kind: 'story', kicker: 'ACT I', title: 'A story powerful enough to stop the questions', subtitle: 'The product and the myth separate.'},
  {spanId: 'SPN-0007', dur: 9.706, chapter: 'act2', kind: 'timeline2015', kicker: 'ACT II', title: '2015: The Wall Street Journal investigates', subtitle: 'Documents and whistleblowers.'},
  {spanId: 'SPN-0008', dur: 23.034, chapter: 'act2', kind: 'machineSwap', kicker: 'ACT II', title: "Tests run on other companies' machines", subtitle: 'Own device -> commercial machines.', ai: true},
  {spanId: 'SPN-0009', dur: 10.449, chapter: 'act2', kind: 'diagnosisChain', kicker: 'ACT II', title: 'Bad data becomes a decision', subtitle: 'A medical number is not a demo.', ai: true},
  {spanId: 'SPN-0010', dur: 24.427 + 7, chapter: 'act2', kind: 'secCollapse', kicker: 'ACT II', title: '2018: SEC civil charge; company dissolves', subtitle: 'Settled without admitting or denying wrongdoing.', citation: 'SEC charges 2018 - settled, no admission'},
  {spanId: 'SPN-0011', dur: 22.756 + 11.5, chapter: 'act2', kind: 'failureFraud', kicker: 'ACT II', title: 'Failure - or fraud?', subtitle: 'A sad story is not automatically a crime.'},
  {spanId: 'SPN-0012', dur: 9.985 + 29.582, chapter: 'act3', kind: 'definition', kicker: 'ACT III', title: 'Fraud = intent to deceive', subtitle: 'Not just failure.', ai: true},
  {spanId: 'SPN-0024', dur: 26.099, chapter: 'act3', kind: 'trialSplit', kicker: 'ACT III', title: 'Prosecution: she knew. Defense: a true believer.', subtitle: 'The jury decided count by count.'},
  {spanId: 'SPN-0013', dur: 23.266 + 20, chapter: 'act3', kind: 'verdictGuilty', kicker: 'ACT III', title: '2022 - GUILTY: 4 investor counts', subtitle: 'One conspiracy count + three wire-fraud counts.', citation: 'United States v. Holmes (N.D. Cal.) - verdict Jan 3, 2022'},
  {spanId: 'SPN-0014', dur: 16.44, chapter: 'act3', kind: 'verdictSplit', kicker: 'ACT III', title: 'ACQUITTED: patient counts - NO VERDICT: 3 counts', subtitle: 'No GUILTY label belongs here.', citation: 'United States v. Holmes - split verdict', ai: true},
  {spanId: 'SPN-0015', dur: 42.446, chapter: 'act3', kind: 'acquittalNuance', kicker: 'ACT III', title: 'Acquittal does not mean exoneration', subtitle: 'Balwani: convicted on all 12.'},
  {spanId: 'SPN-0016', dur: 16.3 + 11.5, chapter: 'act3', kind: 'sentence', kicker: 'ACT III', title: 'Sentenced: ~11 years, 3 months', subtitle: '135 months.', ai: true},
  {spanId: 'SPN-0017', dur: 21.78, chapter: 'act4', kind: 'fakeIt', kicker: 'ACT IV', title: '"Fake it till you make it" - usually legal', subtitle: 'Ambition alone is not fraud.', ai: true},
  {spanId: 'SPN-0018', dur: 18.437 + 8, chapter: 'act4', kind: 'boundaryEquation', kicker: 'ACT IV', title: 'The line: knowingly false + relied upon = fraud', subtitle: 'Intent and reliance draw the line.'},
  {spanId: 'SPN-0019', dur: 22.105 + 11.5, chapter: 'act4', kind: 'stakes', kicker: 'ACT IV', title: 'A failed app costs money. A wrong test costs a diagnosis.', subtitle: 'The stakes are different.', ai: true},
  {spanId: 'SPN-0020', dur: 33.112 + 7, chapter: 'ending', kind: 'seriesTriptych', kicker: 'ENDING', title: 'One question, many costumes: where is the line?', subtitle: 'Stop/arrest. Identify/investigate. Promise/lie.', ai: true},
  {spanId: 'SPN-0021', dur: 21.037 + 5, chapter: 'ending', kind: 'lineRedrawn', kicker: 'ENDING', title: 'The line keeps moving', subtitle: 'Technology, money, and power move it.'},
  {spanId: 'SPN-0022', dur: 9.799 + 16, chapter: 'ending', kind: 'subscribe', kicker: 'ENDING', title: 'Subscribe - one line at a time', subtitle: 'Prime Documentary continues here.', ai: true},
];

const BODY_SCENES: BodyScene[] = BODY_INPUT.reduce<BodyScene[]>((acc, scene) => {
  const start = acc.length === 0 ? 0 : acc[acc.length - 1].start + acc[acc.length - 1].dur;
  acc.push({...scene, start});
  return acc;
}, []);

const BODY_SEC = BODY_SCENES.reduce((sum, scene) => sum + scene.dur, 0);
const TOTAL_SEC = CONTENT_START_SEC + BODY_SEC + ENDCARD_SEC;

const getShot = (spanId: string) => {
  const shot = THERANOS_ROUGHCUT.shots.find((item) => item.spanId === spanId);
  if (!shot) throw new Error(`Missing Theranos roughcut shot ${spanId}`);
  return shot;
};

const fitTitle = (text: string): number => Math.min(78, Math.max(38, 1380 / Math.max(text.length, 16)));

const ImagePlate: React.FC<{spanId: string; duration: number; seed: string; dim?: number}> = ({spanId, duration, seed, dim = 0.72}) => {
  const frame = useCurrentFrame();
  const shot = getShot(spanId);
  const images = (shot.images && shot.images.length > 0 ? shot.images : shot.src ? [shot.src] : []).filter(Boolean);
  const segmentFrames = Math.max(1, Math.round(FPS * 4.5));
  const fadeFrames = Math.round(FPS * 0.45);
  const index = images.length > 0 ? Math.floor(frame / segmentFrames) % images.length : 0;
  const nextIndex = images.length > 0 ? (index + 1) % images.length : 0;
  const local = frame % segmentFrames;
  const cross = images.length > 1 ? interpolate(local, [segmentFrames - fadeFrames, segmentFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const progress = interpolate(frame, [0, Math.max(1, duration * FPS)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = seed.charCodeAt(seed.length - 1) % 2 === 0 ? 1 : -1;
  const render = (src: string, opacity: number, offset: number) => (
    <Img
      src={staticFile(src)}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        opacity,
        transform: `translate3d(${dir * (-28 + progress * 56 + offset * 14)}px, ${10 - progress * 24 - offset * 8}px, 0) scale(${1.045 + progress * 0.075 + offset * 0.018})`,
        transformOrigin: dir > 0 ? '58% 46%' : '42% 46%',
        filter: `brightness(${dim}) contrast(1.18) saturate(0.96)`,
      }}
    />
  );
  if (images.length === 0) {
    return <AbsoluteFill style={{background: `radial-gradient(90% 78% at 56% 42%, ${NAVY} 0%, ${INK} 82%)`}} />;
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: INK}}>
      {render(images[index], 1, 0)}
      {images.length > 1 ? render(images[nextIndex], cross, 1) : null}
    </AbsoluteFill>
  );
};

const VideoPlate: React.FC<{spanId: string; duration: number; seed: string; muted?: boolean}> = ({spanId, duration, seed, muted = true}) => {
  const frame = useCurrentFrame();
  const shot = getShot(spanId);
  const clips = shot.clips && shot.clips.length > 0 ? shot.clips : shot.src ? [{src: shot.src, clipSeconds: duration}] : [];
  const segmentFrames = Math.max(1, Math.round(FPS * 5.2));
  const index = clips.length > 0 ? Math.floor(frame / segmentFrames) % clips.length : 0;
  const local = frame % segmentFrames;
  const clip = clips[index];
  const p = interpolate(frame, [0, Math.max(1, duration * FPS)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = seed.charCodeAt(seed.length - 1) % 2 === 0 ? 1 : -1;
  if (!clip) {
    return <ImagePlate spanId={spanId} duration={duration} seed={seed} />;
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: INK}}>
      <Video
        src={staticFile(clip.src)}
        muted={muted}
        startFrom={Math.max(0, Math.round(local * 0.72))}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translate3d(${dir * (-18 + p * 36)}px, ${8 - p * 18}px, 0) scale(${1.035 + p * 0.045})`,
          filter: 'brightness(0.66) contrast(1.2) saturate(0.9)',
        }}
      />
    </AbsoluteFill>
  );
};

const CitationBadge: React.FC<{text?: string}> = ({text}) => {
  if (!text) return null;
  return (
    <div
      style={{
        position: 'absolute',
        right: 58,
        bottom: 158,
        maxWidth: 610,
        fontFamily: BRAND.font.body,
        fontSize: 20,
        lineHeight: 1.15,
        color: GOLD,
        background: '#000000B8',
        borderTop: `3px solid ${GOLD}`,
        padding: '10px 14px',
        textAlign: 'right',
        zIndex: 70,
      }}
    >
      {text}
    </div>
  );
};

const ReconstructionLabel: React.FC<{show?: boolean}> = ({show = true}) => {
  if (!show) return null;
  return (
    <div
      style={{
        position: 'absolute',
        right: 56,
        top: 50,
        fontFamily: BRAND.font.body,
        fontSize: 18,
        color: SILVER,
        background: '#0000009E',
        border: `1px solid ${GOLD}88`,
        padding: '8px 12px',
        zIndex: 90,
      }}
    >
      symbolic reconstruction
    </div>
  );
};

const UpperTelop: React.FC<{scene: BodyScene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 95}});
  return (
    <div style={{position: 'absolute', left: 58, top: 46, maxWidth: 1340, opacity: Math.min(1, enter), zIndex: 65}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, fontWeight: 900, color: GOLD, letterSpacing: '0.08em'}}>{scene.kicker}</div>
      <div style={{width: 285, height: 3, background: GOLD, marginTop: 9, marginBottom: 20}} />
      <div
        style={{
          fontFamily: BRAND.font.display,
          fontSize: fitTitle(scene.title),
          lineHeight: 0.98,
          color: WHITE,
          textTransform: 'uppercase',
          textShadow: '0 5px 28px #000',
        }}
      >
        {scene.title}
      </div>
      {scene.subtitle ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 10, maxWidth: 980, textShadow: '0 3px 16px #000'}}>
          {scene.subtitle}
        </div>
      ) : null}
    </div>
  );
};

const CaptionBand: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const lastCaptionEnd = Math.max(0, ...THERANOS_CAPTIONS.map((item) => item.end));
  if (lastCaptionEnd < TOTAL_SEC - ENDCARD_SEC - 28) return null;
  const cue = THERANOS_CAPTIONS.find((item) => t >= item.start && t < item.end);
  if (!cue) return null;
  const longest = Math.max(...cue.text.split('\n').map((line) => line.length));
  const fontSize = longest > 48 ? 44 : longest > 36 ? 50 : 56;
  return (
    <div
      style={{
        position: 'absolute',
        left: 190,
        right: 190,
        bottom: 38,
        minHeight: 88,
        padding: '16px 34px 18px',
        background: '#000000D9',
        borderTop: `3px solid ${GOLD}`,
        color: WHITE,
        fontFamily: BRAND.font.body,
        fontWeight: 900,
        fontSize,
        lineHeight: 1.06,
        textAlign: 'center',
        textShadow: '0 3px 14px #000, 0 0 5px #000',
        WebkitTextStroke: '1.1px #000',
        whiteSpace: 'pre-line',
        zIndex: 100,
      }}
    >
      {cue.text}
    </div>
  );
};

const SceneShell: React.FC<{scene: BodyScene; media: React.ReactNode; children?: React.ReactNode}> = ({scene, media, children}) => (
  <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
    {media}
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}B8 0%, #00000024 44%, ${INK}DD 100%)`}} />
    <AbsoluteFill style={{background: `radial-gradient(78% 64% at 68% 45%, ${scene.chapter === 'act3' ? `${GOLD}24` : `${BLUE}20`} 0%, #00000000 70%)`, mixBlendMode: 'screen'}} />
    <LightSweep seed={scene.spanId} color={scene.chapter === 'act3' ? GOLD : BLUE} />
    <Particles seed={scene.spanId} color={scene.chapter === 'act3' ? GOLD : BLUE} count={22} />
    {children}
    <UpperTelop scene={scene} />
    <CitationBadge text={scene.citation} />
    <ReconstructionLabel show={scene.ai || scene.kind.includes('verdict') || scene.kind.includes('valuation') || scene.kind === 'definition'} />
    <Vignette strength={1} />
    <Grain opacity={0.045} />
  </AbsoluteFill>
);

const ValuationGraph: React.FC<{mode: 'rise' | 'crash'}> = ({mode}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames * 0.74], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const crash = mode === 'crash' ? interpolate(frame, [durationInFrames * 0.48, durationInFrames * 0.78], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
  const risePoints = [
    [300, 720],
    [530, 650],
    [760, 560],
    [980, 430],
    [1180, 330],
  ];
  const end = mode === 'crash' ? [1560, 735] : [1530, 260];
  const pts = [...risePoints, end];
  const visible = Math.max(2, Math.floor(pts.length * Math.max(p, 0.34)));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.24">
        {Array.from({length: 5}, (_, i) => <line key={`h${i}`} x1="260" x2="1640" y1={260 + i * 115} y2={260 + i * 115} stroke={SILVER} strokeWidth="2" />)}
        {Array.from({length: 6}, (_, i) => <line key={`v${i}`} x1={300 + i * 260} x2={300 + i * 260} y1="235" y2="745" stroke={SILVER} strokeWidth="2" />)}
      </g>
      <polyline points={pts.slice(0, visible).map(([x, y]) => `${x},${y}`).join(' ')} fill="none" stroke={mode === 'crash' ? RED : GOLD} strokeWidth="10" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={1180} cy={330} r={18} fill={GOLD} opacity="0.95" />
      <text x="1180" y="282" fill={GOLD} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">~$9B</text>
      {mode === 'crash' ? (
        <g opacity={Math.min(1, crash * 1.3)}>
          <circle cx={1560} cy={735} r={20} fill={RED} />
          <text x="1560" y="812" fill={WHITE} fontFamily={BRAND.font.display} fontSize="74" textAnchor="middle">$0</text>
          <path d="M 1440 632 L 1560 735 L 1515 600" fill="none" stroke={RED} strokeWidth="6" opacity="0.8" />
        </g>
      ) : (
        <text x="1530" y="220" fill={GOLD} fontFamily={BRAND.font.display} fontSize="54" textAnchor="middle">VALUATION</text>
      )}
    </svg>
  );
};

const ArrowFlip: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const turn = spring({frame: frame - Math.round(1.0 * fps), fps, config: {damping: 16, stiffness: 80}});
  const angle = interpolate(turn, [0, 1], [0, 180]);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{display: 'flex', gap: 50, alignItems: 'center', marginTop: 150}}>
        <Panel title="STATE" sub="searches, tracks, takes" color={BLUE} />
        <div style={{fontFamily: BRAND.font.display, color: GOLD, fontSize: 150, transform: `rotateY(${angle}deg)`}}>{'->'}</div>
        <Panel title="ONE PERSON" sub="words reach everyone" color={GOLD} />
      </div>
    </AbsoluteFill>
  );
};

const Panel: React.FC<{title: string; sub: string; color: string}> = ({title, sub, color}) => (
  <div style={{width: 420, minHeight: 210, border: `3px solid ${color}`, background: '#020409CC', padding: 28}}>
    <div style={{fontFamily: BRAND.font.display, color, fontSize: 58, textTransform: 'uppercase'}}>{title}</div>
    <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 26, marginTop: 14}}>{sub}</div>
  </div>
);

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string; leftColor?: string; rightColor?: string}> = ({
  left,
  right,
  leftSub,
  rightSub,
  leftColor = BLUE,
  rightColor = GOLD,
}) => (
  <div style={{position: 'absolute', left: 220, right: 220, top: 380, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 44}}>
    {[
      {title: left, sub: leftSub, color: leftColor},
      {title: right, sub: rightSub, color: rightColor},
    ].map((item) => (
      <div key={item.title} style={{minHeight: 250, border: `3px solid ${item.color}`, background: '#020409D8', padding: 32, boxShadow: `0 14px 42px #00000088`}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 54, lineHeight: 0.98, color: item.color, textTransform: 'uppercase'}}>{item.title}</div>
        {item.sub ? <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: SILVER, marginTop: 18}}>{item.sub}</div> : null}
      </div>
    ))}
  </div>
);

const Doors: React.FC<{labels: string[]}> = ({labels}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', left: 210, right: 210, top: 355, display: 'grid', gridTemplateColumns: `repeat(${labels.length}, 1fr)`, gap: 22}}>
      {labels.map((label, i) => {
        const on = interpolate(frame, [i * 10, i * 10 + 18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <div key={label} style={{height: 250, opacity: on, transform: `translateY(${(1 - on) * 26}px)`, border: `3px solid ${i === 0 ? GOLD : `${SILVER}66`}`, background: '#05070AD9', padding: 22}}>
            <div style={{height: 5, width: '62%', background: i === 0 ? GOLD : BLUE, marginBottom: 24}} />
            <div style={{fontFamily: BRAND.font.display, fontSize: 38, color: i === 0 ? GOLD : WHITE, textTransform: 'uppercase', lineHeight: 1.02}}>{label}</div>
          </div>
        );
      })}
    </div>
  );
};

const AuthorityStack: React.FC = () => {
  const frame = useCurrentFrame();
  const lens = interpolate(frame, [20, 130], [1.35, 0.58], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <Doors labels={['former statesmen', 'military leaders', 'famous believers', 'valuation']} />
      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        <g transform={`translate(1320 660) scale(${lens})`}>
          <circle cx="0" cy="0" r="88" fill="none" stroke={GOLD} strokeWidth="10" />
          <line x1="62" y1="62" x2="150" y2="150" stroke={GOLD} strokeWidth="12" strokeLinecap="round" />
          <text x="0" y="14" fill={WHITE} fontFamily={BRAND.font.display} fontSize="34" textAnchor="middle">VERIFY</text>
        </g>
      </svg>
    </>
  );
};

const NeedleBox: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <g transform="translate(250 400)">
      <circle cx="145" cy="165" r="42" fill={RED} opacity="0.86" />
      <path d="M145 212 C102 260, 188 260, 145 212" fill={RED} opacity="0.72" />
      <text x="145" y="310" fill={WHITE} fontFamily={BRAND.font.display} fontSize="42" textAnchor="middle">one drop</text>
    </g>
    <g transform="translate(760 470)">
      <line x1="0" y1="80" x2="440" y2="80" stroke={SILVER} strokeWidth="12" strokeLinecap="round" />
      <line x1="365" y1="80" x2="490" y2="30" stroke={SILVER} strokeWidth="5" />
      <rect x="70" y="120" width="260" height="70" rx="22" fill={`${BLUE}33`} stroke={SILVER} strokeWidth="4" />
      <text x="200" y="245" fill={WHITE} fontFamily={BRAND.font.display} fontSize="42" textAnchor="middle">needle + vial</text>
    </g>
    <g transform="translate(1210 350)">
      <rect x="0" y="0" width="360" height="300" rx="24" fill="#030509" stroke={GOLD} strokeWidth="4" />
      <rect x="48" y="60" width="264" height="64" rx="12" fill={`${SILVER}22`} />
      <text x="180" y="188" fill={GOLD} fontFamily={BRAND.font.display} fontSize="44" textAnchor="middle">BLACK BOX</text>
      <text x="180" y="238" fill={SILVER} fontFamily={BRAND.font.body} fontSize="24" textAnchor="middle">symbolic, not the real device</text>
    </g>
  </svg>
);

const MachineSwap: React.FC = () => {
  const frame = useCurrentFrame();
  const swap = interpolate(frame, [45, 105], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <>
      <TwoColumn left="Own device" right="Commercial machines" leftSub="the story sold" rightSub="what the investigation reported" leftColor={SILVER} rightColor={GOLD} />
      <svg width="1920" height="1080" style={{position: 'absolute'}}>
        <path d="M 850 535 C 930 470, 995 470, 1070 535" fill="none" stroke={GOLD} strokeWidth="8" strokeLinecap="round" strokeDasharray="18 12" opacity={0.8} />
        <polygon points={`${1066 + swap * 35},535 ${1016 + swap * 35},506 ${1016 + swap * 35},564`} fill={GOLD} />
      </svg>
    </>
  );
};

const DiagnosisChain: React.FC = () => {
  const frame = useCurrentFrame();
  const items = ['wrong number', 'wrong decision', 'real consequence'];
  return (
    <div style={{position: 'absolute', left: 230, right: 230, top: 425, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 34}}>
      {items.map((item, i) => {
        const on = interpolate(frame, [i * 22, i * 22 + 16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <div key={item} style={{opacity: on, minHeight: 180, border: `3px solid ${i === 2 ? GOLD : BLUE}`, background: '#020409D8', padding: 28}}>
            <div style={{fontFamily: BRAND.font.display, fontSize: 46, color: i === 2 ? GOLD : WHITE, textTransform: 'uppercase'}}>{item}</div>
          </div>
        );
      })}
    </div>
  );
};

const DefinitionCard: React.FC = () => (
  <div style={{position: 'absolute', left: 260, right: 260, top: 330, border: `4px solid ${GOLD}`, background: '#03060BE8', padding: 42, textAlign: 'center'}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: 92, color: GOLD, textTransform: 'uppercase'}}>criminal fraud</div>
    <div style={{fontFamily: BRAND.font.body, fontSize: 38, color: WHITE, marginTop: 28}}>knowingly false statement + reliance + value</div>
    <div style={{height: 4, width: 540, margin: '30px auto', background: GOLD}} />
    <div style={{fontFamily: BRAND.font.body, fontSize: 32, color: SILVER}}>Failure alone is not enough.</div>
  </div>
);

const VerdictBoard: React.FC<{mode: 'guilty' | 'split'}> = ({mode}) => {
  const frame = useCurrentFrame();
  const guiltyRows = ['conspiracy - investors', 'wire fraud - investor 1', 'wire fraud - investor 2', 'wire fraud - investor 3'];
  const splitRows = [
    {label: 'patient counts', value: 'ACQUITTED', color: GREEN},
    {label: 'three investor counts', value: 'NO VERDICT', color: BLUE},
  ];
  return (
    <div style={{position: 'absolute', left: 250, right: 250, top: 255, background: '#020409E8', border: `4px solid ${mode === 'guilty' ? GOLD : SILVER}`, padding: 28, boxShadow: `0 18px 70px #000000AA`}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', borderBottom: `2px solid ${GOLD}88`, paddingBottom: 16, marginBottom: 18}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 54, color: WHITE}}>JAN 3, 2022 VERDICT</div>
        <div style={{fontFamily: BRAND.font.body, fontSize: 22, color: SILVER}}>count by count</div>
      </div>
      {mode === 'guilty' ? (
        guiltyRows.map((row, i) => {
          const on = interpolate(frame, [20 + i * 20, 36 + i * 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return (
            <div key={row} style={{display: 'grid', gridTemplateColumns: '1fr 270px', gap: 24, alignItems: 'center', opacity: on, margin: '13px 0'}}>
              <div style={{fontFamily: BRAND.font.body, fontSize: 29, color: WHITE, textTransform: 'uppercase'}}>{row}</div>
              <div style={{fontFamily: BRAND.font.display, fontSize: 45, color: GOLD, textAlign: 'center', border: `3px solid ${GOLD}`, padding: '7px 12px'}}>GUILTY</div>
            </div>
          );
        })
      ) : (
        <>
          {splitRows.map((row, i) => {
            const on = interpolate(frame, [16 + i * 24, 34 + i * 24], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
            return (
              <div key={row.label} style={{display: 'grid', gridTemplateColumns: '1fr 330px', gap: 24, alignItems: 'center', opacity: on, margin: '20px 0'}}>
                <div style={{fontFamily: BRAND.font.body, fontSize: 32, color: WHITE, textTransform: 'uppercase'}}>{row.label}</div>
                <div style={{fontFamily: BRAND.font.display, fontSize: 43, color: row.color, textAlign: 'center', border: `3px solid ${row.color}`, padding: '9px 12px'}}>{row.value}</div>
              </div>
            );
          })}
          <div style={{fontFamily: BRAND.font.body, fontSize: 26, color: SILVER, marginTop: 28}}>Not guilty is not the same as exoneration; no patient count receives a GUILTY label.</div>
        </>
      )}
    </div>
  );
};

const BigNumber: React.FC<{top: string; bottom: string}> = ({top, bottom}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.25 * fps), fps, config: {damping: 14, stiffness: 90}});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{transform: `scale(${interpolate(enter, [0, 1], [0.86, 1])})`, opacity: Math.min(1, enter), textAlign: 'center'}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 180, color: GOLD, textShadow: '0 8px 40px #000'}}>{top}</div>
        <div style={{fontFamily: BRAND.font.body, fontSize: 38, color: WHITE, marginTop: 10}}>{bottom}</div>
      </div>
    </AbsoluteFill>
  );
};

const FakeItCard: React.FC = () => (
  <div style={{position: 'absolute', left: 250, right: 250, top: 360, textAlign: 'center'}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: 94, color: WHITE, textTransform: 'uppercase', textShadow: '0 5px 35px #000'}}>"Fake it till you make it"</div>
    <div style={{fontFamily: BRAND.font.body, fontSize: 36, color: GOLD, marginTop: 22}}>usually legal - until knowingly false facts are used to get reliance</div>
  </div>
);

const BoundaryEquation: React.FC = () => {
  const frame = useCurrentFrame();
  const parts = ['knowingly false', '+ relied upon', '= fraud'];
  return (
    <div style={{position: 'absolute', left: 160, right: 160, top: 415, display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 22, alignItems: 'center'}}>
      {parts.map((part, i) => {
        const on = interpolate(frame, [18 + i * 22, 36 + i * 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <div key={part} style={{opacity: on, minHeight: 165, border: `4px solid ${i === 2 ? GOLD : BLUE}`, background: '#020409E6', display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 20}}>
            <div style={{fontFamily: BRAND.font.display, fontSize: i === 2 ? 66 : 48, color: i === 2 ? GOLD : WHITE, textTransform: 'uppercase', textAlign: 'center', lineHeight: 0.98}}>{part}</div>
          </div>
        );
      })}
    </div>
  );
};

const SeriesTriptych: React.FC = () => {
  const rows = [
    ['stop', 'arrest'],
    ['identify', 'investigate'],
    ['promise', 'lie'],
  ];
  return (
    <div style={{position: 'absolute', left: 170, right: 170, top: 360, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 26}}>
      {rows.map(([a, b], i) => (
        <div key={a} style={{height: 280, border: `3px solid ${i === 2 ? GOLD : BLUE}`, background: '#020409D9', padding: 28}}>
          <div style={{fontFamily: BRAND.font.display, fontSize: 58, color: WHITE, textTransform: 'uppercase'}}>{a}</div>
          <div style={{height: 4, background: i === 2 ? GOLD : BLUE, margin: '22px 0'}} />
          <div style={{fontFamily: BRAND.font.display, fontSize: 58, color: i === 2 ? GOLD : SILVER, textTransform: 'uppercase'}}>{b}</div>
        </div>
      ))}
    </div>
  );
};

const SubscribeCTA: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 0.92 + 0.04 * Math.sin(frame * 0.08);
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{transform: `scale(${pulse})`, border: `4px solid ${GOLD}`, background: '#05070AE8', padding: '34px 58px', textAlign: 'center'}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 96, color: WHITE, textTransform: 'uppercase'}}>Subscribe</div>
        <div style={{fontFamily: BRAND.font.body, fontSize: 34, color: GOLD, marginTop: 10}}>one line at a time</div>
      </div>
    </AbsoluteFill>
  );
};

const SceneVisual: React.FC<{scene: BodyScene}> = ({scene}) => {
  const shot = getShot(scene.spanId);
  const baseMedia = shot.assetType === 'stock_video' ? <VideoPlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} /> : <ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} />;
  switch (scene.kind) {
    case 'valuationCrash':
      return <SceneShell scene={scene} media={<ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} dim={0.55} />}><ValuationGraph mode="crash" /></SceneShell>;
    case 'arrowFlip':
      return <SceneShell scene={scene} media={baseMedia}><ArrowFlip /></SceneShell>;
    case 'timeline2003':
      return <SceneShell scene={scene} media={baseMedia}><SceneArt visualMode="timeline" motifHint="document" onScreenText={['2003', 'startup promise']} seed={scene.spanId} /></SceneShell>;
    case 'needleBox':
      return <SceneShell scene={scene} media={baseMedia}><NeedleBox /></SceneShell>;
    case 'valuationRise':
      return <SceneShell scene={scene} media={<ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} dim={0.54} />}><ValuationGraph mode="rise" /><Doors labels={['prominent board', 'limited Walgreens', 'paper billionaire']} /></SceneShell>;
    case 'authority':
      return <SceneShell scene={scene} media={baseMedia}><AuthorityStack /></SceneShell>;
    case 'story':
      return <SceneShell scene={scene} media={baseMedia}><TwoColumn left="Product" right="Story" leftSub="questions remain" rightSub="prestige fills the silence" /></SceneShell>;
    case 'timeline2015':
      return <SceneShell scene={scene} media={baseMedia}><SceneArt visualMode="timeline" motifHint="document" onScreenText={['2015', 'investigation']} seed={scene.spanId} /></SceneShell>;
    case 'machineSwap':
      return <SceneShell scene={scene} media={baseMedia}><MachineSwap /></SceneShell>;
    case 'diagnosisChain':
      return <SceneShell scene={scene} media={baseMedia}><DiagnosisChain /></SceneShell>;
    case 'secCollapse':
      return <SceneShell scene={scene} media={<ImagePlate spanId={scene.spanId} duration={scene.dur} seed={scene.spanId} dim={0.54} />}><SceneArt visualMode="timeline" motifHint="document" onScreenText={['2018', 'civil settlement', 'no admission']} seed={`${scene.spanId}-sec`} /><ValuationGraph mode="crash" /></SceneShell>;
    case 'failureFraud':
      return <SceneShell scene={scene} media={baseMedia}><TwoColumn left="Failure" right="Fraud" leftSub="hard thing collapses" rightSub="intent to deceive" /></SceneShell>;
    case 'definition':
      return <SceneShell scene={scene} media={baseMedia}><SceneArt visualMode="object" motifHint="scales" onScreenText={['intent', 'reliance']} seed={scene.spanId} /><DefinitionCard /></SceneShell>;
    case 'trialSplit':
      return <SceneShell scene={scene} media={baseMedia}><TwoColumn left="Prosecution" right="Defense" leftSub="she knew" rightSub="a true believer" /></SceneShell>;
    case 'verdictGuilty':
      return <SceneShell scene={scene} media={baseMedia}><SceneArt visualMode="timeline" motifHint="document" onScreenText={['2022', 'verdict']} seed={scene.spanId} /><VerdictBoard mode="guilty" /></SceneShell>;
    case 'verdictSplit':
      return <SceneShell scene={scene} media={baseMedia}><VerdictBoard mode="split" /></SceneShell>;
    case 'acquittalNuance':
      return <SceneShell scene={scene} media={baseMedia}><TwoColumn left="Acquittal" right="Balwani" leftSub="not proven beyond a reasonable doubt" rightSub="convicted on all 12" leftColor={GREEN} rightColor={GOLD} /></SceneShell>;
    case 'sentence':
      return <SceneShell scene={scene} media={baseMedia}><BigNumber top="~11y 3m" bottom="135 months in federal prison" /></SceneShell>;
    case 'fakeIt':
      return <SceneShell scene={scene} media={baseMedia}><FakeItCard /></SceneShell>;
    case 'boundaryEquation':
      return <SceneShell scene={scene} media={baseMedia}><BoundaryEquation /></SceneShell>;
    case 'stakes':
      return <SceneShell scene={scene} media={baseMedia}><TwoColumn left="failed app" right="wrong blood test" leftSub="money loss" rightSub="diagnosis risk" /></SceneShell>;
    case 'seriesTriptych':
      return <SceneShell scene={scene} media={baseMedia}><SeriesTriptych /></SceneShell>;
    case 'lineRedrawn':
      return <SceneShell scene={scene} media={baseMedia}><BoundaryEquation /></SceneShell>;
    case 'subscribe':
      return <SceneShell scene={scene} media={baseMedia}><SubscribeCTA /></SceneShell>;
    default:
      return <SceneShell scene={scene} media={baseMedia} />;
  }
};

const HookBeat: React.FC<{spanId: string; label: string; from: number; dur: number; kind?: 'image' | 'video'}> = ({spanId, label, dur, kind}) => {
  const media = kind === 'video' ? <VideoPlate spanId={spanId} duration={dur} seed={`hook-${spanId}`} /> : <ImagePlate spanId={spanId} duration={dur} seed={`hook-${spanId}`} dim={0.56} />;
  const frame = useCurrentFrame();
  const pop = spring({frame, fps: FPS, config: {damping: 16, stiffness: 120}});
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {media}
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${INK}E8 0%, ${INK}A8 48%, #00000022 100%)`}} />
      <LightSweep seed={`hook-${spanId}`} color={GOLD} />
      <Particles seed={`hook-${spanId}`} count={18} color={GOLD} />
      <div style={{position: 'absolute', left: 74, top: 60, fontFamily: BRAND.font.body, color: GOLD, fontWeight: 900, fontSize: 18, letterSpacing: '0.1em'}}>SERIES FINALE</div>
      <div style={{position: 'absolute', left: 74, top: 92, width: 260, height: 3, background: GOLD}} />
      <div style={{position: 'absolute', left: 78, bottom: 150, maxWidth: 1160, fontFamily: BRAND.font.display, color: WHITE, fontSize: 74, lineHeight: 0.94, textTransform: 'uppercase', textShadow: '0 5px 30px #000', opacity: Math.min(1, pop), transform: `translateY(${interpolate(pop, [0, 1], [22, 0])}px)`}}>
        {label}
      </div>
      <Vignette strength={1} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};

const HookMontage: React.FC = () => {
  const beats = [
    {spanId: 'SPN-0001', label: 'A drop. A valuation. A collapse.', from: 0, dur: 1.8},
    {spanId: 'SPN-0013', label: 'Four investor counts: guilty.', from: 1.8, dur: 1.9},
    {spanId: 'SPN-0014', label: 'Patients: acquitted. Three: no verdict.', from: 3.7, dur: 1.8},
    {spanId: 'SPN-0016', label: '~11 years, 3 months.', from: 5.5, dur: 1.5},
  ];
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {beats.map((beat) => (
        <Sequence key={beat.spanId} from={Math.round(beat.from * FPS)} durationInFrames={Math.round(beat.dur * FPS)}>
          <HookBeat {...beat} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const Bridge: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const fade = interpolate(frame, [0, durationInFrames], [1, 0.24], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: INK, opacity: fade}}>
      <LightSweep seed="theranos-bridge" color={GOLD} />
      <Particles seed="theranos-bridge" color={GOLD} count={20} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 520, textAlign: 'center', fontFamily: BRAND.font.display, color: GOLD, fontSize: 48, textTransform: 'uppercase'}}>
        where is the line?
      </div>
      <Vignette strength={1} />
    </AbsoluteFill>
  );
};

export const TheranosPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Sequence from={0} durationInFrames={Math.round(HOOK_MONTAGE_SEC * FPS)} name="PART_HOOK_MONTAGE">
      <HookMontage />
    </Sequence>
    <Sequence from={Math.round(HOOK_MONTAGE_SEC * FPS)} durationInFrames={Math.round(BRIDGE_SEC * FPS)} name="PART_BRIDGE">
      <Bridge />
    </Sequence>
    <Sequence from={Math.round((HOOK_MONTAGE_SEC + BRIDGE_SEC) * FPS)} durationInFrames={Math.round(OPENING_SEC * FPS)} name="PART_OPENING">
      <BrandOpening seriesLabel="Prime Documentary" title="Theranos" subtitle="When a promise becomes a crime" />
    </Sequence>
    {BODY_SCENES.map((scene) => (
      <Sequence key={scene.spanId} from={Math.round((CONTENT_START_SEC + scene.start) * FPS)} durationInFrames={Math.round(scene.dur * FPS)} name={`${scene.chapter}_${scene.spanId}`}>
        <SceneVisual scene={scene} />
      </Sequence>
    ))}
    <Sequence from={Math.round((CONTENT_START_SEC + BODY_SEC) * FPS)} durationInFrames={Math.round(ENDCARD_SEC * FPS)} name="PART_ENDCARD">
      <BrandEndcard />
    </Sequence>
    <Audio src={staticFile(MIX_SRC)} />
    <CaptionBand />
  </AbsoluteFill>
);

export const theranosPremiumDurationInFrames = (fps: number = FPS): number => Math.round(TOTAL_SEC * fps);
