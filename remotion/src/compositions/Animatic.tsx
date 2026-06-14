import React from 'react';
import {
  AbsoluteFill,
  Audio,
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
import {Grain} from '../components/Grain';
import {WipeTransition} from '../components/Transition';
import {AnimaticScene, MIRANDA_ANIMATIC} from '../data/miranda_animatic';

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
  const {visualMode: m, onScreenText: ost, motifHint} = scene;
  // MJ-EP images take priority over visualMode dispatch
  if (motifHint.startsWith('MJ-EP:')) {
    return <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} />;
  }
  if (m === 'typography') {
    const lines = (ost.length ? ost : ['Prime Documentary']).map((t, i) => ({text: t, at: i * 8}));
    return <KineticType lines={lines} />;
  }
  if (m === 'diagram') {
    const steps = ost.length >= 2 ? ost.slice(0, 4) : ['Cause', 'Mechanism', 'Effect'];
    return <DiagramFlow steps={steps} />;
  }
  if (m === 'abstract' || m === 'breathing' || m === 'transition_texture') {
    return <SymbolicScene />;
  }
  // map / timeline / object / reenactment / archival_illustration / location:
  // coded symbolic art so it reads as a video, not a placeholder box.
  return <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} />;
};

/** Split text into chunks of ~8 words at natural boundaries. */
function toChunks(text: string, size = 8): string[] {
  const words = text.replace(/\s+/g, ' ').trim().split(' ');
  const chunks: string[] = [];
  for (let i = 0; i < words.length; i += size) {
    chunks.push(words.slice(i, i + size).join(' '));
  }
  return chunks;
}

/** VO-preview caption — shows 5 words at a time, fades between chunks. */
const ScriptCaption: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const chunks = toChunks(text, 5);
  // leave last 10% of scene caption-free so it breathes before transition
  const activeDur = durationInFrames * 0.90;
  const cpf = activeDur / chunks.length;          // frames per chunk
  const idx = Math.min(Math.floor(frame / cpf), chunks.length - 1);
  const f0 = idx * cpf;
  const fadeIn  = interpolate(frame, [f0, f0 + 5],        [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [f0 + cpf - 6, f0 + cpf], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const opacity = frame >= activeDur ? 0 : Math.min(fadeIn, fadeOut);

  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 72, pointerEvents: 'none'}}>
      <div style={{
        opacity,
        background: 'rgba(10,10,12,0.72)',
        borderRadius: 6,
        padding: '10px 28px',
        color: BRAND.color.white,
        fontFamily: BRAND.font.body,
        fontSize: 36,
        fontWeight: 600,
        textAlign: 'center',
        maxWidth: '72%',
        lineHeight: 1.35,
        letterSpacing: 0.2,
      }}>
        {chunks[idx]}
      </div>
    </AbsoluteFill>
  );
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
            {i > 0 ? <WipeTransition durationFrames={12} /> : null}
          </Sequence>
        );
      })}
      <Grain opacity={0.05} />
      {bgmSrc ? <Audio src={staticFile(bgmSrc)} volume={0.35} loop /> : null}
    </AbsoluteFill>
  );
};

/** Total animatic duration in frames at a given fps. */
export const animaticDurationInFrames = (fps: number): number =>
  Math.round(MIRANDA_ANIMATIC.reduce((a, s) => a + s.durationSec, 0) * fps);
