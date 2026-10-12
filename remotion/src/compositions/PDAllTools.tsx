/**
 * PDAllTools — a reel where EVERY newly-installed tool is actually on screen, each
 * beat labelled with the tool that produced it:
 *   1) Depth Anything V2 + SAM2  -> precise 2.5D depth (SAM2 mask, not a threshold)
 *   2) Wan2.2 (ComfyUI)          -> a REAL AI-generated B-roll clip
 *   3) OpenCLIP semantic search  -> the footage was picked by an English query
 *   4) Blender                   -> the reusable 3D evidence room, camera moving
 * (faster-whisper word-sync is shown in TimbsB2; it needs narration audio.)
 * ~28s @30fps = 840f.
 */
import React from 'react';
import {
  AbsoluteFill, Series, Img, OffthreadVideo, staticFile, interpolate, spring, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {KineticCaptions, FilmGrain, VignetteBreath, LightRays} from '../components/motionkit';

const Tag: React.FC<{tool: string; label: string}> = ({tool, label}) => (
  <AbsoluteFill style={{padding: 56, pointerEvents: 'none'}}>
    <div style={{alignSelf: 'flex-start', background: 'rgba(6,10,18,0.66)', borderLeft: `6px solid ${BRAND.color.electric}`, padding: '12px 22px', borderRadius: 6}}>
      <div style={{fontFamily: BRAND.font.body, fontWeight: 900, letterSpacing: 2, fontSize: 22, color: BRAND.color.electric, textTransform: 'uppercase'}}>{tool}</div>
      <div style={{fontFamily: BRAND.font.display, fontSize: 42, color: BRAND.color.white, textShadow: '0 3px 14px #000'}}>{label}</div>
    </div>
  </AbsoluteFill>
);

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

/** Strong 2.5D from the SAM2 cutout layers. */
const Sam25D: React.FC = () => {
  const f = useCurrentFrame(); const {durationInFrames, fps} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1]);
  const s = spring({frame: f, fps, config: {damping: 200}, durationInFrames});
  const bgScale = interpolate(p, [0, 1], [1.02, 1.08]);
  const bgX = interpolate(p, [0, 1], [0, -22]);
  const fgScale = interpolate(s, [0, 1], [1.03, 1.28]);
  const fgX = interpolate(p, [0, 1], [0, 66]);
  const fgY = interpolate(p, [0, 1], [0, -24]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(${bgScale})`}}>
        <Plate src="timbs/_p08sam/SPN-0007_bg.png" />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgScale})`}}>
        <Plate src="timbs/_p08sam/SPN-0007_fg.png" />
      </AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
    </AbsoluteFill>
  );
};

const Clip: React.FC<{src: string}> = ({src}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </AbsoluteFill>
);

export const pdAllToolsDuration = 840;

export const PDAllTools: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      <Series.Sequence durationInFrames={300}>
        <Sam25D />
        <Tag tool="Depth AI + SAM2" label="Precise 2.5D — real segmentation" />
        <KineticCaptions lines={['SAM2 cut it out — depth moves it.']} style="maskslide" anchor="bottom" emphasisWords={['SAM2', 'depth']} />
      </Series.Sequence>
      <Series.Sequence durationInFrames={150}>
        <Clip src="_ai/wan22_rain.mp4" />
        <Tag tool="Wan2.2 · ComfyUI" label="AI-generated B-roll (real)" />
        <KineticCaptions lines={['This clip did not exist —', 'the AI made it.']} style="maskslide" anchor="bottom" emphasisWords={['AI']} />
      </Series.Sequence>
      <Series.Sequence durationInFrames={150}>
        <Clip src="_ai/searched.mp4" />
        <Tag tool="OpenCLIP search" label="Footage found by an English query" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={120}>
        <Clip src="_set/ev_cam1_enter_room.mp4" />
        <Tag tool="Blender" label="A reusable 3D evidence room" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={120}>
        <Clip src="_set/ev_cam2_push_desk.mp4" />
        <Tag tool="Blender" label="Camera moves through the set" />
      </Series.Sequence>
    </Series>
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
