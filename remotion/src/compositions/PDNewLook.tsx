/**
 * PDNewLook — a ~21s reel that foregrounds the GENUINELY NEW visuals the prior
 * test (PDTest60) left out. It contrasts the old flat treatment with the three
 * new capabilities the existing channel does NOT have:
 *   BEFORE  — flat Ken-Burns still (the current look)
 *   AFTER 1 — 2.5D depth parallax on the SAME still (new)
 *   AFTER 2 — real footage integrated (new pipeline)
 *   AFTER 3 — the 3D PD Evidence Room camera move (new, Blender)
 * Each beat is corner-labelled so the difference is unmistakable. 630f @30fps.
 */
import React from 'react';
import {
  AbsoluteFill, Series, Img, OffthreadVideo, staticFile, interpolate, useCurrentFrame, useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Parallax} from '../components/Parallax';
import {KineticCaptions, FilmGrain, VignetteBreath} from '../components/motionkit';

export const pdNewLookDuration = 630;

const Tag: React.FC<{kicker: string; label: string; warn?: boolean}> = ({kicker, label, warn}) => (
  <AbsoluteFill style={{padding: 54, pointerEvents: 'none'}}>
    <div style={{alignSelf: 'flex-start', background: 'rgba(6,10,18,0.66)', borderLeft: `6px solid ${warn ? BRAND.color.silver : BRAND.color.gold}`, padding: '12px 20px', borderRadius: 6}}>
      <div style={{fontFamily: BRAND.font.body, fontWeight: 900, letterSpacing: 2, fontSize: 22, color: warn ? BRAND.color.silver : BRAND.color.gold, textTransform: 'uppercase'}}>{kicker}</div>
      <div style={{fontFamily: BRAND.font.display, fontSize: 40, color: BRAND.color.white, textShadow: '0 3px 14px #000'}}>{label}</div>
    </div>
  </AbsoluteFill>
);

const KenBurnsStill: React.FC<{src: string}> = ({src}) => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const s = interpolate(f, [0, durationInFrames], [1.03, 1.12]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${s})`}}>
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

const Plate: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);

const Depth25D: React.FC = () => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const kb = interpolate(f, [0, durationInFrames], [1.02, 1.08]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${kb})`}}>
        <Parallax amount={48} layers={[
          {depth: 0.16, node: <Plate src="timbs/_p08/SPN-0007_bg.png" />},
          {depth: 0.95, node: <Plate src="timbs/_p08/SPN-0007_fg.png" />},
        ]} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const PDNewLook: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      {/* BEFORE — the current flat look */}
      <Series.Sequence durationInFrames={105}>
        <KenBurnsStill src="timbs/SPN-0007.png" />
        <Tag kicker="Before" label="Flat still — zoom only" warn />
      </Series.Sequence>
      {/* AFTER 1 — 2.5D depth on the SAME image */}
      <Series.Sequence durationInFrames={225}>
        <Depth25D />
        <Tag kicker="New" label="2.5D depth — it moves in space" />
        <KineticCaptions lines={['The same image — now with depth.']} style="maskslide" anchor="bottom" />
      </Series.Sequence>
      {/* AFTER 2 — real footage integrated */}
      <Series.Sequence durationInFrames={150}>
        <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
          <OffthreadVideo src={staticFile('timbs/pexels_v_20758153.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </AbsoluteFill>
        <Tag kicker="New" label="Real footage, searched + cut in" />
      </Series.Sequence>
      {/* AFTER 3 — the 3D Evidence Room (Blender camera move) */}
      <Series.Sequence durationInFrames={150}>
        <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
          <OffthreadVideo src={staticFile('_set/evroom_cam2.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </AbsoluteFill>
        <Tag kicker="New" label="A reusable 3D evidence room" />
      </Series.Sequence>
    </Series>
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
