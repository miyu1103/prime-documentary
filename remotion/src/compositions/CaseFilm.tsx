import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Particles, LightSweep, Vignette} from '../components/Motion';
import {Grain} from '../components/Grain';
import {BrandOpening, BrandEndcard, OPENING_SEC, ENDCARD_SEC} from '../components/Bookends';

/**
 * CaseFilm — data-driven, MotionSample-style long-form documentary render.
 * Owner-approved style (2026-07-04): footage-forward, floating-card 2.5D on stills
 * (never a plain zoom/pan), drifting atmosphere, motion so it never reads as a
 * slideshow. No left→right sweep line, no yellow/gold full-screen wash. Captions
 * sit low, mid-sized, no heavy box, force-aligned to the narration. Canonical
 * BrandOpening/BrandEndcard bookends. Reusable across EP25/26/27.
 */

const {ink, electric, white, silver} = BRAND.color;

export type Cut = {start: number; dur: number; kind: 'img' | 'footage'; src: string; treatment: string; seed: string};
export type Caption = {start: number; end: number; text: string};
export type FilmData = {
  fps: number;
  narration: string;
  narrationSeconds: number;
  cuts: Cut[];
  captions: Caption[];
};

export const caseFilmDurationInFrames = (data: FilmData, fps: number) =>
  Math.round(OPENING_SEC * fps) + Math.ceil(data.narrationSeconds * fps) + Math.round(ENDCARD_SEC * fps);

/** Full-frame moving footage with a cinematic grade. Footage supplies the motion. */
const Footage: React.FC<{src: string; startFrom: number}> = ({src, startFrom}) => (
  <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
    <OffthreadVideo
      src={staticFile(src)}
      muted
      startFrom={startFrom}
      style={{
        width: '100%',
        height: '100%',
        objectFit: 'cover',
        transform: 'scale(1.05)',
        filter: 'brightness(0.62) contrast(1.1) saturate(0.85)',
      }}
    />
  </AbsoluteFill>
);

/** Fake-2.5D still: a sharp framed photo card floats over a blurred, enlarged copy
 * of itself, each drifting opposite — real depth, never a flat zoom. */
const CardStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(frame, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const bgX = interpolate(p, [0, 1], [-40 * dir, 40 * dir]);
  const bgY = interpolate(p, [0, 1], [-16, 16]);
  const cardX = interpolate(p, [0, 1], [30 * dir, -30 * dir]);
  const cardY = interpolate(p, [0, 1], [14, -14]);
  const cardRot = interpolate(p, [0, 1], [-1.8 * dir, 1.8 * dir]);
  const cardScale = interpolate(p, [0, 1], [1.02, 1.06]);
  const introY = interpolate(frame, [0, 10], [26, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill
        style={{
          transform: `translate(${bgX}px, ${bgY}px) scale(1.42)`,
          filter: 'blur(20px) brightness(0.42) saturate(0.85)',
        }}
      >
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <LightSweep seed={seed} color={electric} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: '69%',
            height: '73%',
            transform: `translate(${cardX}px, ${cardY + introY}px) rotate(${cardRot}deg) scale(${cardScale})`,
            borderRadius: 10,
            overflow: 'hidden',
            border: `1px solid ${silver}40`,
            boxShadow: '0 40px 120px rgba(0,0,0,0.62)',
          }}
        >
          <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
      </AbsoluteFill>
      <Particles seed={seed} count={22} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

const CutView: React.FC<{cut: Cut; index: number}> = ({cut, index}) => {
  const inner = (() => {
    if (cut.kind === 'footage') {
      return <Footage src={cut.src} startFrom={(index * 41) % 140} />;
    }
    return <CardStill src={cut.src} seed={cut.seed} dir={index % 2 === 0 ? 1 : -1} />;
  })();
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 5], [0, 1], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{opacity}}>{inner}</AbsoluteFill>;
};

/** Low, mid-sized captions, no heavy box, force-aligned to the narration. */
const Captions: React.FC<{cues: Caption[]}> = ({cues}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const cue = cues.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center'}}>
      <div
        style={{
          maxWidth: '78%',
          marginBottom: 78,
          textAlign: 'center',
          color: white,
          fontFamily: BRAND.font.body,
          fontSize: 44,
          fontWeight: 600,
          lineHeight: 1.25,
          letterSpacing: 0.2,
          textShadow: '0 2px 10px rgba(0,0,0,0.85), 0 0 4px rgba(0,0,0,0.7)',
        }}
      >
        {cue.text}
      </div>
    </AbsoluteFill>
  );
};

export const CaseFilm: React.FC<{data: FilmData; seriesLabel: string; title: string; subtitle?: string}> = ({
  data,
  seriesLabel,
  title,
  subtitle,
}) => {
  const {fps} = useVideoConfig();
  const op = Math.round(OPENING_SEC * fps);
  const ed = Math.round(ENDCARD_SEC * fps);
  const body = Math.ceil(data.narrationSeconds * fps);
  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      <Sequence from={0} durationInFrames={op} name="Opening">
        <BrandOpening seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
      </Sequence>

      <Sequence from={op} durationInFrames={body} name="Body">
        <Audio src={staticFile(data.narration)} />
        {data.cuts.map((c, i) => (
          <Sequence
            key={i}
            from={Math.round(c.start * fps)}
            durationInFrames={Math.max(1, Math.round(c.dur * fps))}
            name={`cut-${i}`}
          >
            <CutView cut={c} index={i} />
          </Sequence>
        ))}
        <Captions cues={data.captions} />
        <Grain />
      </Sequence>

      <Sequence from={op + body} durationInFrames={ed} name="Endcard">
        <BrandEndcard />
      </Sequence>
    </AbsoluteFill>
  );
};
