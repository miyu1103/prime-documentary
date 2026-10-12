/**
 * PDForfeiture60 — a real ~50s documentary piece whose PRODUCTION uses the new
 * tools (no on-screen tool labels): Wan2.2 AI atmosphere, SAM2+Depth 2.5D hero,
 * OpenCLIP-searched footage, Blender 3D evidence room, core-5 graphics, finishing.
 * Theme: the Excessive Fines clause (general civics; figures are illustrative).
 * Kinetic captions carry it; VO/music can be layered later. 1500f @30fps = 50s.
 */
import React from 'react';
import {
  AbsoluteFill, Series, Img, OffthreadVideo, staticFile, interpolate, useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {BRAND} from '../brand';
import {PenaltyVsProperty, QuoteUnderExamination} from '../components/core5';
import {CinematicTitle, KineticCaptions, FilmGrain, VignetteBreath, LightRays} from '../components/motionkit';

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);
const Clip: React.FC<{src: string; dim?: number}> = ({src, dim = 0}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    {dim ? <AbsoluteFill style={{background: `rgba(6,10,18,${dim})`}} /> : null}
  </AbsoluteFill>
);

const Sam25D: React.FC = () => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  // gentle COORDINATED dolly-in (camera eases into the scene) — not a sliding cutout.
  const p = interpolate(f, [0, durationInFrames], [0, 1], {easing: Easing.inOut(Easing.cubic)});
  const bgS = interpolate(p, [0, 1], [1.00, 1.085]); const bgX = interpolate(p, [0, 1], [0, -6]);
  const fgS = interpolate(p, [0, 1], [1.00, 1.135]); const fgX = interpolate(p, [0, 1], [0, 12]); const fgY = interpolate(p, [0, 1], [0, -6]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(${bgS})`}}><Plate src="timbs/_p08sam/SPN-0007_bg.png" /></AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px,${fgY}px) scale(${fgS})`}}><Plate src="timbs/_p08sam/SPN-0007_fg.png" /></AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
    </AbsoluteFill>
  );
};

export const pdForfeiture60Duration = 1500;

export const PDForfeiture60: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      {/* cold open — AI atmosphere */}
      <Series.Sequence durationInFrames={90}>
        <Clip src="_ai/wan22_rain.mp4" dim={0.25} />
        <KineticCaptions lines={['They can take it —', 'before you are ever convicted.']} style="maskslide" anchor="bottom" emphasisWords={['take', 'convicted']} />
      </Series.Sequence>
      {/* title */}
      <Series.Sequence durationInFrames={150}>
        <CinematicTitle title="EXCESSIVE FINES" subtitle="the limit the Constitution draws" />
      </Series.Sequence>
      {/* 2.5D hero (SAM2 + Depth) */}
      <Series.Sequence durationInFrames={300}>
        <Sam25D />
        <KineticCaptions lines={['A small fine.', 'A far bigger seizure.']} style="maskslide" anchor="bottom" emphasisWords={['bigger']} />
      </Series.Sequence>
      {/* the rule */}
      <Series.Sequence durationInFrames={300}>
        <QuoteUnderExamination quote="nor excessive fines imposed" attribution="Eighth Amendment, 1791" sourceLabel="U.S. Constitution" dur={300} />
      </Series.Sequence>
      {/* the comparison */}
      <Series.Sequence durationInFrames={300}>
        <PenaltyVsProperty left={{label: 'A typical fine', value: 500}} right={{label: 'Property taken', value: 50000}} mode="currency" sourceLabel="Illustrative example" dur={300} />
      </Series.Sequence>
      {/* 3D evidence room as a stage */}
      <Series.Sequence durationInFrames={240}>
        <Clip src="_set/ev_cam2_push_desk.mp4" />
        <KineticCaptions lines={['A limit is only as strong', 'as who can use it.']} style="maskslide" anchor="bottom" emphasisWords={['strong']} />
      </Series.Sequence>
      {/* searched footage + close */}
      <Series.Sequence durationInFrames={120}>
        <Clip src="_ai/searched.mp4" dim={0.2} />
        <KineticCaptions lines={['Next: can they take your home?']} style="maskslide" anchor="bottom" />
      </Series.Sequence>
    </Series>
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
