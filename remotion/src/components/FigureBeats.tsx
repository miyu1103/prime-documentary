import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {AmbientMotion} from './AmbientMotion';
import {StatCounter, Timeline, BarChart} from './Figures';

/**
 * FigureBeats — the §5.6 "Figures tier": data beats rendered as full-screen ANIMATED figures
 * (StatCounter counts up, Timeline draws L->R, BarChart grows) instead of flat kinetic text.
 * Data-driven from film_data.figures; each figure covers its own span (opaque backdrop) so the
 * footage gives way to a dynamic data-viz moment. Captions still render on top. This is the
 * single biggest "画面が生きる" upgrade — numbers/timeline come alive.
 */
export type FigureSpec =
  | {start: number; end: number; kind: 'stat'; value: number; prefix?: string; suffix?: string; decimals?: number; label: string; topLabel?: string}
  | {start: number; end: number; kind: 'timeline'; events: {year: string; text: string}[]}
  | {start: number; end: number; kind: 'bar'; data: {label: string; value: number}[]};

const Backdrop: React.FC = () => (
  <AbsoluteFill
    style={{background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`}}
  />
);

/** Continuous micro-drift so a figure that has finished counting still MOVES (a held stat is
 * otherwise flagged near-still by animation_density). Slow parallax pan + breathing scale. */
const Drift: React.FC<{children: React.ReactNode}> = ({children}) => {
  const f = useCurrentFrame();
  const {durationInFrames: d} = useVideoConfig();
  const p = interpolate(f, [0, d], [0, 1], {extrapolateRight: 'clamp'});
  const x = Math.sin(p * Math.PI * 2) * 14;
  const y = Math.cos(p * Math.PI * 2) * 9;
  const s = 1.015 + 0.02 * p; // gentle continuous push-in
  return (
    <AbsoluteFill style={{transform: `translate(${x}px, ${y}px) scale(${s})`}}>{children}</AbsoluteFill>
  );
};

export const FigureBeats: React.FC<{beats: FigureSpec[]}> = ({beats}) => {
  const {fps} = useVideoConfig();
  const accent = BRAND.color.gold;
  return (
    <>
      {beats.map((b, i) => {
        const dur = Math.max(1, Math.round((b.end - b.start) * fps));
        return (
          <Sequence key={i} from={Math.round(b.start * fps)} durationInFrames={dur} name={`figure-${i}`}>
            <AbsoluteFill>
              <Backdrop />
              <AmbientMotion count={16} intensity={1.0} />
              <Drift>
                {b.kind === 'stat' && (
                  <StatCounter
                    accent={accent}
                    value={b.value}
                    prefix={b.prefix}
                    suffix={b.suffix}
                    decimals={b.decimals ?? 0}
                    label={b.label}
                    topLabel={b.topLabel}
                    dur={dur}
                  />
                )}
                {b.kind === 'timeline' && <Timeline accent={accent} events={b.events} dur={dur} />}
                {b.kind === 'bar' && <BarChart accent={accent} data={b.data} dur={dur} />}
              </Drift>
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </>
  );
};
