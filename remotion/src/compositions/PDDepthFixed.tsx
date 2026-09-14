/**
 * PDDepthFixed — natural 2.5D. The prior "strong" version slid the foreground far
 * from the background, so it read as a cutout coming apart ("絵を分解しただけ").
 * Fix: a gentle COORDINATED dolly-in — both layers push in together, the fg only
 * slightly more (depth), with a tiny parallax offset. Reads as a camera easing
 * into the scene, not a sticker sliding off. 300f @30fps = 10s.
 */
import React from 'react';
import {AbsoluteFill, Img, staticFile, interpolate, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../brand';
import {LightRays, VignetteBreath, FilmGrain} from '../components/motionkit';

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

export const pdDepthFixedDuration = 300;

export const PDDepthFixed: React.FC = () => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {easing: Easing.inOut(Easing.cubic)});
  // coordinated dolly-in: both layers scale up together (camera push).
  const bgScale = interpolate(p, [0, 1], [1.00, 1.085]);
  const fgScale = interpolate(p, [0, 1], [1.00, 1.135]); // only slightly more -> subtle depth
  // tiny parallax drift so it is alive but never detaches
  const bgX = interpolate(p, [0, 1], [0, -6]);
  const fgX = interpolate(p, [0, 1], [0, 12]);
  const fgY = interpolate(p, [0, 1], [0, -6]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(${bgScale})`}}>
        <Plate src="timbs/_p08sam/SPN-0007_bg.png" />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgScale})`}}>
        <Plate src="timbs/_p08sam/SPN-0007_fg.png" />
      </AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
      <VignetteBreath />
      <FilmGrain />
    </AbsoluteFill>
  );
};
