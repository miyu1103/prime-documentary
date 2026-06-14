import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {KineticType} from '../components/KineticType';
import {DiagramFlow} from '../components/DiagramFlow';
import {SymbolicScene} from '../components/Parallax';
import {SceneArt} from '../components/SceneArt';
import {CameraRig, LightSweep, MovingStage, Particles, Vignette} from '../components/Motion';
import {Grain} from '../components/Grain';
import {WipeTransition} from '../components/Transition';
import {AnimaticScene, MIRANDA_ANIMATIC} from '../data/miranda_animatic';
import {SCENE_IMG} from '../data/scene_assets';

/**
 * Real image background: Ken Burns push + scrim + particles.
 * Used for any scene that has a real asset in SCENE_IMG.
 */
const RealImageBg: React.FC<{src: string; sceneId: string; ost: string[]}> = ({src, sceneId, ost}) => {
  const f = useCurrentFrame();
  const S = BRAND.color;
  return (
    <AbsoluteFill style={{backgroundColor: S.ink, overflow: 'hidden'}}>
      <CameraRig seed={sceneId} intensity={0.55}>
        <AbsoluteFill>
          <Img
            src={staticFile(src)}
            style={{width: '100%', height: '100%', objectFit: 'cover'}}
          />
        </AbsoluteFill>
      </CameraRig>
      {/* bottom-up scrim for text legibility */}
      <AbsoluteFill
        style={{background: `linear-gradient(0deg, ${S.ink}E6 0%, ${S.ink}77 30%, ${S.ink}22 58%, transparent 100%)`}}
      />
      <LightSweep seed={sceneId} />
      <Particles seed={sceneId} count={14} />
      <Vignette />
      {ost.length > 0 && (
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', paddingTop: 60}}>
          <div style={{textAlign: 'center', padding: '0 80px'}}>
            {ost.map((t, i) => {
              const o = interpolate(f, [6 + i * 8, 22 + i * 8], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const y = interpolate(o, [0, 1], [18, 0]);
              return (
                <div
                  key={i}
                  style={{
                    opacity: o,
                    transform: `translateY(${y}px)`,
                    color: i === 0 ? S.white : S.gold,
                    fontFamily: BRAND.font.display,
                    fontSize: i === 0 ? 46 : 38,
                    fontWeight: 900,
                    textTransform: 'uppercase' as const,
                    letterSpacing: 1,
                    textShadow: `0 4px 28px ${S.ink}`,
                    marginBottom: 10,
                  }}
                >
                  {t}
                </div>
              );
            })}
          </div>
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

/** Placeholder card for visual modes whose real asset (Midjourney) is not generated yet. */
const PlaceholderCard: React.FC<{mode: string; motif: string; ost: string[]}> = ({mode, motif, ost}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 100% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 85%)`,
      justifyContent: 'center',
      alignItems: 'center',
      gap: 16,
    }}
  >
    <div
      style={{
        border: `2px dashed ${BRAND.color.silver}66`,
        borderRadius: 16,
        padding: '40px 60px',
        textAlign: 'center',
        maxWidth: '70%',
      }}
    >
      <div style={{color: BRAND.color.gold, fontFamily: BRAND.font.display, fontSize: 26, letterSpacing: 4, textTransform: 'uppercase'}}>
        {mode}
      </div>
      <div style={{color: BRAND.color.silver, fontFamily: BRAND.font.body, fontSize: 22, marginTop: 8}}>
        {motif || 'visual'} — asset pending
      </div>
      {ost.length ? (
        <div style={{color: BRAND.color.white, fontFamily: BRAND.font.display, fontSize: 40, marginTop: 18}}>
          {ost.join('  ·  ')}
        </div>
      ) : null}
    </div>
  </AbsoluteFill>
);

const SceneVisual: React.FC<{scene: AnimaticScene}> = ({scene}) => {
  const {visualMode: m, onScreenText: ost, motifHint, sceneId} = scene;

  // Use real image when available — always takes priority over coded art
  const realImg = SCENE_IMG[sceneId];
  if (realImg) {
    return <RealImageBg src={realImg} sceneId={sceneId} ost={ost} />;
  }

  if (m === 'typography') {
    const lines = (ost.length ? ost : ['Prime Documentary']).map((t, i) => ({
      text: t,
      at: i * 8,
      emphasis: i === 0,
    }));
    return (
      <MovingStage seed={sceneId} intensity={0.8} particles={24}>
        <KineticType lines={lines} />
      </MovingStage>
    );
  }
  if (m === 'diagram') {
    const steps = ost.length >= 2 ? ost.slice(0, 4) : ['Cause', 'Mechanism', 'Effect'];
    return (
      <MovingStage seed={sceneId} intensity={0.7} particles={22}>
        <DiagramFlow steps={steps} />
      </MovingStage>
    );
  }
  if (m === 'abstract' || m === 'breathing' || m === 'transition_texture') {
    return (
      <MovingStage seed={sceneId} intensity={0.7} particles={36}>
        <SymbolicScene />
      </MovingStage>
    );
  }
  // map / timeline / object / reenactment / archival_illustration / location:
  // coded symbolic art that animates so it reads as a video, not a placeholder box.
  return <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} seed={sceneId} />;
};

/** VO-preview caption (the narration text, shown as review subtitle — NOT spoken). */
const ScriptCaption: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 12], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 60}}>
      <div
        style={{
          opacity: o,
          maxWidth: '82%',
          background: `${BRAND.color.ink}CC`,
          borderTop: `2px solid ${BRAND.color.gold}`,
          padding: '14px 24px',
          color: BRAND.color.white,
          fontFamily: BRAND.font.body,
          fontSize: 24,
          lineHeight: 1.35,
          textAlign: 'center',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};

/** Soft entrance cover (a quick ink dip) to seat each cut. */
const SceneEnter: React.FC = () => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 12], [0.7, 0], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: BRAND.color.ink, opacity: o, pointerEvents: 'none'}} />;
};

const Hud: React.FC<{scene: AnimaticScene; index: number; total: number}> = ({scene, index, total}) => (
  <AbsoluteFill style={{pointerEvents: 'none'}}>
    {/* watermark */}
    <div style={{position: 'absolute', top: 24, right: 28, color: `${BRAND.color.silver}AA`, fontFamily: BRAND.font.body, fontSize: 18, textAlign: 'right'}}>
      ANIMATIC · no VO · placeholder visuals
    </div>
    {/* scene label */}
    <div style={{position: 'absolute', top: 24, left: 28, color: BRAND.color.gold, fontFamily: BRAND.font.body, fontSize: 18}}>
      {scene.sceneId} ({index + 1}/{total}) · {scene.emotion}
      {scene.review ? '  ⚑ human-review' : ''}
    </div>
    {/* citation */}
    {scene.citation ? (
      <div style={{position: 'absolute', top: 64, left: 28, color: BRAND.color.silver, fontFamily: BRAND.font.body, fontSize: 18, borderLeft: `3px solid ${BRAND.color.gold}`, paddingLeft: 10}}>
        {scene.citation.source} · {scene.citation.claimIds.join(', ')}
      </div>
    ) : null}
  </AbsoluteFill>
);

export type AnimaticProps = {bgmSrc?: string | null};

/** Full-length $0 animatic (no narration). Drives off the approved script + scene plan. */
export const Animatic: React.FC<AnimaticProps> = ({bgmSrc = 'bgm_placeholder.wav'}) => {
  const {fps} = useVideoConfig();
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {MIRANDA_ANIMATIC.map((scene, i) => {
        const from = Math.round(cursor * fps);
        const dur = Math.round(scene.durationSec * fps);
        cursor += scene.durationSec;
        return (
          <Sequence key={scene.sceneId} from={from} durationInFrames={dur} name={scene.sceneId}>
            <SceneVisual scene={scene} />
            <ScriptCaption text={scene.caption} />
            <Hud scene={scene} index={i} total={MIRANDA_ANIMATIC.length} />
            {i > 0 ? <SceneEnter /> : null}
            {i > 0 ? <WipeTransition durationFrames={16} /> : null}
          </Sequence>
        );
      })}
      <Grain opacity={0.07} />
      {bgmSrc ? <Audio src={staticFile(bgmSrc)} volume={0.35} loop /> : null}
    </AbsoluteFill>
  );
};

/** Total animatic duration in frames at a given fps. */
export const animaticDurationInFrames = (fps: number): number =>
  Math.round(MIRANDA_ANIMATIC.reduce((a, s) => a + s.durationSec, 0) * fps);
