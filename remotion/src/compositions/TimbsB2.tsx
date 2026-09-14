/**
 * TimbsB2 — PD Visual System P07 "B2" test-bench = B1 + WhisperX(=faster-whisper) word sync.
 *
 * Same 80.4s window, same narration as B1/baseline_A. Adds a WORD-SYNCED caption
 * band driven by real per-word onsets from faster-whisper
 * (08_edit/whisperx/whisperx_words.v001.json → src/data/timbs_word_timings.ts).
 * Each word appears/highlights on the exact frame it is spoken (onset − lead).
 *
 * B2 layers the word-sync band OVER the unchanged B1 body (DRY; B1's core-5
 * beats + narration audio are reused verbatim).
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {BRAND} from '../brand';
import {TimbsB1, timbsB1DurationInFrames} from './TimbsB1';
import {TIMBS_WORDS_WINDOW, WordTiming} from '../data/timbs_word_timings';

export const timbsB2DurationInFrames = timbsB1DurationInFrames;

const WINDOW_START_SEC = 110.1;      // must match TimbsB1 in-point
const CAPTION_LEAD_SEC = 0.12;       // wav2vec/CTC-style onset-latency correction (repo house value ~0.12-0.30)
const CONTEXT = 6;                    // words shown around the active one

/** Word-synced caption band: highlights the word currently being spoken. */
const WordSyncBand: React.FC<{words: WordTiming[]}> = ({words}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const tAbs = frame / fps + WINDOW_START_SEC + CAPTION_LEAD_SEC; // absolute narration time
  // active word = last word whose onset has passed
  let active = -1;
  for (let i = 0; i < words.length; i++) {
    if (words[i].start <= tAbs) active = i;
    else break;
  }
  if (active < 0) return null;
  const start = Math.max(0, active - CONTEXT);
  const shown = words.slice(start, active + 1);
  return (
    <AbsoluteFill style={{justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 96}}>
      <div style={{
        maxWidth: width * 0.8, display: 'flex', flexWrap: 'wrap', gap: '0 14px',
        justifyContent: 'center', padding: '14px 26px', borderRadius: 10,
        background: 'rgba(6,10,18,0.62)', boxShadow: '0 6px 30px rgba(0,0,0,0.5)',
      }}>
        {shown.map((w, i) => {
          const isActive = start + i === active;
          const pop = isActive ? interpolate(frame % 3, [0, 2], [1.0, 1.06]) : 1;
          return (
            <span key={start + i} style={{
              fontFamily: BRAND.font.body, fontWeight: 800,
              fontSize: 52, lineHeight: 1.15,
              color: isActive ? BRAND.color.gold : BRAND.color.white,
              opacity: isActive ? 1 : 0.62,
              transform: `scale(${pop})`, transition: 'none',
              textShadow: '0 3px 12px #000',
            }}>{w.word}</span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

export const TimbsB2: React.FC = () => (
  <AbsoluteFill>
    <TimbsB1 />
    <WordSyncBand words={TIMBS_WORDS_WINDOW} />
  </AbsoluteFill>
);
