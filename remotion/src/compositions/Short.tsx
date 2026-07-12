import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
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
};

export type ShortCaption = {word: string; startSec: number; endSec: number};

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
  beats: ShortBeat[];
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
const MovingImageV: React.FC<{src: string; motion: ShortBeat['motion']; fast?: boolean}> = ({
  src,
  motion,
  fast,
}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const ease = {extrapolateRight: 'clamp' as const, easing: Easing.inOut(Easing.cubic)};
  const range: [number, number] =
    motion === 'pushin' ? [1.08, fast ? 1.34 : 1.24] : motion === 'parallax' ? [1.1, 1.22] : [1.08, 1.2];
  const scale = interpolate(f, [0, d], range, ease);
  // continuous multi-axis camera (always moving, direction varies by motion type)
  const dir = motion === 'parallax' ? 1 : motion === 'kenburns' ? -1 : 0.5;
  const driftX = interpolate(f, [0, d], [-30 * dir, 30 * dir], ease);
  const driftY = interpolate(f, [0, d], [30, -30], ease) * (motion === 'pushin' ? 0.4 : 1);
  const rot = interpolate(f, [0, d], [-0.6, 0.6], ease) * (motion === 'parallax' ? 1 : 0.5);
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

const DepthImageV: React.FC<{src: string; motion: ShortBeat['motion']; fast?: boolean}> = ({src, motion, fast}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d, width, height} = useVideoConfig();
  const dir = motion === 'kenburns' ? -1 : 1;
  const dolly = interpolate(f, [0, Math.max(1, d)], [0, 1], {
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
        <Video
          src={staticFile(src)}
          muted
          loop
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

/** Closing CTA endcard (last beat). Platform-specific text; TikTok never names an external site. */
const CtaLayer: React.FC<{text: string}> = ({text}) => {
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
      </div>
    </AbsoluteFill>
  );
};

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
              <DepthImageV src={beat.src} motion={beat.motion} fast={beat.fast} />
            ) : (
              <MovingImageV src={beat.src} motion={beat.motion} fast={beat.fast} />
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
      {isCta ? <CtaLayer text={ctaText} /> : beat.telop ? <TelopTop text={beat.telop} /> : null}
    </AbsoluteFill>
  );
};

/** Bottom-zone captions (y1280–1560), word-synced to narration. Strictly below the telop zone. */
const CaptionLayer: React.FC<{captions: ShortCaption[] | null}> = ({captions}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!captions || captions.length === 0) return null;
  const t = frame / fps;
  // Show the single caption phrase active now (1–2 readable lines), exactly matching the narration.
  const cue = captions.find((c) => t >= c.startSec && t < c.endSec);
  const line = cue?.word ?? '';
  if (!line) return null;
  const mostlyAscii = /^[\u0000-\u007f\s.,!?'"-]+$/.test(line);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: 1280,
        height: 280,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '0 90px',
        pointerEvents: 'none',
      }}
    >
      <div
        style={{
          color: BRAND.color.white,
          background: `${BRAND.color.ink}a8`,
          borderRadius: 14,
          padding: '14px 26px',
          fontFamily: BRAND.font.body,
          fontWeight: 800,
          fontSize: mostlyAscii ? 50 : 62,
          lineHeight: mostlyAscii ? 1.1 : 1.18,
          textAlign: 'center',
          maxWidth: '100%',
          textShadow: `0 3px 12px ${BRAND.color.ink}`,
          letterSpacing: 0,
        }}
      >
        {line}
      </div>
    </div>
  );
};

export const Short: React.FC<{data: ShortData; platform: ShortPlatform; depth?: boolean}> = ({
  data,
  platform,
  depth,
}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Series>
        {data.beats.map((beat) => (
          <Series.Sequence key={beat.id} durationInFrames={framesFor(beat.durSec, fps)}>
            <BeatView beat={beat} platform={platform} data={data} depth={depth} />
          </Series.Sequence>
        ))}
      </Series>
      <CaptionLayer captions={data.captions} />
      {data.narrationSrc ? <Audio src={staticFile(data.narrationSrc)} /> : null}
      {data.bgmSrc ? <Audio src={staticFile(data.bgmSrc)} volume={0.16} /> : null}
      {data.ambienceSrc ? <Audio src={staticFile(data.ambienceSrc)} volume={0.06} /> : null}
    </AbsoluteFill>
  );
};

/** Vertical thumbnail (Still): key-visual background + big headline (avoid UI edges). */
export const ShortThumb: React.FC<{data: ShortData; headline: string; backgroundSrc: string | null; badge?: string}> = ({
  headline,
  backgroundSrc,
  badge,
}) => {
  const mostlyAscii = /^[\u0000-\u007f\s.,!?'"-]+$/.test(headline);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {backgroundSrc ? (
        <Img
          src={staticFile(backgroundSrc)}
          style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(0.58) contrast(1.06) saturate(1.12)'}}
        />
      ) : (
        <BrandCard />
      )}
      {/* Strong darkening so the headline reads instantly; heaviest behind the text band. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `linear-gradient(180deg, ${BRAND.color.ink}ee 0%, ${BRAND.color.ink}99 26%, ${BRAND.color.ink}aa 50%, ${BRAND.color.ink}80 70%, ${BRAND.color.ink}f5 100%)`,
        }}
      />
      {badge ? (
        <div
          style={{
            position: 'absolute',
            top: 98,
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
          top: mostlyAscii ? 300 : 280,
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
