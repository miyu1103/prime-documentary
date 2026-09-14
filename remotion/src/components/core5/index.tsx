/**
 * PD Visual System — CORE 5 components (single import point).
 *
 * The ONLY five core visual components (CLAUDE §14 / component-registry.json):
 *   EvidenceReveal · PenaltyVsProperty · CaseJourney · QuoteUnderExamination · VerdictReversal
 * Legacy/alias names resolve here via the registry (DocumentReveal→EvidenceReveal,
 * ComparisonSplit→PenaltyVsProperty, LegalTimeline/CourtHierarchy→CaseJourney,
 * RedactionReveal→EvidenceReveal). DO NOT add a 6th core component without a gap report.
 *
 * Each is a THIN COMPOSITION over the existing MOTIONKIT primitives (no re-implementation,
 * invariant 14). Contract satisfied by every component:
 *  - 16:9 1920x1080 @30fps (reads useVideoConfig; no hardcoded size)
 *  - duration-resilient: everything scales off `dur ?? durationInFrames`
 *  - props drive content / position / intensity; `seed` fixes any variation
 *  - text stays in safe area (motionkit primitives already enforce it)
 *  - NO hardcoded case names — all copy is props
 *  - English is production; `jaNote` carries the JP confirmation string (never rendered)
 *  - `preview` drops the atmosphere bed for low-load studio scrubbing
 *  - word-timestamp sync: place the component inside <Sequence from={wordFrame}> — its
 *    internal beats scale with `dur`, so aligning the mount aligns the reveal.
 */
import React from 'react';
import {AbsoluteFill, Sequence, Img, staticFile, useVideoConfig} from 'remotion';
import {BRAND} from '../../brand';
import {
  ComparisonBars,
  NumberTicker,
  VoteTally,
  StampReveal,
  QuoteCard,
  EvidenceCard,
  RouteMap,
  ProcessSteps,
  YearSweep,
  LowerThird,
  Spotlight,
  HighlightRing,
  SoftGlow,
  VignetteBreath,
} from '../motionkit';

// Reuse the EXACT prop types of composed primitives (guarantees type-safety).
type RoutePins = React.ComponentProps<typeof RouteMap>['pins'];
type Steps = React.ComponentProps<typeof ProcessSteps>['steps'];

/** Shared, seedable atmosphere bed. Dropped in preview mode for low load. */
const Bed: React.FC<{preview?: boolean}> = ({preview}) =>
  preview ? null : (
    <>
      <SoftGlow />
      <VignetteBreath />
    </>
  );

/** Copy that is displayed (English) plus an un-rendered JP confirmation note. */
export interface CoreCommon {
  /** frames; defaults to the full composition/sequence length */
  dur?: number;
  /** deterministic seed for any variation (kept stable across renders) */
  seed?: number;
  /** low-load preview: skip atmosphere bed */
  preview?: boolean;
  /** JP confirmation copy — stored only, never rendered (English is production) */
  jaNote?: string;
  /** gold source/citation strip shown along the bottom safe area */
  sourceLabel?: string;
}

// ────────────────────────────────────────────────────────────────────────────
// 1) EvidenceReveal — verb: Reveal
//    Move the eye from the whole exhibit to its core. Real footage/still + guided
//    spotlight/ring focus regions, or a slam-in exhibit card when no asset.
// ────────────────────────────────────────────────────────────────────────────
export interface EvidenceRevealProps extends CoreCommon {
  /** staticFile path of a real document/photo; if omitted an exhibit card is used */
  asset?: string;
  /** focus regions in 0..1 ratio coords, revealed in order */
  focusRegions?: {cx: number; cy: number; r: number; label?: string}[];
  mode?: 'document' | 'photograph' | 'record' | 'exhibit';
  tag?: string;
  caption?: string;
}
export const EvidenceReveal: React.FC<EvidenceRevealProps> = ({
  asset, focusRegions = [], mode = 'document', tag, caption, sourceLabel, dur, preview,
}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const n = Math.max(focusRegions.length, 1);
  const holdIn = Math.round(total * 0.18);
  const per = Math.floor((total - holdIn) / n);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {asset ? (
        <AbsoluteFill>
          <Img src={staticFile(asset)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </AbsoluteFill>
      ) : (
        <EvidenceCard tag={tag ?? 'EXHIBIT'} caption={caption} dur={total} />
      )}
      {asset && focusRegions.map((f, i) => (
        <Sequence key={i} from={holdIn + i * per} durationInFrames={per} name={`focus-${i}`}>
          <Spotlight cx={f.cx} cy={f.cy} r={f.r} />
          <HighlightRing cx={f.cx} cy={f.cy} r={f.r} label={f.label} />
        </Sequence>
      ))}
      <Bed preview={preview} />
      {sourceLabel ? <LowerThird primary={sourceLabel} secondary={mode.toUpperCase()} /> : null}
    </AbsoluteFill>
  );
};

// ────────────────────────────────────────────────────────────────────────────
// 2) PenaltyVsProperty — verb: Compare
//    Two values on a common axis + the ratio spelled out. Fixes the timbs
//    "$10,000 fine vs ~$42,000 car" near-still shot (P01 finding).
// ────────────────────────────────────────────────────────────────────────────
export interface PenaltyVsPropertyProps extends CoreCommon {
  left: {label: string; value: number};
  right: {label: string; value: number};
  comparisonAxis?: string;
  mode?: 'currency' | 'generic' | 'before_after' | 'ratio';
  currency?: string;
}
export const PenaltyVsProperty: React.FC<PenaltyVsPropertyProps> = ({
  left, right, comparisonAxis, mode = 'currency', currency = '$', sourceLabel, dur, preview,
}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const hi = Math.max(left.value, right.value);
  const lo = Math.min(left.value, right.value) || 1;
  const ratio = hi / lo;
  const barsDur = Math.round(total * 0.62);
  const items = [
    {label: left.label, value: left.value, accent: BRAND.color.electric},
    {label: right.label, value: right.value, accent: BRAND.color.gold},
  ];
  const ratioLabel = comparisonAxis ?? `${ratio.toFixed(1)}× the smaller`;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Sequence durationInFrames={barsDur} name="bars">
        <ComparisonBars items={items} dur={barsDur} />
      </Sequence>
      <Sequence from={barsDur} name="ratio">
        <NumberTicker
          value={mode === 'ratio' ? ratio : hi}
          prefix={mode === 'currency' ? currency : ''}
          decimals={mode === 'ratio' ? 1 : 0}
          suffix={mode === 'ratio' ? '×' : ''}
          topLabel={ratioLabel}
          dur={total - barsDur}
        />
      </Sequence>
      <Bed preview={preview} />
      {sourceLabel ? <LowerThird primary={sourceLabel} /> : null}
    </AbsoluteFill>
  );
};

// ────────────────────────────────────────────────────────────────────────────
// 3) CaseJourney — verb: Trace
//    A path through courts / dates / places, current position kept to one.
// ────────────────────────────────────────────────────────────────────────────
export interface CaseJourneyProps extends CoreCommon {
  mode?: 'timeline' | 'court_hierarchy' | 'map_route' | 'procedural_path';
  stops?: Steps;
  pins?: RoutePins;
  from?: number;
  to?: number;
  label?: string;
}
export const CaseJourney: React.FC<CaseJourneyProps> = ({
  mode = 'procedural_path', stops = [], pins, from, to, label, sourceLabel, dur, preview,
}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {mode === 'map_route' && pins ? (
        <RouteMap pins={pins} dur={total} />
      ) : mode === 'timeline' && from != null && to != null ? (
        <YearSweep from={from} to={to} label={label} dur={total} />
      ) : (
        <ProcessSteps steps={stops} dur={total} />
      )}
      <Bed preview={preview} />
      {sourceLabel ? <LowerThird primary={sourceLabel} secondary={label} /> : null}
    </AbsoluteFill>
  );
};

// ────────────────────────────────────────────────────────────────────────────
// 4) QuoteUnderExamination — verb: Isolate
//    Verbatim quote/testimony with a guided "examination" beat on the key phrase.
// ────────────────────────────────────────────────────────────────────────────
export interface QuoteUnderExaminationProps extends CoreCommon {
  quote: string;
  attribution: string;
  /** center of the phrase to examine, 0..1 ratio (defaults to page center) */
  examineAt?: {cx: number; cy: number; r: number};
}
export const QuoteUnderExamination: React.FC<QuoteUnderExaminationProps> = ({
  quote, attribution, examineAt, sourceLabel, dur, preview,
}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const examStart = Math.round(total * 0.6);
  const ex = examineAt ?? {cx: 0.5, cy: 0.42, r: 0.5};
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <QuoteCard quote={quote} attribution={attribution} dur={total} />
      <Sequence from={examStart} name="examine">
        <Spotlight cx={ex.cx} cy={ex.cy} r={ex.r} dim={0.5} />
      </Sequence>
      <Bed preview={preview} />
      {sourceLabel ? <LowerThird primary={sourceLabel} /> : null}
    </AbsoluteFill>
  );
};

// ────────────────────────────────────────────────────────────────────────────
// 5) VerdictReversal — verb: Overturn
//    Show the vote, then stamp the reversal. Lower court → higher court flip.
// ────────────────────────────────────────────────────────────────────────────
export interface VerdictReversalProps extends CoreCommon {
  vote?: {majority: number; dissent: number};
  fromLabel?: string;
  stampText?: string;
  stampColor?: string;
}
export const VerdictReversal: React.FC<VerdictReversalProps> = ({
  vote = {majority: 9, dissent: 0}, fromLabel, stampText = 'REVERSED', stampColor,
  sourceLabel, dur, preview,
}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const voteDur = Math.round(total * 0.55);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      <Sequence durationInFrames={voteDur} name="vote">
        <VoteTally majority={vote.majority} dissent={vote.dissent} label={fromLabel} dur={voteDur} />
      </Sequence>
      <Sequence from={voteDur} name="stamp">
        <StampReveal text={stampText} color={stampColor} dur={total - voteDur} />
      </Sequence>
      <Bed preview={preview} />
      {sourceLabel ? <LowerThird primary={sourceLabel} /> : null}
    </AbsoluteFill>
  );
};

/** Registry-aligned alias map (mirrors config/pd-visual-system/component-registry.json). */
export const CORE5_ALIASES = {
  DocumentReveal: 'EvidenceReveal',
  RedactionReveal: 'EvidenceReveal',
  ComparisonSplit: 'PenaltyVsProperty',
  LegalTimeline: 'CaseJourney',
  CourtHierarchy: 'CaseJourney',
} as const;
