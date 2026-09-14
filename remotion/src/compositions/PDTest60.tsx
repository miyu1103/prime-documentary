/**
 * PDTest60 — a 60-second end-to-end demo of the PD Visual System pipeline.
 * Theme: "Excessive Fines — a 60-second explainer" (general civics; the 8th
 * Amendment's excessive-fines clause is public fact; the dollar figures are
 * labelled ILLUSTRATIVE, no claim about any real case). Exercises all five core
 * components + kinetic captions + cinematic finishing. Music/VO can be layered
 * later; this test is visual-first. 1800f @30fps = 60s.
 */
import React from 'react';
import {AbsoluteFill, Series} from 'remotion';
import {BRAND} from '../brand';
import {
  EvidenceReveal, PenaltyVsProperty, CaseJourney, QuoteUnderExamination, VerdictReversal,
} from '../components/core5';
import {CinematicTitle, KineticCaptions, FilmGrain, VignetteBreath} from '../components/motionkit';

export const pdTest60Duration = 1800;

const Cap: React.FC<{lines: string[]; emph?: string[]}> = ({lines, emph = []}) => (
  <KineticCaptions lines={lines} style="maskslide" emphasisWords={emph} anchor="bottom" />
);

export const PDTest60: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
    <Series>
      {/* 1 — hero title */}
      <Series.Sequence durationInFrames={165}>
        <CinematicTitle title="EXCESSIVE FINES" subtitle="a 60-second explainer" />
      </Series.Sequence>

      {/* 2 — the constitutional rule (verbatim, public) */}
      <Series.Sequence durationInFrames={300}>
        <AbsoluteFill>
          <QuoteUnderExamination
            quote="nor excessive fines imposed"
            attribution="Eighth Amendment, 1791"
            sourceLabel="U.S. Constitution"
            dur={300}
          />
          <Cap lines={['One line. Written in 1791.']} emph={['1791']} />
        </AbsoluteFill>
      </Series.Sequence>

      {/* 3 — why it matters: fine vs. what can be taken (ILLUSTRATIVE) */}
      <Series.Sequence durationInFrames={330}>
        <AbsoluteFill>
          <PenaltyVsProperty
            left={{label: 'A typical fine', value: 500}}
            right={{label: 'Property taken', value: 50000}}
            mode="currency"
            sourceLabel="Illustrative example — not a specific case"
            dur={330}
          />
          <Cap lines={['A small fine.', 'A far bigger seizure.']} emph={['bigger']} />
        </AbsoluteFill>
      </Series.Sequence>

      {/* 4 — how the limit reaches you */}
      <Series.Sequence durationInFrames={330}>
        <AbsoluteFill>
          <CaseJourney
            mode="procedural_path"
            stops={[
              {title: 'Local court'},
              {title: 'State appeals'},
              {title: 'State supreme'},
              {title: 'U.S. Supreme'},
            ]}
            sourceLabel="How a limit reaches every state"
            dur={330}
          />
          <Cap lines={['It climbs every court', 'until it binds all of them.']} emph={['every', 'all']} />
        </AbsoluteFill>
      </Series.Sequence>

      {/* 5 — the source document */}
      <Series.Sequence durationInFrames={300}>
        <AbsoluteFill>
          <EvidenceReveal
            tag="BILL OF RIGHTS"
            caption="Ratified 1791 — ten limits on power"
            mode="record"
            sourceLabel="The Bill of Rights"
            dur={300}
          />
          <Cap lines={['Ten amendments.', 'Ten limits on power.']} emph={['Ten', 'limits']} />
        </AbsoluteFill>
      </Series.Sequence>

      {/* 6 — the point */}
      <Series.Sequence durationInFrames={225}>
        <AbsoluteFill>
          <VerdictReversal
            vote={{majority: 9, dissent: 0}}
            fromLabel="Does it bind the states?"
            stampText="A LIMIT"
            sourceLabel="A check on government power"
            dur={225}
          />
          <Cap lines={['A limit is only as strong', 'as who can use it.']} emph={['strong']} />
        </AbsoluteFill>
      </Series.Sequence>

      {/* 7 — outro */}
      <Series.Sequence durationInFrames={150}>
        <CinematicTitle title="PRIME DOCUMENTARY" subtitle="the line the Constitution draws" />
      </Series.Sequence>
    </Series>

    {/* cinematic finishing bed over everything */}
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at 50% 34%, ${BRAND.color.gold}0E 0%, transparent 44%),
                    linear-gradient(180deg, ${BRAND.color.navy}22 0%, transparent 30%, ${BRAND.color.ink}30 100%)`,
        mixBlendMode: 'soft-light', pointerEvents: 'none',
      }}
    />
    <VignetteBreath />
    <FilmGrain />
  </AbsoluteFill>
);
