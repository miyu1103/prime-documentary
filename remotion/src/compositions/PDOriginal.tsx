/**
 * PDOriginal — an original ~63s documentary piece that leans HARD on the new tools:
 *   - narration (local TTS) + faster-whisper WORD-SYNCED caption band (ORIG_WORDS)
 *   - multiple 2.5D depth shots (Depth Anything V2 + SAM2 cutouts) — Depth25D
 *   - 3D Evidence Room camera moves (Blender) — OffthreadVideo
 *   - Wan2.2 AI atmosphere beds (subtle, honest use)
 *   - OpenCLIP-searched footage + core-5 graphics + cinematic finishing
 * Theme: civil forfeiture & the Excessive Fines clause (general civics; the $ figures
 * are illustrative). 1890f @30fps = 63s (narration ends ~61.8s).
 */
import React from 'react';
import {
  AbsoluteFill, Series, Audio, Img, OffthreadVideo, staticFile, interpolate,
  useCurrentFrame, useVideoConfig, Easing,
} from 'remotion';
import {BRAND} from '../brand';
import {PenaltyVsProperty, QuoteUnderExamination, VerdictReversal} from '../components/core5';
import {FilmGrain, VignetteBreath, LightRays} from '../components/motionkit';
import {ORIG_WORDS} from '../data/orig_words';

const FPS = 30;
export const pdOriginalDuration = 1890;
const LEAD = 0.10; // caption onset-latency correction (s)

const P: React.FC<{src: string}> = ({src}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
);
const Clip: React.FC<{src: string; dim?: number}> = ({src, dim = 0}) => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    {dim ? <AbsoluteFill style={{background: `rgba(6,10,18,${dim})`}} /> : null}
  </AbsoluteFill>
);

/** Gentle coordinated dolly-in 2.5D (no "decomposed" slide). */
const Depth25D: React.FC<{name: string}> = ({name}) => {
  const f = useCurrentFrame(); const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {easing: Easing.inOut(Easing.cubic)});
  const bgS = interpolate(p, [0, 1], [1.00, 1.08]);
  const fgS = interpolate(p, [0, 1], [1.00, 1.13]);
  const fgX = interpolate(p, [0, 1], [0, 12]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${bgS})`}}><P src={`timbs/_p08sam/${name}_bg.png`} /></AbsoluteFill>
      <AbsoluteFill style={{transform: `translateX(${fgX}px) scale(${fgS})`}}><P src={`timbs/_p08sam/${name}_fg.png`} /></AbsoluteFill>
      <LightRays color={BRAND.color.gold} />
    </AbsoluteFill>
  );
};

/** Word-synced caption band from faster-whisper timings — highlights the spoken word. */
const WordBand: React.FC = () => {
  const frame = useCurrentFrame(); const {fps, width} = useVideoConfig();
  const t = frame / fps + LEAD;
  let active = -1;
  for (let i = 0; i < ORIG_WORDS.length; i++) { if (ORIG_WORDS[i].start <= t) active = i; else break; }
  if (active < 0) return null;
  const start = Math.max(0, active - 6);
  const shown = ORIG_WORDS.slice(start, active + 1);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 92}}>
      <div style={{maxWidth: width * 0.82, display: 'flex', flexWrap: 'wrap', gap: '0 12px', justifyContent: 'center', padding: '12px 24px', borderRadius: 10, background: 'rgba(6,10,18,0.6)'}}>
        {shown.map((w, i) => {
          const on = start + i === active;
          return <span key={start + i} style={{fontFamily: BRAND.font.body, fontWeight: 800, fontSize: 46, color: on ? BRAND.color.gold : BRAND.color.white, opacity: on ? 1 : 0.6, textShadow: '0 3px 12px #000'}}>{w.word}</span>;
        })}
      </div>
    </AbsoluteFill>
  );
};

// beat = [durationFrames, node]
const beats: [number, React.ReactNode][] = [
  [150, <Clip src="_ai/wan22_rain.mp4" dim={0.28} />],                                  // 0-5  cold open (AI atmosphere)
  [120, <Clip src="_ai/searched.mp4" dim={0.15} />],                                    // 5-9  searched footage
  [180, <Depth25D name="SPN-0002" />],                                                  // 9-15 2.5D forfeiture
  [150, <PenaltyVsProperty left={{label: 'A fine', value: 500}} right={{label: 'Property taken', value: 50000}} mode="currency" sourceLabel="Illustrative example" dur={150} />], // 15-20
  [150, <Depth25D name="SPN-0007" />],                                                  // 20-25 2.5D scale
  [210, <QuoteUnderExamination quote="nor excessive fines imposed" attribution="Eighth Amendment, 1791" sourceLabel="U.S. Constitution" dur={210} />], // 25-32
  [180, <Clip src="_set/ev_cam1_enter_room.mp4" />],                                    // 32-38 3D room
  [180, <VerdictReversal vote={{majority: 9, dissent: 0}} fromLabel="Does it bind the states?" stampText="9–0" sourceLabel="Supreme Court, 2019" dur={180} />], // 38-44
  [150, <Depth25D name="SPN-0020" />],                                                  // 44-49 2.5D limit
  [150, <Clip src="_set/ev_cam2_push_desk.mp4" />],                                     // 49-54 3D room
  [180, <Depth25D name="SPN-0025" />],                                                  // 54-60 2.5D reach
  [90, <Clip src="_ai/wan22_atmos.mp4" dim={0.2} />],                                   // 60-63 atmosphere close
];

export const PDOriginal: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      {beats.map(([d, node], i) => (
        <Series.Sequence key={i} durationInFrames={d}>{node as React.ReactNode}</Series.Sequence>
      ))}
    </Series>
    <WordBand />
    <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 36%, ${BRAND.color.gold}0E 0%, transparent 44%), linear-gradient(180deg, ${BRAND.color.navy}1F 0%, transparent 30%, ${BRAND.color.ink}30 100%)`, mixBlendMode: 'soft-light', pointerEvents: 'none'}} />
    <VignetteBreath />
    <FilmGrain />
    <Audio src={staticFile('_orig/narration.wav')} />
  </AbsoluteFill>
);
