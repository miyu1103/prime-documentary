import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {KineticType} from '../components/KineticType';
import {DiagramFlow} from '../components/DiagramFlow';
import {SceneArt} from '../components/SceneArt';
import {Grain} from '../components/Grain';
import {CameraRig, Particles, LightSweep, Vignette} from '../components/Motion';
import type {AnimaticScene} from '../data/miranda_animatic';
import {MAPP_ANIMATIC, MAPP_SCENE_IMG} from '../data/mapp_animatic';

/**
 * MappPremium — EP3 (Mapp v. Ohio), 0004-standard cut. Every shot MOVES (the moving
 * stage: CameraRig + drifting particles + light sweep + vignette), so even coded/
 * typography beats never read as a slideshow. 87 fine-grained shots scaled to the
 * narration master (visual change every ~4–8s). SDXL substitute stills (swap to
 * Midjourney later). AI reenactment shots carry a "symbolic reconstruction" label
 * (invariant 11). Brand grade + grain applied in the ffmpeg finish.
 */

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;
const SILVER = BRAND.color.silver;

const IMG: Partial<Record<string, string>> = {...MAPP_SCENE_IMG};

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
  <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'flex-start', padding: '0 52px 96px'}}>
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

const DIAGRAM_MODES = new Set(['diagram', 'map', 'timeline', 'data_visualization']);

const StillStage: React.FC<{scene: AnimaticScene}> = ({scene}) => {
  const {visualMode: m, onScreenText: ost, motifHint, sceneId, review} = scene;
  const imgSrc = IMG[sceneId];

  let inner: React.ReactNode;
  if (m === 'typography') {
    const lines = (ost.length ? ost : ['Prime Documentary']).map((t, i) => ({text: t, at: i * 8, emphasis: i === 0}));
    inner = imgSrc
      ? (<AbsoluteFill><ImageBase src={imgSrc} /><TopShade /><BottomGrad /><KineticType lines={lines} transparent /></AbsoluteFill>)
      : (<AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${NAVY} 0%, ${INK} 85%)`}}><KineticType lines={lines} /></AbsoluteFill>);
  } else if (DIAGRAM_MODES.has(m) && ost.length >= 2) {
    inner = (<AbsoluteFill><AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${NAVY} 0%, ${INK} 85%)`}} /><DiagramFlow steps={ost.slice(0, 4)} /></AbsoluteFill>);
  } else if (imgSrc) {
    const hasCap = ost.length > 0;
    inner = (<AbsoluteFill><ImageBase src={imgSrc} />{hasCap && <BottomGrad />}{hasCap && <ImageCaption lines={ost.slice(0, 2)} italic={m === 'reenactment'} />}</AbsoluteFill>);
  } else {
    inner = <SceneArt visualMode={m} motifHint={motifHint} onScreenText={ost} seed={sceneId} />;
  }

  const isRoom = m === 'establishing' || m === 'reenactment';
  return (
    <AbsoluteFill style={{backgroundColor: INK, overflow: 'hidden'}}>
      <CameraRig seed={sceneId} intensity={1}>{inner}</CameraRig>
      <LightSweep seed={sceneId} />
      <Particles seed={sceneId} count={isRoom ? 26 : 30} />
      <Vignette />
      {review && <ReconLabel />}
    </AbsoluteFill>
  );
};

export const MappPremium: React.FC = () => {
  const {fps} = useVideoConfig();
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: INK}}>
      {MAPP_ANIMATIC.map((scene) => {
        const from = Math.round(cursor * fps);
        const dur = Math.max(1, Math.round(scene.durationSec * fps));
        cursor += scene.durationSec;
        return (
          <Sequence key={scene.sceneId} from={from} durationInFrames={dur} name={scene.sceneId}>
            <StillStage scene={scene} />
          </Sequence>
        );
      })}
      <Grain opacity={0.05} />
    </AbsoluteFill>
  );
};

export const mappPremiumDurationInFrames = (fps: number): number =>
  Math.round(MAPP_ANIMATIC.reduce((a, s) => a + s.durationSec, 0) * fps);
