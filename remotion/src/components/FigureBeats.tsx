import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
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
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </>
  );
};
