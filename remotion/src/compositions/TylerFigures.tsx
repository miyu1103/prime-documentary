/**
 * TylerFigures — EP33（PD-2026-033-tyler）の新規 bespoke 図5部品の motion-reel。
 * §6.3: 静止コンタクトシートで「紙芝居でない」と宣言してはならない → 各図を実尺で
 * 連続再生し、動きを人間承認できる自己完結プレビュー（外部メディア不要・決定論）。
 * FilmGrain ベッド + ForcefulCut 相当のストレート切替。
 */
import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {FilmGrain} from '../components/motionkit';
import {
  EquityTheftTally,
  GovtArgumentCard,
  HallEquityLadder,
  SplitLadder,
  OralArgQuestionTally,
} from '../components/tyler';

type Seg = {C: React.FC<{dur: number}>; d: number; name: string};

// 各図 ~4秒（fps=30 → 120f）。GovtArgumentCard は崩壊まで見せるため長め。
const segs = (fps: number): Seg[] => [
  {C: EquityTheftTally, d: Math.round(fps * 5.0), name: 'EquityTheftTally'},
  {C: (p) => <GovtArgumentCard dur={p.dur} mode="collapse" />, d: Math.round(fps * 5.5), name: 'GovtArgumentCard'},
  {C: HallEquityLadder, d: Math.round(fps * 4.5), name: 'HallEquityLadder'},
  {C: SplitLadder, d: Math.round(fps * 4.5), name: 'SplitLadder'},
  {C: OralArgQuestionTally, d: Math.round(fps * 5.0), name: 'OralArgQuestionTally'},
];

export const tylerFiguresDurationInFrames = (fps: number): number =>
  segs(fps).reduce((a, s) => a + s.d, 0);

export const TylerFigures: React.FC = () => {
  const {fps} = useVideoConfig();
  const list = segs(fps);
  let at = 0;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {list.map((s, i) => {
        const from = at;
        at += s.d;
        const Comp = s.C;
        return (
          <Sequence key={i} from={from} durationInFrames={s.d} name={s.name}>
            <Comp dur={s.d} />
          </Sequence>
        );
      })}
      <FilmGrain />
    </AbsoluteFill>
  );
};
