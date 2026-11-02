/**
 * MotionkitReels — three themed mini-films built from MOTIONKIT components with
 * intentional, director-authored props (not random presets). Self-contained.
 */
import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {
  CinematicTitle, ActTitle, NumberTicker, VoteTally, PriceCrashChart, MoneyFlow,
  DonutReveal, PonziCurve, RegionHighlightMap, CorkboardWeb, RecordsScan,
  TerminalType, EvidenceCard, HeadlineStack, YearSweep, StampReveal, QuoteCard,
  FilmGrain, GlitchCut,
} from '../components/motionkit';

type Seg = {C: React.FC<any>; p: Record<string, unknown>; d: number};

const Reel: React.FC<{scenes: Seg[]; punchAfter?: number[]}> = ({scenes, punchAfter = []}) => {
  const {durationInFrames} = useVideoConfig();
  let acc = 0;
  const starts: number[] = [];
  const els = scenes.map((s, i) => {
    const from = acc;
    starts.push(from);
    acc += s.d;
    return (
      <Sequence key={i} from={from} durationInFrames={s.d} name={s.C.name || `s${i}`}>
        <s.C {...s.p} />
      </Sequence>
    );
  });
  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {els}
      {punchAfter.map((sceneIdx, i) => {
        const f = starts[sceneIdx + 1] ?? acc;
        return (
          <Sequence key={`p${i}`} from={f - 7} durationInFrames={14} name={`punch${i}`}>
            <GlitchCut dur={14} />
          </Sequence>
        );
      })}
      <Sequence from={0} durationInFrames={durationInFrames} name="grain">
        <FilmGrain />
      </Sequence>
    </AbsoluteFill>
  );
};

const dur = (scenes: Seg[]): number => scenes.reduce((a, s) => a + s.d, 0);

// ---------------------------------------------------------------- COLLAPSE
const collapse: Seg[] = [
  {C: CinematicTitle, p: {title: 'COLLAPSE', subtitle: 'How sixty-five billion dollars vanished'}, d: 95},
  {C: PriceCrashChart, p: {label: 'DOW JONES', crashLabel: 'BLACK MONDAY'}, d: 100},
  {C: MoneyFlow, p: {nodes: [{x: 0.22, y: 0.36, label: 'INVESTORS'}, {x: 0.5, y: 0.62, label: 'THE FUND'}, {x: 0.8, y: 0.33, label: 'OFFSHORE'}], edges: [{from: 0, to: 1, weight: 2}, {from: 1, to: 2, weight: 2}]}, d: 100},
  {C: PonziCurve, p: {peakLabel: 'Promised 12% a year', collapseLabel: 'The fund was empty'}, d: 95},
  {C: DonutReveal, p: {slices: [{label: 'Paid to early investors', value: 46}, {label: 'Personal luxury', value: 31}, {label: 'Legal & PR', value: 14}, {label: 'Actually invested', value: 9}], centerLabel: 'THE MONEY'}, d: 95},
  {C: NumberTicker, p: {value: 65, prefix: '$', suffix: 'B', topLabel: 'TOTAL INVESTOR LOSSES', label: 'Wiped out in the collapse'}, d: 90},
  {C: StampReveal, p: {text: 'FRAUD'}, d: 80},
];
export const ReelCollapse: React.FC = () => <Reel scenes={collapse} punchAfter={[1, 4]} />;
export const reelCollapseDuration = (): number => dur(collapse);

// ---------------------------------------------------------------- THE VERDICT
const verdict: Seg[] = [
  {C: CinematicTitle, p: {title: 'THE VERDICT', subtitle: 'A nation divided, five to four'}, d: 95},
  {C: ActTitle, p: {kicker: 'The Question', title: 'IS IT LEGAL?', index: 1}, d: 85},
  {C: QuoteCard, p: {quote: 'The right of the people to be secure in their persons shall not be violated.', attribution: 'The Fourth Amendment'}, d: 100},
  {C: RegionHighlightMap, p: {label: 'It depends on your state', pattern: 'varied'}, d: 90},
  {C: VoteTally, p: {majority: 5, dissent: 4, label: 'THE DECIDING VOTE'}, d: 92},
  {C: StampReveal, p: {text: 'OVERRULED', color: '#1F6BFF'}, d: 80},
  {C: CinematicTitle, p: {title: 'PRECEDENT SET', subtitle: 'the law is never settled'}, d: 90},
];
export const ReelVerdict: React.FC = () => <Reel scenes={verdict} punchAfter={[4]} />;
export const reelVerdictDuration = (): number => dur(verdict);

// ---------------------------------------------------------------- COLD CASE
const coldcase: Seg[] = [
  {C: CinematicTitle, p: {title: 'COLD CASE', subtitle: 'Thirty years of silence'}, d: 95},
  {C: YearSweep, p: {from: 1988, to: 2018, label: 'The trail went cold'}, d: 90},
  {C: CorkboardWeb, p: {nodes: [{x: 0.28, y: 0.36, label: 'THE SUSPECT'}, {x: 0.62, y: 0.3, label: 'THE WITNESS'}, {x: 0.5, y: 0.64, label: 'THE BROKER'}], links: [[0, 1], [0, 2], [1, 2]]}, d: 100},
  {C: RecordsScan, p: {highlightIndex: 3}, d: 95},
  {C: TerminalType, p: {lines: ['ACCESSING COLD CASE FILES...', 'CROSS-REFERENCING DNA', 'MATCH FOUND — CASE #4471'], prompt: '> '}, d: 100},
  {C: EvidenceCard, p: {tag: 'EXHIBIT A', caption: 'The letter that reopened the case'}, d: 90},
  {C: HeadlineStack, p: {headlines: ['DECADES-OLD CASE REOPENED', 'NEW EVIDENCE SURFACES', 'ARREST AFTER 30 YEARS']}, d: 95},
];
export const ReelColdCase: React.FC = () => <Reel scenes={coldcase} punchAfter={[2]} />;
export const reelColdCaseDuration = (): number => dur(coldcase);
