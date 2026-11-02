import React from 'react';
import {
  AbsoluteFill,
  Img,
  Sequence,
  Series,
  Video,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {BrandEndcard, BrandOpening, ENDCARD_SEC, OPENING_SEC} from '../components/Bookends';
import {Grain} from '../components/Grain';
import {CameraRig, LightSweep, Particles, Vignette} from '../components/Motion';
import {WipeTransition} from '../components/Transition';
import {casePremiumDurationInFrames} from './CasePremiumFromRoughCut';
import type {RoughCutData, RoughShot} from './RoughCut';
import {VARSITYBLUES_ROUGHCUT} from '../data/varsityblues_roughcut';
import {GRAPHIC_FOR_SPAN} from './varsityblues/Graphics';

/**
 * EP19 "Operation Varsity Blues" — bespoke premium composition.
 *
 * Fixes the "PowerPoint slideshow" problem: instead of one Ken-Burns still per
 * shot, every shot is a moving film layer — cinematic hero stills with a real
 * camera rig, interleaved with genuine stock b-roll for motion, and, on the key
 * conceptual beats, purpose-built MEANINGFUL motion graphics (the three doors,
 * the laundry, the target score, the fake athlete, the sentences, the scarce
 * seats, the collapse). Rendered SILENT; the mastered voice+music mix is muxed
 * on afterwards by the build script.
 */

const {ink, navy, electric, gold, white, silver} = BRAND.color;
const DISPLAY = BRAND.font.display;
const BODY = BRAND.font.body;

const TOTAL_SEC = 1660.313;

export const varsityBluesPremiumDurationInFrames = (fps: number): number =>
  casePremiumDurationInFrames(VARSITYBLUES_ROUGHCUT, fps, TOTAL_SEC);

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));

// Hero image pools per chapter (EP19-IMG-NNN.png live in public/varsityblues/).
const HERO_RANGES: Record<string, [number, number]> = {
  hook: [1, 6],
  opening: [7, 14],
  act1: [15, 30],
  act2: [31, 52],
  act3: [53, 70],
  act4: [71, 86],
  ending: [87, 92],
};

const heroSrc = (n: number): string => `varsityblues/EP19-IMG-${String(n).padStart(3, '0')}.png`;

/** Pick a hero image for a shot given its position within its chapter. */
const heroForShot = (chapterId: string, idxInChapter: number, countInChapter: number): string => {
  const [lo, hi] = HERO_RANGES[chapterId] ?? [1, 6];
  const pool = hi - lo + 1;
  const pick = lo + (countInChapter <= 1 ? 0 : Math.round((idxInChapter / (countInChapter - 1)) * (pool - 1)));
  return heroSrc(Math.min(hi, Math.max(lo, pick)));
};

const CHAPTER_TITLE: Record<string, string> = {
  opening: 'The Three Doors',
  act1: 'Act One — The Fixer',
  act2: 'Act Two — The Two Machines',
  act3: 'Act Three — The Families',
  act4: 'Act Four — The Reckoning',
  ending: 'What Is a Seat Worth?',
};

type TimedShot = RoughShot & {start: number; dur: number; heroIdxInChapter: number; chapterCount: number};

const SafetyLabel: React.FC = () => (
  <div
    style={{
      position: 'absolute',
      right: 52,
      top: 40,
      fontFamily: BODY,
      fontSize: 17,
      color: silver,
      padding: '6px 11px',
      border: `1px solid ${gold}88`,
      background: '#000000A8',
      letterSpacing: 0.5,
    }}
  >
    symbolic reconstruction / not case footage
  </div>
);

/** Clean chapter marker that rises in at the start of each chapter (replaces the old motif telop). */
const ChapterMark: React.FC<{title: string}> = ({title}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame: frame - Math.round(0.15 * fps), fps, config: {damping: 18, stiffness: 95}});
  const leave = interpolate(frame, [Math.round(3.4 * fps), Math.round(4.0 * fps)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const op = Math.min(enter, leave);
  return (
    <div style={{position: 'absolute', left: 64, top: 120, opacity: op, transform: `translateY(${interpolate(enter, [0, 1], [30, 0])}px)`}}>
      <div style={{fontFamily: BODY, fontSize: 20, fontWeight: 800, letterSpacing: 4, color: gold, textTransform: 'uppercase'}}>Prime Documentary</div>
      <div style={{width: interpolate(enter, [0, 1], [0, 260]), height: 3, background: gold, margin: '10px 0 14px', boxShadow: `0 0 14px ${gold}88`}} />
      <div style={{fontFamily: DISPLAY, fontSize: 56, color: white, textTransform: 'uppercase', lineHeight: 0.98, textShadow: '0 5px 30px #000', maxWidth: 900}}>{title}</div>
    </div>
  );
};

/** A few distinct hero image numbers spread across the chapter pool, offset per shot. */
const pickHeroNumbers = (chapterId: string, idxInChapter: number, n: number): number[] => {
  const [lo, hi] = HERO_RANGES[chapterId] ?? [1, 6];
  const pool = hi - lo + 1;
  return Array.from({length: n}, (_, k) => lo + ((idxInChapter + k * 2) % pool));
};

/** Shared cinematic overlay stack (gradient + travelling light + particles + vignette + grain). */
const SceneOverlays: React.FC<{seed: string}> = ({seed}) => (
  <>
    <AbsoluteFill style={{background: `linear-gradient(180deg, ${ink}bb 0%, #00000018 40%, ${ink}dd 100%)`}} />
    <LightSweep seed={seed} color={electric} />
    <Particles seed={seed} count={14} color={gold} />
    <Vignette strength={0.96} />
    <Grain opacity={0.05} />
  </>
);

/** One base cut: a moving hero still, with a wipe on entry. */
const HeroCut: React.FC<{src: string; seed: string}> = ({src, seed}) => (
  <AbsoluteFill style={{overflow: 'hidden'}}>
    <CameraRig seed={seed} intensity={1.2}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.82) contrast(1.14) saturate(1.05)'}} />
    </CameraRig>
    <WipeTransition durationFrames={12} />
  </AbsoluteFill>
);

/** One base cut: genuine stock b-roll (real motion), with a wipe on entry. */
const StockCut: React.FC<{src: string; seed: string; clipSeconds: number}> = ({src, seed, clipSeconds}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const maxStart = Math.max(0, Math.round(clipSeconds * fps) - durationInFrames - 2);
  const startFrom = maxStart > 0 ? (seed.length * 17) % maxStart : 0;
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <Video src={staticFile(src)} muted startFrom={startFrom} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.78) contrast(1.16) saturate(1.02)', transform: 'scale(1.05)'}} />
      <WipeTransition durationFrames={12} />
    </AbsoluteFill>
  );
};

/**
 * Cut a shot into ~CUT_SEC segments that alternate hero stills and genuine stock b-roll, so
 * the frame is always changing (never a single 20-second still) and real footage appears
 * throughout the episode.
 */
const CUT_SEC = 4.8;
const VisualSequence: React.FC<{shot: TimedShot}> = ({shot}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const chapterId = shot.chapterId ?? 'act1';
  const heroes = pickHeroNumbers(chapterId, shot.heroIdxInChapter, 3).map(heroSrc);
  const clip = shot.clips?.[0];
  const n = Math.max(1, Math.round(durationInFrames / Math.round(CUT_SEC * fps)));
  const playlist: {kind: 'hero' | 'stock'; src: string}[] = [];
  let h = 0;
  for (let i = 0; i < n; i += 1) {
    if (clip && i % 2 === 1) {
      playlist.push({kind: 'stock', src: clip.src});
    } else {
      playlist.push({kind: 'hero', src: heroes[h % heroes.length]});
      h += 1;
    }
  }
  const per = Math.ceil(durationInFrames / playlist.length);
  return (
    <Series>
      {playlist.map((item, i) => (
        <Series.Sequence key={i} durationInFrames={per}>
          {item.kind === 'stock' ? (
            <StockCut src={item.src} seed={`${shot.spanId}-${i}`} clipSeconds={clip?.clipSeconds ?? shot.seconds} />
          ) : (
            <HeroCut src={item.src} seed={`${shot.spanId}-${i}`} />
          )}
        </Series.Sequence>
      ))}
    </Series>
  );
};

/** Darkened hero base behind a meaningful motion graphic. */
const GraphicBase: React.FC<{src: string; seed: string}> = ({src, seed}) => (
  <AbsoluteFill style={{overflow: 'hidden'}}>
    <CameraRig seed={seed} intensity={0.5}>
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.32) contrast(1.1) saturate(0.9)'}} />
    </CameraRig>
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 42%, ${navy}aa 0%, ${ink}f0 82%)`}} />
  </AbsoluteFill>
);

const Scene: React.FC<{shot: TimedShot; showChapter: boolean}> = ({shot, showChapter}) => {
  const chapterId = shot.chapterId ?? 'act1';
  const Graphic = GRAPHIC_FOR_SPAN[shot.spanId];
  const hero = heroForShot(chapterId, shot.heroIdxInChapter, shot.chapterCount);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      {Graphic ? (
        <>
          <GraphicBase src={hero} seed={shot.spanId} />
          <Graphic />
          <LightSweep seed={shot.spanId} color={gold} />
          <Particles seed={shot.spanId} count={12} color={gold} />
          <Vignette strength={0.98} />
          <Grain opacity={0.05} />
        </>
      ) : (
        <>
          <VisualSequence shot={shot} />
          <SceneOverlays seed={shot.spanId} />
        </>
      )}
      {showChapter && CHAPTER_TITLE[chapterId] ? <ChapterMark title={CHAPTER_TITLE[chapterId]} /> : null}
      <SafetyLabel />
    </AbsoluteFill>
  );
};

/** Hook — a fast hero montage with kinetic promise lines. */
const Hook: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const imgs = [1, 2, 3, 4, 5, 6].map(heroSrc);
  const per = Math.ceil(durationInFrames / imgs.length);
  const lines = [
    {text: 'Not the front door.', at: 0.4, big: false},
    {text: 'Not the back door.', at: 2.1, big: false},
    {text: 'A side door.', at: 3.9, big: true},
  ];
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <Series>
        {imgs.map((src, i) => (
          <Series.Sequence key={src} durationInFrames={per}>
            <AbsoluteFill style={{overflow: 'hidden'}}>
              <CameraRig seed={`hook-${i}`} intensity={1.5}>
                <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.7) contrast(1.2) saturate(1.05)'}} />
              </CameraRig>
              <WipeTransition durationFrames={10} />
            </AbsoluteFill>
          </Series.Sequence>
        ))}
      </Series>
      <AbsoluteFill style={{background: `linear-gradient(90deg, ${ink}e6 0%, #00000033 58%, ${ink}a0 100%)`}} />
      {lines.map((l) => {
        const local = frame - Math.round(l.at * fps);
        const enter = spring({frame: local, fps, config: {damping: 16, stiffness: 120}});
        return (
          <div
            key={l.text}
            style={{
              position: 'absolute',
              left: 74,
              bottom: l.big ? 210 : 320,
              opacity: Math.min(1, enter * 1.4),
              transform: `translateY(${interpolate(enter, [0, 1], [50, 0])}px)`,
              fontFamily: DISPLAY,
              color: l.big ? gold : white,
              fontSize: l.big ? 118 : 60,
              textTransform: 'uppercase',
              lineHeight: 0.95,
              textShadow: l.big ? `0 0 44px ${gold}88` : '0 6px 30px #000',
            }}
          >
            {l.text}
          </div>
        );
      })}
      <div style={{position: 'absolute', left: 76, bottom: 176, width: 360, height: 5, background: gold}} />
      <Particles seed="hook" count={20} color={gold} />
      <Vignette strength={1} />
      <Grain opacity={0.055} />
      <SafetyLabel />
    </AbsoluteFill>
  );
};

const CaptionBand: React.FC<{captions: RoughCutData['captions']}> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!captions || captions.length === 0) return null;
  const t = frame / fps;
  const cue = captions.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  const longest = Math.max(...cue.text.split('\n').map((line) => line.length));
  const fontSize = longest > 58 ? 34 : longest > 46 ? 38 : 42;
  return (
    <div
      style={{
        position: 'absolute',
        left: 260,
        right: 260,
        bottom: 58,
        minHeight: 82,
        padding: '15px 30px 17px',
        background: '#050505E8',
        borderLeft: `5px solid ${gold}`,
        borderRadius: 6,
        boxShadow: '0 18px 44px #000000A8',
        color: white,
        fontFamily: BODY,
        fontWeight: 900,
        fontSize,
        lineHeight: 1.18,
        textAlign: 'center',
        textShadow: '0 2px 10px #000, 0 0 4px #000',
        WebkitTextStroke: '0.7px #000',
        whiteSpace: 'pre-line',
      }}
    >
      {cue.text}
    </div>
  );
};

export const VarsityBluesPremium: React.FC = () => {
  const {fps} = useVideoConfig();
  const data = VARSITYBLUES_ROUGHCUT;
  const shots = data.shots;
  const hook = shots[0];
  const hookSec = hook.seconds;
  const bodyStart = hookSec + OPENING_SEC;
  const sourceBodySec = shots.slice(1).reduce((sum, shot) => sum + shot.seconds, 0);
  const availableBodySec = Math.max(1, TOTAL_SEC - bodyStart - ENDCARD_SEC);
  const scale = availableBodySec / sourceBodySec;

  // group body shots by chapter to distribute hero images + detect chapter starts
  const chapterCounts: Record<string, number> = {};
  shots.slice(1).forEach((s) => {
    const c = s.chapterId ?? 'act1';
    chapterCounts[c] = (chapterCounts[c] ?? 0) + 1;
  });

  const chapterSeen: Record<string, number> = {};
  let cursor = bodyStart;
  const bodyShots: TimedShot[] = shots.slice(1).map((shot) => {
    const c = shot.chapterId ?? 'act1';
    const idxInChapter = chapterSeen[c] ?? 0;
    chapterSeen[c] = idxInChapter + 1;
    const dur = shot.seconds * scale;
    const timed: TimedShot = {...shot, start: cursor, dur, heroIdxInChapter: idxInChapter, chapterCount: chapterCounts[c]};
    cursor += dur;
    return timed;
  });

  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      <Sequence from={0} durationInFrames={framesFor(hookSec, fps)} name="PART_1_HOOK">
        <Hook />
      </Sequence>
      <Sequence from={framesFor(hookSec, fps)} durationInFrames={framesFor(OPENING_SEC, fps)} name="PART_2_BRAND_OPENING">
        <BrandOpening seriesLabel="Prime Documentary" title="OPERATION VARSITY BLUES" subtitle="The side door into elite colleges" />
      </Sequence>
      {bodyShots.map((shot) => (
        <Sequence key={shot.spanId} from={framesFor(shot.start, fps)} durationInFrames={framesFor(shot.dur, fps)} name={`${shot.chapterId ?? 'body'}_${shot.spanId}`}>
          <Scene shot={shot} showChapter={shot.heroIdxInChapter === 0} />
        </Sequence>
      ))}
      <Sequence from={framesFor(TOTAL_SEC - ENDCARD_SEC, fps)} durationInFrames={framesFor(ENDCARD_SEC, fps)} name="PART_4_BRAND_ENDCARD">
        <BrandEndcard />
      </Sequence>
      <CaptionBand captions={data.captions} />
    </AbsoluteFill>
  );
};
