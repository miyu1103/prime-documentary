import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Loop,
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
import {KING_CAPTIONS} from '../data/king_captions';
import {KING_SCENE_TIMING, KING_TOTAL_SEC} from '../data/king_timing';

const FPS = BRAND.video.fps;
const TARGET_SEC = KING_TOTAL_SEC;
const RAW_SEC = 603.2;
const SCALE = (TARGET_SEC - OPENING_SEC - ENDCARD_SEC) / RAW_SEC;
const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const BLUE = BRAND.color.electric;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;
const RED = '#D84B4B';

type Kind =
  | 'dnaFlow'
  | 'splitQuestion'
  | 'maryland'
  | 'notReason'
  | 'matchGrid'
  | 'dualView'
  | 'bothTrue'
  | 'fingerprintSearch'
  | 'bookingEquation'
  | 'fingerprintDna'
  | 'codis'
  | 'blueprint'
  | 'ruling'
  | 'kennedyQuote'
  | 'kennedyColumns'
  | 'coalition'
  | 'scaliaWords'
  | 'national'
  | 'scales'
  | 'trade'
  | 'finalSplit'
  | 'seriesStack'
  | 'nextHome'
  | 'brand'
  | 'end';

type Scene = {
  id: string;
  kind: Kind;
  rawDur: number;
  title: string;
  subtitle?: string;
  kicker?: string;
  citation?: string;
  images?: string[];
  videos?: string[];
  factory?: string[];
  overlay?: string[];
  texture?: string;
};

const imgs = (id: string, count: number): string[] => [
  `king/${id}.png`,
  ...Array.from({length: count - 1}, (_, i) => `king/${id}_${String(i + 2).padStart(2, '0')}.png`),
];

const bodyScenes: Scene[] = [
  {
    id: 'SPN-0001',
    kind: 'dnaFlow',
    rawDur: 29.6,
    title: 'Arrested — not convicted',
    subtitle: 'A booking swab enters a database.',
    kicker: 'HOOK',
    factory: ['king/factory/AF-BG-7106__dna_laboratory_blue.mp4', 'king/factory/AF-BG-25661__dna_double_helix_render.mp4'],
    overlay: ['king/factory/AF-PART-0049__dust_particles_floating.mp4'],
  },
  {
    id: 'SPN-0002',
    kind: 'splitQuestion',
    rawDur: 46.0,
    title: 'Identification — or a search?',
    subtitle: 'The Fourth Amendment question.',
    kicker: 'OPENING',
    images: imgs('SPN-0002', 11),
    factory: ['king/factory/AF-BG-6465__us_constitution_document.mp4'],
    texture: 'king/factory/AF-TEX-0002__old_paper_texture.jpg',
  },
  {
    id: 'SPN-0003',
    kind: 'maryland',
    rawDur: 16.0,
    title: 'Maryland, 2009',
    subtitle: 'Arrested for assault.',
    kicker: 'ACT I',
    factory: ['king/factory/AF-BG-6724__police_badge_close_up.mp4'],
  },
  {
    id: 'SPN-0004',
    kind: 'notReason',
    rawDur: 18.4,
    title: 'The swab was NOT the reason for arrest',
    subtitle: 'The assault arrest came first.',
    kicker: 'ACT I',
    images: imgs('SPN-0004', 5),
    factory: ['king/factory/AF-BG-23406__police_interrogation_room_empty.mp4'],
  },
  {
    id: 'SPN-0005',
    kind: 'matchGrid',
    rawDur: 18.8,
    title: 'Match: an unsolved 2003 case',
    subtitle: 'Database hit after booking.',
    kicker: 'ACT I',
    factory: ['king/factory/AF-BG-0979__server_room_blue.mp4', 'king/factory/AF-BG-7463__circuit_data_flow.mp4'],
    overlay: ['king/factory/AF-LIGHT-0057__light_leak_overlay.mp4'],
  },
  {
    id: 'SPN-0006',
    kind: 'dualView',
    rawDur: 34.8,
    title: 'A cold case solved — vs — a suspicionless search',
    kicker: 'ACT I',
    videos: ['king/pexels_phone_scroll.mp4', 'king/pexels_cell_tower.mp4'],
    factory: ['king/factory/AF-BG-23685__case_files_stack_desk.mp4'],
  },
  {
    id: 'SPN-0007',
    kind: 'bothTrue',
    rawDur: 4.4,
    title: 'Both descriptions are true',
    kicker: 'ACT I',
    images: imgs('SPN-0007', 1),
    overlay: ['king/factory/AF-PART-0050__dust_particles_floating.mp4'],
  },
  {
    id: 'SPN-0008',
    kind: 'fingerprintSearch',
    rawDur: 11.6,
    title: 'Fingerprint or search?',
    kicker: 'ACT II',
    images: imgs('SPN-0008', 3),
    factory: ['king/factory/AF-BG-8374__fingerprint_scan_blue.mp4'],
  },
  {
    id: 'SPN-0009',
    kind: 'bookingEquation',
    rawDur: 26.0,
    title: 'Booking: fingerprints + photo = identify',
    kicker: 'ACT II',
    videos: ['king/pexels_demolition.mp4', 'king/pexels_v_5636977.mp4'],
    factory: ['king/factory/AF-BG-23407__police_interrogation_room_empty.mp4'],
  },
  {
    id: 'SPN-0010',
    kind: 'fingerprintDna',
    rawDur: 20.8,
    title: 'The fingerprint of the 21st century',
    kicker: 'ACT II',
    images: imgs('SPN-0010', 5),
    factory: ['king/factory/AF-BG-8374__fingerprint_scan_blue.mp4', 'king/factory/AF-BG-25661__dna_double_helix_render.mp4'],
  },
  {
    id: 'SPN-0011',
    kind: 'codis',
    rawDur: 47.2,
    title: "CODIS — the FBI's national DNA database",
    kicker: 'ACT II',
    images: imgs('SPN-0011', 11),
    factory: ['king/factory/AF-BG-12983__world_map_dark_glowing.mp4', 'king/factory/AF-LOOP-0001__abstract_loop_dark.mp4'],
  },
  {
    id: 'SPN-0022',
    kind: 'blueprint',
    rawDur: 30.4,
    title: 'A fingerprint vs. a genetic blueprint',
    kicker: 'ACT II',
    videos: ['king/pexels_v_10617219.mp4', 'king/pixabay_v_5392.mp4'],
    factory: ['king/factory/AF-BG-8374__fingerprint_scan_blue.mp4', 'king/factory/AF-BG-25662__dna_double_helix_render.mp4'],
  },
  {
    id: 'SPN-0012',
    kind: 'ruling',
    rawDur: 16.8,
    title: '2013 — 5–4',
    subtitle: 'Maryland v. King, 569 U.S. 435',
    kicker: 'ACT III',
    citation: 'Maryland v. King, 569 U.S. 435 (2013)',
    factory: ['king/factory/AF-BG-0510__courtroom_interior.mp4', 'king/factory/AF-BG-3351__judge_gavel_wooden.mp4'],
    overlay: ['king/factory/AF-VFX-0056__smoke_on_black_background.mp4', 'king/factory/AF-LIGHT-0058__light_leak_overlay.mp4'],
    texture: 'king/factory/AF-TEX-0003__old_paper_texture.jpg',
  },
  {
    id: 'SPN-0013',
    kind: 'kennedyQuote',
    rawDur: 30.0,
    title: '"like fingerprinting and photographing"',
    kicker: 'ACT III',
    videos: ['king/pixabay_v_37417.mp4', 'king/pexels_v_6101367.mp4'],
    factory: ['king/factory/AF-BG-0511__courtroom_interior.mp4'],
  },
  {
    id: 'SPN-0023',
    kind: 'kennedyColumns',
    rawDur: 27.6,
    title: 'Identification meant more than a name',
    kicker: 'ACT III',
    images: imgs('SPN-0023', 7),
    factory: ['king/factory/AF-BG-0585__law_library_books.mp4'],
  },
  {
    id: 'SPN-0014',
    kind: 'coalition',
    rawDur: 21.6,
    title: 'Dissent: Scalia + Ginsburg, Sotomayor, Kagan',
    kicker: 'ACT III',
    images: imgs('SPN-0014', 5),
    factory: ['king/factory/AF-BG-0512__courtroom_interior.mp4'],
    overlay: ['king/factory/AF-PART-0051__dust_particles_floating.mp4'],
  },
  {
    id: 'SPN-0015',
    kind: 'scaliaWords',
    rawDur: 49.2,
    title: 'rightly or wrongly, and for whatever reason',
    kicker: 'ACT III',
    images: imgs('SPN-0015', 11),
    texture: 'king/factory/AF-TEX-0006__grunge_texture_dark.jpg',
  },
  {
    id: 'SPN-0016',
    kind: 'national',
    rawDur: 22.4,
    title: 'Arrested for a serious offense',
    subtitle: 'In much of the country, that can mean DNA on file.',
    kicker: 'ACT IV',
    videos: ['king/pixabay_v_145738.mp4', 'king/pexels_v_29188241.mp4'],
    factory: ['king/factory/AF-BG-1822__prison_corridor.mp4', 'king/factory/AF-BG-6836__jail_cell_bars.mp4'],
  },
  {
    id: 'SPN-0017',
    kind: 'scales',
    rawDur: 34.4,
    title: 'It solves crimes. It also files the merely arrested.',
    kicker: 'ACT IV',
    images: imgs('SPN-0017', 8),
    factory: ['king/factory/AF-BG-10005__balance_scale_brass.mp4'],
  },
  {
    id: 'SPN-0018',
    kind: 'trade',
    rawDur: 24.0,
    title: 'A trade decided by one vote',
    kicker: 'ACT IV',
    images: imgs('SPN-0018', 6),
    overlay: ['king/factory/AF-PART-0052__dust_particles_floating.mp4'],
  },
  {
    id: 'SPN-0019',
    kind: 'finalSplit',
    rawDur: 24.8,
    title: 'Identify you — or investigate you?',
    kicker: 'ENDING',
    videos: ['king/pixabay_v_50109.mp4', 'king/pexels_v_8061661.mp4'],
    factory: ['king/factory/AF-BG-23408__police_interrogation_room_empty.mp4'],
  },
  {
    id: 'SPN-0020',
    kind: 'seriesStack',
    rawDur: 20.4,
    title: 'Pockets → phone → property → contracts → body',
    kicker: 'ENDING',
    images: imgs('SPN-0020', 5),
    factory: ['king/factory/AF-BG-7464__circuit_data_flow.mp4', 'king/factory/AF-LOOP-0002__abstract_loop_dark.mp4'],
  },
  {
    id: 'SPN-0021',
    kind: 'nextHome',
    rawDur: 28.0,
    title: 'Next: can a cop follow you into your home?',
    kicker: 'NEXT',
    images: imgs('SPN-0021', 6),
    factory: ['king/factory/AF-BG-1742__front_door_house.mp4', 'king/factory/AF-BG-1607__suburban_house_exterior_night.jpg'],
  },
];

const scenes = (() => {
  let cursor = 0;
  const out: Array<Scene & {start: number; dur: number}> = [];
  bodyScenes.forEach((scene, index) => {
    if (index === 1) {
      const hookTiming = KING_SCENE_TIMING['SPN-0001'];
      out.push({id: 'brand', kind: 'brand', rawDur: OPENING_SEC, start: hookTiming ? hookTiming.start + hookTiming.dur : cursor, dur: OPENING_SEC, title: 'King'});
      cursor += OPENING_SEC;
    }
    const timing = KING_SCENE_TIMING[scene.id];
    const dur = timing ? timing.dur : scene.rawDur * SCALE;
    const start = timing ? timing.start : cursor;
    out.push({...scene, start, dur});
    cursor = start + dur;
  });
  out.push({id: 'end', kind: 'end', rawDur: ENDCARD_SEC, start: cursor, dur: ENDCARD_SEC, title: ''});
  return out;
})();

const fit = (text: string, max = 76): number => Math.min(max, Math.max(34, 1120 / Math.max(text.length, 14)));

const progress = (frame: number, duration: number): number =>
  interpolate(frame, [0, Math.max(1, duration)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

const ease = (p: number): number => p * p * (3 - 2 * p);

const ImageCycle: React.FC<{images?: string[]; seed: string; dim?: number}> = ({images = [], seed, dim = 0.76}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  if (!images.length) return null;
  const seg = Math.max(Math.round(4.5 * fps), Math.round(durationInFrames / images.length));
  const idx = Math.floor(frame / seg) % images.length;
  const next = (idx + 1) % images.length;
  const local = frame % seg;
  const p = ease(progress(local, seg));
  const cross = images.length > 1 ? interpolate(local, [seg * 0.78, seg], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 0;
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
        transform: `translate3d(${dir * (-44 + p * 88) + offset * 20}px, ${20 - p * 44 - offset * 12}px, 0) scale(${1.08 + p * 0.08 + offset * 0.03})`,
        filter: `brightness(${dim}) contrast(1.2) saturate(1.02)`,
      }}
    />
  );
  return (
    <AbsoluteFill>
      {render(images[idx], 1, 0)}
      {images.length > 1 ? render(images[next], cross, 1) : null}
    </AbsoluteFill>
  );
};

const VideoCycle: React.FC<{videos?: string[]; dim?: number}> = ({videos = [], dim = 0.54}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  if (!videos.length) return null;
  const seg = Math.max(Math.round(4.5 * fps), Math.round(durationInFrames / videos.length));
  const idx = Math.floor(frame / seg) % videos.length;
  return (
    <AbsoluteFill>
      <Loop durationInFrames={seg}>
        <Video
          src={staticFile(videos[idx])}
          muted
          style={{width: '100%', height: '100%', objectFit: 'cover', filter: `brightness(${dim}) contrast(1.15) saturate(0.9)`}}
        />
      </Loop>
    </AbsoluteFill>
  );
};

const FactoryLayer: React.FC<{scene: Scene}> = ({scene}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const assets = scene.factory ?? [];
  const seg = Math.max(Math.round(6 * fps), Math.round(durationInFrames / Math.max(1, assets.length)));
  const src = assets.length ? assets[Math.floor(frame / seg) % assets.length] : null;
  const overlay = (scene.overlay ?? [])[0];
  return (
    <>
      <AbsoluteFill style={{background: `radial-gradient(80% 75% at 62% 38%, #14335c 0%, ${NAVY} 34%, ${INK} 86%)`}} />
      {src ? src.endsWith('.mp4') ? (
        <AbsoluteFill style={{opacity: 0.36, mixBlendMode: 'screen'}}>
          <Loop durationInFrames={seg}>
            <Video src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.66) contrast(1.2) saturate(0.9)'}} />
          </Loop>
        </AbsoluteFill>
      ) : (
        <Img src={staticFile(src)} style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: 0.32, filter: 'brightness(0.66) contrast(1.18)'}} />
      ) : null}
      {scene.texture ? (
        <Img
          src={staticFile(scene.texture)}
          style={{position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', opacity: 0.13, mixBlendMode: 'overlay'}}
        />
      ) : null}
      {overlay ? (
        <AbsoluteFill style={{opacity: scene.kind === 'ruling' ? 0.34 : 0.16, mixBlendMode: 'screen'}}>
          <Loop durationInFrames={Math.round(5 * fps)}>
            <Video src={staticFile(overlay)} muted style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.9) contrast(1.25)'}} />
          </Loop>
        </AbsoluteFill>
      ) : null}
    </>
  );
};

const Shell: React.FC<{scene: Scene; children: React.ReactNode}> = ({scene, children}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = ease(progress(frame, durationInFrames));
  const drift = interpolate(p, [0, 1], [-24, 24]);
  const sceneColor = scene.kind === 'ruling' || scene.kind === 'scales' ? GOLD : BLUE;
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate3d(${drift}px, ${-drift * 0.3}px, 0) scale(${1.02 + p * 0.045})`}}>
        <FactoryLayer scene={scene} />
        <ImageCycle images={scene.images} seed={scene.id} />
        <VideoCycle videos={scene.videos} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: `linear-gradient(180deg, ${INK}DD 0%, #00000010 40%, ${INK}E8 100%)`}} />
      <LightSweep seed={scene.id} color={sceneColor} />
      <Particles seed={scene.id} count={scene.kind === 'ruling' ? 34 : 22} color={sceneColor} />
      {children}
      <Lower scene={scene} />
      <ReconLabel />
      <Citation scene={scene} />
      <Vignette strength={1} />
      <Grain opacity={0.045} />
    </AbsoluteFill>
  );
};

const ReconLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 52,
      top: 48,
      fontFamily: BRAND.font.body,
      fontSize: 19,
      color: SILVER,
      padding: '8px 12px',
      border: `1px solid ${GOLD}77`,
      background: '#00000094',
      letterSpacing: 0,
    }}
  >
    AI / symbolic reconstruction
  </div>
);

const Citation: React.FC<{scene: Scene}> = ({scene}) => {
  if (!scene.citation) return null;
  return (
    <div style={{position: 'absolute', right: 56, bottom: 208, fontFamily: BRAND.font.body, fontSize: 22, color: GOLD, background: '#000000AA', padding: '9px 13px', borderTop: `2px solid ${GOLD}`}}>
      {scene.citation}
    </div>
  );
};

const Lower: React.FC<{scene: Scene}> = ({scene}) => {
  if (!scene.title || scene.kind === 'end' || scene.kind === 'brand') return null;
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - Math.round(0.12 * fps), fps, config: {damping: 18, stiffness: 92}});
  return (
    <div style={{position: 'absolute', left: 56, top: 44, opacity: Math.min(1, e), maxWidth: 1220}}>
      <div style={{fontFamily: BRAND.font.body, fontSize: 18, color: GOLD, fontWeight: 800}}>{scene.kicker ?? 'PRIME DOCUMENTARY'}</div>
      <div style={{width: 282, height: 2, background: GOLD, marginTop: 9, marginBottom: 20}} />
      <div style={{fontFamily: BRAND.font.display, fontSize: fit(scene.title), color: WHITE, textTransform: 'uppercase', textShadow: '0 4px 24px #000', lineHeight: 1.02}}>
        {scene.title}
      </div>
      {scene.subtitle ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 10, maxWidth: 960}}>{scene.subtitle}</div> : null}
    </div>
  );
};

const TwoColumn: React.FC<{left: string; right: string; leftSub?: string; rightSub?: string}> = ({left, right, leftSub, rightSub}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <div style={{position: 'absolute', left: 245, right: 245, top: 372, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 46}}>
      {[{t: left, s: leftSub, c: BLUE, d: 0}, {t: right, s: rightSub, c: GOLD, d: 8}].map((b) => {
        const e = spring({frame: frame - Math.round(0.25 * fps) - b.d, fps, config: {damping: 18, stiffness: 110}});
        return (
          <div key={b.t} style={{border: `3px solid ${b.c}`, background: '#020409d8', minHeight: 254, padding: 34, transform: `translateY(${interpolate(e, [0, 1], [32, 0])}px)`, opacity: Math.min(1, e)}}>
            <div style={{fontFamily: BRAND.font.display, fontSize: fit(b.t, 62), color: b.c, textTransform: 'uppercase', lineHeight: 1.02}}>{b.t}</div>
            {b.s ? <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 20}}>{b.s}</div> : null}
          </div>
        );
      })}
    </div>
  );
};

const DnaFlow: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = ease(progress(frame, durationInFrames));
  const cells = Array.from({length: 56}, (_, i) => ({x: 1120 + (i % 8) * 72, y: 292 + Math.floor(i / 8) * 58}));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.9" transform={`translate(${interpolate(p, [0, 1], [-40, 110])} 0)`}>
        <rect x="248" y="506" width="370" height="36" rx="18" fill={WHITE} opacity="0.9" />
        <rect x="575" y="496" width="126" height="56" rx="12" fill={GOLD} opacity="0.92" />
        <text x="432" y="485" fill={SILVER} fontSize="24" fontFamily={BRAND.font.body} textAnchor="middle">cheek swab</text>
      </g>
      <g fill="none" strokeLinecap="round" opacity="0.95">
        {Array.from({length: 18}, (_, i) => {
          const x = 690 + i * 28 + p * 330;
          const y1 = 440 + Math.sin(i * 0.8 + frame * 0.07) * 80;
          const y2 = 620 - Math.sin(i * 0.8 + frame * 0.07) * 80;
          return (
            <g key={i}>
              <line x1={x} y1={y1} x2={x} y2={y2} stroke={i % 2 ? BLUE : GOLD} strokeWidth="4" opacity={1 - p * 0.2} />
              <circle cx={x} cy={y1} r="7" fill={BLUE} />
              <circle cx={x} cy={y2} r="7" fill={GOLD} />
            </g>
          );
        })}
      </g>
      <g>
        {cells.map((c, i) => {
          const on = interpolate(p, [0.35 + i * 0.006, 0.52 + i * 0.006], [0.14, 0.88], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return <rect key={i} x={c.x} y={c.y} width="50" height="38" fill={i === 37 ? GOLD : BLUE} opacity={on} stroke={SILVER} strokeOpacity="0.25" />;
        })}
      </g>
      <text x="1365" y="790" fill={GOLD} fontSize="34" fontFamily={BRAND.font.display} textAnchor="middle">DATABASE SEARCH</text>
    </svg>
  );
};

const MarylandMap: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 0.4 + 0.6 * Math.sin(frame * 0.12);
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <path d="M415 580 C520 450 680 410 795 450 C900 485 1010 430 1115 468 C1250 518 1335 500 1482 545" fill="none" stroke={SILVER} strokeWidth="10" opacity="0.42" />
      <circle cx="1252" cy="512" r={42 + pulse * 34} fill="none" stroke={GOLD} strokeWidth="5" opacity="0.7" />
      <circle cx="1252" cy="512" r="14" fill={GOLD} />
      <text x="1252" y="454" fill={WHITE} fontFamily={BRAND.font.display} fontSize="56" textAnchor="middle">MARYLAND</text>
      <text x="760" y="760" fill={GOLD} fontFamily={BRAND.font.display} fontSize="118" textAnchor="middle">2009</text>
      <rect x="1055" y="718" width="500" height="76" fill="#000000B8" stroke={RED} strokeWidth="3" />
      <text x="1305" y="770" fill={RED} fontFamily={BRAND.font.display} fontSize="52" textAnchor="middle">ASSAULT ARREST</text>
    </svg>
  );
};

const MatchGrid: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = progress(frame, durationInFrames);
  const scanX = interpolate(p, [0.1, 0.72], [330, 1500], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.62">
        {Array.from({length: 11}, (_, y) =>
          Array.from({length: 17}, (_, x) => {
            const match = x === 12 && y === 6;
            const lit = p > 0.58 && match;
            return <rect key={`${x}-${y}`} x={330 + x * 72} y={240 + y * 52} width="48" height="34" fill={lit ? GOLD : BLUE} opacity={lit ? 1 : 0.28} stroke={SILVER} strokeOpacity="0.22" />;
          }),
        )}
      </g>
      <rect x={scanX} y="226" width="18" height="610" fill={GOLD} opacity="0.76" />
      {p > 0.58 ? (
        <g>
          <rect x="1172" y="544" width="258" height="104" fill="#000000D8" stroke={GOLD} strokeWidth="5" />
          <text x="1301" y="615" fill={GOLD} fontFamily={BRAND.font.display} fontSize="70" textAnchor="middle">MATCH</text>
          <text x="1301" y="685" fill={SILVER} fontFamily={BRAND.font.body} fontSize="30" textAnchor="middle">2003 cold case</text>
        </g>
      ) : null}
    </svg>
  );
};

const FingerprintIcon: React.FC<{x: number; y: number; color: string}> = ({x, y, color}) => (
  <g transform={`translate(${x} ${y})`} fill="none" stroke={color} strokeWidth="5" strokeLinecap="round">
    {[0, 1, 2, 3, 4].map((i) => <path key={i} d={`M ${-80 + i * 20} ${20 + i * 8} C ${-70 + i * 18} ${-96 + i * 3}, ${72 - i * 10} ${-96 + i * 8}, ${88 - i * 24} ${18 + i * 10}`} opacity={0.9 - i * 0.1} />)}
  </g>
);

const FingerprintDna: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = ease(progress(frame, durationInFrames));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <FingerprintIcon x={610 - p * 90} y={560} color={BLUE} />
      <text x="590" y="770" fill={BLUE} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">FINGERPRINT</text>
      <path d={`M 820 560 C 960 ${390 + p * 80}, 1110 ${730 - p * 110}, 1260 540`} fill="none" stroke={GOLD} strokeWidth="8" opacity={0.75} />
      {Array.from({length: 13}, (_, i) => <circle key={i} cx={1030 + i * 28} cy={540 + Math.sin(i * 0.85 + frame * 0.08) * 90} r="8" fill={i % 2 ? BLUE : GOLD} />)}
      <text x="1255" y="770" fill={GOLD} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">DNA</text>
      <text x="960" y="850" fill={WHITE} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">"the fingerprint of the 21st century"</text>
    </svg>
  );
};

const CodisNetwork: React.FC = () => {
  const frame = useCurrentFrame();
  const nodes = Array.from({length: 42}, (_, i) => ({
    x: 370 + ((i * 137) % 1180),
    y: 260 + ((i * 83) % 520),
  }));
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <g opacity="0.42">
        {nodes.map((n, i) => <line key={i} x1={n.x} y1={n.y} x2="960" y2="540" stroke={i % 3 ? BLUE : GOLD} strokeWidth="2" />)}
      </g>
      {nodes.map((n, i) => {
        const on = interpolate(frame, [i * 3, i * 3 + 18], [0.15, 0.95], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        return <circle key={i} cx={n.x} cy={n.y} r={i % 7 === 0 ? 11 : 7} fill={i % 5 === 0 ? GOLD : BLUE} opacity={on} />;
      })}
      <circle cx="960" cy="540" r="82" fill="#000000D8" stroke={GOLD} strokeWidth="5" />
      <text x="960" y="556" fill={GOLD} fontFamily={BRAND.font.display} fontSize="62" textAnchor="middle">CODIS</text>
    </svg>
  );
};

const Vote: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <svg width="1920" height="1080" style={{position: 'absolute'}}>
      <text x="960" y="280" fill={GOLD} fontFamily={BRAND.font.display} fontSize="96" textAnchor="middle">2013</text>
      <g transform="translate(530 408)">
        {Array.from({length: 9}, (_, i) => {
          const e = spring({frame: frame - Math.round(0.45 * fps) - i * 3, fps, config: {damping: 15, stiffness: 110}});
          const yes = i < 5;
          return <rect key={i} x={(i % 5) * 150} y={Math.floor(i / 5) * 142} width="95" height="95" rx="10" fill={yes ? BLUE : '#3A3D46'} stroke={yes ? GOLD : SILVER} strokeWidth="4" opacity={Math.min(1, e)} />;
        })}
        <text x="365" y="342" fill={WHITE} fontFamily={BRAND.font.display} fontSize="112" textAnchor="middle">5–4</text>
      </g>
      <path d="M620 830 L1300 830" stroke={GOLD} strokeWidth="5" />
      <text x="960" y="888" fill={GOLD} fontFamily={BRAND.font.body} fontSize="34" textAnchor="middle">569 U.S. 435</text>
    </svg>
  );
};

const KennedyColumns: React.FC = () => (
  <div style={{position: 'absolute', left: 360, right: 360, top: 342, display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 28}}>
    {[
      ['Dangerousness', 'What risk is in custody?'],
      ['Flight risk', 'Will this person appear?'],
      ['Safe processing', 'How should custody work?'],
    ].map(([a, b]) => (
      <div key={a} style={{minHeight: 280, padding: 30, background: '#020409D8', border: `3px solid ${GOLD}`}}>
        <div style={{fontFamily: BRAND.font.display, fontSize: 48, color: GOLD, textTransform: 'uppercase'}}>{a}</div>
        <div style={{fontFamily: BRAND.font.body, fontSize: 28, color: SILVER, marginTop: 24}}>{b}</div>
      </div>
    ))}
  </div>
);

const Coalition: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    {[
      ['SCALIA', 420, 350, BLUE],
      ['GINSBURG', 420, 690, GOLD],
      ['SOTOMAYOR', 1500, 350, GOLD],
      ['KAGAN', 1500, 690, GOLD],
    ].map(([name, x, y, color]) => (
      <g key={name as string}>
        <text x={x as number} y={y as number} fill={color as string} fontFamily={BRAND.font.display} fontSize="58" textAnchor="middle">{name}</text>
        <line x1={x as number} y1={(y as number) + 24} x2="960" y2="540" stroke={color as string} strokeWidth="5" opacity="0.75" />
      </g>
    ))}
    <circle cx="960" cy="540" r="78" fill="#000000D8" stroke={GOLD} strokeWidth="5" />
    <text x="960" y="558" fill={WHITE} fontFamily={BRAND.font.display} fontSize="48" textAnchor="middle">DISSENT</text>
  </svg>
);

const ScaliaWords: React.FC = () => {
  const frame = useCurrentFrame();
  const words = ['rightly', 'or', 'wrongly,', 'and', 'for', 'whatever', 'reason'];
  return (
    <div style={{position: 'absolute', left: 250, right: 250, top: 340, display: 'flex', flexWrap: 'wrap', gap: 18, justifyContent: 'center'}}>
      {words.map((word, i) => {
        const show = frame > i * 38;
        return (
          <div key={word} style={{fontFamily: BRAND.font.display, fontSize: i === 6 ? 84 : 70, color: i === 6 ? GOLD : WHITE, opacity: show ? 1 : 0.08, padding: '10px 16px', background: show ? '#000000B8' : '#00000044', borderBottom: `3px solid ${show ? GOLD : SILVER}`}}>
            {word}
          </div>
        );
      })}
    </div>
  );
};

const BalanceScales: React.FC = () => (
  <svg width="1920" height="1080" style={{position: 'absolute'}}>
    <line x1="960" y1="310" x2="960" y2="780" stroke={GOLD} strokeWidth="8" />
    <line x1="610" y1="430" x2="1310" y2="430" stroke={GOLD} strokeWidth="8" />
    {[
      ['Crimes solved', 610, BLUE],
      ['Merely arrested', 1310, GOLD],
    ].map(([label, x, color]) => (
      <g key={label as string}>
        <line x1={x as number} y1="430" x2={(x as number) - 130} y2="610" stroke={SILVER} strokeWidth="4" />
        <line x1={x as number} y1="430" x2={(x as number) + 130} y2="610" stroke={SILVER} strokeWidth="4" />
        <path d={`M ${(x as number) - 170} 612 Q ${x} 692 ${(x as number) + 170} 612`} fill="none" stroke={color as string} strokeWidth="7" />
        <text x={x as number} y="745" fill={color as string} fontFamily={BRAND.font.display} fontSize="46" textAnchor="middle">{label}</text>
      </g>
    ))}
  </svg>
);

const SeriesStack: React.FC = () => {
  const frame = useCurrentFrame();
  const items = ['pockets', 'phone', 'property', 'contracts', 'body'];
  return (
    <div style={{position: 'absolute', left: 420, right: 420, top: 265}}>
      {items.map((item, i) => {
        const on = frame > 18 + i * 22;
        return (
          <div key={item} style={{height: 95, marginBottom: 14, border: `3px solid ${i === 4 ? GOLD : BLUE}`, background: '#020409D8', opacity: on ? 1 : 0.12, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <span style={{fontFamily: BRAND.font.display, color: i === 4 ? GOLD : WHITE, fontSize: i === 4 ? 70 : 56, textTransform: 'uppercase'}}>{item}</span>
          </div>
        );
      })}
    </div>
  );
};

const SceneContent: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'brand') return <BrandOpening seriesLabel="Prime Documentary" title="Maryland v. King" subtitle="DNA at booking" />;
  if (scene.kind === 'end') return <BrandEndcard />;
  return (
    <Shell scene={scene}>
      {scene.kind === 'dnaFlow' ? <DnaFlow /> : null}
      {scene.kind === 'splitQuestion' ? <TwoColumn left="Identification" right="Search" leftSub="booking process" rightSub="evidence gathering" /> : null}
      {scene.kind === 'maryland' ? <MarylandMap /> : null}
      {scene.kind === 'notReason' ? <TwoColumn left="Assault arrest" right="NOT the reason" leftSub="already underway" rightSub="cheek swab came during booking" /> : null}
      {scene.kind === 'matchGrid' ? <MatchGrid /> : null}
      {scene.kind === 'dualView' ? <TwoColumn left="Cold case solved" right="Suspicionless search" leftSub="public safety" rightSub="privacy objection" /> : null}
      {scene.kind === 'bothTrue' ? <BigCenter text="BOTH DESCRIPTIONS ARE TRUE" /> : null}
      {scene.kind === 'fingerprintSearch' ? <TwoColumn left="Fingerprint" right="Search?" leftSub="identify" rightSub="investigate" /> : null}
      {scene.kind === 'bookingEquation' ? <BigCenter text="FINGERPRINTS + PHOTO = IDENTIFY" /> : null}
      {scene.kind === 'fingerprintDna' ? <FingerprintDna /> : null}
      {scene.kind === 'codis' ? <CodisNetwork /> : null}
      {scene.kind === 'blueprint' ? <TwoColumn left="Fingerprint" right="Genetic blueprint" leftSub="thin identifier" rightSub="deeper private information" /> : null}
      {scene.kind === 'ruling' ? <Vote /> : null}
      {scene.kind === 'kennedyQuote' ? <BigCenter text="LIKE FINGERPRINTING AND PHOTOGRAPHING" /> : null}
      {scene.kind === 'kennedyColumns' ? <KennedyColumns /> : null}
      {scene.kind === 'coalition' ? <Coalition /> : null}
      {scene.kind === 'scaliaWords' ? <ScaliaWords /> : null}
      {scene.kind === 'national' ? <BigCenter text="ARREST → DNA SAMPLE → DATABASE" /> : null}
      {scene.kind === 'scales' ? <BalanceScales /> : null}
      {scene.kind === 'trade' ? <BigCenter text="ONE VOTE DECIDED THE TRADE" /> : null}
      {scene.kind === 'finalSplit' ? <TwoColumn left="Identify you" right="Investigate you?" /> : null}
      {scene.kind === 'seriesStack' ? <SeriesStack /> : null}
      {scene.kind === 'nextHome' ? <BigCenter text="CAN THEY FOLLOW YOU INSIDE?" /> : null}
    </Shell>
  );
};

const CaptionOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cap = KING_CAPTIONS.find((c) => t >= c.start && t <= c.end);
  if (!cap) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 220,
        right: 220,
        bottom: 44,
        minHeight: 104,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        padding: '16px 28px',
        background: '#000000B0',
        borderRadius: 4,
        boxShadow: '0 10px 34px #000000AA',
        zIndex: 20,
      }}
    >
      <div
        style={{
          fontFamily: BRAND.font.body,
          fontSize: cap.text.length > 58 ? 48 : 54,
          lineHeight: 1.13,
          fontWeight: 900,
          color: WHITE,
          textShadow: '0 3px 0 #000, 0 0 16px #000, 0 0 26px #000',
          maxWidth: 1320,
        }}
      >
        {cap.text}
      </div>
    </div>
  );
};

const BigCenter: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - Math.round(0.2 * fps), fps, config: {damping: 16, stiffness: 100}});
  return (
    <div style={{position: 'absolute', left: 220, right: 220, top: 425, textAlign: 'center', transform: `scale(${interpolate(e, [0, 1], [0.92, 1])})`, opacity: Math.min(1, e)}}>
      <div style={{display: 'inline-block', fontFamily: BRAND.font.display, fontSize: fit(text, 86), color: WHITE, textTransform: 'uppercase', padding: '22px 34px', background: '#000000C8', border: `3px solid ${text.includes('NOT') ? RED : GOLD}`, textShadow: '0 5px 30px #000'}}>
        {text}
      </div>
    </div>
  );
};

export const KingPremium: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: INK}}>
    <Audio src={staticFile('king/audio/final_mix_v001.mp3')} />
    {scenes.map((scene) => (
      <Sequence key={scene.id} from={Math.round(scene.start * FPS)} durationInFrames={Math.round(scene.dur * FPS)}>
        <SceneContent scene={scene} />
      </Sequence>
    ))}
    <CaptionOverlay />
  </AbsoluteFill>
);

export const kingPremiumDurationInFrames = (fps: number): number => Math.round(TARGET_SEC * fps);
