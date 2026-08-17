import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  OffthreadVideo,
  Sequence,
  Series,
  Video,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {ThreeCanvas} from '@remotion/three';
import {useLoader, useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {BRAND} from '../brand';
import {AmbientMotion} from '../components/AmbientMotion';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';
import {
  BigNumberVertical,
  CitationTopLeft,
  DiagramFlowVertical,
  DoorsVertical,
  VoteVertical,
} from '../components/ShortVerticalArt';
// Premium motion layer (motionkit) — named exports, self-animating, pure DOM/SVG (no WebGL).
import {
  AuroraField,
  CinematicTitle,
  DepthParticles,
  LightRays,
  MoneyFlow,
  NumberTicker,
  QuoteCard,
  StackedProportion,
  VoteTally,
  YearSweep,
} from '../components/motionkit';

/**
 * Short — vertical 9:16 (1080x1920) Short assembler. SHORTS_REMOTION_SPEC.md (spec A) §3–5.
 * One data file per Short (data/shortNN.ts); this template lays out the beats, moves every
 * image (never static), keeps telop (top zone) and captions (bottom zone) strictly separated,
 * drops a "meaningful animation" over the climax/number beats, and mixes the audio.
 *
 * Same video for YouTube Shorts and TikTok — only the closing CTA differs (`platform`), so the
 * exact same footage exports twice (§10). TikTok must never name an external platform.
 */

export type ShortArt =
  | {kind: 'bignum'; top: string; bottom?: string}
  | {kind: 'vote'; yes: number; no: number}
  | {kind: 'diagram'; steps: string[]}
  | {kind: 'doors'; items: string[]; title?: string}
  | {kind: 'citation'; label: string; source?: string}
  // --- PREMIUM motionkit art (SCENE = opaque full-frame, replaces the still for that beat) ---
  | {kind: 'ticker'; value: number; prefix?: string; suffix?: string; decimals?: number; topLabel?: string; label?: string}
  | {kind: 'money'; nodes: {x: number; y: number; label?: string}[]; edges: {from: number; to: number; weight?: number}[]}
  | {kind: 'stack'; parts: {label: string; value: number; accent?: string}[]; title?: string}
  | {kind: 'votetally'; majority: number; dissent: number; label?: string}
  | {kind: 'quote'; quote: string; attribution: string}
  | {kind: 'cititle'; title: string; subtitle?: string}
  | {kind: 'yearsweep'; from: number; to: number; label?: string}
  // --- PREMIUM motionkit art (OVERLAY = transparent, layers over the depth still) ---
  | {kind: 'lightrays'; color?: string};

/** SCENE arts paint their own opaque backdrop, so they stand in for the beat's image. */
export const SCENE_ART_KINDS = new Set([
  'ticker',
  'money',
  'stack',
  'votetally',
  'quote',
  'cititle',
  'yearsweep',
]);

/**
 * Composited decoration layer over (or under) the hero — factory light/particle/vfx clips or a
 * background plate. Blend defaults to 'screen' (light/leak/strobe/smoke read as additive glow).
 * Keep it tasteful: 1–2 layers per beat so the hero, telop and captions stay readable.
 */
export type ShortLayer = {
  src: string; // staticFile-relative path under remotion/public
  kind?: 'video' | 'image'; // default 'video' (factory clips loop muted)
  blend?: 'screen' | 'add' | 'overlay' | 'multiply' | 'normal'; // default 'screen'
  opacity?: number; // 0..1, default 0.5
  motion?: ShortBeat['motion']; // optional drift (image layers)
};

export type ShortBeat = {
  id: string; // 'hook' | 'b1' ... | 'cta'
  startSec: number;
  durSec: number;
  src: string | null; // staticFile-relative path under remotion/public; null -> brand card
  kind: 'image' | 'video' | 'card';
  motion: 'kenburns' | 'parallax' | 'pushin' | 'video';
  telop?: string; // top-zone headline/keyword
  fast?: boolean; // hook fast-cut (shorter, stronger SFX)
  art?: ShortArt; // meaningful animation over the background (middle zone)
  bg?: string | null; // background plate behind the hero (factory b-roll / image); cinematic depth
  bgKind?: 'video' | 'image'; // default 'video'
  overlays?: ShortLayer[]; // light/particle/vfx composited above the hero (below grade/telop)
  /** Run this beat's camera backwards so it ends on the opening framing (loop seam). */
  rewind?: boolean;
};

export type ShortCaption = {word: string; startSec: number; endSec: number};

/** One mid-roll kinetic-typography hit, built in After Effects and composited here.
 *
 *  Remotion does the depth moves and the cutting; what it does not do cheaply is per-character
 *  typography with real motion blur, which is the thing the owner keeps describing as missing.
 *  The overlay is rendered once as a VP9 WebM carrying a real alpha channel
 *  (scripts/ae/render_beats.sh) and dropped in here, so no Short needs hand work in AE.
 *
 *  `atSec`/`durSec` must sit INSIDE the cut they land on. A hit that outlives its cut leaves the
 *  rule and the scrim hanging over an unrelated shot — measured on the first short118 pass. */
export type KineticBeat = {
  src: string; // staticFile-relative, e.g. 'kinetic/short118_a.webm'
  atSec: number;
  durSec: number;
  phrase?: string; // what it says, for the acceptance report — not read at render time
};

export type ShortData = {
  shortId: string; // 'short08'
  episodeId: string; // 'PD-2026-008-carpenter'
  durationSec: number; // = sum(beats). 35–45
  narrationSrc: string | null;
  captions: ShortCaption[] | null; // forced-alignment result
  bgmSrc: string | null;
  ambienceSrc?: string | null;
  sfx?: {atSec: number; src: string; gainDb?: number}[];
  ctaTextYT?: string; // YouTube CTA (e.g. "続きはYouTubeで")
  ctaTextTT?: string; // TikTok CTA (no external platform name, e.g. "フル版はプロフィールから")
  // --- Long-form funnel end-card (SHORTS_CONVERSION_v001 §4-2). ALL THREE OPTIONAL. ---
  // Supply any one of them and the closing beat renders the long-form card (thumbnail + title +
  // headline) instead of the legacy `SUBSCRIBE` end-card. Supply none and the closing beat is
  // byte-identical to what it was before — already-scheduled Shorts must not move.
  ctaLongThumbSrc?: string; // matching long-form's thumbnail, staticFile-relative, 16:9 (1280x720)
  ctaLongTitle?: string; // shortened long-form title. ONE line, <= 36 ASCII chars.
  ctaHeadline?: string; // default 'FULL CASE'. UPPERCASE, <= 2 words, <= 12 ASCII chars.
  /** Optional y for the caption band (px, 1080x1920). Omit to keep the METHOD default of
   *  1000, which sits at 52-69% of the frame. Set ~1270 to drop captions to the lower
   *  third, clear of the subject and still above the Shorts bottom overlay. */
  captionTop?: number;
  /** Seconds of fade at the END of the CTA beat. The card's backdrop is the hook plate, so
   *  fading only the card away leaves the opening image as the final frame and the Short loops
   *  without a visible seam - the destination still holds for everything before the fade. */
  ctaFadeOutSec?: number;
  beats: ShortBeat[];
  /** Optional. Omit and the Short renders byte-identical to before, so already-scheduled Shorts
   *  do not move. One or two per Short — more reads as decoration rather than emphasis. */
  kineticBeats?: KineticBeat[];
};

export type ShortPlatform = 'yt' | 'tiktok';

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));

export const shortDurationInFrames = (data: ShortData, fps: number): number =>
  Math.max(1, Math.round(data.durationSec * fps));

const grade = (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background: `linear-gradient(180deg, ${BRAND.color.ink}cc 0%, transparent 22%, transparent 64%, ${BRAND.color.ink}ee 100%)`,
    }}
  />
);

/** CSS mix-blend-mode for a decoration layer ('add' has no CSS name -> plus-lighter). */
const BLEND: Record<NonNullable<ShortLayer['blend']>, string> = {
  screen: 'screen',
  add: 'plus-lighter',
  overlay: 'overlay',
  multiply: 'multiply',
  normal: 'normal',
};

/** Vertical moving image — 2.5D & never static. A soft, over-scaled copy of the same frame sits behind
 * the sharp hero and drifts the opposite way, so a flat still reads as depth (foreground + background
 * parallax). The hero always moves on scale + X + Y + a hair of rotation (eased), so no frame sits still.
 * `fast` (hook) wraps the hero in a motion-blur Trail for a punchy, produced feel. */
const MovingImageV: React.FC<{src: string; motion: ShortBeat['motion']; fast?: boolean; rewind?: boolean}> = ({
  src,
  motion,
  fast,
  rewind,
}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const ease = {extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.cubic)};
  // `rewind` runs the camera backwards so the beat ENDS where the opening beat BEGAN. Without it
  // the closing plate is the same picture at a different focal length, and the loop seam measured
  // 41.6/255 - visibly a cut. The motion is still continuous; it just travels the other way.
  const range: [number, number] =
    motion === 'pushin' ? [1.08, fast ? 1.34 : 1.24] : motion === 'parallax' ? [1.1, 1.22] : [1.08, 1.2];
  const span: [number, number] = rewind ? [range[1], range[0]] : range;
  const scale = interpolate(f, [0, d], span, ease);
  // continuous multi-axis camera (always moving, direction varies by motion type)
  const dir = (motion === 'parallax' ? 1 : motion === 'kenburns' ? -1 : 0.5) * (rewind ? -1 : 1);
  const driftX = interpolate(f, [0, d], [-30 * dir, 30 * dir], ease);
  const driftY = interpolate(f, [0, d], rewind ? [-30, 30] : [30, -30], ease) * (motion === 'pushin' ? 0.4 : 1);
  const rot = interpolate(f, [0, d], rewind ? [0.6, -0.6] : [-0.6, 0.6], ease) * (motion === 'parallax' ? 1 : 0.5);
  // background depth plate: same image, blurred & larger, drifting opposite the hero
  const bgScale = interpolate(f, [0, d], [1.28, 1.42], ease);
  const hero = (
    <AbsoluteFill
      style={{
        transform: `translate(${driftX}px, ${driftY}px) scale(${scale}) rotate(${rot}deg)`,
        transformOrigin: '50% 46%',
      }}
    >
      <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </AbsoluteFill>
  );
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill
        style={{
          transform: `translate(${-driftX * 1.6}px, ${-driftY * 1.6}px) scale(${bgScale})`,
          transformOrigin: '50% 46%',
          filter: 'blur(14px) brightness(0.5)',
        }}
      >
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      {fast ? (
        <Trail layers={5} lagInFrames={1.2} trailOpacity={0.4}>
          {hero}
        </Trail>
      ) : (
        hero
      )}
    </AbsoluteFill>
  );
};

/** depth (pilot): REAL 3D depth-map parallax for the vertical Short, ported from CaseFilm's
 *  DepthStill and re-tuned for 9:16. The still is a subdivided plane displaced by its DPT depth
 *  map (`<name>_depth.png` from tools/depth/gen_depth.py); a small camera dolly gives genuine
 *  parallax — foreground moves more than background — instead of the pseudo-2.5D blur plate. */
const depthSrcOfV = (src: string) => src.replace(/\.[^.]+$/, '_depth.png');

const DepthCamV: React.FC<{dolly: number; dir: number}> = ({dolly, dir}) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(Math.sin(dolly * Math.PI) * 0.14 * dir, 0.05 - dolly * 0.08, 5.2 - dolly * 1.5);
  camera.lookAt(0, 0, 0.4);
  camera.updateProjectionMatrix();
  return null;
};

const DepthPlaneV: React.FC<{src: string; displace: number}> = ({src, displace}) => {
  const color = useLoader(THREE.TextureLoader, staticFile(src));
  const disp = useLoader(THREE.TextureLoader, staticFile(depthSrcOfV(src)));
  color.colorSpace = THREE.SRGBColorSpace;
  // plane aspect = 9:16 (0.5625) to match the frame; overscan 1.2 keeps displaced edges off-frame
  return (
    <mesh scale={[1.2, 1.2, 1]}>
      <planeGeometry args={[2.25, 4.0, 220, 380]} />
      <meshStandardMaterial map={color} displacementMap={disp} displacementScale={displace} roughness={1} metalness={0} toneMapped={false} />
    </mesh>
  );
};

const DepthImageV: React.FC<{src: string; motion: ShortBeat['motion']; fast?: boolean; rewind?: boolean}> = ({src, motion, fast, rewind}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d, width, height} = useVideoConfig();
  const dir = (motion === 'kenburns' ? -1 : 1) * (rewind ? -1 : 1);
  // With `depth` on, THIS is the renderer - not MovingImageV. The first attempt at a loop seam
  // added rewind only to MovingImageV and the measured seam did not move at all (0.464 structural
  // match, before and after), because every plate in these Shorts goes through the depth path.
  const dolly = interpolate(f, [0, Math.max(1, d)], rewind ? [1, 0] : [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 42, position: [0, 0, 5.2], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <ambientLight intensity={2.4} />
        <DepthCamV dolly={dolly} dir={dir} />
        <DepthPlaneV src={src} displace={fast ? 0.62 : 0.5} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};

/** Full-frame factory b-roll (hero or background plate), slowly drifting so it never sits still. */
const MovingVideoV: React.FC<{src: string; plate?: boolean}> = ({src, plate}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const ease = {extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.cubic)};
  const scale = interpolate(f, [0, durationInFrames], plate ? [1.12, 1.22] : [1.04, 1.12], ease);
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 46%'}}>
        {/* OffthreadVideo, not Video: the hero clip is decoded by ffmpeg instead of by Chrome.
            Chrome's decoder threw MEDIA_ERR code 3 (PIPELINE_ERROR_DISCONNECTED, "video decode
            error") partway through every render of the Wan-i2v clips, at a different frame each
            time. Re-encoding the clips (30 fps, Main profile, faststart, closed GOP) did not fix
            it; taking the decode out of the browser did. */}
        {/* No loop prop on OffthreadVideo in this Remotion version: every clip in use (~3.5 s) is
            longer than any beat that shows it (<=2.3 s), so it never needs to wrap. A future beat
            longer than its clip must trim the beat, not re-introduce <Video>. */}
        <OffthreadVideo
          src={staticFile(src)}
          muted
          style={{width: '100%', height: '100%', objectFit: 'cover', filter: plate ? 'brightness(0.7)' : 'none'}}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** One composited decoration layer (light leak / police strobe / dust / smoke), screen-blended.
 * Video layers loop; still-image layers (light-leak / dust JPGs) are kept alive with a slow eased
 * drift + scale + gentle opacity breathing so they read as moving light/particles, never a flat plate. */
const OverlayLayer: React.FC<{layer: ShortLayer}> = ({layer}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const ease = {extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.sin)};
  const blend = BLEND[layer.blend ?? 'screen'];
  const base = layer.opacity ?? 0.5;
  const common = {width: '100%', height: '100%', objectFit: 'cover' as const};
  const isVideo = (layer.kind ?? 'video') === 'video';
  // breathe opacity a touch so light never sits perfectly still
  const opacity = base * interpolate(f, [0, d / 2, d], [0.82, 1, 0.82], ease);
  const dx = interpolate(f, [0, d], [-24, 24], ease);
  const dy = interpolate(f, [0, d], [18, -18], ease);
  const sc = interpolate(f, [0, d], [1.06, 1.16], ease);
  return (
    <AbsoluteFill style={{mixBlendMode: blend as React.CSSProperties['mixBlendMode'], opacity, pointerEvents: 'none'}}>
      {isVideo ? (
        <Video src={staticFile(layer.src)} muted loop style={common} />
      ) : (
        <AbsoluteFill style={{transform: `translate(${dx}px, ${dy}px) scale(${sc})`, transformOrigin: '50% 50%'}}>
          <Img src={staticFile(layer.src)} style={common} />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};

/** Top-zone telop (y180–560): big Impact headline. Each line mask-reveals (overflow-hidden + translateY
 * rise) with a per-line stagger, then the block keeps a subtle continuous float so it never freezes.
 * Never overlaps the caption band. */
const TelopTop: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = text.split('\n');
  const float = Math.sin(frame / 22) * 4; // gentle ongoing drift
  return (
    <div
      style={{
        position: 'absolute',
        top: 180,
        left: 60,
        right: 60,
        height: 380,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
        pointerEvents: 'none',
        transform: `translateY(${float}px)`,
      }}
    >
      {lines.map((l, i) => {
        const enter = spring({frame: frame - i * 5, fps, config: {damping: 20, stiffness: 130, mass: 0.7}});
        const rise = interpolate(enter, [0, 1], [110, 0]);
        return (
          <div key={i} style={{overflow: 'hidden', padding: '0 6px'}}>
            <div
              style={{
                transform: `translateY(${rise}%)`,
                color: BRAND.color.white,
                fontFamily: BRAND.font.display,
                fontSize: 96,
                lineHeight: 1.06,
                letterSpacing: -1,
                textAlign: 'center',
                textShadow: `0 4px 24px ${BRAND.color.ink}, 0 0 50px ${BRAND.color.ink}`,
              }}
            >
              {l}
            </div>
          </div>
        );
      })}
    </div>
  );
};

/** Closing CTA endcard (last beat). Platform-specific text; TikTok never names an external site.
 *
 * On TikTok the brand wordmark and the SUBSCRIBE pill are both omitted (2026-08-17). TikTok's
 * originality policy states that repurposed content carrying a watermark or logo is in most cases
 * not treated as original, and unoriginal content is made ineligible for the For You feed. These
 * Shorts are the same files published on YouTube, so the burned-in wordmark is exactly the signal
 * that policy describes. Measured before the change: the first two posts on a brand-new account
 * with a clean handle sat at 0 views for 7 and 3 hours. The closing line itself stays.
 */
const CtaLayer: React.FC<{text: string; platform: ShortPlatform}> = ({text, platform}) => {
  const brand = platform !== 'tiktok';
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const enter = spring({frame, fps, config: {damping: 16, stiffness: 120}});
  const isLong = text.length >= 10;
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
      <div
        style={{
          transform: `scale(${interpolate(enter, [0, 1], [0.8, 1])})`,
          opacity: enter,
          textAlign: 'center',
          padding: '0 80px',
        }}
      >
        {brand ? (
          <div
            style={{
              color: BRAND.color.gold,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 44,
              letterSpacing: 4,
              marginBottom: 22,
            }}
          >
            PRIME DOCUMENTARY
          </div>
        ) : null}
        <div
          style={{
          color: BRAND.color.white,
          fontFamily: BRAND.font.display,
          fontSize: isLong ? 78 : 104,
          lineHeight: 1.08,
          wordBreak: 'keep-all',
          overflowWrap: 'normal',
            textShadow: `0 6px 30px ${BRAND.color.ink}`,
          }}
        >
          {text}
        </div>
        {brand && (
        <div
          style={{
            marginTop: 30,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 14,
            padding: '14px 30px',
            borderRadius: 999,
            background: BRAND.color.gold,
            color: BRAND.color.ink,
            fontFamily: BRAND.font.display,
            fontSize: 40,
            letterSpacing: 2,
            transform: `translateY(${interpolate(enter, [0, 1], [24, 0])}px)`,
            opacity: enter,
          }}
        >
          <span style={{fontSize: 30}}>▶</span> SUBSCRIBE
        </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

/* ---------------------------------------------------------------------------------------------
 * Long-form funnel end-card — SHORTS_CONVERSION_v001 §4.
 *
 * WHY: 22 published Shorts ended on a bare `SUBSCRIBE` pill and converted 0 subscribers
 * (§1, measured). The fix is not a louder ask, it is a *destination*: show the exact long-form
 * this Short is a trailer for — its thumbnail, its title, and a headline that matches the spoken
 * close. The string `SUBSCRIBE` never appears in this layer (§4-4).
 *
 * OPT-IN: rendered only when the data file supplies ctaLongThumbSrc / ctaLongTitle / ctaHeadline.
 * Without them BeatView falls through to the legacy `CtaLayer` above, unchanged.
 *
 * SAFE AREA (§4-4): the Shorts UI covers x > 840 and y > 1500, so every element here lives inside
 * x 80–1000 / y 300–1400. Legibility floor for a phone-sized 1080x1920 frame: headline 88px,
 * title >= 34px on a 6px gold-bordered card, pill 40px, all on a 0.72 ink scrim.
 * ------------------------------------------------------------------------------------------- */

const CTA_HEADLINE_DEFAULT = 'FULL CASE';
/** §4-4 geometry, in frame px. Kept as named constants — no magic numbers inside the JSX. */
const CTA_LAYOUT = {
  headTop: 430,
  headHeight: 110,
  headSize: 88,
  cardLeft: 180,
  cardTop: 570,
  cardW: 720,
  cardH: 405, // 16:9
  titleTop: 1030,
  titleLeft: 120,
  titleW: 840,
  titleSize: 46,
  pillTop: 1130,
  pillHeight: 76,
  pillSize: 40,
  brandTop: 1250,
  brandSize: 36,
} as const;

/** Text that rises out of a clipped box (overflow:hidden + translateY) — the channel's standard
 * reveal. `enter` is a 0..1 spring value; never a bare opacity fade. */
const CtaMaskRise: React.FC<{enter: number; height: number; children: React.ReactNode}> = ({
  enter,
  height,
  children,
}) => (
  <div style={{overflow: 'hidden', height, display: 'flex', alignItems: 'flex-end', justifyContent: 'center'}}>
    <div style={{transform: `translateY(${interpolate(enter, [0, 1], [110, 0])}%)`, width: '100%'}}>{children}</div>
  </div>
);

const CtaFunnelLayer: React.FC<{
  thumbSrc?: string;
  title?: string;
  headline: string;
  platform: ShortPlatform;
  fadeOutSec?: number;
}> = ({thumbSrc, title, headline, platform, fadeOutSec}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  // Owner 2026-08-02: make the Short loop. The backdrop of this beat is already the hook plate,
  // so fading the CARD out at the end - not the picture - returns the frame to exactly what the
  // viewer saw at t=0. Everything before the fade still holds the destination on screen.
  const fadeF = Math.round((fadeOutSec ?? 0) * fps);
  const exit = fadeF > 0
    ? interpolate(frame, [durationInFrames - fadeF, durationInFrames - 1], [1, 0],
                  {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
    : 1;
  // Every timing below is authored in SECONDS and converted here — no hard-coded frame numbers.
  const F = (s: number) => Math.round(s * fps);
  const easeOut = {
    extrapolateLeft: 'clamp' as const,
    extrapolateRight: 'clamp' as const,
    easing: Easing.out(Easing.cubic),
  };

  // L1 — ink scrim over the outgoing beat. Never opacity-only: the plate pushes in as it darkens
  // (1.00 -> 1.04 by 0.13 s) and keeps creeping to 1.08 so no frame of the hold is static (§4-3).
  // 0.72 buried the backdrop: the closing 8.6 s of short89 measured a mean luma of 11.8/255,
  // unreadable on a phone outdoors, even though the card itself was legible. The card sits on
  // its own gold-bordered panel and does not need the whole frame darkened to be read.
  const scrim = interpolate(frame, [0, F(0.13)], [0, 0.46], easeOut);
  const bgScale = interpolate(
    frame,
    [0, F(0.13), F(1.1), Math.max(F(1.1) + 1, durationInFrames)],
    [1, 1.04, 1.04, 1.08],
    easeOut
  );

  // Staggered entries (§4-3): card 0.13 s, headline 0.20 s, title 0.40 s, pill 0.67 s, brand 0.87 s.
  const cardEnter = spring({frame: frame - F(0.13), fps, config: {damping: 18, stiffness: 130, mass: 0.8}});
  const headEnter = spring({frame: frame - F(0.2), fps, config: {damping: 20, stiffness: 130, mass: 0.7}});
  const titleEnter = spring({frame: frame - F(0.4), fps, config: {damping: 20, stiffness: 130, mass: 0.7}});
  const pillEnter = spring({frame: frame - F(0.67), fps, config: {damping: 16, stiffness: 120}});
  const brandEnter = spring({frame: frame - F(0.87), fps, config: {damping: 16, stiffness: 120}});

  // Continuous micro-float on the whole block so the hold never freezes (§4-3, f33+).
  const float = Math.sin(frame / 22) * 3;

  // The card's entry (0.13–0.60 s) is the only motion-blurred element — Trail on text kills
  // legibility (§4-3). After the entry the Trail is dropped so the hold renders sharp and cheap.
  const cardMoving = frame < F(0.62);

  // One line, always. 0.47 em/char is Oswald-700 measured off a rendered still (a 36-char title
  // occupied ~600 of the 840px column at 40px), with headroom. A title longer than the §4-2 cap
  // scales down to a 34px floor instead of clipping or spilling past the safe area.
  const titleText = title ?? '';
  const titleSize = Math.max(
    34,
    Math.min(CTA_LAYOUT.titleSize, Math.floor(CTA_LAYOUT.titleW / (Math.max(1, titleText.length) * 0.47)))
  );

  const card = thumbSrc ? (
    <div
      style={{
        position: 'absolute',
        left: CTA_LAYOUT.cardLeft,
        top: CTA_LAYOUT.cardTop,
        width: CTA_LAYOUT.cardW,
        height: CTA_LAYOUT.cardH,
        borderRadius: 18,
        border: `6px solid ${BRAND.color.gold}`,
        boxShadow: `0 24px 64px ${BRAND.color.ink}`,
        overflow: 'hidden',
        backgroundColor: BRAND.color.ink,
        transform: `translateY(${interpolate(cardEnter, [0, 1], [52, 0])}px) scale(${interpolate(
          cardEnter,
          [0, 1],
          [0.86, 1]
        )})`,
      }}
    >
      <Img src={staticFile(thumbSrc)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
    </div>
  ) : null;

  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: exit}}>
      {/* L1 — darkening + pushing-in scrim over the outgoing beat */}
      <AbsoluteFill
        style={{
          backgroundColor: BRAND.color.ink,
          opacity: scrim,
          transform: `scale(${bgScale})`,
          transformOrigin: '50% 45%',
        }}
      />
      {/* L2 — radial navy glow behind the card */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(70% 44% at 50% 41%, ${BRAND.color.navy} 0%, transparent 72%)`,
          opacity: interpolate(frame, [0, F(0.3)], [0, 0.95], easeOut),
          transform: `scale(${bgScale})`,
        }}
      />
      {/* L3–L7 — the block itself, floating as one so nothing drifts apart */}
      <AbsoluteFill style={{transform: `translateY(${float}px)`}}>
        {/* L3 — headline (mask rise) */}
        <div style={{position: 'absolute', left: CTA_LAYOUT.cardLeft, top: CTA_LAYOUT.headTop, width: CTA_LAYOUT.cardW}}>
          <CtaMaskRise enter={headEnter} height={CTA_LAYOUT.headHeight}>
            <div
              style={{
                color: BRAND.color.gold,
                fontFamily: BRAND.font.display,
                fontSize: CTA_LAYOUT.headSize,
                lineHeight: 1.1,
                letterSpacing: 6,
                textAlign: 'center',
                textTransform: 'uppercase',
                textShadow: `0 6px 30px ${BRAND.color.ink}`,
              }}
            >
              {headline}
            </div>
          </CtaMaskRise>
        </div>

        {/* L4 — the long-form thumbnail card (motion-blurred on entry only) */}
        {cardMoving ? (
          <Trail layers={4} lagInFrames={1.0} trailOpacity={0.35}>
            {card}
          </Trail>
        ) : (
          card
        )}

        {/* L5 — long-form title, one line (mask rise, 6f staggered behind the headline) */}
        {titleText ? (
          <div
            style={{
              position: 'absolute',
              left: CTA_LAYOUT.titleLeft,
              top: CTA_LAYOUT.titleTop,
              width: CTA_LAYOUT.titleW,
            }}
          >
            <CtaMaskRise enter={titleEnter} height={Math.round(titleSize * 1.5)}>
              <div
                style={{
                  color: BRAND.color.white,
                  fontFamily: BRAND.font.body,
                  fontWeight: 700,
                  fontSize: titleSize,
                  lineHeight: 1.15,
                  whiteSpace: 'nowrap',
                  textAlign: 'center',
                  textShadow: `0 4px 22px ${BRAND.color.ink}`,
                }}
              >
                {titleText}
              </div>
            </CtaMaskRise>
          </div>
        ) : null}

        {/* L6 — destination pill. TikTok never names an external platform (§4-5). */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: CTA_LAYOUT.pillTop,
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 14,
              height: CTA_LAYOUT.pillHeight,
              padding: '0 30px',
              borderRadius: 999,
              background: BRAND.color.gold,
              color: BRAND.color.ink,
              fontFamily: BRAND.font.display,
              fontSize: CTA_LAYOUT.pillSize,
              letterSpacing: 2,
              transform: `translateY(${interpolate(pillEnter, [0, 1], [24, 0])}px) scale(${interpolate(
                pillEnter,
                [0, 1],
                [0.9, 1]
              )})`,
              opacity: pillEnter,
            }}
          >
            {/* Owner 2026-08-02: "ボタンを押したらそこに飛ぶ仕様になってる？" - it never did.
                A pill burned into the frame looks tappable and is not, which is worse than no
                pill: the viewer taps, nothing happens, and the one real link goes unused.
                The only 1-tap native path out of a Short is the Studio 'Related video' link,
                which YouTube renders BELOW the player. So this element stops imitating a button
                and starts pointing at the real one. TikTok has no such link, so it keeps the
                profile wording (and still names no external platform). */}
            <span style={{fontSize: 30}}>{platform === 'tiktok' ? '▶' : '▼'}</span>
            {platform === 'tiktok' ? 'ON OUR PROFILE' : 'LINK BELOW'}
          </div>
        </div>

        {/* L7 — brand line */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: CTA_LAYOUT.brandTop,
            textAlign: 'center',
            color: BRAND.color.gold,
            opacity: 0.7 * brandEnter,
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: CTA_LAYOUT.brandSize,
            letterSpacing: 4,
            transform: `translateY(${interpolate(brandEnter, [0, 1], [18, 0])}px)`,
          }}
        >
          PRIME DOCUMENTARY
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** True when the data file opted into the long-form funnel end-card (§4-2). */
const hasFunnelCta = (data: ShortData): boolean =>
  Boolean(data.ctaLongThumbSrc || data.ctaLongTitle || data.ctaHeadline);

const ArtLayer: React.FC<{art: ShortArt; durFrames: number}> = ({art, durFrames}) => {
  switch (art.kind) {
    case 'bignum':
      return <BigNumberVertical top={art.top} bottom={art.bottom} />;
    case 'vote':
      return <VoteVertical yes={art.yes} no={art.no} />;
    case 'diagram':
      return <DiagramFlowVertical steps={art.steps} />;
    case 'doors':
      return <DoorsVertical items={art.items} title={art.title} />;
    case 'citation':
      return <CitationTopLeft label={art.label} source={art.source} />;
    // --- premium motionkit (dur = this beat's frames so intro/outro fit the cut) ---
    case 'ticker':
      return (
        <NumberTicker
          value={art.value}
          prefix={art.prefix}
          suffix={art.suffix}
          decimals={art.decimals}
          topLabel={art.topLabel}
          label={art.label}
          dur={durFrames}
        />
      );
    case 'money':
      return <MoneyFlow nodes={art.nodes} edges={art.edges} dur={durFrames} />;
    case 'stack':
      return <StackedProportion parts={art.parts} title={art.title} dur={durFrames} />;
    case 'votetally':
      return <VoteTally majority={art.majority} dissent={art.dissent} label={art.label} dur={durFrames} />;
    case 'quote':
      return <QuoteCard quote={art.quote} attribution={art.attribution} dur={durFrames} />;
    case 'cititle':
      return <CinematicTitle title={art.title} subtitle={art.subtitle} dur={durFrames} />;
    case 'yearsweep':
      return <YearSweep from={art.from} to={art.to} label={art.label} dur={durFrames} />;
    case 'lightrays':
      return <LightRays color={art.color} dur={durFrames} />;
    default:
      return null;
  }
};

/** Brand card for a beat with no asset (keeps the timeline complete). */
const BrandCard: React.FC = () => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 80% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 82%)`,
    }}
  />
);

const BeatView: React.FC<{beat: ShortBeat; platform: ShortPlatform; data: ShortData; depth?: boolean}> = ({
  beat,
  platform,
  data,
  depth,
}) => {
  const isCta = beat.id === 'cta';
  const ctaText = (platform === 'tiktok' ? data.ctaTextTT : data.ctaTextYT) ?? '';
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const durFrames = framesFor(beat.durSec, fps);
  // short entry punch so each cut lands like an edit, not a hard slide-show swap
  const enter = spring({frame, fps, config: {damping: 200, stiffness: 140, mass: 0.5}});
  const enterScale = interpolate(enter, [0, 1], [1.05, 1]);
  const enterOpacity = interpolate(enter, [0, 1], [0, 1], {extrapolateRight: 'clamp'});
  // PREMIUM scene arts (money/vote/quote/title/ticker/stack/year) paint their own opaque backdrop,
  // so they ARE the beat's visual — the depth still is skipped for those beats.
  const sceneArt = beat.art && SCENE_ART_KINDS.has(beat.art.kind);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, transform: `scale(${enterScale})`, opacity: enterOpacity}}>
      {sceneArt ? (
        <>
          {/* premium data/motion scene stands in for the still */}
          <ArtLayer art={beat.art!} durFrames={durFrames} />
          <Vignette />
          <Grain opacity={0.05} />
        </>
      ) : (
        <>
          {/* optional background plate behind the hero (cinematic depth) */}
          {beat.bg ? (
            (beat.bgKind ?? 'video') === 'video' ? (
              <MovingVideoV src={beat.bg} plate />
            ) : (
              <MovingImageV src={beat.bg} motion="kenburns" />
            )
          ) : null}
          {/* hero */}
          {beat.kind === 'video' && beat.src ? (
            <MovingVideoV src={beat.src} />
          ) : beat.src ? (
            depth ? (
              <DepthImageV src={beat.src} motion={beat.motion} fast={beat.fast} rewind={beat.rewind} />
            ) : (
              <MovingImageV src={beat.src} motion={beat.motion} fast={beat.fast} rewind={beat.rewind} />
            )
          ) : !beat.bg ? (
            <BrandCard />
          ) : null}
          {/* light/particle/vfx decoration (screen-blended) */}
          {beat.overlays?.map((layer, i) => (
            <OverlayLayer key={i} layer={layer} />
          ))}
          {/* procedural ambient motion so no frame is ever static (drifting bokeh + soft glows) */}
          <AmbientMotion count={isCta ? 22 : 15} intensity={beat.fast ? 1.15 : 1} />
          {grade}
          <Vignette />
          <Grain opacity={0.05} />
          {/* overlay art (transparent, e.g. light rays) layers over the still */}
          {beat.art && !sceneArt ? <ArtLayer art={beat.art} durFrames={durFrames} /> : null}
        </>
      )}
      {isCta ? (
        hasFunnelCta(data) ? (
          <CtaFunnelLayer
            thumbSrc={data.ctaLongThumbSrc}
            title={data.ctaLongTitle}
            headline={data.ctaHeadline ?? CTA_HEADLINE_DEFAULT}
            platform={platform}
            fadeOutSec={data.ctaFadeOutSec}
          />
        ) : (
          <CtaLayer text={ctaText} platform={platform} />
        )
      ) : beat.telop ? (
        <TelopTop text={beat.telop} />
      ) : null}
    </AbsoluteFill>
  );
};

/** SHORTS_METHOD persona signature — a fixed wordmark, top-center inside the UI-safe band, on every
 * frame so the channel is instantly recognizable across the muted feed (rule 9b/10). */
const PersonaMark: React.FC = () => (
  <div style={{position: 'absolute', top: 96, left: 0, right: 0, display: 'flex', justifyContent: 'center', pointerEvents: 'none'}}>
    <div
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 12,
        padding: '10px 24px',
        borderRadius: 999,
        background: `${BRAND.color.ink}cc`,
        border: `2px solid ${BRAND.color.gold}`,
        color: BRAND.color.gold,
        fontFamily: BRAND.font.body,
        fontWeight: 800,
        fontSize: 30,
        letterSpacing: 4,
        textShadow: `0 2px 10px ${BRAND.color.ink}`,
      }}
    >
      <span style={{fontSize: 24}}>▶</span> PRIME DOCUMENTARY
    </div>
  </div>
);

/** Word-synced captions. Default = lower band (y1280). METHOD mode raises them into the vertical
 * CENTER-safe band (y1000–1320) so they clear the YouTube/TikTok/Reels bottom title + right
 * action-rail UI (rule 11), with a fixed kinetic pop + gold keyline (reusable persona caption style,
 * rule 10). Strictly below the telop zone either way. */
const CaptionLayer: React.FC<{captions: ShortCaption[] | null; method?: boolean; topOverride?: number}> = ({
  captions,
  method,
  topOverride,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!captions || captions.length === 0) return null;
  const t = frame / fps;
  // Show the single caption phrase active now (1–2 readable lines), exactly matching the narration.
  const cue = captions.find((c) => t >= c.startSec && t < c.endSec);
  const line = cue?.word ?? '';
  if (!line) return null;
  const mostlyAscii = /^[\u0000-\u007f\s.,!?'"-]+$/.test(line);
  const popScale = method
    ? interpolate(
        spring({frame: frame - Math.round((cue?.startSec ?? 0) * fps), fps, config: {damping: 14, stiffness: 200, mass: 0.6}}),
        [0, 1],
        [0.86, 1]
      )
    : 1;
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        // METHOD's default band is y1000-1320, i.e. 52-69% of the frame - dead centre, over the
        // subject. `captionTop` lets one Short drop the band toward the lower third without
        // moving any already-published cut. y1270 + 250 ends at 1520, still clear of the Shorts
        // bottom overlay (measured/estimated at y1500+ for a one-line title).
        top: topOverride ?? (method ? 1000 : 1280),
        height: topOverride ? 220 : method ? 320 : 280,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: method ? '0 110px' : '0 90px',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          color: BRAND.color.white,
          background: `${BRAND.color.ink}${method ? 'c2' : 'a8'}`,
          borderRadius: 16,
          border: method ? `3px solid ${BRAND.color.gold}` : undefined,
          padding: method ? '18px 30px' : '14px 26px',
          fontFamily: BRAND.font.body,
          fontWeight: 800,
          fontSize: method ? (mostlyAscii ? 58 : 66) : mostlyAscii ? 50 : 62,
          lineHeight: mostlyAscii ? 1.12 : 1.18,
          textAlign: 'center',
          maxWidth: '100%',
          transform: `scale(${popScale})`,
          textShadow: `0 3px 12px ${BRAND.color.ink}`,
          letterSpacing: 0,
        }}
      >
        {line}
      </div>
    </div>
  );
};

/** Composites the After Effects overlays over the cut, under the caption band.
 *
 *  `transparent` is not optional: without it Remotion's frame extractor decodes the WebM without
 *  its alpha plane and the overlay arrives as type on a black card that hides the picture. The
 *  alpha itself is verified upstream by render_beats.sh (alpha_mode=1). */
const KineticBeatLayer: React.FC<{beats?: KineticBeat[]}> = ({beats}) => {
  const {fps} = useVideoConfig();
  if (!beats || beats.length === 0) return null;
  return (
    <>
      {beats.map((b, i) => (
        <Sequence
          key={`${b.src}-${i}`}
          from={Math.round(b.atSec * fps)}
          durationInFrames={Math.max(1, Math.round(b.durSec * fps))}
        >
          <AbsoluteFill style={{pointerEvents: 'none'}}>
            <OffthreadVideo src={staticFile(b.src)} transparent muted style={{width: '100%', height: '100%'}} />
          </AbsoluteFill>
        </Sequence>
      ))}
    </>
  );
};

export const Short: React.FC<{data: ShortData; platform: ShortPlatform; depth?: boolean; method?: boolean}> = ({
  data,
  platform,
  depth,
  method,
}) => {
  const {fps} = useVideoConfig();
  // §4-4: the funnel end-card occupies y430–1290, which is exactly where the caption band sits.
  // Any cue inside the CTA beat would cover the long-form title and the pill, so cues in that
  // window are dropped. Only applies to the opt-in funnel CTA — the legacy path keeps every cue.
  const ctaBeat = hasFunnelCta(data) ? data.beats.find((b) => b.id === 'cta') : undefined;
  const captions =
    ctaBeat && data.captions
      ? data.captions.filter((c) => c.startSec < ctaBeat.startSec || c.startSec >= ctaBeat.startSec + ctaBeat.durSec)
      : data.captions;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Series>
        {data.beats.map((beat) => (
          <Series.Sequence key={beat.id} durationInFrames={framesFor(beat.durSec, fps)}>
            <BeatView beat={beat} platform={platform} data={data} depth={depth} />
          </Series.Sequence>
        ))}
      </Series>
      {/* Not on TikTok (2026-08-17). PersonaMark is a wordmark on EVERY frame, and TikTok's
          originality policy says repurposed content carrying a watermark or logo is in most cases
          not treated as original - unoriginal content being made ineligible for the For You feed.
          These files are the same ones published on YouTube, so the mark is the exact signal that
          policy describes, and 159 of the 199 TikTok compositions carry it. YouTube keeps it: the
          persona signature is a deliberate recognition device there (rule 9b/10). */}
      {method && platform !== 'tiktok' ? <PersonaMark /> : null}
      {/* Under the captions on purpose: the type lives at y420–1050 and the band at ~y1305, but if
          a Short ever moves its captions up, the spoken line must still win. */}
      <KineticBeatLayer beats={data.kineticBeats} />
      <CaptionLayer captions={captions} method={method} topOverride={data.captionTop} />
      {data.narrationSrc ? <Audio src={staticFile(data.narrationSrc)} /> : null}
      {data.bgmSrc ? <Audio src={staticFile(data.bgmSrc)} volume={0.16} /> : null}
      {data.ambienceSrc ? <Audio src={staticFile(data.ambienceSrc)} volume={0.06} /> : null}
    </AbsoluteFill>
  );
};

/** Vertical thumbnail (Still): key-visual background + big headline (avoid UI edges). */
export const ShortThumb: React.FC<{
  data: ShortData;
  headline: string;
  backgroundSrc: string | null;
  badge?: string;
  /**
   * 'tt' composes the same design for TikTok, where a cover is judged twice: full 9:16 in the feed,
   * and cropped to the middle 3:4 in the profile grid. The YouTube layout puts the headline high,
   * which in that crop sits against the top edge with two thirds of the tile left black - measured
   * on the live profile on 2026-08-09. This centres the headline and lifts the background so a
   * tile reads as a picture instead of a black square.
   */
  layout?: 'yt' | 'tt';
}> = ({headline, backgroundSrc, badge, layout = 'yt'}) => {
  const tt = layout === 'tt';
  const mostlyAscii = /^[\u0000-\u007f\s.,!?'"-]+$/.test(headline);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {backgroundSrc ? (
        <Img
          src={staticFile(backgroundSrc)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: tt
              ? 'brightness(0.80) contrast(1.10) saturate(1.16)'
              : 'brightness(0.58) contrast(1.06) saturate(1.12)',
          }}
        />
      ) : (
        <BrandCard />
      )}
      {/* Strong darkening so the headline reads instantly; heaviest behind the text band. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: tt
            ? `linear-gradient(180deg, ${BRAND.color.ink}77 0%, ${BRAND.color.ink}33 30%, ${BRAND.color.ink}55 52%, ${BRAND.color.ink}33 74%, ${BRAND.color.ink}99 100%)`
            : `linear-gradient(180deg, ${BRAND.color.ink}ee 0%, ${BRAND.color.ink}99 26%, ${BRAND.color.ink}aa 50%, ${BRAND.color.ink}80 70%, ${BRAND.color.ink}f5 100%)`,
        }}
      />
      {badge ? (
        <div
          style={{
            position: 'absolute',
            // inside TikTok's 3:4 crop (y 240-1680) and clear of the centred headline
            top: tt ? 430 : 98,
            left: 64,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '26px 40px',
            background: '#ef233c',
            border: '10px solid #ffd166',
            boxShadow: `0 20px 54px ${BRAND.color.ink}, 0 0 60px #ef233c88`,
            transform: 'rotate(-6deg)',
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontSize: 74,
            lineHeight: 0.95,
            letterSpacing: 0,
            textShadow: `0 4px 8px ${BRAND.color.ink}`,
            WebkitTextStroke: `2px ${BRAND.color.ink}`,
          }}
        >
          {badge}
        </div>
      ) : null}
      <div
        style={{
          position: 'absolute',
          // TikTok crops the grid tile to the middle 3:4, so the headline is centred on the frame
          // rather than hung from the top.
          ...(tt
            ? {top: 0, bottom: 0, display: 'flex', flexDirection: 'column' as const, justifyContent: 'center'}
            : {top: mostlyAscii ? 300 : 280}),
          left: 40,
          right: 40,
          textAlign: 'center',
          fontFamily: BRAND.font.display,
          fontSize: mostlyAscii ? 172 : 150,
          lineHeight: 1.0,
          letterSpacing: 0,
        }}
      >
        {headline.split('\n').map((line, i) => {
          // Every line is a solid, opaque, high-contrast block so the words read in a glance:
          // alternating dark-with-yellow-border and yellow-with-dark-border. Big, flashy, legible.
          const yellow = i % 2 === 1;
          return (
            <div
              key={i}
              style={{
                display: 'inline-block',
                marginBottom: 24,
                padding: '8px 34px 22px',
                borderRadius: 14,
                background: yellow ? '#ffd60a' : '#0b1220',
                color: yellow ? '#0b1220' : '#ffffff',
                border: yellow ? '8px solid #0b1220' : '8px solid #ffd60a',
                boxShadow: `0 22px 60px ${BRAND.color.ink}, 0 0 0 4px ${BRAND.color.ink}`,
                boxDecorationBreak: 'clone',
              }}
            >
              {line}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
