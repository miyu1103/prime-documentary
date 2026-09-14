import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {FIGURE_REGISTRY, HinderLane} from '../components/hinders';
import {BRAND} from '../brand';

/**
 * HindersFigTest — smoke-test harness for the 27 EP35 "hinders" FigureBeats.
 * Each figure plays full-frame for BEAT seconds so a still-render at any beat's mid-point proves
 * the component renders (no runtime error) and its motion reads. Dev/verification only — not shipped.
 * WebGL heroes (F3/F11/F14/F14b/F15) need `--concurrency=4` for a sequence render.
 */
const BEAT = 4; // seconds per figure

// F-order + the lane each beat belongs to (manifest §6: Iowa / Federal / NC).
const ORDER: {id: string; lane: HinderLane}[] = [
  {id: 'F1', lane: 'iowa'},
  {id: 'F2', lane: 'federal'},
  {id: 'F2b', lane: 'federal'},
  {id: 'F3', lane: 'federal'},
  {id: 'F4', lane: 'federal'},
  {id: 'F5', lane: 'iowa'},
  {id: 'F5b', lane: 'federal'},
  {id: 'F6', lane: 'federal'},
  {id: 'F7', lane: 'federal'},
  {id: 'F8', lane: 'federal'},
  {id: 'F9', lane: 'federal'},
  {id: 'F10', lane: 'federal'},
  {id: 'F11', lane: 'federal'},
  {id: 'F12', lane: 'federal'},
  {id: 'F13', lane: 'federal'},
  {id: 'F14', lane: 'nc'},
  {id: 'F14b', lane: 'nc'},
  {id: 'F14c', lane: 'nc'},
  {id: 'F15', lane: 'federal'},
  {id: 'F15b', lane: 'federal'},
  {id: 'F16', lane: 'nc'},
  {id: 'F17', lane: 'federal'},
  {id: 'F17b', lane: 'nc'},
  {id: 'F18', lane: 'federal'},
  {id: 'F19', lane: 'federal'},
  {id: 'F20', lane: 'iowa'},
  {id: 'F21', lane: 'federal'},
];

export const HindersFigTest: React.FC = () => {
  const {fps} = useVideoConfig();
  const d = Math.round(BEAT * fps);
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {ORDER.map(({id, lane}, i) => {
        const Fig = FIGURE_REGISTRY[id];
        return (
          <Sequence key={id} from={i * d} durationInFrames={d} name={`${id}`}>
            <Fig lane={lane} dur={d} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

export const HINDERS_FIG_TEST_FRAMES = 27 * Math.round(BEAT * 60);
