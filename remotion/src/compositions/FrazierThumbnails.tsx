import React from 'react';
import {AbsoluteFill} from 'remotion';

export type FrazierThumbnailConcept = {
  id: '01' | '02' | '03';
  headline: string;
  accent: string;
};

export const FRAZIER_THUMBS: FrazierThumbnailConcept[] = [
  {id: '01', headline: 'POLICE\nCAN LIE', accent: '#E5B53A'},
  {id: '02', headline: "I DIDN'T\nDO IT", accent: '#E5B53A'},
  {id: '03', headline: 'NO ONE\nCOMING', accent: '#1F6BFF'},
];

const Headline: React.FC<{concept: FrazierThumbnailConcept}> = ({concept}) => (
  <div
    style={{
      position: 'absolute',
      left: 58,
      bottom: 40,
      whiteSpace: 'pre-line',
      fontFamily: '"Anton", "Oswald", Impact, sans-serif',
      fontSize: 126,
      fontWeight: 900,
      lineHeight: 0.86,
      letterSpacing: 0,
      color: '#F5F7FA',
      textShadow: '0 7px 0 #030408, 0 0 22px #000000',
    }}
  >
    {concept.headline}
    <div style={{width: 360, height: 10, marginTop: 18, background: concept.accent, boxShadow: `0 0 24px ${concept.accent}`}} />
  </div>
);

const PaperLie: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(circle at 76% 28%, #17304e 0%, #0B1A2B 38%, #030609 90%)'}}>
    <div style={{position: 'absolute', right: 42, top: 76, width: 710, height: 430, transform: 'rotate(-4deg)', background: '#eef0ea', boxShadow: '0 30px 70px #000b'}}>
      {Array.from({length: 8}).map((_, i) => (
        <div key={i} style={{height: 8, width: i % 3 === 0 ? '58%' : '78%', margin: '25px 55px 0', background: '#98a0a7'}} />
      ))}
      <div style={{position: 'absolute', left: 130, top: 130, padding: '12px 26px', border: '14px solid #981b1f', color: '#981b1f', fontFamily: 'Anton, Impact, sans-serif', fontSize: 96, fontWeight: 900, transform: 'rotate(-9deg)', lineHeight: 1}}>
        FAKE
      </div>
    </div>
    <div style={{position: 'absolute', right: 560, top: -70, width: 290, height: 620, borderRadius: '48% 52% 38% 42%', transform: 'rotate(24deg)', background: 'linear-gradient(120deg, #dbc0aa, #8c6652 66%, #4b3029)', boxShadow: '0 25px 70px #000a'}} />
    <div style={{position: 'absolute', right: 472, top: 250, width: 420, height: 150, borderRadius: 75, transform: 'rotate(8deg)', background: 'linear-gradient(180deg, #d8baa5, #805b49)', boxShadow: '0 22px 45px #0008'}} />
  </AbsoluteFill>
);

const BrokenStatement: React.FC = () => (
  <AbsoluteFill style={{background: 'radial-gradient(circle at 70% 42%, #18345a 0%, #0B1A2B 45%, #020407 100%)'}}>
    <div style={{position: 'absolute', right: 70, top: 84, width: 650, height: 320, borderRadius: 30, background: '#f5f7fa', boxShadow: '0 25px 70px #000b'}}>
      <div style={{position: 'absolute', left: -56, bottom: 56, width: 120, height: 120, background: '#f5f7fa', transform: 'rotate(45deg)'}} />
      <div style={{display: 'flex', width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center', fontFamily: 'Anton, Impact, sans-serif', fontSize: 108, fontWeight: 900, color: '#111820'}}>
        I DID IT
      </div>
      <div style={{position: 'absolute', left: 40, right: 40, top: 150, height: 12, background: '#E5B53A', transform: 'rotate(-8deg)', boxShadow: '0 0 20px #E5B53A'}} />
      <div style={{position: 'absolute', left: 304, top: 100, width: 28, height: 118, background: '#0B1A2B', transform: 'rotate(24deg)'}} />
    </div>
    <div style={{position: 'absolute', right: 315, bottom: -220, width: 520, height: 430, borderRadius: '50% 50% 40% 40%', background: 'linear-gradient(160deg, #d8b39c, #855847 58%, #2a1718)', boxShadow: '0 -10px 55px #0008'}} />
    <div style={{position: 'absolute', right: 455, bottom: 92, width: 250, height: 28, borderRadius: 20, background: '#402326'}} />
  </AbsoluteFill>
);

const ClockDoor: React.FC = () => (
  <AbsoluteFill style={{background: 'linear-gradient(90deg, #020407 0%, #09121d 48%, #111820 100%)'}}>
    <div style={{position: 'absolute', left: 42, top: 44, width: 510, height: 510, borderRadius: '50%', border: '18px solid #1F6BFF', boxShadow: '0 0 42px #1F6BFFaa, inset 0 0 35px #1F6BFFaa', background: '#07101acc'}}>
      {Array.from({length: 12}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 238, top: 24, width: 10, height: 46, background: '#C8CDD6', transformOrigin: '5px 231px', transform: `rotate(${i * 30}deg)`}} />
      ))}
      <div style={{position: 'absolute', left: 243, top: 110, width: 12, height: 165, background: '#F5F7FA', transformOrigin: '6px 145px', transform: 'rotate(56deg)'}} />
      <div style={{position: 'absolute', left: 244, top: 156, width: 10, height: 120, background: '#E5B53A', transformOrigin: '5px 98px', transform: 'rotate(188deg)'}} />
      <div style={{position: 'absolute', left: 228, top: 228, width: 36, height: 36, borderRadius: '50%', background: '#F5F7FA'}} />
    </div>
    <div style={{position: 'absolute', right: 36, top: 32, width: 520, height: 640, border: '18px solid #76818d', background: 'linear-gradient(115deg, #252d34, #0d1217 58%, #27313b)', boxShadow: '-25px 0 50px #000c'}}>
      <div style={{position: 'absolute', inset: '70px 72px 280px', background: '#0a1118', border: '8px solid #56616b', boxShadow: 'inset 0 0 30px #1F6BFF55'}} />
      <div style={{position: 'absolute', left: 145, top: 170, width: 190, height: 250, borderRadius: '50% 50% 20% 20%', background: '#020305', filter: 'blur(5px)'}} />
      <div style={{position: 'absolute', right: 34, top: 330, width: 38, height: 38, borderRadius: '50%', background: '#C8CDD6'}} />
    </div>
    <div style={{position: 'absolute', left: 620, top: 0, width: 18, height: 720, background: '#F5F7FA', boxShadow: '0 0 38px #1F6BFF'}} />
  </AbsoluteFill>
);

export const FrazierThumbnail: React.FC<{concept: FrazierThumbnailConcept}> = ({concept}) => (
  <AbsoluteFill style={{overflow: 'hidden'}}>
    {concept.id === '01' ? <PaperLie /> : null}
    {concept.id === '02' ? <BrokenStatement /> : null}
    {concept.id === '03' ? <ClockDoor /> : null}
    <AbsoluteFill style={{background: 'linear-gradient(90deg, #000000d8 0%, #00000066 46%, transparent 75%)'}} />
    <Headline concept={concept} />
  </AbsoluteFill>
);
