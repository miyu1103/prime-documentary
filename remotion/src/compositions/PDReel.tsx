/**
 * PDReel — a fast-cut, high-energy ~18s montage (a distinctly different TEMPO from
 * the calm explainer pieces). Rapid 1-1.5s cuts across the whole new toolset:
 * 3D room, 2.5D depth, searched footage, AI atmosphere, a core-5 graphic — driven
 * by punchy kinetic text. 540f @30fps = 18s.
 */
import React from 'react';
import {
  AbsoluteFill, Series, Img, OffthreadVideo, staticFile, interpolate, useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {BRAND} from '../brand';
import {PenaltyVsProperty} from '../components/core5';
import {KineticCaptions, FilmGrain, VignetteBreath} from '../components/motionkit';

const Clip: React.FC<{src: string}> = ({src}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
  </AbsoluteFill>
);

const Sam25D: React.FC = () => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {easing: Easing.inOut(Easing.cubic)});
  const bgS = interpolate(p, [0, 1], [1.00, 1.06]); const fgS = interpolate(p, [0, 1], [1.00, 1.10]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${bgS})`}}><Img src={staticFile('timbs/_p08sam/SPN-0007_bg.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></AbsoluteFill>
      <AbsoluteFill style={{transform: `translateX(8px) scale(${fgS})`}}><Img src={staticFile('timbs/_p08sam/SPN-0007_fg.png')} style={{width: '100%', height: '100%', objectFit: 'cover'}} /></AbsoluteFill>
    </AbsoluteFill>
  );
};

const Word: React.FC<{text: string}> = ({text}) => (
  <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
    <div style={{fontFamily: BRAND.font.display, fontSize: 120, color: BRAND.color.white, textShadow: '0 6px 30px #000', letterSpacing: 2}}>{text}</div>
  </AbsoluteFill>
);

export const pdReelDuration = 540;

export const PDReel: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      <Series.Sequence durationInFrames={60}><Clip src="_ai/wan22_atmos.mp4" /><Word text="THE LINE" /></Series.Sequence>
      <Series.Sequence durationInFrames={48}><Clip src="_set/ev_cam1_enter_room.mp4" /></Series.Sequence>
      <Series.Sequence durationInFrames={90}><Sam25D /><Word text="EXCESSIVE" /></Series.Sequence>
      <Series.Sequence durationInFrames={48}><Clip src="_ai/searched.mp4" /></Series.Sequence>
      <Series.Sequence durationInFrames={126}>
        <PenaltyVsProperty left={{label: 'A fine', value: 500}} right={{label: 'Taken', value: 50000}} mode="currency" sourceLabel="Illustrative" dur={126} />
      </Series.Sequence>
      <Series.Sequence durationInFrames={48}><Clip src="_set/ev_cam2_push_desk.mp4" /></Series.Sequence>
      <Series.Sequence durationInFrames={72}><Clip src="timbs/pexels_v_20758153.mp4" /><Word text="WHO DECIDES?" /></Series.Sequence>
    </Series>
    <KineticCaptions lines={['The Constitution drew a line.']} style="wordpop" anchor="bottom" />
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
