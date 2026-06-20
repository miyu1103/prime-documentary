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

const TOTAL_SEC = 646;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Mode =
  | 'hook'
  | 'phone'
  | 'map'
  | 'evidence'
  | 'stamp'
  | 'type'
  | 'split'
  | 'logic'
  | 'wallet'
  | 'cloud'
  | 'secure'
  | 'court'
  | 'quote'
  | 'booth'
  | 'apps'
  | 'trail'
  | 'end';

type Scene = {
  id: string;
  start: number;
  dur: number;
  mode: Mode;
  title: string;
  subtitle?: string;
  kicker: string;
  image?: string;
  citation?: string;
  text?: string[];
  recon?: boolean;
};

const scenes: Scene[] = [
  {id: 'S001', start: 0, dur: 28, mode: 'hook', title: 'Can they search your phone?', kicker: 'HOOK', image: 'riley/PD-2026-007-S001-IMG-001.v001.png', text: ['Can they search your phone?'], recon: true},
  {id: 'S002', start: 28, dur: 44, mode: 'phone', title: "A phone is not an object. It's a window.", kicker: 'OPENING', text: ['photos', 'messages', 'maps', 'searches', 'cloud']},
  {id: 'S003', start: 72, dur: 22, mode: 'map', title: 'San Diego - 2009', kicker: 'ACT I', citation: 'CLM-0006', recon: true},
  {id: 'S004', start: 94, dur: 22, mode: 'evidence', title: 'Phone taken from pocket', subtitle: 'Car search. Firearms. Arrest.', kicker: 'ACT I', citation: 'CLM-0006', recon: true},
  {id: 'S005', start: 116, dur: 32, mode: 'stamp', title: 'Searched twice. No warrant.', kicker: 'ACT I', citation: 'CLM-0006', text: ['PHONE SEARCH', 'NO WARRANT'], recon: true},
  {id: 'S006', start: 148, dur: 18, mode: 'type', title: 'Traffic stop -> shooting case', kicker: 'ACT I'},
  {id: 'S007', start: 166, dur: 28, mode: 'split', title: 'Riley v. California + United States v. Wurie', kicker: 'ACT I', citation: 'CLM-0001 / CLM-0007', text: ['Riley', 'Wurie']},
  {id: 'S008', start: 194, dur: 12, mode: 'type', title: 'Search incident to arrest', kicker: 'ACT II'},
  {id: 'S009', start: 206, dur: 32, mode: 'logic', title: '1) Officer safety  2) Preserve evidence', kicker: 'ACT II', text: ['officer safety', 'preserve evidence']},
  {id: 'S010', start: 238, dur: 23, mode: 'wallet', title: 'If a wallet, why not a phone?', kicker: 'ACT II', text: ['wallet', 'phone']},
  {id: 'S011', start: 261, dur: 30, mode: 'wallet', title: 'Wallet vs. smartphone', kicker: 'ACT II', text: ['wallet', 'smartphone']},
  {id: 'S012', start: 291, dur: 24, mode: 'cloud', title: 'Half in your pocket, half in the cloud', kicker: 'ACT II'},
  {id: 'S013', start: 315, dur: 26, mode: 'secure', title: 'Data is not a weapon', subtitle: 'Secure the device', kicker: 'ACT II'},
  {id: 'S014', start: 341, dur: 26, mode: 'court', title: '2014 / 9-0 result', subtitle: 'Riley v. California, 573 U.S. 373', kicker: 'ACT III', citation: 'CLM-0002'},
  {id: 'S015', start: 367, dur: 25, mode: 'quote', title: '"the privacies of life"', kicker: 'ACT III', citation: 'CLM-0003'},
  {id: 'S016', start: 392, dur: 24, mode: 'logic', title: 'More revealing than a house', kicker: 'ACT III', text: ['home', 'phone']},
  {id: 'S017', start: 416, dur: 20, mode: 'quote', title: '"Get a warrant."', kicker: 'ACT III', citation: 'CLM-0001'},
  {id: 'S018', start: 436, dur: 27, mode: 'booth', title: 'Katz v. United States (1967): people, not places', kicker: 'ACT III'},
  {id: 'S019', start: 463, dur: 18, mode: 'phone', title: 'One rule for the phone category', kicker: 'ACT III'},
  {id: 'S020', start: 481, dur: 10, mode: 'type', title: 'Exception: true emergencies', kicker: 'ACT III'},
  {id: 'S021', start: 491, dur: 26, mode: 'secure', title: 'Contents protected', subtitle: 'Warrant, consent, emergency', kicker: 'ACT III'},
  {id: 'S022', start: 517, dur: 28, mode: 'apps', title: 'A phone can reveal a life', kicker: 'ACT IV', text: ['calendar', 'photos', 'banking', 'health', 'messages', 'search']},
  {id: 'S023', start: 545, dur: 24, mode: 'trail', title: 'Automatic records', kicker: 'ACT IV'},
  {id: 'S024', start: 569, dur: 12, mode: 'split', title: 'Inside the phone vs. the trail it leaves', kicker: 'ACT IV', text: ['inside', 'trail']},
  {id: 'S025', start: 581, dur: 22, mode: 'quote', title: 'For that, police need a warrant.', kicker: 'ACT IV'},
  {id: 'S026', start: 603, dur: 16, mode: 'split', title: 'Chosen contents | Automatic records', kicker: 'ENDING', text: ['chosen contents', 'automatic records']},
  {id: 'S027', start: 619, dur: 21, mode: 'trail', title: "Next: your phone is tracking you", kicker: 'NEXT'},
  {id: 'S028', start: 640, dur: 6, mode: 'end', title: 'Prime Documentary', subtitle: 'Subscribe', kicker: 'END'},
];

const fitTitle = (text: string): number => Math.min(82, Math.max(38, 1380 / Math.max(text.length, 15)));

const ReconstructionLabel: React.FC = () => (
  <div style={{
    position: 'absolute',
    right: 54,
    top: 48,
    fontFamily: BRAND.font.body,
    fontSize: 18,
    color: SILVER,
    padding: '7px 11px',
    border: `1px solid ${GOLD}88`,
    background: '#000000A8',
    letterSpacing: 0,
  }}>
    symbolic reconstruction
  </div>
);

const LowerThird: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.mode === 'end') return null;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.14 * fps), fps, config: {damping: 19, stiffness: 90}});
  return (
    <div style={{position: 'absolute', left: 58, top: 48, opacity: Math.min(1, enter), maxWidth: 1340}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800, letterSpacing: 0}}>{scene.kicker}</div>
      <div style={{width: 310, height: 2, background: GOLD, marginTop: 9, marginBottom: 21}} />
      <div style={{
        fontFamily: BRAND.font.display,
        fontSize: fitTitle(scene.title),
        color: WHITE,
        textTransform: 'uppercase',
        lineHeight: 0.95,
        textShadow: '0 5px 30px #000',
        letterSpacing: 0,
      }}>{scene.title}</div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 12, maxWidth: 1080, letterSpacing: 0}}>{scene.subtitle}</div> : null}
      {scene.id === 'S014' ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 20, color: SILVER, marginTop: 12, maxWidth: 1080, letterSpacing: 0}}>
          Result unanimous; Alito concurred in part and in the judgment.
        </div>
      ) : null}
      {scene.citation ? (
        <div style={{fontFamily: BRAND.font.body, fontSize: 19, color: GOLD, marginTop: 15, background: '#000000AA', padding: '7px 11px', display: 'inline-block', letterSpacing: 0}}>
          {scene.citation}
        </div>
      ) : null}
    </div>
  );
};

const Shell: React.FC<{scene: Scene; children: React.ReactNode}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const scale = 1.015 + p * 0.055;
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
              transform: `scale(${scale}) translateY(${p * -18}px)`,
              filter: 'brightness(0.58) contrast(1.18) saturate(0.95)',
            }}
          />
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{background: `radial-gradient(90% 70% at 64% 34%, #14345f 0%, ${NAVY} 35%, ${INK} 84%)`}} />
      )}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}E8 0%, #00000016 43%, ${INK}F4 100%)`}} />
      <LightSweep seed={scene.id} color={scene.mode === 'court' || scene.mode === 'quote' ? GOLD : BLUE} />
      <Particles seed={scene.id} count={scene.image ? 18 : 28} color={scene.mode === 'court' ? GOLD : BLUE} />
      {children}
      <LowerThird scene={scene} />
      {scene.recon ? <ReconstructionLabel /> : null}
      <Vignette strength={1} />
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

const PhoneFrame: React.FC<{x: number; y: number; w: number; h: number; glow?: string}> = ({x, y, w, h, glow = BLUE}) => (
  <div style={{
    position: 'absolute',
    left: x,
    top: y,
    width: w,
    height: h,
    borderRadius: 44,
    border: `5px solid ${SILVER}66`,
    background: '#02040A',
    boxShadow: `0 0 48px ${glow}88, inset 0 0 26px #ffffff18`,
  }}>
    <div style={{position: 'absolute', left: w * 0.4, top: 18, width: w * 0.2, height: 8, borderRadius: 8, background: `${SILVER}66`}} />
  </div>
);

const HookGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = interpolate(Math.sin(frame / 11), [-1, 1], [0.55, 1]);
  return (
    <>
      <PhoneFrame x={785} y={285} w={360} h={520} glow={BLUE} />
      <div style={{position: 'absolute', left: 865, top: 430, width: 200, height: 200, border: `4px solid ${GOLD}`, borderRadius: 100, opacity: pulse}} />
      <div style={{position: 'absolute', left: 934, top: 482, fontFamily: BRAND.font.display, fontSize: 86, color: GOLD, textShadow: `0 0 26px ${GOLD}`}}>?</div>
    </>
  );
};

const PhoneWindow: React.FC<{scene: Scene}> = ({scene}) => {
  const labels = scene.text ?? ['photos', 'messages', 'maps', 'cloud'];
  const frame = useCurrentFrame();
  return (
    <>
      <PhoneFrame x={780} y={230} w={360} h={580} glow={BLUE} />
      {labels.map((label, i) => {
        const delay = i * 12;
        const lift = spring({frame: frame - delay, fps: 30, config: {damping: 17, stiffness: 70}});
        return (
          <div key={label} style={{
            position: 'absolute',
            left: 500 + (i % 3) * 310,
            top: 390 + Math.floor(i / 3) * 130 - lift * 38,
            width: 250,
            height: 76,
            border: `2px solid ${i % 2 ? GOLD : BLUE}`,
            background: '#000000AA',
            color: i % 2 ? GOLD : WHITE,
            fontFamily: BRAND.font.body,
            fontSize: 30,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            opacity: Math.min(1, lift),
            letterSpacing: 0,
          }}>{label}</div>
        );
      })}
    </>
  );
};

const MapGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const p = spring({frame, fps: 30, config: {damping: 18, stiffness: 75}});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {Array.from({length: 9}, (_, i) => <line key={`h${i}`} x1="300" x2="1620" y1={270 + i * 64} y2={270 + i * 64} stroke={SILVER} strokeWidth="2" opacity="0.13" />)}
      {Array.from({length: 12}, (_, i) => <line key={`v${i}`} x1={340 + i * 110} x2={340 + i * 110} y1="230" y2="815" stroke={SILVER} strokeWidth="2" opacity="0.11" />)}
      <path d="M520 710 C680 540 790 610 900 460 C1020 300 1170 440 1370 330" fill="none" stroke={BLUE} strokeWidth="12" opacity="0.75" strokeLinecap="round" />
      <circle cx={980} cy={500} r={26 + p * 26} fill="none" stroke={GOLD} strokeWidth="6" opacity={0.9 - p * 0.3} />
      <circle cx="980" cy="500" r="16" fill={GOLD} />
      <text x="1018" y="509" fill={WHITE} fontFamily={BRAND.font.body} fontSize="28">roadside stop</text>
    </svg>
  );
};

const EvidenceGraphic: React.FC = () => (
  <>
    <div style={{position: 'absolute', left: 520, top: 435, width: 880, height: 310, background: '#02040ACC', border: `2px solid ${SILVER}44`, transform: 'rotate(-2deg)'}} />
    <div style={{position: 'absolute', left: 650, top: 500, width: 360, height: 150, border: `3px solid ${GOLD}`, background: '#000000AA', transform: 'rotate(3deg)'}}>
      <div style={{fontFamily: BRAND.font.display, color: GOLD, fontSize: 42, margin: 20, letterSpacing: 0}}>EVIDENCE</div>
      <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 24, marginLeft: 22, letterSpacing: 0}}>symbolic reconstruction</div>
    </div>
    <PhoneFrame x={1080} y={438} w={190} h={286} glow={GOLD} />
  </>
);

const StampGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const slam = spring({frame: frame - 34, fps: 30, config: {damping: 10, stiffness: 170}});
  return (
    <>
      <EvidenceGraphic />
      <div style={{
        position: 'absolute',
        left: 690,
        top: 460,
        width: 560,
        height: 150,
        border: `8px solid ${GOLD}`,
        color: GOLD,
        fontFamily: BRAND.font.display,
        fontSize: 62,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `rotate(-10deg) scale(${0.72 + slam * 0.28})`,
        opacity: Math.min(1, slam),
        background: '#00000055',
        letterSpacing: 0,
      }}>{scene.text?.[1] ?? 'NO WARRANT'}</div>
    </>
  );
};

const TypeWall: React.FC<{scene: Scene}> = ({scene}) => (
  <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 140}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: fitTitle(scene.title) + 24, color: WHITE, lineHeight: 0.93, textAlign: 'center', textTransform: 'uppercase', textShadow: `0 0 38px ${BLUE}77`, letterSpacing: 0}}>
      {scene.title}
    </div>
  </div>
);

const SplitGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const labels = scene.text ?? ['left', 'right'];
  return (
    <div style={{position: 'absolute', left: 390, right: 170, top: 390, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 48}}>
      {labels.slice(0, 2).map((label, i) => (
        <div key={label} style={{height: 230, border: `3px solid ${i ? GOLD : BLUE}`, background: '#0000009C', padding: 30, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{fontFamily: BRAND.font.display, fontSize: 56, color: i ? GOLD : WHITE, textTransform: 'uppercase', textAlign: 'center', letterSpacing: 0}}>{label}</div>
        </div>
      ))}
    </div>
  );
};

const LogicGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const labels = scene.text ?? ['reason', 'rule'];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <rect x="430" y="410" width="420" height="210" fill="#00000099" stroke={BLUE} strokeWidth="4" />
      <rect x="1070" y="410" width="420" height="210" fill="#00000099" stroke={GOLD} strokeWidth="4" />
      <line x1="850" x2="1070" y1="515" y2="515" stroke={SILVER} strokeWidth="5" opacity="0.55" />
      <text x="640" y="520" textAnchor="middle" fill={WHITE} fontFamily={BRAND.font.display} fontSize="48">{labels[0]}</text>
      <text x="1280" y="520" textAnchor="middle" fill={GOLD} fontFamily={BRAND.font.display} fontSize="48">{labels[1] ?? 'rule'}</text>
      <text x="935" y="504" fill={SILVER} fontFamily={BRAND.font.body} fontSize="28">vs</text>
    </svg>
  );
};

const WalletGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const labels = scene.text ?? ['wallet', 'smartphone'];
  return (
    <>
      <div style={{position: 'absolute', left: 455, top: 438, width: 390, height: 230, borderRadius: 18, border: `4px solid ${GOLD}`, background: '#2c2110', boxShadow: `0 0 34px ${GOLD}55`}}>
        <div style={{position: 'absolute', left: 32, right: 32, top: 72, height: 5, background: `${GOLD}AA`}} />
        <div style={{fontFamily: BRAND.font.display, color: GOLD, fontSize: 48, margin: 42, letterSpacing: 0}}>{labels[0]}</div>
      </div>
      <PhoneFrame x={1080} y={330} w={280} h={450} glow={BLUE} />
      <div style={{position: 'absolute', left: 1115, top: 520, fontFamily: BRAND.font.display, fontSize: 44, color: WHITE, textTransform: 'uppercase', letterSpacing: 0}}>{labels[1]}</div>
      <div style={{position: 'absolute', left: 898, top: 510, fontFamily: BRAND.font.display, fontSize: 78, color: SILVER, letterSpacing: 0}}>vs</div>
    </>
  );
};

const CloudGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <rect x="770" y="350" width="260" height="390" rx="40" fill="#02040A" stroke={BLUE} strokeWidth="5" />
    <path d="M1160 470 C1180 405 1260 400 1298 450 C1365 440 1420 490 1420 555 C1420 625 1362 665 1290 665 L1125 665 C1065 665 1020 625 1020 568 C1020 514 1060 475 1160 470 Z" fill="#00000099" stroke={GOLD} strokeWidth="5" />
    {Array.from({length: 7}, (_, i) => <line key={i} x1={1028 + i * 16} y1={420 + i * 45} x2={1165 + i * 26} y2={500 + i * 20} stroke={i % 2 ? GOLD : BLUE} strokeWidth="4" opacity="0.8" />)}
    <text x="842" y="786" fill={SILVER} fontFamily={BRAND.font.body} fontSize="28">pocket</text>
    <text x="1188" y="723" fill={GOLD} fontFamily={BRAND.font.body} fontSize="28">cloud</text>
  </svg>
);

const SecureGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <rect x="800" y="315" width="320" height="500" rx="44" fill="#02040A" stroke={BLUE} strokeWidth="5" />
    <rect x="868" y="520" width="184" height="138" rx="14" fill="#000000" stroke={GOLD} strokeWidth="5" />
    <path d="M900 520 L900 472 C900 414 1020 414 1020 472 L1020 520" fill="none" stroke={GOLD} strokeWidth="14" strokeLinecap="round" />
    <circle cx="960" cy="586" r="18" fill={GOLD} />
    <line x1="960" x2="960" y1="604" y2="632" stroke={GOLD} strokeWidth="8" />
  </svg>
);

const CourtGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <polygon points="520,390 960,250 1400,390" fill="#000000AA" stroke={GOLD} strokeWidth="5" />
    {Array.from({length: 7}, (_, i) => <rect key={i} x={600 + i * 115} y="410" width="54" height="270" fill={SILVER} opacity="0.28" />)}
    <rect x="545" y="690" width="830" height="44" fill={GOLD} opacity="0.72" />
    {Array.from({length: 9}, (_, i) => <circle key={i} cx={720 + i * 60} cy="805" r="18" fill={BLUE} opacity="0.92" />)}
    <text x="1250" y="818" fill={GOLD} fontFamily={BRAND.font.display} fontSize="52">9-0</text>
  </svg>
);

const QuoteGraphic: React.FC<{scene: Scene}> = ({scene}) => (
  <div style={{position: 'absolute', left: 260, right: 260, top: 350, bottom: 220, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
    <div style={{fontFamily: BRAND.font.display, color: scene.id === 'S017' ? GOLD : WHITE, fontSize: scene.id === 'S017' ? 118 : 82, textAlign: 'center', lineHeight: 0.98, textTransform: 'uppercase', textShadow: `0 0 48px ${scene.id === 'S017' ? GOLD : BLUE}88`, letterSpacing: 0}}>
      {scene.title}
    </div>
  </div>
);

const BoothGraphic: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <rect x="760" y="265" width="400" height="585" fill="#07111F" stroke={SILVER} strokeWidth="5" />
    <rect x="808" y="325" width="304" height="170" fill="#0E2744" stroke={BLUE} strokeWidth="3" opacity="0.9" />
    <rect x="825" y="545" width="95" height="210" fill="#00000088" stroke={GOLD} strokeWidth="4" />
    <path d="M982 585 C1040 590 1064 620 1050 680" fill="none" stroke={SILVER} strokeWidth="10" strokeLinecap="round" />
    <text x="780" y="912" fill={GOLD} fontFamily={BRAND.font.body} fontSize="30">people, not places</text>
  </svg>
);

const AppsGraphic: React.FC<{scene: Scene}> = ({scene}) => {
  const labels = scene.text ?? ['calendar', 'photos', 'banking', 'health'];
  return (
    <div style={{position: 'absolute', left: 560, top: 315, width: 820, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 22}}>
      {labels.map((label, i) => (
        <div key={label} style={{height: 142, borderRadius: 22, border: `2px solid ${i % 2 ? GOLD : BLUE}`, background: '#000000A8', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 24px ${i % 2 ? GOLD : BLUE}44`}}>
          <div style={{fontFamily: BRAND.font.body, color: i % 2 ? GOLD : WHITE, fontSize: 28, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 0}}>{label}</div>
        </div>
      ))}
    </div>
  );
};

const TrailGraphic: React.FC = () => {
  const frame = useCurrentFrame();
  const dots = Math.min(10, Math.floor(interpolate(frame, [0, 220], [1, 10], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M430 745 C610 575 730 645 875 500 C1030 345 1170 530 1430 330" fill="none" stroke={BLUE} strokeWidth="10" strokeLinecap="round" strokeDasharray="18 22" opacity="0.78" />
      {Array.from({length: dots}, (_, i) => {
        const x = 430 + i * 110;
        const y = 745 - (i % 3) * 95 - i * 18;
        return <circle key={i} cx={x} cy={y} r={14} fill={i === dots - 1 ? GOLD : BLUE} opacity="0.94" />;
      })}
      <rect x="1300" y="520" width="190" height="300" rx="28" fill="#02040A" stroke={GOLD} strokeWidth="4" />
    </svg>
  );
};

const EndGraphic: React.FC = () => (
  <AbsoluteFill style={{background: `radial-gradient(70% 70% at 50% 42%, #12345C 0%, ${NAVY} 38%, ${INK} 84%)`, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
    <div style={{textAlign: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 96, textTransform: 'uppercase', letterSpacing: 0}}>Prime Documentary</div>
      <div style={{fontFamily: BRAND.font.body, color: GOLD, fontSize: 34, marginTop: 16, fontWeight: 800, letterSpacing: 0}}>Subscribe</div>
    </div>
    <Grain opacity={0.05} />
  </AbsoluteFill>
);

const SceneBody: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.mode === 'end') return <EndGraphic />;
  return (
    <Shell scene={scene}>
      {scene.mode === 'hook' ? <HookGraphic /> : null}
      {scene.mode === 'phone' ? <PhoneWindow scene={scene} /> : null}
      {scene.mode === 'map' ? <MapGraphic /> : null}
      {scene.mode === 'evidence' ? <EvidenceGraphic /> : null}
      {scene.mode === 'stamp' ? <StampGraphic scene={scene} /> : null}
      {scene.mode === 'type' ? <TypeWall scene={scene} /> : null}
      {scene.mode === 'split' ? <SplitGraphic scene={scene} /> : null}
      {scene.mode === 'logic' ? <LogicGraphic scene={scene} /> : null}
      {scene.mode === 'wallet' ? <WalletGraphic scene={scene} /> : null}
      {scene.mode === 'cloud' ? <CloudGraphic /> : null}
      {scene.mode === 'secure' ? <SecureGraphic /> : null}
      {scene.mode === 'court' ? <CourtGraphic /> : null}
      {scene.mode === 'quote' ? <QuoteGraphic scene={scene} /> : null}
      {scene.mode === 'booth' ? <BoothGraphic /> : null}
      {scene.mode === 'apps' ? <AppsGraphic scene={scene} /> : null}
      {scene.mode === 'trail' ? <TrailGraphic /> : null}
    </Shell>
  );
};

export const RileyPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    {scenes.map((scene) => (
      <Sequence key={scene.id} from={Math.round(scene.start * BRAND.video.fps)} durationInFrames={Math.round(scene.dur * BRAND.video.fps)} name={scene.id}>
        <SceneBody scene={scene} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

export const rileyPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
