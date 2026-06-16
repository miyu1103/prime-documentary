import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {KineticType} from '../components/KineticType';
import {DiagramFlow} from '../components/DiagramFlow';
import {SceneArt} from '../components/SceneArt';
import {Grain} from '../components/Grain';
import {AnimaticScene, MIRANDA_ANIMATIC} from '../data/miranda_animatic';

const SCENE_IMG: Partial<Record<string, string>> = {
  S002: 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  S003: 'mj/s003_phoenix_arrest.png',
  S004: 'approved/s004_interrogation_room_01_primary.png',
  S005: 'mj/s005_interrogation_imbalance.png',
  S006: 'mj/s006_arrest_record.png',
  S007: 'approved/s007_courtroom_1960s_01_primary.png',
  S008: 'mj/s008_scotus_exterior.png',
  S009: 'mj/s009_four_cases_scotus.png',
  S010: 'mj/s010_s015_chief_justice.png',
  S011: 'mj/s008_scotus_exterior.png',
  S012: 'mj/s012_scotus_chamber.png',
  S013: 'mj/s013_miranda_rights_card.png',
  S014: 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  S015: 'mj/s010_s015_chief_justice.png',
  S016: 'approved/s016_miranda_warning_card_01_primary.png',
  S017: 'mj/s017_miranda_warning_reading.png',
  S018: 'approved/s018_retrial_symbolic_01_primary.png',
  S019: 'mj/s016_miranda_rights_wall.png',
  S020: 'mj/s007_courtroom_trial.png',
  S021: 'approved/s002_s014_constitution_fifth_amendment_01_primary.png',
  S022: 'mj/s018_courtroom_retrial.png',
};

const INK   = BRAND.color.ink;
const NAVY  = BRAND.color.navy;
const GOLD  = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

const DARK_BG: React.CSSProperties = {
  background: `radial-gradient(120% 100% at 50% 40%, ${NAVY} 0%, ${INK} 85%)`,
};

/** Ken Burns pan-and-zoom. No dark overlay — images are meant to be seen. */
const ImageBg: React.FC<{src: string}> = ({src}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = durationInFrames > 1 ? frame / (durationInFrames - 1) : 0;
  const scale = 1.0 + p * 0.05;
  const tx = p * -18;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Img
        src={staticFile(src)}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `scale(${scale}) translateX(${tx}px)`,
          transformOrigin: 'center center',
        }}
      />
    </AbsoluteFill>
  );
};

/** Bottom-gradient so caption text is always readable over images. */
const BottomGrad: React.FC = () => (
  <AbsoluteFill style={{
    background: `linear-gradient(to bottom, transparent 50%, ${INK}CC 100%)`,
    pointerEvents: 'none',
  }} />
);

/** Caption pinned to bottom-left of image. */
const ImageCaption: React.FC<{lines: string[]; italic?: boolean}> = ({lines, italic = false}) => (
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-start', padding: '0 52px 72px'}}>
    {lines.map((line, i) => (
      <div key={i} style={{
        color: i === 0 ? WHITE : SILVER,
        fontFamily: BRAND.font.display,
        fontSize: i === 0 ? 28 : 20,
        fontStyle: italic ? 'italic' : 'normal',
        letterSpacing: 0.5,
        marginBottom: 4,
        borderLeft: i === 0 ? `3px solid ${GOLD}` : undefined,
        paddingLeft: i === 0 ? 14 : 17,
      }}>
        {line}
      </div>
    ))}
  </AbsoluteFill>
);

/** Thin top-bar so the KineticType is legible over images. */
const TopShade: React.FC = () => (
  <AbsoluteFill style={{
    background: `linear-gradient(to bottom, ${INK}BB 0%, transparent 40%)`,
    pointerEvents: 'none',
  }} />
);

const SceneVisual: React.FC<{scene: AnimaticScene; sceneImg: Partial<Record<string, string>>}> = ({scene, sceneImg}) => {
  const {visualMode: m, onScreenText: ost, motifHint, sceneId} = scene;
  const imgSrc = sceneImg[sceneId];

  // ── Typography ─────────────────────────────────────────────────────────────
  if (m === 'typography') {
    const lines = (ost.length ? ost : ['Prime Documentary']).map((t, i) => ({
      text: t, at: i * 8, emphasis: i === 0,
    }));
    return (
      <AbsoluteFill>
        {imgSrc ? <ImageBg src={imgSrc} /> : <AbsoluteFill style={DARK_BG} />}
        {imgSrc && <TopShade />}
        <KineticType lines={lines} />
      </AbsoluteFill>
    );
  }

  // ── Diagram (multi-step flow) ───────────────────────────────────────────────
  if (m === 'diagram') {
    if (ost.length >= 2) {
      return (
        <AbsoluteFill>
          {imgSrc ? <ImageBg src={imgSrc} /> : <AbsoluteFill style={DARK_BG} />}
          {imgSrc && <TopShade />}
          <DiagramFlow steps={ost.slice(0, 4)} />
        </AbsoluteFill>
      );
    }
    // Single label → image + caption
    return (
      <AbsoluteFill>
        {imgSrc ? <ImageBg src={imgSrc} /> : <AbsoluteFill style={DARK_BG} />}
        {imgSrc && ost.length > 0 && <><BottomGrad /><ImageCaption lines={ost} /></>}
        {!imgSrc && ost.length > 0 && <ImageCaption lines={ost} />}
      </AbsoluteFill>
    );
  }

  // ── Abstract / atmospheric ─────────────────────────────────────────────────
  if (m === 'abstract' || m === 'breathing' || m === 'transition_texture') {
    if (imgSrc) return <ImageBg src={imgSrc} />;
    return <AbsoluteFill style={{background: `radial-gradient(ellipse at 40% 60%, ${NAVY}88 0%, ${INK} 70%)`}} />;
  }

  // ── Map / reenactment / archival / object / location / timeline ────────────
  if (imgSrc) {
    const isRec = m === 'reenactment';
    const hasCaption = ost.length > 0;
    return (
      <AbsoluteFill>
        <ImageBg src={imgSrc} />
        {hasCaption && <BottomGrad />}
        {hasCaption && <ImageCaption lines={ost.slice(0, 2)} italic={isRec} />}
      </AbsoluteFill>
    );
  }

  // ── Fallback: coded art (no image available) ───────────────────────────────
  return <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} seed={sceneId} />;
};

export type AnimaticProps = {
  bgmSrc?: string | null;
  scenes?: AnimaticScene[];
  sceneImg?: Partial<Record<string, string>>;
};

export const Animatic: React.FC<AnimaticProps> = ({
  bgmSrc = 'bgm_placeholder.wav',
  scenes = MIRANDA_ANIMATIC,
  sceneImg = SCENE_IMG,
}) => {
  const {fps} = useVideoConfig();
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {scenes.map((scene) => {
        const from = Math.round(cursor * fps);
        const dur  = Math.round(scene.durationSec * fps);
        cursor += scene.durationSec;
        return (
          // No transition component — hard cuts look clean with Ken Burns motion
          <Sequence key={scene.sceneId} from={from} durationInFrames={dur} name={scene.sceneId}>
            <SceneVisual scene={scene} sceneImg={sceneImg} />
          </Sequence>
        );
      })}
      <Grain opacity={0.04} />
      {bgmSrc ? <Audio src={staticFile(bgmSrc)} volume={0.35} loop /> : null}
    </AbsoluteFill>
  );
};

export const durationInFramesFor = (scenes: AnimaticScene[], fps: number): number =>
  Math.round(scenes.reduce((a, s) => a + s.durationSec, 0) * fps);

export const animaticDurationInFrames = (fps: number): number =>
  durationInFramesFor(MIRANDA_ANIMATIC, fps);
