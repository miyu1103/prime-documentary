import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Particles, LightSweep, Vignette} from '../components/Motion';
import {Grain} from '../components/Grain';
import {BrandOpening, BrandEndcard, OPENING_SEC, ENDCARD_SEC} from '../components/Bookends';

/**
 * CaseFilm v002 — data-driven long-form documentary render, owner-tuned.
 * Fixes from EP25 review: (1) high asset variety / no reuse cluster, (2) an 8s cold-open
 * HOOK montage before the brand opening, (3) FIVE distinct still treatments so the diagonal
 * 2.5D "card" is rare — the rest move via bleed-parallax, thermal-scan overlays, duotone
 * atmosphere, and rack-focus. No left→right sweep line, no yellow/gold full-screen wash,
 * no plain zoom. Low mid-size captions, canonical bookends. BGM is mixed in post.
 */

const {ink, navy, electric, white, silver, gold} = BRAND.color;
// lifted from v003 (acceptance images_present flagged 98%-black crush on the darkest shots):
// keep the noir mood but never let a shot fall to near-total black.
const GRADE = 'brightness(0.82) contrast(1.06) saturate(0.9)';

export type Cut = {start: number; dur: number; kind: 'img' | 'footage'; src: string; treatment: string; seed: string};
export type Caption = {start: number; end: number; text: string};
export type HookCut = {start: number; dur: number; kind: string; src: string; seed: string};
export type Beat = {start: number; end: number; lines: string[]};
export type FilmData = {
  fps: number;
  narration: string;
  narrationSeconds: number;
  hookSeconds: number;
  hookLine: string;
  hook: HookCut[];
  cuts: Cut[];
  captions: Caption[];
  graphics: Beat[];
};

export const caseFilmDurationInFrames = (data: FilmData, fps: number) =>
  Math.round((data.hookSeconds || 0) * fps) +
  Math.round(OPENING_SEC * fps) +
  Math.ceil(data.narrationSeconds * fps) +
  Math.round(ENDCARD_SEC * fps);

const Cover: React.FC<{src: string; style?: React.CSSProperties}> = ({src, style}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', ...style}} />
);

/** Footage: graded + navy-tinted + vignetted so bright/washed clips (fog, snow, white tech)
 * unify into the dark navy palette; a slow push (camera move on real footage — not a still zoom)
 * gives a motion floor so even near-locked clips never read as frozen. */
const Footage: React.FC<{src: string; startFrom: number; dir: number}> = ({src, startFrom, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const s = interpolate(p, [0, 1], [1.04, 1.1]);
  const x = interpolate(p, [0, 1], [-14 * dir, 14 * dir]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <OffthreadVideo
        src={staticFile(src)}
        muted
        startFrom={startFrom}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translateX(${x}px) scale(${s})`,
          filter: 'brightness(0.8) contrast(1.12) saturate(0.7)',
        }}
      />
      <AbsoluteFill style={{pointerEvents: 'none', backgroundColor: navy, opacity: 0.14, mixBlendMode: 'multiply'}} />
      <AbsoluteFill
        style={{pointerEvents: 'none', background: `radial-gradient(135% 108% at 50% 44%, transparent 60%, ${ink}55 100%)`}}
      />
    </AbsoluteFill>
  );
};

/** bleed: full-frame depth — a blurred enlarged layer and the sharp image drift opposite ways. No tilt. */
const BleedStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const bgX = interpolate(p, [0, 1], [-26 * dir, 26 * dir]);
  const fgX = interpolate(p, [0, 1], [16 * dir, -16 * dir]);
  const fgS = interpolate(p, [0, 1], [1.05, 1.1]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(1.34)`, filter: 'blur(22px) brightness(0.62)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translateX(${fgX}px) scale(${fgS})`, filter: GRADE}}>
        <Cover src={src} />
      </AbsoluteFill>
      <Particles seed={seed} count={14} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

/** shared divergent-parallax base (bg blur + sharp fg drift opposite) — genuine depth motion,
 * never a flat zoom, and enough pixel movement that nothing reads as a frozen slide. */
const parallax = (p: number, dir: number) => ({
  bgX: interpolate(p, [0, 1], [-32 * dir, 32 * dir]),
  bgY: interpolate(p, [0, 1], [-14, 14]),
  fgX: interpolate(p, [0, 1], [20 * dir, -20 * dir]),
  fgY: interpolate(p, [0, 1], [10, -10]),
  fgS: interpolate(p, [0, 1], [1.05, 1.11]),
});

/** scan: parallax base + a thermal light pool and a slow-drifting measurement grid. */
const ScanStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  const gy = interpolate(p, [0, 1], [0, 80]);
  const lx = 50 + 26 * Math.sin(p * Math.PI * 2);
  const ly = 40 + 12 * Math.cos(p * Math.PI * 2);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(22px) brightness(0.62)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgS})`, filter: 'brightness(0.76) contrast(1.1) saturate(0.82)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          opacity: 0.08,
          transform: `translateY(${gy}px)`,
          backgroundImage: `repeating-linear-gradient(0deg, ${electric}00 0px, ${electric}00 46px, ${electric}ff 47px, ${electric}00 48px)`,
        }}
      />
      <AbsoluteFill
        style={{pointerEvents: 'none', background: `radial-gradient(38% 50% at ${lx}% ${ly}%, ${electric}22 0%, transparent 70%)`}}
      />
      <Particles seed={seed} count={18} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

/** duotone: parallax base + duotone grade + travelling light + drifting motes + vignette breath. */
const DuotoneStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  const vig = 0.9 + 0.1 * Math.sin(p * Math.PI * 2);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(22px) brightness(0.5)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgS})`, filter: 'brightness(0.74) contrast(1.12) saturate(0.74) hue-rotate(-6deg)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <LightSweep seed={seed} color={silver} />
      <Particles seed={seed} count={20} color={silver} />
      <Vignette strength={vig} />
    </AbsoluteFill>
  );
};

/** focus: parallax base + rack-focus reveal on the sharp layer (soft -> sharp). */
const FocusStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const blur = interpolate(f, [0, 22], [16, 0], {extrapolateRight: 'clamp'});
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(24px) brightness(0.62)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgS})`, filter: `blur(${blur}px) ${GRADE}`}}>
        <Cover src={src} />
      </AbsoluteFill>
      <Particles seed={seed} count={14} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

/** card: the diagonal 2.5D floating photo card — RARE, for accent only. */
const CardStill: React.FC<{src: string; seed: string; dir: number}> = ({src, seed, dir}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const bgX = interpolate(p, [0, 1], [-40 * dir, 40 * dir]);
  const cardX = interpolate(p, [0, 1], [30 * dir, -30 * dir]);
  const cardRot = interpolate(p, [0, 1], [-1.8 * dir, 1.8 * dir]);
  const intro = interpolate(f, [0, 10], [26, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(1.4)`, filter: 'blur(20px) brightness(0.55)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <LightSweep seed={seed} color={electric} />
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: '69%',
            height: '73%',
            transform: `translate(${cardX}px, ${intro}px) rotate(${cardRot}deg) scale(1.03)`,
            borderRadius: 10,
            overflow: 'hidden',
            border: `1px solid ${silver}40`,
            boxShadow: '0 40px 120px rgba(0,0,0,0.62)',
          }}
        >
          <Cover src={src} />
        </div>
      </AbsoluteFill>
      <Particles seed={seed} count={18} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

const Still: React.FC<{cut: Cut; index: number}> = ({cut, index}) => {
  const dir = index % 2 === 0 ? 1 : -1;
  switch (cut.treatment) {
    case 'scan':
      return <ScanStill src={cut.src} seed={cut.seed} dir={dir} />;
    case 'duotone':
      return <DuotoneStill src={cut.src} seed={cut.seed} dir={dir} />;
    case 'focus':
      return <FocusStill src={cut.src} seed={cut.seed} dir={dir} />;
    case 'card':
      return <CardStill src={cut.src} seed={cut.seed} dir={dir} />;
    case 'bleed':
    default:
      return <BleedStill src={cut.src} seed={cut.seed} dir={dir} />;
  }
};

const CutView: React.FC<{cut: Cut; index: number}> = ({cut, index}) => {
  const f = useCurrentFrame();
  const opacity = interpolate(f, [0, 5], [0, 1], {extrapolateRight: 'clamp'});
  const inner =
    cut.kind === 'footage' ? (
      <Footage src={cut.src} startFrom={(index * 47) % 160} dir={index % 2 === 0 ? 1 : -1} />
    ) : (
      <Still cut={cut} index={index} />
    );
  return <AbsoluteFill style={{opacity}}>{inner}</AbsoluteFill>;
};

const Captions: React.FC<{cues: Caption[]}> = ({cues}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
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
          textShadow: '0 2px 10px rgba(0,0,0,0.85), 0 0 4px rgba(0,0,0,0.7)',
        }}
      >
        {cue.text}
      </div>
    </AbsoluteFill>
  );
};

/** GRAPHICS BEATS — the designed on_screen_text (script.annotated) rendered as big kinetic
 * typography with motion-blur entrances, timed to each span's narration. This is the dynamic
 * motion-graphics layer (dates, "5–4", the holding, the quotes) that makes it premium, not a
 * slideshow. Sits in the upper third so it never collides with the bottom captions. */
const BeatText: React.FC<{lines: string[]}> = ({lines}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const outOp = interpolate(f, [durationInFrames - 12, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: '19%'}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18, opacity: outOp, maxWidth: '86%'}}>
        {lines.map((ln, i) => {
          const enter = spring({frame: f - i * 9, fps, config: {damping: 15, stiffness: 120, mass: 0.8}});
          const x = interpolate(enter, [0, 1], [(i % 2 === 0 ? -1 : 1) * 70, 0]);
          const y = interpolate(enter, [0, 1], [30, 0]);
          const sc = interpolate(enter, [0, 1], [0.8, 1]);
          const op = Math.min(enter * 1.6, 1);
          const short = ln.length <= 18;
          return (
            <div
              key={i}
              style={{
                transform: `translate(${x}px, ${y}px) scale(${sc})`,
                opacity: op,
                color: i === 0 ? white : gold,
                fontFamily: BRAND.font.display,
                fontWeight: 900,
                fontSize: short ? 88 : 52,
                lineHeight: 1.08,
                letterSpacing: -0.5,
                textAlign: 'center',
                textShadow: `0 4px 24px rgba(0,0,0,0.92), 0 0 34px ${electric}55`,
              }}
            >
              {ln}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const GraphicsBeats: React.FC<{beats: Beat[]}> = ({beats}) => {
  const {fps} = useVideoConfig();
  return (
    <>
      {beats.map((b, i) => (
        <Sequence
          key={i}
          from={Math.round(b.start * fps)}
          durationInFrames={Math.max(1, Math.round((b.end - b.start) * fps))}
          name={`gfx-${i}`}
        >
          <BeatText lines={b.lines} />
        </Sequence>
      ))}
    </>
  );
};

/** 8-second cold-open: fast punch cuts of the strongest shots + a bold hook line. BGM (post-mix) carries it. */
const PunchShot: React.FC<{src: string}> = ({src}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const p = interpolate(f, [0, durationInFrames], [0, 1], {extrapolateRight: 'clamp'});
  const s = interpolate(p, [0, 1], [1.16, 1.04]);
  const op = interpolate(f, [0, 4], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden', opacity: op}}>
      <AbsoluteFill style={{transform: `scale(${s})`, filter: 'brightness(0.62) contrast(1.15) saturate(0.85)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <Vignette strength={1.1} />
    </AbsoluteFill>
  );
};

const Hook: React.FC<{hook: HookCut[]; line: string}> = ({hook, line}) => {
  const {fps} = useVideoConfig();
  const f = useCurrentFrame();
  const enter = spring({frame: f - 26, fps, config: {damping: 16, stiffness: 110, mass: 0.8}});
  const y = interpolate(enter, [0, 1], [30, 0]);
  const lineOp = interpolate(f, [26, 40], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      {hook.map((h, i) => (
        <Sequence key={i} from={Math.round(h.start * fps)} durationInFrames={Math.max(1, Math.round(h.dur * fps))}>
          <PunchShot src={h.src} />
        </Sequence>
      ))}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 120}}>
        <div
          style={{
            transform: `translateY(${y}px)`,
            opacity: lineOp,
            color: white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 82,
            lineHeight: 1.04,
            letterSpacing: -1,
            textAlign: 'center',
            textTransform: 'uppercase',
            textShadow: '0 6px 30px rgba(0,0,0,0.8)',
            maxWidth: '86%',
          }}
        >
          {line}
        </div>
      </AbsoluteFill>
      <Grain />
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
  const hook = Math.round((data.hookSeconds || 0) * fps);
  const op = Math.round(OPENING_SEC * fps);
  const ed = Math.round(ENDCARD_SEC * fps);
  const body = Math.ceil(data.narrationSeconds * fps);
  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      {hook > 0 && (
        <Sequence from={0} durationInFrames={hook} name="Hook">
          <Hook hook={data.hook} line={data.hookLine} />
        </Sequence>
      )}

      <Sequence from={hook} durationInFrames={op} name="Opening">
        <BrandOpening seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
      </Sequence>

      <Sequence from={hook + op} durationInFrames={body} name="Body">
        <Audio src={staticFile(data.narration)} />
        {data.cuts.map((c, i) => (
          <Sequence key={i} from={Math.round(c.start * fps)} durationInFrames={Math.max(1, Math.round(c.dur * fps))} name={`cut-${i}`}>
            <CutView cut={c} index={i} />
          </Sequence>
        ))}
        {/* faint ambient so the very darkest shots never read as 98% black (acceptance images_present) */}
        <AbsoluteFill
          style={{pointerEvents: 'none', background: `radial-gradient(105% 72% at 50% 46%, ${navy}22 0%, transparent 80%)`}}
        />
        <GraphicsBeats beats={data.graphics} />
        <Captions cues={data.captions} />
        <Grain opacity={0.11} />
      </Sequence>

      <Sequence from={hook + op + body} durationInFrames={ed} name="Endcard">
        <BrandEndcard />
      </Sequence>
    </AbsoluteFill>
  );
};
