/**
 * EP36 williams — WilliamsFilm (full-length PREMIUM-ANIMATION composition).
 *
 * Replaces the rejected still-heavy CaseFilm cut. Driven 1:1 by the pre-made beatsheet
 * `episodes/PD-2026-036-williams/04_scenes/premium_beatsheet.v001.json` (128 beats = 122 kinetic
 * + 6 GlitchCut overlays), every beat frame-timed @30fps against the real narration offsets.
 *
 * Each beat becomes a <Sequence from={start_frame} durationInFrames={dur_frames}> wrapping the
 * mapped premium component with the beat's props/treatment. GlitchCut beats overlay at the section
 * boundaries. Video only — narration/music are muxed later (no <Audio> here).
 *
 * Every mapped component keeps its own premium motion (spring, @remotion/motion-blur Trail, mask
 * reveals) — this composition only places and times them.
 *
 * Preview:  cd remotion && npm run studio  → open "WilliamsFilm"
 * Render:   cd remotion && npx remotion render WilliamsFilm out/PD-2026-036-williams.mp4 --gl=angle
 */
import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, spring, interpolate} from 'remotion';
import {BRAND} from '../brand';
import williamsCaptions from '../data/williams_captions.v003.json';
import {BrandOpening, BrandEndcard} from '../components/Bookends';
import {
  WilliamsScene,
  WilliamsFactoryCut,
  FaceMatchGrid,
  BiasBars,
  CaseTimeline,
  LineupLoop,
  DatasetImbalance,
  Treatment,
} from '../components/williams';
import {
  GlitchCut,
  KineticCaptions,
  ActTitle,
  NumberTicker,
  StampReveal,
  PinDropMap,
} from '../components/motionkit';
// eslint-disable-next-line @typescript-eslint/no-var-requires
import beatsheetJson from '../../../episodes/PD-2026-036-williams/04_scenes/premium_beatsheet.v001.json';

// ---------------------------------------------------------------------
// Beatsheet shape (only the fields the composition consumes).
// ---------------------------------------------------------------------
type Beat = {
  beat: number;
  kind: string;
  component: string;
  start_frame: number;
  dur_frames: number;
  silent?: boolean;
  src?: string;
  hero_id?: string;
  treatment?: string;
  accent?: string;
  onscreen?: string[];
  props?: Record<string, unknown>;
};

type Beatsheet = {
  meta: {projected_runtime_frames: number; fps: number; width: number; height: number};
  beats: Beat[];
};

const BEATSHEET = beatsheetJson as unknown as Beatsheet;

// Full runtime is read from the beatsheet meta (do NOT hardcode).
export const williamsFilmDurationInFrames = (): number =>
  BEATSHEET.meta.projected_runtime_frames;

// accent token → hex ('gold' is the only accent used; default = electric cyan).
const accentHex = (accent?: string): string | undefined =>
  accent === 'gold' ? BRAND.color.gold : undefined;

// ---------------------------------------------------------------------
// Signature MGs (FaceMatchGrid/BiasBars/…) and the reused motionkit parts do NOT accept an
// `onScreen` prop — they burn their own grade-A internal labels. When such a beat carries a
// narration caption, we overlay KineticCaptions(maskslide) as a bottom-third sibling (transparent
// overlay) so the on-screen line is present without disturbing the graphic's own timeline.
// ---------------------------------------------------------------------
const MgWithCaption: React.FC<{
  onScreen?: string[];
  dur: number;
  children: React.ReactNode;
}> = ({onScreen, dur, children}) => {
  // 署名MG（FaceMatchGrid/BiasBars/…）は主役がリビール後に着地して静止しがち。
  // グラフィック丸ごとに“ごく緩い連続ブレス”を掛け、hold 区間が near-still に落ちないようにする。
  // （データ・アニメ自体は不変：全体を微小に scale/translate するだけ。位相ずらしで常時 velocity>0。
  //   scale ベースライン 1.008 が translate 端をインセットで隠す＝背景ink露出なし。）
  const frame = useCurrentFrame();
  const t = frame / Math.max(1, dur);
  const bScale = 1.008 + 0.012 * (0.5 - 0.5 * Math.cos(t * Math.PI * 2));
  const bx = Math.sin(t * Math.PI * 1.5 + 0.5) * 5;
  const by = Math.cos(t * Math.PI * 1.3) * 4;
  return (
    <AbsoluteFill style={{transform: `translate(${bx}px, ${by}px) scale(${bScale})`, transformOrigin: '50% 50%'}}>
      {children}
      {onScreen && onScreen.length ? (
        // UPPER THIRD 配置: ボトムの BurnedCaptions（焼き込みナレーション字幕）と衝突させない
        <KineticCaptions lines={onScreen} style="maskslide" dur={dur} anchor="top" />
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// One beat → its mapped premium element. `dur` is always the beat length so each component's
// internal in/out animation aligns to its <Sequence>.
// ---------------------------------------------------------------------
const renderBeat = (b: Beat): React.ReactNode => {
  const dur = b.dur_frames;
  const onScreen = b.onscreen;

  switch (b.component) {
    // Hero still → animated scene (push/parallax/pixel + atmos + maskslide captions).
    case 'WilliamsScene':
      return (
        <WilliamsScene
          src={b.src}
          onScreen={onScreen}
          treatment={(b.treatment as Treatment) ?? 'push'}
          accent={accentHex(b.accent)}
          placeholderLabel={b.hero_id}
          dur={dur}
        />
      );

    // Factory .mp4 → graded, drifting texture cut (+ optional caption).
    case 'FactoryClip':
      return (
        <WilliamsFactoryCut src={b.src} onScreen={onScreen} accent={accentHex(b.accent)} dur={dur} />
      );

    // Section-boundary glitch transitions (transparent overlay).
    case 'GlitchCut':
      return <GlitchCut dur={dur} />;

    // Canonical bookends (props from beat; do NOT fork).
    case 'BrandOpening':
      return (
        <BrandOpening
          seriesLabel={String(b.props?.seriesLabel ?? '')}
          title={String(b.props?.title ?? '')}
          subtitle={b.props?.subtitle ? String(b.props.subtitle) : undefined}
        />
      );
    case 'BrandEndcard':
      return (
        <BrandEndcard
          channel={b.props?.channel ? String(b.props.channel) : undefined}
          ctaLine={b.props?.ctaLine ? String(b.props.ctaLine) : undefined}
          cadenceLine={b.props?.cadenceLine ? String(b.props.cadenceLine) : undefined}
        />
      );

    // Act slam cards.
    case 'ActTitle':
      return (
        <ActTitle
          kicker={b.props?.kicker ? String(b.props.kicker) : undefined}
          title={String(b.props?.title ?? '')}
          dur={dur}
        />
      );

    // Signature motion-graphics (self-contained; caption overlaid when present).
    case 'FaceMatchGrid':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <FaceMatchGrid dur={dur} />
        </MgWithCaption>
      );
    case 'BiasBars':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <BiasBars dur={dur} />
        </MgWithCaption>
      );
    case 'CaseTimeline':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <CaseTimeline dur={dur} />
        </MgWithCaption>
      );
    case 'LineupLoop':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <LineupLoop dur={dur} />
        </MgWithCaption>
      );
    case 'DatasetImbalance':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <DatasetImbalance dur={dur} />
        </MgWithCaption>
      );

    // Reused motionkit parts wired with EP36 grade-A content (matches ep36_motion_preview).
    // NumberTicker30 = "~30 HOURS held" damped count-up (SPN-0004).
    case 'NumberTicker30':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <NumberTicker
            value={30}
            topLabel="HOURS IN A CELL"
            label="No charge. No crime. A face-match was enough."
            dur={dur}
          />
        </MgWithCaption>
      );
    // StampCharges = "CHARGES DROPPED" slam (SPN-0005).
    case 'StampCharges':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <StampReveal text="CHARGES DROPPED" color="#3E8E5A" dur={dur} />
        </MgWithCaption>
      );
    // PinDropMap = "one city · new rules" (SPN-0014).
    case 'PinDropMap':
      return (
        <MgWithCaption onScreen={onScreen} dur={dur}>
          <PinDropMap pins={[{x: 0.72, y: 0.34, label: 'ONE CITY · NEW RULES'}]} dur={dur} />
        </MgWithCaption>
      );

    default:
      // Unknown component: render nothing (keeps timeline intact). None expected — all 14
      // beatsheet component names are mapped above.
      return null;
  }
};

// Burned-in narration captions (PD house style): full spoken line at the bottom, springing up per
// cue so it's never a static block. Sits ABOVE every beat so it stays crisp. Cues are film-timed
// (williams_captions.v003.json, derived from captions.v003.srt on the rebuilt 713s timeline).
type CaptionCue = {start: number; end: number; text: string};

const BurnedCaptions: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  const cue = (williamsCaptions as CaptionCue[]).find((c) => t >= c.start && t < c.end);
  if (!cue) return null;
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
          color: '#ffffff',
          fontFamily: BRAND.font.body,
          fontSize: 44,
          fontWeight: 600,
          lineHeight: 1.25,
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

export const WilliamsFilm: React.FC = () => {
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {BEATSHEET.beats.map((b) => (
        <Sequence
          key={b.beat}
          from={b.start_frame}
          durationInFrames={b.dur_frames}
          name={`${b.beat}·${b.component}${b.hero_id ? `·${b.hero_id}` : ''}`}
        >
          {renderBeat(b)}
        </Sequence>
      ))}
      {/* burned-in narration captions on top of every beat */}
      <BurnedCaptions />
    </AbsoluteFill>
  );
};
