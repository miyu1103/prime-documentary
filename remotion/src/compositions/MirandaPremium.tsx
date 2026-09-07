import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  OffthreadVideo,
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
import {MIRANDA_CAPTIONS} from '../data/miranda_captions';
import {MIRANDA_FACTORY} from '../data/miranda_factory_assets';
import {MIRANDA_SCENE_DURATIONS, MIRANDA_TOTAL_SEC} from '../data/miranda_timing';

const FPS = BRAND.video.fps;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const AI_LABEL = 'symbolic reconstruction / AI-assisted imagery';

type Kind =
  | 'hook'
  | 'brand'
  | 'thesis'
  | 'place'
  | 'room'
  | 'asymmetry'
  | 'question'
  | 'evidence'
  | 'appeal'
  | 'fourCases'
  | 'pattern'
  | 'gap'
  | 'vote'
  | 'warnings'
  | 'fifth'
  | 'dissent'
  | 'cards'
  | 'door'
  | 'cell'
  | 'next'
  | 'stock'
  | 'recap'
  | 'tease'
  | 'cta'
  | 'endcard';

type Scene = {
  id: string;
  kind: Kind;
  dur: number;
  title: string;
  subtitle?: string;
  kicker?: string;
  citation?: string;
  factory?: string[];
  telop?: string[];
  ai?: string[];
};

const imgSet = (span: string, count: number): string[] =>
  Array.from({length: count}, (_, i) => `miranda/${span}${i === 0 ? '' : `_${String(i + 1).padStart(2, '0')}`}.png`);

const factory = (key: string, index = 0): string | undefined => {
  const groups = MIRANDA_FACTORY as unknown as Record<string, readonly string[]>;
  const list = groups[key] ?? [];
  return list[index % Math.max(1, list.length)];
};

const scenes: Scene[] = [
  {id: 'SPN-0001', kind: 'hook', dur: 30, title: 'The warning was not written for television.', subtitle: 'A confession. A 5-4 ruling. A rule that outlived the man.', kicker: 'HOOK', factory: ['police_interrogation_room_empty', 'police_strobe_red_and_blue', 'smoke_on_black'], ai: [...imgSet('SPN-0001', 7), ...imgSet('SPN-0004', 3), ...imgSet('SPN-0018', 3), ...imgSet('SPN-0021', 2)]},
  {id: 'brand', kind: 'brand', dur: OPENING_SEC, title: 'Miranda', subtitle: 'Why police read you your rights'},
  {id: 'SPN-0002', kind: 'thesis', dur: 28, title: 'Not a courtesy. A repair.', subtitle: 'The fix is anchored in the Fifth Amendment.', kicker: 'OPENING', factory: ['parchment_texture', 'light_leak_overlay'], citation: 'CLM-0003', ai: imgSet('SPN-0002', 6)},
  {id: 'SPN-0003', kind: 'place', dur: 33, title: '1963 — Phoenix, Arizona', subtitle: 'An ordinary arrest becomes the test case.', kicker: 'ACT I', factory: ['atmosphere_symbolic', 'dust_motes_sunlight'], citation: 'CLM-0006', ai: imgSet('SPN-0003', 5)},
  {id: 'SPN-0004', kind: 'room', dur: 28, title: 'Never told he could stay silent.', subtitle: 'No lawyer beside him.', kicker: 'ACT I', factory: ['one_way_mirror_room', 'floating_dust_in_light_beam'], citation: 'CLM-0006', ai: imgSet('SPN-0004', 6)},
  {id: 'SPN-0005', kind: 'asymmetry', dur: 29, title: 'The room is tilted.', subtitle: 'Door. Clock. Questions.', kicker: 'ACT I', factory: ['single_chair_empty_room', 'clock_ticking_macro'], ai: imgSet('SPN-0005', 5), telop: ['trained investigators', 'one person alone']},
  {id: 'SPN-0006', kind: 'question', dur: 28, title: '"Did he know he had a choice?"', subtitle: 'The question shifts.', kicker: 'ACT I', factory: ['old_paper_texture', 'light_leak_overlay'], ai: imgSet('SPN-0006', 5)},
  {id: 'SPN-0007', kind: 'evidence', dur: 34, title: 'His own words become evidence.', subtitle: 'Confession → evidence → conviction.', kicker: 'ACT II', factory: ['case_files_stack_desk', 'old_paper_texture'], citation: 'CLM-0006', ai: imgSet('SPN-0007', 5)},
  {id: 'SPN-0008', kind: 'appeal', dur: 28, title: 'The case keeps climbing.', subtitle: 'The confession should never have counted.', kicker: 'ACT II', factory: ['law_library_books', 'god_rays'], citation: 'CLM-0006', ai: imgSet('SPN-0008', 5)},
  {id: 'SPN-0009', kind: 'fourCases', dur: 32, title: 'Four cases. One question.', subtitle: 'Vignera · Westover · California v. Stewart · Miranda', kicker: 'ACT II', factory: ['parchment_texture', 'dust_motes_sunlight'], citation: 'CLM-0005'},
  {id: 'SPN-0010', kind: 'pattern', dur: 33, title: 'The Court sees a pattern.', subtitle: 'Not one bad day. A recurring gap.', kicker: 'ACT II', factory: ['supreme_court_building', 'light_leak_overlay'], ai: imgSet('SPN-0010', 5)},
  {id: 'SPN-0011', kind: 'gap', dur: 34, title: 'Having a right is not knowing it.', subtitle: 'The distance becomes the case.', kicker: 'ACT II', factory: ['police_interrogation_room_empty', 'floating_dust_in_light_beam'], ai: imgSet('SPN-0011', 6)},
  {id: 'SPN-0012', kind: 'vote', dur: 28, title: 'June 13, 1966 — 5–4', subtitle: 'Miranda v. Arizona, 384 U.S. 436', kicker: 'ACT III', factory: ['courtroom_interior', 'god_rays', 'smoke_on_black'], citation: 'CLM-0002 / CLM-0001'},
  {id: 'SPN-0013', kind: 'warnings', dur: 33, title: 'The four warnings', subtitle: 'A floor the state must clear.', kicker: 'ACT III', factory: ['parchment_texture', 'light_leak_overlay'], citation: 'CLM-0004'},
  {id: 'SPN-0014', kind: 'fifth', dur: 27, title: 'No forced self-incrimination.', subtitle: 'The Fifth Amendment, made audible in the room.', kicker: 'ACT III', factory: ['us_constitution_document', 'god_rays'], citation: 'CLM-0003', ai: imgSet('SPN-0014', 5)},
  {id: 'SPN-0015', kind: 'dissent', dur: 26, title: 'Dissent — "reached too far"', subtitle: 'Public safety and individual rights remain in tension.', kicker: 'ACT III', factory: ['courtroom_interior', 'smoke_on_black'], citation: 'CLM-0007', ai: imgSet('SPN-0015', 5)},
  {id: 'SPN-0016', kind: 'cards', dur: 35, title: 'Printed on cards. Recited at arrest.', subtitle: 'The routine hardens.', kicker: 'ACT IV', factory: ['police_badge_close_up', 'old_paper_texture'], citation: 'CLM-0008', ai: imgSet('SPN-0016', 6)},
  {id: 'SPN-0017', kind: 'door', dur: 30, title: 'A small transfer of power.', subtitle: 'The closed room is forced to admit choices.', kicker: 'ACT IV', factory: ['police_interrogation_room_empty', 'light_leak_overlay'], ai: imgSet('SPN-0017', 5)},
  {id: 'SPN-0018', kind: 'cell', dur: 33, title: 'Retried — convicted again.', subtitle: 'He won a rule, not freedom.', kicker: 'ACT IV', factory: ['jail_cell_bars', 'prison_corridor'], citation: 'CLM-0006', ai: imgSet('SPN-0018', 7)},
  {id: 'SPN-0019', kind: 'next', dur: 30, title: 'Not for Miranda alone.', subtitle: 'For the next person, and the next.', kicker: 'ACT IV', factory: ['single_chair_empty_room', 'god_rays'], ai: imgSet('SPN-0019', 5)},
  {id: 'SPN-0020', kind: 'stock', dur: 16, title: 'The gap closes out loud.', subtitle: 'Every single time.', kicker: 'ACT IV', factory: ['police_car_lights_night', 'police_strobe_red_and_blue'], citation: 'CLM-0001'},
  {id: 'SPN-0021', kind: 'recap', dur: 30, title: 'Structural — not set dressing.', subtitle: 'A line around the state gathering your own words.', kicker: 'ENDING', factory: ['police_interrogation_room_empty', 'film_grain_texture'], citation: 'CLM-0001 / CLM-0003 / CLM-0004', ai: imgSet('SPN-0021', 5)},
  {id: 'SPN-0022', kind: 'cell', dur: 34, title: 'The warning outlived his case.', subtitle: 'A structural fix for everyone questioned after him.', kicker: 'ENDING', factory: ['jail_cell_bars', 'light_leak_overlay'], citation: 'CLM-0006', ai: imgSet('SPN-0022', 5)},
  {id: 'SPN-0023', kind: 'tease', dur: 28, title: 'Next: who gets a lawyer?', subtitle: 'Gideon changes the next threshold.', kicker: 'NEXT', factory: ['law_library_books', 'god_rays'], ai: imgSet('SPN-0023', 5)},
  {id: 'SPN-0024', kind: 'cta', dur: 4, title: 'Subscribe', subtitle: 'Landmark rights cases, opened one by one.', kicker: 'PRIME DOCUMENTARY', factory: ['looping_light_rays', 'atmospheric_loop']},
  {id: 'endcard', kind: 'endcard', dur: ENDCARD_SEC, title: ''},
];

const sceneDuration = (scene: Scene): number => MIRANDA_SCENE_DURATIONS[scene.id] ?? scene.dur;
const TOTAL_SEC = MIRANDA_TOTAL_SEC ?? scenes.reduce((sum, s) => sum + sceneDuration(s), 0);

const fit = (text: string, max = 92): number => Math.min(max, Math.max(42, 1220 / Math.max(text.length, 12)));

const ScenePlate: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const localFrames = Math.max(1, Math.round(sceneDuration(scene) * FPS));
  const p = interpolate(frame, [0, localFrames], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const e = p * p * (3 - 2 * p);
  const imgs = scene.ai ?? [];
  const seg = Math.max(38, Math.round(4.7 * FPS));
  const i = imgs.length ? Math.floor(frame / seg) % imgs.length : 0;
  const next = imgs.length ? (i + 1) % imgs.length : 0;
  const segP = interpolate(frame % seg, [seg * 0.72, seg], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const dir = scene.id.charCodeAt(scene.id.length - 1) % 2 === 0 ? 1 : -1;
  const scale = 1.08 + e * 0.13;
  const tx = dir * interpolate(e, [0, 1], [-54, 54]);
  const ty = interpolate(e, [0, 1], [24, -24]);
  const baseFactory = scene.factory?.[0] ? factory(scene.factory[0]) : undefined;
  const overlayA = scene.factory?.[1] ? factory(scene.factory[1], 0) : undefined;
  const overlayB = scene.factory?.[2] ? factory(scene.factory[2], 0) : undefined;
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
        transform: `translate3d(${tx + offset * 18}px, ${ty - offset * 10}px, 0) scale(${scale + offset * 0.025}) rotate(${dir * 0.28}deg)`,
        filter: 'brightness(0.78) contrast(1.22) saturate(1.06)',
      }}
    />
  );
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <AbsoluteFill style={{background: `radial-gradient(80% 68% at 58% 42%, #173a68 0%, ${NAVY} 36%, ${INK} 86%)`}} />
      {baseFactory ? <FactoryMedia src={baseFactory} opacity={scene.kind === 'stock' || scene.kind === 'cta' ? 0.72 : scene.kind === 'fourCases' ? 0.08 : 0.16} /> : null}
      {imgs.length ? (
        <AbsoluteFill>
          {renderImage(imgs[i], 1, 0)}
          {imgs.length > 1 ? renderImage(imgs[next], segP, 1) : null}
        </AbsoluteFill>
      ) : null}
      {overlayA ? <FactoryMedia src={overlayA} opacity={0.24} blend="screen" /> : null}
      {overlayB ? <FactoryMedia src={overlayB} opacity={0.22} blend="screen" /> : null}
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}D8 0%, #00000010 42%, ${INK}E8 100%)`}} />
      <LightSweep seed={scene.id} color={scene.kind === 'vote' || scene.kind === 'warnings' ? GOLD : BLUE} />
      <Particles seed={scene.id} count={26} color={scene.kind === 'vote' ? GOLD : BLUE} />
    </AbsoluteFill>
  );
};

const FactoryMedia: React.FC<{src: string; opacity: number; blend?: React.CSSProperties['mixBlendMode']}> = ({src, opacity, blend = 'normal'}) => {
  const isVideo = src.toLowerCase().endsWith('.mp4') || src.toLowerCase().endsWith('.mov') || src.toLowerCase().endsWith('.webm');
  const style: React.CSSProperties = {
    position: 'absolute',
    inset: 0,
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    opacity,
    mixBlendMode: blend,
    filter: 'brightness(0.7) contrast(1.15) saturate(0.9)',
  };
  return isVideo ? <OffthreadVideo src={staticFile(src)} muted style={style} /> : <Img src={staticFile(src)} style={style} />;
};

const TitleLayer: React.FC<{scene: Scene}> = ({scene}) => {
  if (!scene.title || scene.kind === 'endcard' || scene.kind === 'brand') return null;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 100}});
  return (
    <div style={{position: 'absolute', left: 58, top: 44, opacity: Math.min(1, s), transform: `translateY(${interpolate(s, [0, 1], [22, 0])}px)`}}>
      <div style={{fontFamily: BRAND.font.body, color: GOLD, fontSize: 18, fontWeight: 900, letterSpacing: 2}}>{scene.kicker ?? 'PRIME DOCUMENTARY'}</div>
      <div style={{width: 300, height: 2, background: GOLD, marginTop: 10, marginBottom: 22, boxShadow: `0 0 18px ${GOLD}`}} />
      <div style={{fontFamily: BRAND.font.display, color: WHITE, fontSize: fit(scene.title), maxWidth: 1160, textTransform: 'uppercase', textShadow: '0 6px 32px #000'}}>
        {scene.title}
      </div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 28, maxWidth: 920, marginTop: 8}}>{scene.subtitle}</div> : null}
    </div>
  );
};

const Labels: React.FC<{scene: Scene}> = ({scene}) => (
  <>
    <div style={{position: 'absolute', right: 48, top: 48, fontFamily: BRAND.font.body, fontSize: 18, color: SILVER, padding: '8px 12px', background: '#00000099', border: `1px solid ${GOLD}88`}}>
      {AI_LABEL}
    </div>
    {scene.citation ? (
      <div style={{position: 'absolute', right: 48, bottom: 188, fontFamily: BRAND.font.body, fontSize: 20, color: GOLD, padding: '8px 12px', background: '#000000A8', borderTop: `2px solid ${GOLD}`}}>
        Source: {scene.citation}
      </div>
    ) : null}
  </>
);

const SceneContent: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'brand') return <BrandOpening seriesLabel="Prime Documentary" title="Miranda" subtitle="Why police read you your rights" />;
  if (scene.kind === 'endcard') return <BrandEndcard />;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <ScenePlate scene={scene} />
      {scene.kind === 'hook' ? <HookMontage /> : null}
      {scene.kind === 'asymmetry' ? <Asymmetry /> : null}
      {scene.kind === 'question' ? <ChoiceQuestion /> : null}
      {scene.kind === 'evidence' ? <EvidenceFlow /> : null}
      {scene.kind === 'fourCases' ? <FourCases /> : null}
      {scene.kind === 'gap' ? <KnowledgeGap /> : null}
      {scene.kind === 'vote' ? <VoteMoment /> : null}
      {scene.kind === 'warnings' ? <Warnings /> : null}
      {scene.kind === 'dissent' ? <Dissent /> : null}
      {scene.kind === 'cards' ? <WarningCards /> : null}
      {scene.kind === 'door' ? <OpeningDoor /> : null}
      {scene.kind === 'cta' ? <SubscribeButton /> : null}
      <TitleLayer scene={scene} />
      <Labels scene={scene} />
      <Vignette strength={1} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};

const HookMontage: React.FC = () => {
  const frame = useCurrentFrame();
  const words = ['confession', '5–4', 'four warnings', 'still convicted', 'next person'];
  const active = Math.floor(frame / 45) % words.length;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 250, textAlign: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, color: active === 1 ? GOLD : WHITE, fontSize: 86, textTransform: 'uppercase', textShadow: '0 8px 40px #000'}}>
        {words[active]}
      </div>
    </div>
  );
};

const Asymmetry: React.FC = () => {
  const frame = useCurrentFrame();
  const tilt = interpolate(frame, [0, 90, 180], [-2, 0, 2], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: 210, right: 210, top: 390, display: 'grid', gridTemplateColumns: '1.25fr 0.75fr', gap: 34, transform: `rotate(${tilt}deg)`}}>
      <Panel color={BLUE} title="Control" lines={['door', 'clock', 'questions']} />
      <Panel color={GOLD} title="Alone" lines={['no lawyer', 'no script', 'no map']} />
    </div>
  );
};

const Panel: React.FC<{color: string; title: string; lines: string[]}> = ({color, title, lines}) => (
  <div style={{minHeight: 250, background: '#020409cc', border: `3px solid ${color}`, padding: 30, boxShadow: '0 18px 52px #000'}}>
    <div style={{fontFamily: BRAND.font.display, color, fontSize: 60, textTransform: 'uppercase'}}>{title}</div>
    {lines.map((l) => <div key={l} style={{fontFamily: BRAND.font.body, color: SILVER, fontSize: 29, marginTop: 12}}>• {l}</div>)}
  </div>
);

const ChoiceQuestion: React.FC = () => {
  const frame = useCurrentFrame();
  const s = spring({frame: frame - 12, fps: FPS, config: {damping: 13, stiffness: 82}});
  return (
    <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 96, color: GOLD, textTransform: 'uppercase', transform: `scale(${0.84 + s * 0.16})`, textShadow: '0 10px 45px #000'}}>
        Choice?
      </div>
    </div>
  );
};

const EvidenceFlow: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['Confession', 'Evidence', 'Conviction'];
  return <Flow labels={labels} active={Math.floor(frame / 80)} />;
};

const Flow: React.FC<{labels: string[]; active: number}> = ({labels, active}) => (
  <div style={{position: 'absolute', left: 250, right: 250, top: 460, display: 'grid', gridTemplateColumns: `repeat(${labels.length}, 1fr)`, gap: 38}}>
    {labels.map((label, i) => (
      <div key={label} style={{height: 150, border: `3px solid ${i <= active ? GOLD : `${SILVER}55`}`, background: '#03060bcc', color: i <= active ? WHITE : SILVER, display: 'grid', placeItems: 'center', fontFamily: BRAND.font.display, fontSize: 44, textTransform: 'uppercase'}}>
        {label}
      </div>
    ))}
  </div>
);

const FourCases: React.FC = () => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [20, 135], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const cases = ['Vignera', 'Westover', 'Stewart', 'Miranda'];
  const positions = [[220, 350], [1260, 350], [220, 660], [1260, 660]];
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      {positions.map(([x0, y0], i) => {
        const x = interpolate(p, [0, 1], [x0, 760]);
        const y = interpolate(p, [0, 1], [y0, 500]);
        return (
          <g key={cases[i]} transform={`translate(${x} ${y})`}>
            <rect width="400" height="150" fill="#020409dd" stroke={i === 3 ? GOLD : BLUE} strokeWidth="4" />
            <text x="200" y="88" fill={i === 3 ? GOLD : WHITE} fontFamily={BRAND.font.display} fontSize="42" textAnchor="middle">{cases[i]}</text>
          </g>
        );
      })}
      <text x="960" y="742" fill={GOLD} fontFamily={BRAND.font.display} fontSize="66" textAnchor="middle" opacity={p}>ONE QUESTION</text>
    </svg>
  );
};

const KnowledgeGap: React.FC = () => (
  <div style={{position: 'absolute', left: 250, right: 250, top: 420}}>
    <Flow labels={['has a right', 'knows the right', 'can use it']} active={2} />
  </div>
);

const VoteMoment: React.FC = () => {
  const frame = useCurrentFrame();
  const reveal = spring({frame: frame - 72, fps: FPS, config: {damping: 10, stiffness: 70}});
  const cite = spring({frame: frame - 150, fps: FPS, config: {damping: 12, stiffness: 100}});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g transform={`translate(480 410) scale(${0.82 + reveal * 0.18})`} opacity={Math.min(1, reveal * 1.2)}>
        {Array.from({length: 9}, (_, i) => {
          const yes = i < 5;
          return <rect key={i} x={(i % 5) * 154} y={Math.floor(i / 5) * 142} width="100" height="100" rx="12" fill={yes ? BLUE : '#30343f'} stroke={yes ? GOLD : SILVER} strokeWidth="4" />;
        })}
        <text x="372" y="354" fill={WHITE} fontFamily={BRAND.font.display} fontSize="124" textAnchor="middle">5–4</text>
      </g>
      <g opacity={Math.min(1, cite * 1.3)}>
        <line x1="430" x2="1490" y1="820" y2="820" stroke={GOLD} strokeWidth="5" />
        <text x="960" y="786" fill={GOLD} fontFamily={BRAND.font.body} fontWeight="800" fontSize="34" textAnchor="middle">Miranda v. Arizona, 384 U.S. 436</text>
      </g>
    </svg>
  );
};

const Warnings: React.FC = () => {
  const frame = useCurrentFrame();
  const labels = ['Silent', 'Used against you', 'Lawyer', 'One appointed'];
  return (
    <div style={{position: 'absolute', left: 170, right: 170, top: 360, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 26}}>
      {labels.map((label, i) => {
        const on = interpolate(frame, [i * 42 + 18, i * 42 + 46], [0.25, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return (
          <div key={label} style={{height: 280, background: '#eadfbf', color: INK, padding: 26, boxShadow: `0 0 ${28 * on}px ${GOLD}`, opacity: 0.72 + on * 0.28, transform: `translateY(${(1 - on) * 26}px)`}}>
            <div style={{fontFamily: BRAND.font.display, fontSize: 34, color: '#10131a'}}>0{i + 1}</div>
            <div style={{fontFamily: BRAND.font.display, fontSize: label.length > 12 ? 42 : 54, lineHeight: 1, marginTop: 40, textTransform: 'uppercase'}}>{label}</div>
          </div>
        );
      })}
    </div>
  );
};

const Dissent: React.FC = () => <Flow labels={['Majority', 'Dissent', 'Echoes today']} active={2} />;

const WarningCards: React.FC = () => <Warnings />;

const OpeningDoor: React.FC = () => {
  const frame = useCurrentFrame();
  const open = spring({frame: frame - 35, fps: FPS, config: {damping: 14, stiffness: 70}});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <rect x="720" y="220" width="480" height="640" fill="#03060b" stroke={SILVER} strokeWidth="5" />
      <rect x="720" y="220" width="480" height="640" fill={GOLD} opacity={0.18 + open * 0.35} />
      <g transform={`translate(720 220) skewY(${open * -10}) translate(${open * -210} 0)`}>
        <rect width="480" height="640" fill="#080d17" stroke={GOLD} strokeWidth="5" />
        <circle cx="420" cy="330" r="10" fill={GOLD} />
      </g>
      <text x="960" y="900" fill={GOLD} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">CHOICES ENTER THE ROOM</text>
    </svg>
  );
};

const SubscribeButton: React.FC = () => {
  const frame = useCurrentFrame();
  const s = spring({frame: frame - 5, fps: FPS, config: {damping: 12, stiffness: 120}});
  return (
    <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center'}}>
      <div style={{fontFamily: BRAND.font.display, fontSize: 80, color: WHITE, background: `${GOLD}E6`, padding: '24px 62px', borderRadius: 8, transform: `scale(${0.75 + s * 0.25})`, boxShadow: `0 0 48px ${GOLD}`}}>
        SUBSCRIBE
      </div>
    </div>
  );
};

const CaptionLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  const cap = MIRANDA_CAPTIONS.find((c) => t >= c.start && t <= c.end);
  if (!cap) return null;
  return (
    <div style={{position: 'absolute', left: 220, right: 220, bottom: 44, minHeight: 116, background: '#000000B0', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px 32px', boxShadow: '0 -8px 28px #00000088'}}>
      <div style={{fontFamily: BRAND.font.body, color: WHITE, fontWeight: 900, fontSize: 54, lineHeight: 1.16, textAlign: 'center', textShadow: '0 3px 0 #000, 0 0 16px #000'}}>
        {cap.text}
      </div>
    </div>
  );
};

export const MirandaPremium: React.FC = () => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <Audio src={staticFile('miranda/audio/final_mix_v001.mp3')} />
      {scenes.map((scene) => {
        const from = Math.round(cursor * FPS);
        const dur = sceneDuration(scene);
        cursor += dur;
        return (
          <Sequence key={scene.id} from={from} durationInFrames={Math.round(dur * FPS)}>
            <SceneContent scene={scene} />
          </Sequence>
        );
      })}
      <CaptionLayer />
    </AbsoluteFill>
  );
};

export const mirandaPremiumDurationInFrames = (fps: number): number => Math.round(TOTAL_SEC * fps);
