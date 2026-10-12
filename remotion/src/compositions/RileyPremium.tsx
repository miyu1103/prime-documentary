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
import {BrandEndcard, BrandOpening, OPENING_SEC} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';
import {rileyV004PlateCount, rileyV004Plates} from '../data/riley_v004_plates';

const TOTAL_SEC = 646;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

type Mode =
  | 'hook'
  | 'still'
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
  {id: 'S001', start: 0, dur: 28, mode: 'hook', title: 'Can they search your phone?', kicker: 'HOOK', image: 'riley/PD-2026-007-S001-IMG-001.v003.png', text: ['Can they search your phone?'], recon: true},
  {id: 'S002', start: 28, dur: 44, mode: 'still', title: "A phone is not an object. It's a window.", kicker: 'OPENING', image: 'riley/PD-2026-007-S002-IMG-001.v003.png', text: ['photos', 'messages', 'maps', 'searches', 'cloud']},
  {id: 'S003', start: 72, dur: 22, mode: 'still', title: 'San Diego - 2009', kicker: 'ACT I', image: 'riley/PD-2026-007-S003-IMG-001.v003.png', citation: 'CLM-0006', recon: true},
  {id: 'S004', start: 94, dur: 22, mode: 'still', title: 'Phone taken from pocket', subtitle: 'Car search. Firearms. Arrest.', kicker: 'ACT I', image: 'riley/PD-2026-007-S001-IMG-001.v003.png', citation: 'CLM-0006', recon: true},
  {id: 'S005', start: 116, dur: 32, mode: 'stamp', title: 'Searched twice. No warrant.', kicker: 'ACT I', image: 'riley/PD-2026-007-S017-IMG-001.v003.png', citation: 'CLM-0006', text: ['PHONE SEARCH', 'NO WARRANT'], recon: true},
  {id: 'S006', start: 148, dur: 18, mode: 'type', title: 'Traffic stop -> shooting case', kicker: 'ACT I'},
  {id: 'S007', start: 166, dur: 28, mode: 'still', title: 'Riley v. California + United States v. Wurie', kicker: 'ACT I', image: 'riley/PD-2026-007-S017-IMG-001.v003.png', citation: 'CLM-0001 / CLM-0007', text: ['Riley', 'Wurie']},
  {id: 'S008', start: 194, dur: 12, mode: 'type', title: 'Search incident to arrest', kicker: 'ACT II'},
  {id: 'S009', start: 206, dur: 32, mode: 'logic', title: '1) Officer safety  2) Preserve evidence', kicker: 'ACT II', text: ['officer safety', 'preserve evidence']},
  {id: 'S010', start: 238, dur: 23, mode: 'still', title: 'If a wallet, why not a phone?', kicker: 'ACT II', image: 'riley/PD-2026-007-S002-IMG-001.v003.png', text: ['wallet', 'phone']},
  {id: 'S011', start: 261, dur: 30, mode: 'still', title: 'Wallet vs. smartphone', kicker: 'ACT II', image: 'riley/PD-2026-007-S002-IMG-001.v003.png', text: ['wallet', 'smartphone']},
  {id: 'S012', start: 291, dur: 24, mode: 'still', title: 'Half in your pocket, half in the cloud', kicker: 'ACT II', image: 'riley/PD-2026-007-S002-IMG-001.v003.png'},
  {id: 'S013', start: 315, dur: 26, mode: 'secure', title: 'Data is not a weapon', subtitle: 'Secure the device', kicker: 'ACT II'},
  {id: 'S014', start: 341, dur: 26, mode: 'still', title: '2014 / 9-0 result', subtitle: 'Riley v. California, 573 U.S. 373', kicker: 'ACT III', image: 'riley/PD-2026-007-S017-IMG-001.v003.png', citation: 'CLM-0002'},
  {id: 'S015', start: 367, dur: 25, mode: 'quote', title: '"the privacies of life"', kicker: 'ACT III', image: 'riley/PD-2026-007-S022-IMG-001.v003.png', citation: 'CLM-0003'},
  {id: 'S016', start: 392, dur: 24, mode: 'logic', title: 'More revealing than a house', kicker: 'ACT III', text: ['home', 'phone']},
  {id: 'S017', start: 416, dur: 20, mode: 'quote', title: '"Get a warrant."', kicker: 'ACT III', image: 'riley/PD-2026-007-S017-IMG-001.v003.png', citation: 'CLM-0001'},
  {id: 'S018', start: 436, dur: 27, mode: 'still', title: 'Katz v. United States (1967): people, not places', kicker: 'ACT III', image: 'riley/PD-2026-007-S018-IMG-001.v001.png'},
  {id: 'S019', start: 463, dur: 18, mode: 'phone', title: 'One rule for the phone category', kicker: 'ACT III'},
  {id: 'S020', start: 481, dur: 10, mode: 'type', title: 'Exception: true emergencies', kicker: 'ACT III'},
  {id: 'S021', start: 491, dur: 26, mode: 'secure', title: 'Contents protected', subtitle: 'Warrant, consent, emergency', kicker: 'ACT III'},
  {id: 'S022', start: 517, dur: 28, mode: 'apps', title: 'A phone can reveal a life', kicker: 'ACT IV', image: 'riley/PD-2026-007-S022-IMG-001.v003.png', text: ['calendar', 'photos', 'banking', 'health', 'messages', 'search']},
  {id: 'S023', start: 545, dur: 24, mode: 'still', title: 'Automatic records', kicker: 'ACT IV', image: 'riley/PD-2026-007-S022-IMG-001.v003.png'},
  {id: 'S024', start: 569, dur: 12, mode: 'split', title: 'Inside the phone vs. the trail it leaves', kicker: 'ACT IV', text: ['inside', 'trail']},
  {id: 'S025', start: 581, dur: 22, mode: 'quote', title: 'For that, police need a warrant.', kicker: 'ACT IV', image: 'riley/PD-2026-007-S017-IMG-001.v003.png'},
  {id: 'S026', start: 603, dur: 18, mode: 'split', title: 'Chosen contents | Automatic records', kicker: 'ENDING', text: ['chosen contents', 'automatic records']},
  {id: 'S027', start: 621, dur: 16, mode: 'still', title: "Next: your phone is tracking you", kicker: 'NEXT', image: 'riley/PD-2026-007-S027-IMG-001.v003.png'},
  {id: 'S028', start: 637, dur: 9, mode: 'end', title: 'Prime Documentary', subtitle: 'Subscribe', kicker: 'END'},
];

const fitTitle = (text: string): number => Math.min(82, Math.max(38, 1380 / Math.max(text.length, 15)));

const sceneNumber = (id: string): number => {
  const match = id.match(/\d+/);
  return match ? Number(match[0]) : 1;
};

const plateImagesFor = (scene: Scene): string[] => {
  const plates = rileyV004Plates[scene.id] ?? [];
  if (plates.length > 0) return plates;
  return scene.image ? [scene.image] : [];
};

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
      {scene.mode !== 'quote' ? (
        <div style={{
          fontFamily: BRAND.font.display,
          fontSize: fitTitle(scene.title),
          color: WHITE,
          textTransform: 'uppercase',
          lineHeight: 0.95,
          textShadow: '0 5px 30px #000',
          letterSpacing: 0,
        }}>{scene.title}</div>
      ) : null}
      {scene.subtitle && scene.mode !== 'quote' ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 12, maxWidth: 1080, letterSpacing: 0}}>{scene.subtitle}</div> : null}
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
  const {fps} = useVideoConfig();
  const sceneFrames = Math.max(1, Math.round(scene.dur * fps));
  const seed = sceneNumber(scene.id);
  const panX = Math.sin(seed * 1.63) * 28;
  const panY = Math.cos(seed * 1.21) * 18;
  const rotate = Math.sin((frame + seed * 19) / 180) * 0.16;
  const images = plateImagesFor(scene);
  const slotFrames = images.length > 0 ? Math.max(14, sceneFrames / images.length) : sceneFrames;
  const imageIndex = images.length > 0 ? Math.min(images.length - 1, Math.floor(frame / slotFrames)) : 0;
  const nextIndex = images.length > 0 ? Math.min(images.length - 1, imageIndex + 1) : 0;
  const slotProgress = images.length > 0 ? (frame - imageIndex * slotFrames) / slotFrames : 0;
  const crossfade = interpolate(slotProgress, [0.58, 0.92], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const hideLowerThird =
    (scene.id === 'S001' && frame < Math.round(3.25 * fps)) ||
    (scene.id === 'S002' && frame < Math.round(OPENING_SEC * fps)) ||
    (scene.id === 'S003' && frame < Math.round(2.55 * fps)) ||
    (scene.id === 'S026' && frame < Math.round(2.65 * fps));
  const renderPlate = (src: string, index: number, opacity: number, extraScale: number) => {
    const local = frame - index * slotFrames;
    const lp = interpolate(local, [0, slotFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
    const localSeed = seed * 19 + index * 7;
    const dir = index % 2 === 0 ? 1 : -1;
    const driftX = interpolate(lp, [0, 1], [-46 * dir, 46 * dir]);
    const driftY = interpolate(lp, [0, 1], [22 * dir, -22 * dir]);
    const localScale = 1.045 + extraScale + lp * (0.062 + (index % 3) * 0.012);
    return (
      <Img
        src={staticFile(src)}
        style={{
          position: 'absolute',
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          objectPosition: `${50 + Math.sin(localSeed) * 9}% ${50 + Math.cos(localSeed) * 7}%`,
          transform: `scale(${localScale}) translate(${driftX + panX * 0.2}px, ${driftY + panY * 0.2}px) rotate(${rotate}deg)`,
          filter: 'brightness(0.95) contrast(1.08) saturate(1.12)',
          opacity,
        }}
      />
    );
  };
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      {images.length > 0 ? (
        <AbsoluteFill style={{overflow: 'hidden'}}>
          {renderPlate(images[imageIndex], imageIndex, 1, 0)}
          {nextIndex !== imageIndex ? renderPlate(images[nextIndex], nextIndex, crossfade, 0.025) : null}
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{background: `radial-gradient(90% 70% at 64% 34%, #14345f 0%, ${NAVY} 35%, ${INK} 84%)`}} />
      )}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}A8 0%, #00000000 43%, ${INK}B8 100%)`}} />
      {children}
      {hideLowerThird ? null : <LowerThird scene={scene} />}
      {scene.recon ? <ReconstructionLabel /> : null}
      {rileyV004PlateCount >= 180 ? (
        <div style={{position: 'absolute', right: 54, bottom: 42, fontFamily: BRAND.font.body, fontSize: 15, color: `${SILVER}AA`, letterSpacing: 0}}>
          180 symbolic visual plates
        </div>
      ) : null}
      <Vignette strength={images.length > 0 ? 0.72 : 1} />
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

const SectionBumper: React.FC<{label: string; title: string; subtitle?: string; tone?: 'blue' | 'gold'}> = ({label, title, subtitle, tone = 'blue'}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const color = tone === 'gold' ? GOLD : BLUE;
  const inS = spring({frame: frame - Math.round(0.08 * fps), fps, config: {damping: 18, stiffness: 100}});
  const out = interpolate(frame, [durationInFrames - Math.round(0.42 * fps), durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const rule = interpolate(frame, [8, 28], [0, 620], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(95% 85% at 52% 42%, ${tone === 'gold' ? '#3A2A08' : '#0F356B'} 0%, ${NAVY} 39%, ${INK} 86%)`, opacity: Math.min(inS, out), overflow: 'hidden'}}>
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 25, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 0, opacity: inS}}>
          {label}
        </div>
        <div style={{width: rule, height: 3, background: color, margin: '18px 0 26px', boxShadow: `0 0 20px ${color}`}} />
        <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: 96, lineHeight: 0.92, textTransform: 'uppercase', textAlign: 'center', textShadow: `0 0 44px ${color}66`, transform: `translateY(${interpolate(inS, [0, 1], [32, 0])}px)`, opacity: inS, letterSpacing: 0}}>
          {title}
        </div>
        {subtitle ? (
          <div style={{fontFamily: BRAND.font.body, color: color, fontSize: 30, fontWeight: 800, marginTop: 18, opacity: inS, letterSpacing: 0}}>
            {subtitle}
          </div>
        ) : null}
      </AbsoluteFill>
      <Vignette strength={1} />
      <Grain opacity={0.06} />
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
      <path d="M430 745 L650 635 L875 500 L1110 435 L1430 330" fill="none" stroke={BLUE} strokeWidth="8" strokeLinecap="round" opacity="0.62" />
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
  <BrandEndcard />
);

const SceneBody: React.FC<{scene: Scene}> = ({scene}) => {
  const useGeneratedPlates = plateImagesFor(scene).length > 0;
  if (scene.mode === 'end') {
    return (
      <Shell scene={scene}>
        <EndGraphic />
      </Shell>
    );
  }
  return (
    <Shell scene={scene}>
      {!useGeneratedPlates && scene.mode === 'hook' ? <HookGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'phone' ? <PhoneWindow scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'map' ? <MapGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'evidence' ? <EvidenceGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'stamp' ? <StampGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'type' ? <TypeWall scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'split' ? <SplitGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'logic' ? <LogicGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'wallet' ? <WalletGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'cloud' ? <CloudGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'secure' ? <SecureGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'court' ? <CourtGraphic /> : null}
      {scene.mode === 'quote' ? <QuoteGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'booth' ? <BoothGraphic /> : null}
      {!useGeneratedPlates && scene.mode === 'apps' ? <AppsGraphic scene={scene} /> : null}
      {!useGeneratedPlates && scene.mode === 'trail' ? <TrailGraphic /> : null}
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
    <Sequence from={0} durationInFrames={Math.round(3.2 * BRAND.video.fps)} name="HOOK_BUMPER">
      <SectionBumper label="Hook" title="Can they search your phone?" subtitle="The arrest question" tone="blue" />
    </Sequence>
    <Sequence from={Math.round(28 * BRAND.video.fps)} durationInFrames={Math.round(OPENING_SEC * BRAND.video.fps)} name="BRAND_OPENING">
      <BrandOpening seriesLabel="Landmark Rights Cases" title="Riley v. California" subtitle="When your phone became different" />
    </Sequence>
    <Sequence from={Math.round(72 * BRAND.video.fps)} durationInFrames={Math.round(2.5 * BRAND.video.fps)} name="MAIN_BODY_BUMPER">
      <SectionBumper label="Main Story" title="The case and the rule" subtitle="Riley + Wurie -> Get a warrant" tone="gold" />
    </Sequence>
    <Sequence from={Math.round(603 * BRAND.video.fps)} durationInFrames={Math.round(2.6 * BRAND.video.fps)} name="ENDING_BUMPER">
      <SectionBumper label="Ending" title="The edge of protection" subtitle="Inside the phone vs. the trail it leaves" tone="blue" />
    </Sequence>
  </AbsoluteFill>
);

export const rileyPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
