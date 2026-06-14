import React from 'react';
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../brand';
import {MovingStage} from '../components/Motion';
import {Grain} from '../components/Grain';

/**
 * Cold-open hook (owner-approved 2026-06-14): grab in the first 5s, lead with the
 * paradox, end on the title. Built to work *now* with coded moving backgrounds and
 * to upgrade automatically when real B-roll is dropped in (per-beat `broll`).
 * Structure: recognition -> subversion -> the surprise -> the promise.
 */

export type HookLine = {text: string; gold?: boolean; big?: boolean};
export type HookBeat = {
  durationInFrames: number;
  seed: string;
  /** optional B-roll clip in remotion/public; falls back to coded moving art. */
  broll?: string | null;
  lines: HookLine[];
};

export const MIRANDA_HOOK: HookBeat[] = [
  {durationInFrames: 120, seed: 'h1', broll: null, lines: [{text: 'You have the right', big: true}, {text: 'to remain silent.', big: true}]},
  {durationInFrames: 150, seed: 'h2', broll: null, lines: [{text: 'It was not written'}, {text: 'by a screenwriter.', gold: true}]},
  {durationInFrames: 210, seed: 'h3', broll: null, lines: [{text: 'He won at the Supreme Court —'}, {text: 'and still went to prison.', gold: true, big: true}]},
  {durationInFrames: 120, seed: 'h4', broll: null, lines: [{text: 'Four sentences rewrote'}, {text: 'every arrest in America.', gold: true}]},
];

export const hookDurationInFrames = (beats: HookBeat[]): number =>
  beats.reduce((a, b) => a + b.durationInFrames, 0);

const BeatText: React.FC<{lines: HookLine[]}> = ({lines}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: 130}}>
      <div style={{textAlign: 'center'}}>
        {lines.map((l, i) => {
          const enter = spring({frame: f - i * 9, fps, config: {damping: 200}});
          const y = interpolate(enter, [0, 1], [44, 0]);
          return (
            <div
              key={i}
              style={{
                transform: `translateY(${y}px)`,
                opacity: enter,
                color: l.gold ? BRAND.color.gold : BRAND.color.white,
                fontFamily: BRAND.font.display,
                fontWeight: 900,
                fontSize: l.big ? 100 : 66,
                lineHeight: 1.04,
                letterSpacing: -1.5,
                textTransform: 'none',
                textShadow: `0 8px 44px ${BRAND.color.ink}`,
              }}
            >
              {l.text}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/** Soft ink dip in/out so each beat cut is seated. */
const BeatSeat: React.FC<{durationInFrames: number}> = ({durationInFrames}) => {
  const f = useCurrentFrame();
  const o = Math.max(
    interpolate(f, [0, 10], [0.65, 0], {extrapolateRight: 'clamp'}),
    interpolate(f, [durationInFrames - 10, durationInFrames], [0, 0.5], {extrapolateLeft: 'clamp'}),
  );
  return <AbsoluteFill style={{backgroundColor: BRAND.color.ink, opacity: o, pointerEvents: 'none'}} />;
};

export type ColdOpenProps = {beats: HookBeat[]};

export const ColdOpen: React.FC<ColdOpenProps> = ({beats}) => {
  let cursor = 0;
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {beats.map((b, i) => {
        const from = cursor;
        cursor += b.durationInFrames;
        return (
          <Sequence key={i} from={from} durationInFrames={b.durationInFrames} name={`beat-${i + 1}`}>
            {b.broll ? (
              <AbsoluteFill>
                <OffthreadVideo
                  src={staticFile(b.broll)}
                  muted
                  style={{width: '100%', height: '100%', objectFit: 'cover'}}
                />
                {/* darken B-roll so the text reads */}
                <AbsoluteFill style={{background: `${BRAND.color.ink}66`}} />
              </AbsoluteFill>
            ) : (
              <MovingStage seed={b.seed} intensity={0.9} particles={42}>
                <AbsoluteFill
                  style={{
                    background: `radial-gradient(120% 100% at 50% 42%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 86%)`,
                  }}
                />
              </MovingStage>
            )}
            <BeatText lines={b.lines} />
            <BeatSeat durationInFrames={b.durationInFrames} />
          </Sequence>
        );
      })}
      <Grain opacity={0.08} />
    </AbsoluteFill>
  );
};
