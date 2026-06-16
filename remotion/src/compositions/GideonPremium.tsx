import React from 'react';
import {
  AbsoluteFill,
  Img,
  OffthreadVideo,
  Sequence,
  spring,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {KineticType} from '../components/KineticType';
import {DiagramFlow} from '../components/DiagramFlow';
import {SceneArt} from '../components/SceneArt';
import {Grain} from '../components/Grain';
import {CameraRig, Particles, LightSweep, Vignette} from '../components/Motion';
import {AnimaticScene} from '../data/miranda_animatic';
import {GIDEON_ANIMATIC, GIDEON_SCENE_IMG} from '../data/gideon_animatic';

/**
 * GideonPremium — the 0004-standard cut: every shot MOVES (CameraRig + drifting
 * particles + light sweep + vignette = the "moving stage", premium with zero warp),
 * real PD assets used first (petition / Black portrait), the 9 Runway clips run as a
 * ~5s motion beat at the head of their scene then cut to the detailed still, and AI
 * reenactment shots carry a "symbolic reconstruction" label (invariant 11). Brand
 * colour-grade + grain are applied uniformly in the ffmpeg finish (assemble_gideon_premium).
 */

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

// Runway clip per scene (5.04s each) — plays as the opening motion beat.
const CLIP: Partial<Record<string, string>> = {
  S002: 'clips/clip_s002_cell_pushin.mp4',
  S005: 'clips/clip_s005_chair_light.mp4',
  S007: 'clips/clip_s007_verdict.mp4',
  S009: 'clips/clip_s009_writing_motion.mp4',
  S011: 'clips/clip_s011_wall_push.mp4',
  S013: 'clips/clip_s013_fortas_walk.mp4',
  S019: 'clips/clip_s019_letter_drift.mp4',
  S020: 'clips/clip_s020_retrial_pan.mp4',
  S024: 'clips/clip_s024_desk_drift.mp4',
};

// Real PD assets first where they exist (overrides the AI still map).
const IMG: Partial<Record<string, string>> = {
  ...GIDEON_SCENE_IMG,
  S001: 'real/gideon_petition_cert_p1.jpg', // hero: the actual pencil petition
  S008: 'real/gideon_petition_cert_p1.jpg',
  S009: 'real/gideon_petition_cert_p2.jpg',
  S010: 'real/gideon_petition_cert_p3.jpg',
  S015: 'real/hugo_black_portrait_loc.jpg', // real opinion author
};

const REAL_SCENES = new Set(['S001', 'S008', 'S009', 'S010', 'S015']); // real PD → no recon label
const RECON = new Set(['S002', 'S004', 'S007', 'S013', 'S020', 'S021', 'S027']); // AI reenactment → label
const CLIP_SEC = 5.0;

const ImageBase: React.FC<{src: string}> = ({src}) => (
  <AbsoluteFill style={{overflow: 'hidden'}}>
    <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </AbsoluteFill>
);

const BottomGrad: React.FC = () => (
  <AbsoluteFill style={{background: `linear-gradient(to bottom, transparent 50%, ${INK}CC 100%)`, pointerEvents: 'none'}} />
);
const TopShade: React.FC = () => (
  <AbsoluteFill style={{background: `linear-gradient(to bottom, ${INK}BB 0%, transparent 40%)`, pointerEvents: 'none'}} />
);

const ImageCaption: React.FC<{lines: string[]; italic?: boolean}> = ({lines, italic = false}) => (
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-start', padding: '0 52px 84px'}}>
    {lines.map((line, i) => (
      <div key={i} style={{
        color: i === 0 ? WHITE : SILVER, fontFamily: BRAND.font.display,
        fontSize: i === 0 ? 30 : 21, fontStyle: italic ? 'italic' : 'normal',
        letterSpacing: 0.5, marginBottom: 5,
        borderLeft: i === 0 ? `3px solid ${GOLD}` : undefined, paddingLeft: i === 0 ? 14 : 17,
      }}>{line}</div>
    ))}
  </AbsoluteFill>
);

const ReconLabel: React.FC = () => (
  <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'flex-end', padding: '24px 28px'}}>
    <div style={{
      color: SILVER, fontFamily: BRAND.font.body, fontSize: 15, letterSpacing: 0.6,
      background: `${INK}99`, padding: '5px 11px', borderRadius: 4, border: `1px solid ${SILVER}33`,
    }}>symbolic reconstruction — not authentic footage</div>
  </AbsoluteFill>
);

/** The detailed still / coded base for a scene, wrapped in the moving stage. */
const StillStage: React.FC<{scene: AnimaticScene}> = ({scene}) => {
  const {visualMode: m, onScreenText: ost, motifHint, sceneId} = scene;
  const imgSrc = IMG[sceneId];
  const isReal = REAL_SCENES.has(sceneId);

  let inner: React.ReactNode;
  if (m === 'typography') {
    const lines = (ost.length ? ost : ['Prime Documentary']).map((t, i) => ({text: t, at: i * 8, emphasis: i === 0}));
    // With a real/detailed still, show it and overlay transparent kinetic; otherwise an opaque kinetic card.
    inner = imgSrc
      ? (<AbsoluteFill><ImageBase src={imgSrc} /><TopShade /><BottomGrad /><KineticType lines={lines} transparent /></AbsoluteFill>)
      : (<AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${NAVY} 0%, ${INK} 85%)`}}><KineticType lines={lines} /></AbsoluteFill>);
  } else if (m === 'diagram' && ost.length >= 2) {
    inner = (<AbsoluteFill><AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${NAVY} 0%, ${INK} 85%)`}} /><DiagramFlow steps={ost.slice(0, 4)} /></AbsoluteFill>);
  } else if (imgSrc) {
    const hasCap = ost.length > 0;
    inner = (<AbsoluteFill><ImageBase src={imgSrc} />{hasCap && <BottomGrad />}{hasCap && <ImageCaption lines={ost.slice(0, 2)} italic={m === 'reenactment'} />}</AbsoluteFill>);
  } else {
    inner = <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} seed={sceneId} />;
  }

  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <CameraRig seed={sceneId} intensity={1}>{inner}</CameraRig>
      <LightSweep seed={sceneId} />
      <Particles seed={sceneId} count={isReal ? 22 : 28} />
      <Vignette />
      {RECON.has(sceneId) && <ReconLabel />}
    </AbsoluteFill>
  );
};

const SceneBlock: React.FC<{scene: AnimaticScene}> = ({scene}) => {
  const {fps} = useVideoConfig();
  const clip = CLIP[scene.sceneId];
  const clipFrames = Math.round(CLIP_SEC * fps);
  const totalFrames = Math.round(scene.durationSec * fps);
  if (!clip || scene.durationSec <= CLIP_SEC + 2) {
    return <StillStage scene={scene} />;
  }
  // Runway motion beat (~5s) → cut to the detailed still moving-stage for the remainder.
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      <Sequence durationInFrames={clipFrames} name="clip">
        <AbsoluteFill style={{overflow: 'hidden'}}>
          <OffthreadVideo src={staticFile(clip)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          <Vignette />
          {RECON.has(scene.sceneId) && <ReconLabel />}
        </AbsoluteFill>
      </Sequence>
      <Sequence from={clipFrames} durationInFrames={totalFrames - clipFrames} name="still">
        <StillStage scene={scene} />
      </Sequence>
    </AbsoluteFill>
  );
};

export const ENDCARD_SEC = 9;

/** A timed reveal line. */
const Reveal: React.FC<{at: number; children: React.ReactNode; style?: React.CSSProperties}> = ({at, children, style}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const e = spring({frame: frame - at, fps, config: {damping: 18, stiffness: 110, mass: 0.7}});
  const y = interpolate(e, [0, 1], [26, 0]);
  return <div style={{transform: `translateY(${y}px)`, opacity: Math.min(e * 1.4, 1), ...style}}>{children}</div>;
};

/** Distinct branded end-card / outro: payoff → attribution → CTA + next-ep tease. */
const EndCard: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  const frame = useCurrentFrame();
  const out = interpolate(frame, [durationInFrames - 18, durationInFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 38%, ${NAVY} 0%, ${INK} 82%)`, opacity: out}}>
      <Particles seed="endcard" count={20} />
      <div style={{position: 'absolute', left: 0, right: 0, bottom: '32%', height: 4, background: GOLD, opacity: 0.85}} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 90, textAlign: 'center', gap: 16}}>
        <Reveal at={Math.round(0.3 * fps)} style={{color: WHITE, fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 78, letterSpacing: -1, textTransform: 'uppercase', textShadow: `0 0 38px ${GOLD}55`}}>
          “You have the right<br />to an attorney.”
        </Reveal>
        <Reveal at={Math.round(3.2 * fps)} style={{color: GOLD, fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 30, letterSpacing: 1}}>
          Gideon v. Wainwright · 1963 — a right won with a pencil.
        </Reveal>
      </AbsoluteFill>
      <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', padding: '0 0 70px', gap: 10}}>
        <Reveal at={Math.round(5.6 * fps)} style={{color: WHITE, fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 34}}>
          ▶ Subscribe — Landmark Rights Cases
        </Reveal>
        <Reveal at={Math.round(6.4 * fps)} style={{color: SILVER, fontFamily: BRAND.font.body, fontSize: 26}}>
          Next: who decides what counts as a crime?
        </Reveal>
        <Reveal at={Math.round(7.0 * fps)} style={{color: SILVER, fontFamily: BRAND.font.body, fontSize: 20, letterSpacing: 3, opacity: 0.8, marginTop: 8}}>
          PRIME DOCUMENTARY
        </Reveal>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const GideonPremium: React.FC = () => {
  const {fps} = useVideoConfig();
  const narrTotal = GIDEON_ANIMATIC.reduce((a, s) => a + s.durationSec, 0);
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {GIDEON_ANIMATIC.map((scene) => {
        const from = Math.round(cursor * fps);
        const dur = Math.round(scene.durationSec * fps);
        cursor += scene.durationSec;
        return (
          <Sequence key={scene.sceneId} from={from} durationInFrames={dur} name={scene.sceneId}>
            <SceneBlock scene={scene} />
          </Sequence>
        );
      })}
      <Sequence from={Math.round(narrTotal * fps)} durationInFrames={Math.round(ENDCARD_SEC * fps)} name="endcard">
        <EndCard />
      </Sequence>
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

export const gideonPremiumDurationInFrames = (fps: number): number =>
  Math.round((GIDEON_ANIMATIC.reduce((a, s) => a + s.durationSec, 0) + ENDCARD_SEC) * fps);
