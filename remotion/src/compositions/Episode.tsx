import React from 'react';
import {AbsoluteFill, Sequence, useVideoConfig} from 'remotion';
import {BRAND} from '../brand';
import {Opening} from './Opening';

/**
 * 12-minute episode template SKELETON (decisions/0002 §4/§F).
 * Cold-open hook -> opening (thesis) -> 4 chronological acts -> ending.
 * Sections are placeholders for now; real content is driven by `edit_plan`
 * (pd_factory) and the component library (lower-thirds, chapters, diagrams, etc.).
 */
export type EpisodeSection = {
  id: string;
  label: string;
  startSec: number;
  durSec: number;
};

export type EpisodeProps = {
  title: string;
  channelName: string;
  sections: EpisodeSection[];
};

const SectionCard: React.FC<{label: string; title?: string}> = ({label, title}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(120% 90% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 80%)`,
      justifyContent: 'center',
      alignItems: 'center',
      gap: 18,
    }}
  >
    <div
      style={{
        color: BRAND.color.gold,
        fontFamily: BRAND.font.display,
        fontSize: 30,
        letterSpacing: 6,
        textTransform: 'uppercase',
      }}
    >
      {label}
    </div>
    {title ? (
      <div
        style={{
          color: BRAND.color.white,
          fontFamily: BRAND.font.display,
          fontSize: 64,
          maxWidth: '70%',
          textAlign: 'center',
        }}
      >
        {title}
      </div>
    ) : null}
    <div style={{color: BRAND.color.silver, fontFamily: BRAND.font.body, fontSize: 22}}>
      [placeholder — filled from edit_plan]
    </div>
  </AbsoluteFill>
);

export const Episode: React.FC<EpisodeProps> = ({title, channelName, sections}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {sections.map((s) => (
        <Sequence
          key={s.id}
          from={Math.round(s.startSec * fps)}
          durationInFrames={Math.round(s.durSec * fps)}
          name={s.label}
        >
          {s.id === 'opening' ? (
            <Opening channelName={channelName} />
          ) : (
            <SectionCard label={s.label} title={s.id === 'hook' ? title : undefined} />
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

/** Default 12-minute structure (decisions/0002 §4). startSec/durSec in seconds. */
export const TEMPLATE_12MIN: EpisodeSection[] = [
  {id: 'hook', label: 'Hook', startSec: 0, durSec: 30},
  {id: 'opening', label: 'Opening', startSec: 30, durSec: 45},
  {id: 'act1', label: 'Act I — Event', startSec: 75, durSec: 120},
  {id: 'act2', label: 'Act II — Trial', startSec: 195, durSec: 150},
  {id: 'act3', label: 'Act III — Ruling', startSec: 345, durSec: 120},
  {id: 'act4', label: 'Act IV — Impact', startSec: 465, durSec: 165},
  {id: 'ending', label: 'Ending', startSec: 630, durSec: 90},
];
