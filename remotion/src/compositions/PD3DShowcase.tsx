/**
 * PD3DShowcase — dials the two genuinely-new capabilities UP: strong 2.5D depth
 * and dynamic 3D Evidence Room camera moves. Foreground pushes toward the viewer
 * far more than the background (a real dolly-into-the-scene feel), and the 3D room
 * uses big sweeping camera travels. ~24s @30fps = 720f.
 */
import React from 'react';
import {
  AbsoluteFill, Series, Img, OffthreadVideo, staticFile, interpolate, spring, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {KineticCaptions, FilmGrain, VignetteBreath, LightRays} from '../components/motionkit';

const Tag: React.FC<{kicker: string; label: string}> = ({kicker, label}) => (
  <AbsoluteFill style={{padding: 56, pointerEvents: 'none'}}>
    <div style={{alignSelf: 'flex-start', background: 'rgba(6,10,18,0.62)', borderLeft: `6px solid ${BRAND.color.gold}`, padding: '12px 22px', borderRadius: 6}}>
      <div style={{fontFamily: BRAND.font.body, fontWeight: 900, letterSpacing: 3, fontSize: 22, color: BRAND.color.gold, textTransform: 'uppercase'}}>{kicker}</div>
      <div style={{fontFamily: BRAND.font.display, fontSize: 44, color: BRAND.color.white, textShadow: '0 3px 14px #000'}}>{label}</div>
    </div>
  </AbsoluteFill>
);

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

/** Strong 2.5D: foreground scales/pushes toward viewer much more than background. */
const Strong25D: React.FC<{dir?: number}> = ({dir = 1}) => {
  const f = useCurrentFrame();
  const {durationInFrames, fps} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1]);
  const s = spring({frame: f, fps, config: {damping: 200}, durationInFrames});
  // background: slow, subtle
  const bgScale = interpolate(p, [0, 1], [1.02, 1.08]);
  const bgX = interpolate(p, [0, 1], [0, -22 * dir]);
  // foreground: big push toward viewer + opposite drift + slight rise
  const fgScale = interpolate(s, [0, 1], [1.03, 1.30]);
  const fgX = interpolate(p, [0, 1], [0, 70 * dir]);
  const fgY = interpolate(p, [0, 1], [0, -26]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(${bgScale})`}}>
        <Plate src="timbs/_p08/SPN-0007_bg.png" />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgScale})`}}>
        <Plate src="timbs/_p08/SPN-0007_fg.png" />
      </AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
    </AbsoluteFill>
  );
};

const RoomClip: React.FC<{src: string}> = ({src}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </AbsoluteFill>
);

export const pd3DShowcaseDuration = 720;

export const PD3DShowcase: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      <Series.Sequence durationInFrames={330}>
        <Strong25D dir={1} />
        <Tag kicker="2.5D depth" label="A still image, moving in space" />
        <KineticCaptions lines={['Not a zoom — real depth.']} style="maskslide" anchor="bottom" emphasisWords={['depth']} />
      </Series.Sequence>
      <Series.Sequence durationInFrames={210}>
        <RoomClip src="_set/ev_cam1_enter_room.mp4" />
        <Tag kicker="3D space" label="A real 3D evidence room" />
      </Series.Sequence>
      <Series.Sequence durationInFrames={180}>
        <RoomClip src="_set/ev_cam2_push_desk.mp4" />
        <Tag kicker="3D space" label="Camera moves through it" />
        <KineticCaptions lines={['Reusable across every episode.']} style="maskslide" anchor="bottom" />
      </Series.Sequence>
    </Series>
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
