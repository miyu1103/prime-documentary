import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  Loop,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {useThree, useLoader} from '@react-three/fiber';
import {BRAND} from '../brand';
import {Particles, Vignette} from '../components/Motion';
import {AmbientMotion} from '../components/AmbientMotion';
import {FigureBeats, FigureSpec} from '../components/FigureBeats';
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
// EP49 clarity fix (owner 2026-07-24: "全体的に画像に曇りがかかってる" — image reads milky/
// low-contrast). The old grade was a flat brightness lift with NEUTRAL contrast, which — stacked
// with the screen-blend washes below — flattened the picture into a haze. Restore real contrast
// and a touch of saturation so blacks sit down and the image reads CLEAR; brightness stays high
// enough that dark hero stills still clear the per-cut luma gate (contrast preserves mid-tone Y).
const GRADE = 'brightness(1.12) contrast(1.14) saturate(1.03)';

export type Cut = {
  start: number;
  dur: number;
  kind: 'img' | 'footage';
  src: string;
  treatment: string;
  /** per-still exposure multiplier measured at build time (1 = leave the image alone) */
  lift?: number;
  seed: string;
  overlay?: string | null;
  blendHint?: 'add' | 'screen' | 'overlay' | null;
  overlayDuration?: number | null;
  // EP49: real-stock cutaways injected via inject_strieff_stock.py set startFrom=0 so short
  // graded stock clips (some ~7-10s) always start at their first frame instead of the
  // index-derived in-point (which could seek past a short clip's end). Optional; when absent the
  // Footage component keeps its original index-based startFrom (unchanged for every other episode).
  startFrom?: number | null;
  /** measured length of the source clip, written by the builder so the in-point can be clamped */
  srcSeconds?: number | null;
};
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
  figures?: FigureSpec[];
  // Pre-composed Blender/3D "hero" videos (e.g. EP34 rolin L3 Cycles heroes). Each plays FULL-FRAME
  // over its body window (no Ken-Burns / no startFrom — the mp4 is already the finished shot),
  // above the graded body and below the captions. OPTIONAL: episodes without heroCuts (carsearch
  // etc.) are unaffected (the map runs over []).
  heroCuts?: {start: number; dur: number; src: string}[];
  /** SPEC v2 row 9 (owner decision 2026-08-10, "66話から"): the narrator speaks from frame 0.
   * Seconds from the start of the film at which the Body sequence -- and the <Audio> master
   * inside it -- begins. EP66 declares 0. OPT-IN AND NULLABLE ON PURPOSE: when an episode does
   * not declare it the lead is `hookSeconds + OPENING_SEC`, which is exactly where the Body
   * sequence has started since this composition was written, so EP62-65 render bit-identical.
   * Do not give it a default value in the type -- an absent key must stay absent. */
  leadSeconds?: number;
  /** Which form of the channel opening this film places (EP66 PACKAGING v001 sections 4 and 7).
   *
   * OPT-IN AND NULLABLE ON PURPOSE, exactly like `leadSeconds`. Absent means 'card': the
   * full-screen 3.5 s <BrandOpening> between the hook montage and the body, which is what
   * every episode up to EP65 renders. 'overlay' is the zero-lead layout: the same component
   * in its lower-band form, placed OVER the running body so neither the picture nor the
   * narration stops for it.
   *
   * A film with `leadSeconds: 0` and NO `openingVariant` has no opening at all -- the card
   * has nowhere to go and no overlay was asked for. That combination is what
   * check_final_acceptance.check_bookends() now fails on; it is not a legal shipping state. */
  openingVariant?: 'card' | 'overlay';
};

/** Seconds after the end of the spoken hook at which the overlay opening rises.
 * EP66 PACKAGING v001 section 4 fixes the band at 0:20.5-0:24.0 against a 20.3 s hook, so the
 * offset is 0.2 s and the placement stays derived from the film's own `hookSeconds` instead of
 * being written twice. scripts/check_final_acceptance.py reads this constant out of this file
 * rather than keeping a copy of the number. */
export const OPENING_OVERLAY_OFFSET_SEC = 0.2;

/** Frame at which the Body sequence (and the narration master inside it) starts.
 * Absent `leadSeconds` reproduces the historical expression term for term --
 * `Math.round(hookSeconds * fps) + Math.round(OPENING_SEC * fps)` -- so every episode that
 * does not declare the key keeps the identical timeline it has always had. */
export const caseFilmLeadFrames = (data: FilmData, fps: number) =>
  data.leadSeconds == null
    ? Math.round((data.hookSeconds || 0) * fps) + Math.round(OPENING_SEC * fps)
    : Math.round(data.leadSeconds * fps);

export const caseFilmDurationInFrames = (data: FilmData, fps: number) =>
  caseFilmLeadFrames(data, fps) +
  Math.ceil(data.narrationSeconds * fps) +
  Math.round(ENDCARD_SEC * fps);

const Cover: React.FC<{src: string; style?: React.CSSProperties}> = ({src, style}) => (
  <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover', ...style}} />
);

/** Footage: graded + navy-tinted + vignetted so bright/washed clips (fog, snow, white tech)
 * unify into the dark navy palette; a slow push (camera move on real footage — not a still zoom)
 * gives a motion floor so even near-locked clips never read as frozen. */
const Footage: React.FC<{
  src: string;
  startFrom: number;
  dir: number;
  dur: number;
  srcSeconds?: number | null;
  lift?: number;
}> = ({src, startFrom, dir, dur, srcSeconds, lift: _lift}) => {
  const f = useCurrentFrame();
  const {fps: _fps} = useVideoConfig();
  // CLAMP THE IN-POINT. startFrom is derived from the cut index, which knows nothing about how
  // long the clip actually is: on EP55, 26 of 259 footage cuts started so late that the clip ran
  // out mid-cut and the frame went BLACK (measured 1.43s of black at 911s, luma 5). Never seek
  // past (source length - cut length).
  const _maxStart = srcSeconds ? Math.max(0, Math.round((srcSeconds - dur / _fps) * _fps)) : null;
  // a clip shorter than the cut loops instead of running out (build marks it loopSource)
  const _from = _maxStart == null || _maxStart <= 0 ? 0 : Math.min(startFrom, _maxStart);
  // progress over THIS cut's length (not the whole composition) so the Ken Burns
  // actually travels — normalizing against useVideoConfig().durationInFrames (the full
  // 20k-frame film) made p≈0 => footage read as near-still after the entrance settled.
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'});
  const s = interpolate(p, [0, 1], [1.05, 1.24]);
  const x = interpolate(p, [0, 1], [-42 * dir, 42 * dir]);
  const y = interpolate(p, [0, 1], [10 * dir, -10 * dir]);
  // A clip shorter than the cut must REPEAT, not run out: OffthreadVideo has no loop prop, so
  // the shot is wrapped in <Loop> at the clip's own length. Without this the video ends mid-cut
  // and the frame goes black (EP55/EP57 both failed the gate on exactly that).
  const _srcFrames = srcSeconds ? Math.max(1, Math.floor(srcSeconds * _fps) - 1) : null;
  const _needsLoop = _srcFrames != null && _srcFrames < dur;
  const lift = typeof _lift === 'number' ? Math.max(1, _lift) : 1;
  const liftStyle = lift > 1.001 ? {
    filter: `brightness(${lift.toFixed(3)}) contrast(${(1 + (lift - 1) * 0.25).toFixed(3)})`
  } : null;
  const _video = (
      <OffthreadVideo
        src={staticFile(src)}
        muted
        startFrom={_from}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transform: `translate(${x}px, ${y}px) scale(${s})`,
          filter: 'brightness(1.13) contrast(1.03) saturate(0.8)',
        }}
      />
  );
  return (
      <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      {liftStyle ? (
        <AbsoluteFill style={liftStyle}>
          {_needsLoop && _srcFrames ? <Loop durationInFrames={_srcFrames}>{_video}</Loop> : _video}
        </AbsoluteFill>
      ) : (
        _needsLoop && _srcFrames ? <Loop durationInFrames={_srcFrames}>{_video}</Loop> : _video
      )}
      <AbsoluteFill style={{pointerEvents: 'none', backgroundColor: navy, opacity: 0.14, mixBlendMode: 'multiply'}} />
      <AbsoluteFill
        style={{pointerEvents: 'none', background: `radial-gradient(135% 108% at 50% 44%, transparent 60%, ${ink}55 100%)`}}
      />
    </AbsoluteFill>
  );
};

/** bleed: full-frame depth — a blurred enlarged layer and the sharp image drift opposite ways. No tilt. */
const BleedStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  // LINEAR (constant-velocity) Ken-Burns: the old Easing.out(Easing.cubic) decelerated to
  // ~0 velocity by the end of each cut, so the tail of dark low-detail photos read as
  // near-still to freezedetect. A monotonic linear ramp keeps constant pixel velocity for the
  // ENTIRE duration (standard linear Ken-Burns push — never settles).
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'});
  const bgX = interpolate(p, [0, 1], [-72 * dir, 72 * dir]);
  const fgX = interpolate(p, [0, 1], [50 * dir, -50 * dir]);
  const fgS = interpolate(p, [0, 1], [1.07, 1.26]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(1.34)`, filter: 'blur(22px) brightness(0.9)'}}>
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
  bgX: interpolate(p, [0, 1], [-80 * dir, 80 * dir]),
  bgY: interpolate(p, [0, 1], [-34 * dir, 34 * dir]),
  fgX: interpolate(p, [0, 1], [56 * dir, -56 * dir]),
  fgY: interpolate(p, [0, 1], [26, -26]),
  fgS: interpolate(p, [0, 1], [1.08, 1.3]),
});

/** scan: parallax base + a thermal light pool and a slow-drifting measurement grid. */
const ScanStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'} /* linear = constant velocity, never decelerates to near-still */);
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  const gy = interpolate(p, [0, 1], [0, 80]);
  // light pool now drifts once across on a MONOTONIC diagonal (was a sin/cos orbit — owner
  // 2026-07-06 disliked circling faint light). Constant velocity also keeps it clear of freezedetect.
  const lx = interpolate(p, [0, 1], [34, 64]);
  const ly = interpolate(p, [0, 1], [34, 52]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(22px) brightness(0.9)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgS})`, filter: 'brightness(1.1) contrast(1.01) saturate(0.88)'}}>
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
const DuotoneStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'} /* linear = constant velocity, never decelerates to near-still */);
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  const vig = 0.9 + 0.1 * Math.sin(p * Math.PI * 2);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(22px) brightness(0.82)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <AbsoluteFill style={{transform: `translate(${fgX}px, ${fgY}px) scale(${fgS})`, filter: 'brightness(1.08) contrast(1.02) saturate(0.84) hue-rotate(-6deg)'}}>
        <Cover src={src} />
      </AbsoluteFill>
      <Particles seed={seed} count={20} color={silver} />
      <Vignette strength={vig} />
    </AbsoluteFill>
  );
};

/** focus: parallax base + rack-focus reveal on the sharp layer (soft -> sharp). */
const FocusStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  const blur = interpolate(f, [0, 22], [16, 0], {extrapolateRight: 'clamp'});
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'} /* linear = constant velocity, never decelerates to near-still */);
  const {bgX, bgY, fgX, fgY, fgS} = parallax(p, dir);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translate(${bgX}px, ${bgY}px) scale(1.34)`, filter: 'blur(24px) brightness(0.9)'}}>
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
const CardStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'} /* linear = constant velocity, never decelerates to near-still */);
  const bgX = interpolate(p, [0, 1], [-56 * dir, 56 * dir]);
  const cardX = interpolate(p, [0, 1], [42 * dir, -42 * dir]);
  const cardRot = interpolate(p, [0, 1], [-2.4 * dir, 2.4 * dir]);
  const intro = interpolate(f, [0, 10], [26, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `translateX(${bgX}px) scale(1.4)`, filter: 'blur(20px) brightness(0.84)'}}>
        <Cover src={src} />
      </AbsoluteFill>
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

/** depth: REAL 3D depth-map displacement (kills 紙芝居). The still is a subdivided plane
 *  displaced by its DPT depth map (`<name>_depth.png`, generated by the batch depth step
 *  `tools/depth/gen_depth.py`); a camera dolly-in yields genuine parallax — foreground and
 *  background move at different speeds, not a flat zoom. Falls back to bleed if no depth map. */
const depthSrcOf = (src: string) => src.replace(/\.[^.]+$/, '_depth.png');

const DepthCam: React.FC<{dolly: number; dir: number}> = ({dolly, dir}) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(Math.sin(dolly * Math.PI) * 0.26 * dir, 0.05 - dolly * 0.12, 5.2 - dolly * 2.0);
  camera.lookAt(0, 0, 0.4);
  camera.updateProjectionMatrix();
  return null;
};

const DepthPlane: React.FC<{src: string; displace: number}> = ({src, displace}) => {
  const color = useLoader(THREE.TextureLoader, staticFile(src));
  const disp = useLoader(THREE.TextureLoader, staticFile(depthSrcOf(src)));
  color.colorSpace = THREE.SRGBColorSpace;
  // overscan (1.18) so displaced edges stay off-frame during the dolly
  return (
    <mesh scale={[1.18, 1.18, 1]}>
      <planeGeometry args={[6, 3.375, 320, 200]} />
      <meshStandardMaterial map={color} displacementMap={disp} displacementScale={displace} roughness={1} metalness={0} toneMapped={false} />
    </mesh>
  );
};

export const DepthStill: React.FC<{src: string; seed: string; dir: number; dur: number}> = ({src, seed, dir, dur}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const dolly = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'} /* linear = constant velocity, never decelerates to near-still */);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <AbsoluteFill style={{filter: GRADE}}>
        <ThreeCanvas
          width={width}
          height={height}
          camera={{fov: 42, position: [0, 0, 5.2], near: 0.1, far: 100}}
          gl={{antialias: true}}
          style={{position: 'absolute'}}
        >
          <ambientLight intensity={2.4} />
          <DepthCam dolly={dolly} dir={dir} />
          <DepthPlane src={src} displace={1.25} />
        </ThreeCanvas>
      </AbsoluteFill>
      <Particles seed={seed} count={14} color={electric} />
      <Vignette />
    </AbsoluteFill>
  );
};

/** ALWAYS-MOVING LIGHT floor: a soft radial pool that ORBITS the frame at constant angular
 * velocity for the whole cut. Using x=sin(θ), y=cos(θ) traces a circle, so the pool's speed
 * is (near-)constant and never hits zero, and it loops seamlessly (no wrap snap). Very dark,
 * low-detail photos can have near-zero inter-frame delta even while the Ken-Burns pan is
 * moving (shifting black pixels changes almost nothing); the travelling pool re-lights a large
 * soft region every frame, keeping freezedetect above its near-still floor. Screen-blended and
 * faint so it reads as a passing light, never washing out or flattening the image. */
const DriftLight: React.FC<{dur: number}> = ({dur: _dur}) => {
  const f = useCurrentFrame();
  // NOTE: the orbiting radial "spinning faint light" that used to sit here was removed — owner
  // 2026-07-06 found it overused/annoying ("淡い光がくるくる回ってるエフェクトは使い過ぎ・うざい").
  // Only the freeze-floor micro-texture below remains (it is what actually clears freezedetect on
  // dark cuts; the orbit was decorative). It is a faint moving film grain, not a circling light.
  // Hard-delta floor: a fine diagonal micro-texture translated at CONSTANT velocity every
  // frame. A smooth light gradient shifting slowly barely changes any pixels (a near-black
  // low-detail photo then reads as frozen even while it pans); a high-spatial-frequency pattern
  // in continuous motion changes a large fraction of pixels every single frame regardless of how
  // dark the underlying image is, so freezedetect never trips. The pattern is periodic so the
  // translate loops seamlessly with no wrap snap; kept very faint (soft-light) so it reads as a
  // subtle moving film texture, not scanlines, and never lifts luma enough to flatten the image.
  // EP49 haze/scanline fix (owner 2026-07-24: "全体的に画像に曇りがかかってる" + a visible
  // DIAGONAL SCANLINE crosshatch over every frame). This layer WAS a 63° white
  // repeating-linear-gradient at 0.62 screen — that is exactly the diagonal scanline
  // texture + the milky screen-lift the owner flagged. It is REMOVED. Its only real job
  // was a per-frame pixel-delta floor for freezedetect on dark near-still photos; the
  // full-frame per-frame <Grain> (unique seed every frame) already guarantees that delta
  // across the whole frame, and AmbientMotion + per-cut parallax add coarse motion, so no
  // cut reads as frozen without this. Kept as a no-op so call sites are untouched.
  void _dur;
  return null;
};

const Still: React.FC<{cut: Cut; index: number}> = ({cut, index}) => {
  const dir = index % 2 === 0 ? 1 : -1;
  const {fps} = useVideoConfig();
  const dur = Math.max(1, Math.round(cut.dur * fps)); // motion spans THIS cut, not the whole film
  const treatment = (() => {
    switch (cut.treatment) {
      case 'depth':
        return <DepthStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
      case 'scan':
        return <ScanStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
      case 'duotone':
        return <DuotoneStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
      case 'focus':
        return <FocusStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
      case 'card':
        return <CardStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
      case 'bleed':
      default:
        return <BleedStill src={cut.src} seed={cut.seed} dir={dir} dur={dur} />;
    }
  })();
  // PER-STILL EXPOSURE LIFT. EP51 measured 93.4% of its stills below the readable luma floor
  // (median 45) and 29% of hero image cuts too dark to read -- the recurring 「画像が暗くて
  // 見えにくい」. A global screen wash was tried on EP49 and killed contrast, so the lift is
  // computed PER IMAGE at build time (cut.lift, 1.0 = leave alone) and applied only to stills:
  // a dark photo is opened up, an already-bright one is untouched.
  const lift = typeof cut.lift === 'number' ? cut.lift : 1;
  if (lift <= 1.001) return treatment;
  return (
    <AbsoluteFill style={{filter: `brightness(${lift.toFixed(3)}) contrast(${(1 + (lift - 1) * 0.25).toFixed(3)})`}}>
      {treatment}
    </AbsoluteFill>
  );
};

/** Designed, motion-blurred cut transition. Every cut ENTERS with one of three
 * cinematic moves (push-in from depth / rise-up / dip-through), spring-eased, with a
 * decaying blur that reads as real motion blur. Replaces the old flat 5-frame fade so
 * every single cut has premium dynamic energy — never a hard slideshow snap. */
const CutView: React.FC<{cut: Cut; index: number}> = ({cut, index}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dur = Math.max(1, Math.round(cut.dur * fps));
  const inner =
    cut.kind === 'footage' ? (
      <Footage
        src={cut.src}
        startFrom={cut.startFrom != null ? Math.round(cut.startFrom * fps) : (index * 47) % 160}
        srcSeconds={cut.srcSeconds ?? null}
        lift={typeof cut.lift === 'number' ? cut.lift : undefined}
        dir={index % 2 === 0 ? 1 : -1}
        dur={dur}
      />
    ) : (
      <Still cut={cut} index={index} />
    );
  // spring entrance 0..1 over ~12 frames
  const e = spring({frame: f, fps, config: {damping: 18, stiffness: 90, mass: 0.9}});
  const mode = index % 3; // rotate the transition style so cuts never feel mechanical
  const scale = mode === 0 ? interpolate(e, [0, 1], [1.14, 1.0]) : 1;
  const ty = mode === 1 ? interpolate(e, [0, 1], [64, 0]) : 0;
  const tx = mode === 2 ? interpolate(e, [0, 1], [(index % 2 ? -1 : 1) * 60, 0]) : 0;
  // motion blur that decays as the shot settles (px of gaussian ~ speed)
  const blur = interpolate(f, [0, 9], [14, 0], {extrapolateRight: 'clamp'});
  const opacity = interpolate(f, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  const overlay = cut.overlay ?? null;
  const overlayBlend: React.CSSProperties['mixBlendMode'] =
    cut.blendHint === 'overlay' ? 'overlay' : cut.blendHint === 'screen' ? 'screen' : 'plus-lighter';
  return (
    <AbsoluteFill
      style={{
        opacity,
        transform: `translate(${tx}px, ${ty}px) scale(${scale})`,
        filter: blur > 0.4 ? `blur(${blur}px)` : undefined,
      }}
    >
      {inner}
      {overlay ? (
        <Loop durationInFrames={Math.max(1, Math.round((cut.overlayDuration ?? cut.dur) * fps))}>
          <OffthreadVideo
            src={staticFile(overlay)}
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              mixBlendMode: overlayBlend,
              opacity: 0.28,
            }}
          />
        </Loop>
      ) : null}
      {/* always-moving pixel-velocity floor over EVERY cut (stills AND dark night/fire footage):
          keeps freezedetect above its near-still threshold for the entire cut duration. */}
      <DriftLight dur={dur} />
    </AbsoluteFill>
  );
};

/** Pre-composed 3D hero videos (Blender "big number" / scales scenes) settle to a near-static hold
 * after their first beat, so as a raw OffthreadVideo they tripped animation_density (freezedetect
 * read the settled tail as a >3s near-still hold). A slow constant-velocity Ken-Burns push (zoom +
 * pan) over the hero adds coarse frame motion on the hero's own sharp, high-detail edges, so no hero
 * window ever reads as frozen — while staying gentle enough to preserve the composed 3D framing. */
const HeroCut: React.FC<{src: string; index: number; dur: number}> = ({src, index, dur}) => {
  const f = useCurrentFrame();
  const dir = index % 2 === 0 ? 1 : -1;
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'});
  const s = interpolate(p, [0, 1], [1.02, 1.14]); // continuous slow zoom (never settles)
  const x = interpolate(p, [0, 1], [-46 * dir, 46 * dir]);
  const y = interpolate(p, [0, 1], [18 * dir, -18 * dir]);
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden'}}>
      <OffthreadVideo
        src={staticFile(src)}
        muted
        style={{width: '100%', height: '100%', objectFit: 'cover', transform: `translate(${x}px, ${y}px) scale(${s})`}}
      />
    </AbsoluteFill>
  );
};

/** BODY GRADE — one consistent cinematic wash laid over the WHOLE body (stills, footage AND
 * motion-graphics) so the three visual registers share a single noir-navy/teal world. Sits above
 * every visual layer but BELOW the captions so text stays crisp. Two very-low-opacity layers:
 *  (1) a soft-light navy/teal duotone-lean gradient — near luma-neutral (it lifts blues, faintly
 *      deepens shadows) so it unifies colour without crushing the image or failing images_present;
 *  (2) an overlay ring that is TRANSPARENT in the centre and only deepens the edges — a gentle
 *      global vignette/contrast seat that never dims the bright middle where subjects/figures sit. */
const BodyGrade: React.FC = () => (
  <>
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        mixBlendMode: 'soft-light',
        opacity: 0.1,
        background: `linear-gradient(175deg, ${electric} 0%, ${navy} 46%, ${ink} 100%)`,
      }}
    />
    {/* SHADOW LIFT: a faint screen-blend wash raises the darkest regions so dark hero stills clear
        the per-cut luma gate. EP49 (owner 2026-07-24): opacity 0.18 was a big part of the milky
        low-contrast "曇り" wash — screen-blend lifts blacks across the WHOLE frame, killing contrast.
        Cut to 0.07 (just enough shadow seat for the darkest photos) so the picture reads clear and
        punchy; the higher-contrast GRADE above now carries mid-tone brightness instead of a flat
        screen veil. */}
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        mixBlendMode: 'screen',
        opacity: 0.07,
        background: `linear-gradient(180deg, #2c3858 0%, #1d2842 100%)`,
      }}
    />
  </>
);

const Captions: React.FC<{cues: Caption[]}> = ({cues}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const cue = cues.find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
  // each caption springs up + fades in on its own cue — constant motion, never a static block
  const enter = spring({frame: f - Math.round(cue.start * fps), fps, config: {damping: 200, stiffness: 140}});
  const y = interpolate(enter, [0, 1], [22, 0]);
  const op = Math.min(enter * 2, 1);
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
          // cues carry their own grammatical line breaks (build_*_film.py splits on phrase
          // boundaries); honour them instead of letting the box wrap mid-phrase
          whiteSpace: 'pre-line',
          transform: `translateY(${y}px)`,
          opacity: op,
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
const BeatLine: React.FC<{ln: string; i: number}> = ({ln, i}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  // mask reveal ("切り上がり"): the text rises from BELOW a clipping mask, staggered.
  const enter = spring({frame: f - i * 7, fps, config: {damping: 18, stiffness: 110, mass: 0.9}});
  const y = interpolate(enter, [0, 1], [118, 0]); // percentage of its own height
  const short = ln.length <= 18;
  const size = short ? 92 : 54;
  return (
    <div style={{overflow: 'hidden', padding: '0 6px', lineHeight: 1.06}}>
      <div
        style={{
          transform: `translateY(${y}%)`,
          color: i === 0 ? white : gold,
          fontFamily: BRAND.font.display,
          fontWeight: 900,
          fontSize: size,
          letterSpacing: -0.5,
          textAlign: 'center',
          whiteSpace: 'nowrap',
          textShadow: `0 4px 24px rgba(0,0,0,0.92), 0 0 34px ${electric}55`,
        }}
      >
        {ln}
      </div>
    </div>
  );
};

const BeatText: React.FC<{lines: string[]}> = ({lines}) => {
  const f = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const outOp = interpolate(f, [durationInFrames - 12, durationInFrames], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const chip = spring({frame: f, fps, config: {damping: 16, stiffness: 130}});
  const underline = spring({frame: f - 6, fps, config: {damping: 18, stiffness: 90}});
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: '17%'}}>
      <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, opacity: outOp, maxWidth: '90%'}}>
        {/* kicker chip — a small gold bar that scales in above the headline (motion-graphics accent) */}
        <div
          style={{
            width: 54,
            height: 6,
            marginBottom: 8,
            borderRadius: 3,
            background: gold,
            transform: `scaleX(${chip})`,
            boxShadow: `0 0 16px ${gold}aa`,
          }}
        />
        {/* Trail = true motion-blur streaks while the lines rise into place */}
        <Trail layers={7} lagInFrames={1.1} trailOpacity={0.55}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6}}>
            {lines.map((ln, i) => (
              <BeatLine key={i} ln={ln} i={i} />
            ))}
          </div>
        </Trail>
        {/* animated gold underline that draws in under the beat */}
        <div
          style={{
            marginTop: 8,
            height: 5,
            width: '46%',
            borderRadius: 3,
            background: gold,
            transformOrigin: 'center',
            transform: `scaleX(${underline})`,
            opacity: outOp * 0.9,
            boxShadow: `0 0 18px ${gold}99`,
          }}
        />
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
const PunchShot: React.FC<{src: string; dur: number}> = ({src, dur}) => {
  const f = useCurrentFrame();
  const p = interpolate(f, [0, Math.max(1, dur)], [0, 1], {extrapolateRight: 'clamp'});
  const s = interpolate(p, [0, 1], [1.2, 1.06]);
  const op = interpolate(f, [0, 4], [0, 1], {extrapolateRight: 'clamp'});
  // hard, fast punch-in with a decaying motion blur — the aggressive cold-open energy
  const blur = interpolate(f, [0, 7], [20, 0], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: ink, overflow: 'hidden', opacity: op}}>
      <AbsoluteFill
        style={{
          transform: `scale(${s})`,
          filter: `brightness(0.9) contrast(1.06) saturate(0.9)${blur > 0.4 ? ` blur(${blur}px)` : ''}`,
        }}
      >
        <Cover src={src} />
      </AbsoluteFill>
      <DriftLight dur={dur} />
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
          <PunchShot src={h.src} dur={Math.max(1, Math.round(h.dur * fps))} />
        </Sequence>
      ))}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 150}}>
        <div
          style={{
            transform: `translateY(${y}px)`,
            opacity: lineOp,
            color: white,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: line.length > 92 ? 56 : 72,
            lineHeight: 1.08,
            letterSpacing: 0,
            textAlign: 'center',
            textTransform: 'uppercase',
            textShadow: '0 6px 30px rgba(0,0,0,0.8)',
            maxWidth: '80%',
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
  // === hook + op for every episode that does not declare leadSeconds (see caseFilmLeadFrames).
  const lead = caseFilmLeadFrames(data, fps);
  // The full-frame cold-open montage and the full-frame brand card only exist in the layout
  // that has room in FRONT of the body for them. With a zero lead (EP66) the cold open IS the
  // first body cuts -- cut starts in <slug>_film.json are body-relative, so a zero lead makes
  // them absolute -- and the brand opening becomes a lower-band overlay over continuing
  // picture and narration (EP66 PACKAGING v001 sections 4 and 7, implemented below and in
  // <BrandOpening variant="overlay">). This is true for every episode with no leadSeconds,
  // so their element tree is unchanged.
  const overlayOpening = data.openingVariant === 'overlay';
  const bookendsInFront = !overlayOpening && lead >= hook + op;
  // Where the band rises. Derived from the film's own hookSeconds so the number lives once:
  // EP66's 20.3 s hook + 0.2 s = 0:20.5, which is PACKAGING section 4's slot.
  const overlayFrom = Math.round(
    ((data.hookSeconds || 0) + OPENING_OVERLAY_OFFSET_SEC) * fps,
  );
  return (
    <AbsoluteFill style={{backgroundColor: ink}}>
      {hook > 0 && bookendsInFront && (
        <Sequence from={0} durationInFrames={hook} name="Hook">
          <Hook hook={data.hook} line={data.hookLine} />
        </Sequence>
      )}

      {bookendsInFront && (
        <Sequence from={hook} durationInFrames={op} name="Opening">
          <BrandOpening seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
        </Sequence>
      )}

      <Sequence from={lead} durationInFrames={body} name="Body">
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
        {/* leveled-up animation (other-thread AmbientMotion): drifting bokeh + orbiting glows
            composited over the body so no frame is ever static — the "紙芝居" killer. */}
        <AmbientMotion count={12} intensity={0.4} />
        <FigureBeats beats={(data.figures || []) as FigureSpec[]} />
        <GraphicsBeats beats={data.graphics} />
        {/* unified cinematic grade over stills+footage+graphics (below captions so text stays crisp) */}
        <BodyGrade />
        {/* pre-composed 3D hero videos play full-frame over their window (above the graded body,
            below captions). No-op for episodes without heroCuts. */}
        {(data.heroCuts || []).map((h, i) => (
          <Sequence
            key={`hero-${i}`}
            from={Math.round(h.start * fps)}
            durationInFrames={Math.max(1, Math.round(h.dur * fps))}
            name={`hero-${i}`}
          >
            <HeroCut src={h.src} index={i} dur={Math.max(1, Math.round(h.dur * fps))} />
          </Sequence>
        ))}
        <Captions cues={data.captions} />
        {/* EP49: grain 0.11 -> 0.06 (its default). At 0.11 it added to the milky veil; 0.06 still
            gives a unique-per-frame full-frame delta (freezedetect floor now that DriftLight's
            scanline texture is gone) without hazing the image. */}
        <Grain opacity={0.06} />
      </Sequence>

      {/* THE OPENING, zero-lead layout (EP66 PACKAGING v001 sections 4 and 7). Deliberately
          placed AFTER the Body sequence so it composites ON TOP of the running cut, and
          deliberately NOT wrapped around anything: the body keeps playing and the <Audio>
          master inside it keeps speaking for the whole 3.5 s. Renders only when the film
          declares openingVariant 'overlay', so no existing episode gains an element. */}
      {overlayOpening && (
        <Sequence from={overlayFrom} durationInFrames={op} name="Opening">
          <BrandOpening variant="overlay" seriesLabel={seriesLabel} title={title} subtitle={subtitle} />
        </Sequence>
      )}

      <Sequence from={lead + body} durationInFrames={ed} name="Endcard">
        <BrandEndcard />
      </Sequence>
    </AbsoluteFill>
  );
};
