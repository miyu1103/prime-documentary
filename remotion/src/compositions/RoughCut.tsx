import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Img,
  Series,
  Video,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {Grain} from '../components/Grain';
import {Vignette} from '../components/Motion';

/**
 * RoughCut — episode rough-cut assembler (U5). Lays out one shot per script span from a
 * generated data file (scripts/import_to_remotion.py), so the team gets a complete, timed,
 * narrated rough cut for human finish. Design goal: nothing is ever STATIC ('shoboi') —
 * video clips play, and every image gets a Ken-Burns / parallax move. Only rights-cleared
 * ('usable') assets are ever wired in; shots without an asset render a branded motion card
 * (their telop), so the timeline is always complete and Codex can drop assets in later.
 *
 * This is a SKELETON the visual team (Codex) refines; it is not a final render.
 */
export type RoughShot = {
  spanId: string;
  chapterId: string | null;
  seconds: number;
  assetType: 'stock_video' | 'stock_image' | 'ai_image' | 'motion_graphic' | 'archival_pd';
  motion: 'video_native' | 'ken_burns' | 'parallax' | 'graphic_anim' | 'static';
  src: string | null; // staticFile path under remotion/public, or null -> branded card
  clipSeconds?: number; // real length of a video clip (so we slow it to fit instead of looping)
  telop: string[];
  priority: 'A' | 'B' | 'C';
};

export type RoughCutData = {
  episodeId: string;
  title: string;
  fps: number;
  narrationSrc: string | null;
  bgmSrc: string | null;
  shots: RoughShot[];
};

const framesFor = (seconds: number, fps: number): number => Math.max(1, Math.round(seconds * fps));

export const roughCutDurationInFrames = (data: RoughCutData): number =>
  data.shots.reduce((sum, s) => sum + framesFor(s.seconds, data.fps), 0);

const grade = (
  <AbsoluteFill
    style={{
      pointerEvents: 'none',
      background: `linear-gradient(180deg, ${BRAND.color.navy}33 0%, transparent 30%, transparent 60%, ${BRAND.color.ink}AA 100%)`,
    }}
  />
);

/** A moving image: Ken-Burns push-in (and a slight drift for 'parallax'). Never static. */
const MovingImage: React.FC<{src: string; motion: RoughShot['motion']}> = ({src, motion}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scale = interpolate(f, [0, durationInFrames], [1.06, 1.16]);
  const drift = motion === 'parallax' ? interpolate(f, [0, durationInFrames], [-26, 26]) : 0;
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `translateX(${drift}px) scale(${scale})`, transformOrigin: '50% 50%'}}>
        <Img src={staticFile(src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/**
 * A playing video clip with a touch of extra push-in. If we know the clip length, we play it
 * ONCE, slowed (or sped) to fit the shot — smooth, no loop jumps ('trembling'). If the clip is
 * far too short to stretch, we fall back to a gentle loop. Unknown length -> loop.
 */
const MovingVideo: React.FC<{src: string; clipSeconds?: number; shotSeconds: number}> = ({
  src,
  clipSeconds,
  shotSeconds,
}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const scale = interpolate(f, [0, durationInFrames], [1.02, 1.09]);
  const ideal = clipSeconds && clipSeconds > 0 ? clipSeconds / shotSeconds : 1;
  const rate = Math.min(1.5, Math.max(0.2, ideal));
  // Single pass only when the clip (at this rate) actually covers the shot; else loop gently.
  const covers = !!clipSeconds && clipSeconds / rate >= shotSeconds - 0.1;
  return (
    <AbsoluteFill style={{overflow: 'hidden', backgroundColor: BRAND.color.ink}}>
      <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 50%'}}>
        <Video
          src={staticFile(src)}
          muted
          loop={!covers}
          playbackRate={rate}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** Branded motion card for shots with no asset yet (telop over an animated ground). */
const GraphicCard: React.FC<{telop: string[]; placeholder: string}> = ({telop, placeholder}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const drift = interpolate(f, [0, durationInFrames], [-18, 18]);
  const line = telop[0] ?? '';
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(130% 100% at 50% 35%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 82%)`,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <AbsoluteFill style={{transform: `translateX(${drift}px)`, opacity: 0.16, justifyContent: 'center', alignItems: 'center'}}>
        <div style={{width: 980, height: 980, borderRadius: '50%', border: `2px solid ${BRAND.color.electric}`}} />
      </AbsoluteFill>
      {line ? (
        <div
          style={{
            maxWidth: '78%',
            textAlign: 'center',
            color: BRAND.color.white,
            fontFamily: BRAND.font.display,
            fontSize: 72,
            lineHeight: 1.08,
            letterSpacing: -1,
            textShadow: `0 6px 30px ${BRAND.color.ink}`,
          }}
        >
          {line}
        </div>
      ) : null}
      <div
        style={{
          position: 'absolute',
          bottom: 40,
          color: `${BRAND.color.silver}99`,
          fontFamily: BRAND.font.body,
          fontSize: 18,
          letterSpacing: 0.4,
        }}
      >
        {placeholder}
      </div>
    </AbsoluteFill>
  );
};

/** Telop lower-third (gold rule), shown when a moving asset is present. */
const Telop: React.FC<{telop: string[]}> = ({telop}) => {
  const line = telop[0];
  if (!line) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 48,
        bottom: 64,
        maxWidth: '70%',
        color: BRAND.color.white,
        background: `${BRAND.color.ink}99`,
        borderLeft: `4px solid ${BRAND.color.gold}`,
        padding: '10px 18px',
        fontFamily: BRAND.font.body,
        fontWeight: 700,
        fontSize: 34,
        lineHeight: 1.2,
      }}
    >
      {line}
    </div>
  );
};

const Shot: React.FC<{shot: RoughShot}> = ({shot}) => {
  const hasVideo = !!shot.src && shot.assetType === 'stock_video';
  const hasImage = !!shot.src && shot.assetType !== 'stock_video' && shot.assetType !== 'motion_graphic';
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {hasVideo ? (
        <>
          <MovingVideo src={shot.src as string} clipSeconds={shot.clipSeconds} shotSeconds={shot.seconds} />
          {grade}
          <Vignette />
          <Grain opacity={0.05} />
          <Telop telop={shot.telop} />
        </>
      ) : hasImage ? (
        <>
          <MovingImage src={shot.src as string} motion={shot.motion} />
          {grade}
          <Vignette />
          <Grain opacity={0.06} />
          <Telop telop={shot.telop} />
          {shot.assetType === 'ai_image' ? (
            <div
              style={{
                position: 'absolute',
                right: 36,
                top: 28,
                color: `${BRAND.color.silver}AA`,
                fontFamily: BRAND.font.body,
                fontSize: 17,
              }}
            >
              Reconstruction — not authentic footage
            </div>
          ) : null}
        </>
      ) : (
        <GraphicCard
          telop={shot.telop}
          placeholder={
            shot.assetType === 'motion_graphic'
              ? `motion graphic — ${shot.spanId}`
              : `asset pending (${shot.assetType}) — ${shot.spanId}`
          }
        />
      )}
    </AbsoluteFill>
  );
};

export const RoughCut: React.FC<{data: RoughCutData}> = ({data}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Series>
        {data.shots.map((shot) => (
          <Series.Sequence key={shot.spanId} durationInFrames={framesFor(shot.seconds, fps)}>
            <Shot shot={shot} />
          </Series.Sequence>
        ))}
      </Series>
      {data.narrationSrc ? <Audio src={staticFile(data.narrationSrc)} /> : null}
      {data.bgmSrc ? <Audio src={staticFile(data.bgmSrc)} volume={0.16} /> : null}
    </AbsoluteFill>
  );
};
