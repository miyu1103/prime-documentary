/**
 * PD Core-5 preview gallery — one composition that scrubs all five core components
 * with demo props. Demo copy lives HERE (not inside the components), proving the
 * components carry no hardcoded case names. Register once in Root as "PDCore5".
 */
import React from 'react';
import {AbsoluteFill, Series, useVideoConfig} from 'remotion';
import {
  EvidenceReveal, PenaltyVsProperty, CaseJourney, QuoteUnderExamination, VerdictReversal,
} from './index';

export const core5PreviewDuration = (fps: number) => Math.round(fps * 3) * 5;

export const PDCore5Preview: React.FC = () => {
  const {fps} = useVideoConfig();
  const seg = Math.round(fps * 3);
  return (
    <AbsoluteFill>
      <Series>
        <Series.Sequence durationInFrames={seg}>
          <PenaltyVsProperty
            left={{label: 'Max fine', value: 10000}}
            right={{label: 'Seized vehicle', value: 42000}}
            mode="currency"
            sourceLabel="Trial record; statutory maximum"
            jaNote="最大罰金1万ドル対 没収された車約4.2万ドル"
            dur={seg}
          />
        </Series.Sequence>
        <Series.Sequence durationInFrames={seg}>
          <EvidenceReveal
            tag="EXHIBIT"
            caption="Vehicle seizure record"
            mode="record"
            sourceLabel="Case docket"
            dur={seg}
          />
        </Series.Sequence>
        <Series.Sequence durationInFrames={seg}>
          <CaseJourney
            mode="procedural_path"
            stops={[
              {title: 'Trial court'},
              {title: 'State appeals'},
              {title: 'State supreme'},
              {title: 'U.S. Supreme'},
            ]}
            sourceLabel="Procedural history"
            dur={seg}
          />
        </Series.Sequence>
        <Series.Sequence durationInFrames={seg}>
          <QuoteUnderExamination
            quote="grossly disproportionate"
            attribution="the Court"
            sourceLabel="Slip opinion"
            dur={seg}
          />
        </Series.Sequence>
        <Series.Sequence durationInFrames={seg}>
          <VerdictReversal
            vote={{majority: 9, dissent: 0}}
            fromLabel="Does the clause bind the states?"
            stampText="REVERSED"
            sourceLabel="Judgment"
            dur={seg}
          />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
