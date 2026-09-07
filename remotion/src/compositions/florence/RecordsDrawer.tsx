/**
 * RecordsDrawer — an ORIGINAL, Florence-only animation (not a reused template).
 * Story beat: "a database that was never updated — one record that never got
 * deleted." A wall of filing drawers sits in the dark; a diagonal wave sweeps
 * across and every drawer clicks shut to a calm SETTLED / CLEARED silver — except
 * ONE, which refuses and pulses red NOT CLEARED. The others dim away and the
 * single fatal clerical error is left isolated: "one line · never deleted".
 * No real names / numbers (anonymized cabinet codes). Self-contained. 180f = 6s.
 */
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../../brand';
import {FilmGrain, VignetteBreath} from '../../components/motionkit';

const RED = '#C0473E';

const COLS = 6;
const ROWS = 4;
const BAD = 15; // row 2, col 3 — the one line that never got deleted

// anonymized cabinet codes (no PII) — deterministic, no randomness
const CODE = (i: number) => `A-${(i * 37 + 104).toString().padStart(4, '0')}`;

export const recordsDrawerDuration = 180;

export const RecordsDrawer: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // panel boot
  const boot = spring({frame: f, fps, config: {damping: 200}, durationInFrames: 26});
  // gentle always-alive float of the whole cabinet
  const floatY = Math.sin(f / 30) * 4;

  const panelW = width * 0.78;
  const panelH = height * 0.66;
  const left = (width - panelW) / 2;
  const top = (height - panelH) / 2;

  const headH = panelH * 0.14;
  const bodyTop = headH;
  const bodyH = panelH - headH;
  const padX = panelW * 0.03;
  const padY = bodyH * 0.06;
  const gap = panelW * 0.014;
  const cellW = (panelW - padX * 2 - gap * (COLS - 1)) / COLS;
  const cellH = (bodyH - padY * 2 - gap * (ROWS - 1)) / ROWS;

  // wave front position 0..1 (diagonal), eased sweep across the wall
  const wave = interpolate(f, [22, 104], [-0.15, 1.2], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // end-state isolation: everyone but the red drawer dims + desaturates
  const isolate = interpolate(f, [132, 160], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, justifyContent: 'center', alignItems: 'center'}}>
      {/* faint blueprint grid */}
      <AbsoluteFill
        style={{
          opacity: 0.09,
          backgroundImage: `linear-gradient(${BRAND.color.electric}55 1px, transparent 1px), linear-gradient(90deg, ${BRAND.color.electric}55 1px, transparent 1px)`,
          backgroundSize: '54px 54px',
        }}
      />
      {/* deep radial ground light */}
      <AbsoluteFill
        style={{background: `radial-gradient(90% 70% at 50% 46%, ${BRAND.color.navy}CC, transparent 70%)`}}
      />

      {/* cabinet */}
      <div
        style={{
          position: 'absolute',
          left,
          top,
          width: panelW,
          height: panelH,
          transform: `translateY(${(1 - boot) * 34 + floatY}px)`,
          opacity: boot,
          background: `linear-gradient(180deg, ${BRAND.color.navy}F2, ${BRAND.color.ink}F5)`,
          border: `1px solid ${BRAND.color.electric}55`,
          borderRadius: 12,
          boxShadow: `0 26px 90px #000B, 0 0 46px ${BRAND.color.electric}1F`,
          overflow: 'hidden',
        }}
      >
        {/* header */}
        <div
          style={{
            height: headH,
            display: 'flex',
            alignItems: 'center',
            padding: `0 ${padX}px`,
            gap: 16,
            borderBottom: `1px solid ${BRAND.color.electric}44`,
          }}
        >
          <div style={{width: 12, height: 12, borderRadius: '50%', background: BRAND.color.electric, boxShadow: `0 0 12px ${BRAND.color.electric}`}} />
          <div style={{fontFamily: BRAND.font.body, fontWeight: 800, letterSpacing: 3, fontSize: 26, color: BRAND.color.silver}}>
            RECORDS · RECONCILIATION
          </div>
          <div style={{marginLeft: 'auto', fontFamily: BRAND.font.body, fontSize: 20, color: `${BRAND.color.silver}99`}}>
            SWEEP · CLOSE OUT
          </div>
        </div>

        {/* the sweeping wave band (diagonal light front) */}
        <div
          style={{
            position: 'absolute',
            left: -panelW * 0.5,
            top: bodyTop,
            width: panelW * 0.5,
            height: bodyH,
            transform: `translateX(${(wave + 0.35) * panelW * 1.15}px) skewX(-14deg)`,
            background: `linear-gradient(90deg, transparent, ${BRAND.color.electric}33, ${BRAND.color.electric}66, transparent)`,
            opacity: interpolate(f, [22, 40, 96, 112], [0, 0.9, 0.9, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            filter: 'blur(6px)',
            pointerEvents: 'none',
          }}
        />

        {/* drawer wall */}
        {Array.from({length: COLS * ROWS}).map((_, i) => {
          const col = i % COLS;
          const row = Math.floor(i / COLS);
          const x = padX + col * (cellW + gap);
          const y = bodyTop + padY + row * (cellH + gap);

          // diagonal coordinate 0..1 → when the wave reaches this drawer
          const diag = (col / (COLS - 1) + row / (ROWS - 1)) / 2;
          const hit = 24 + diag * 74; // frame the wave passes this drawer

          const isBad = i === BAD;
          // click-shut spring — slight overshoot like a drawer snapping closed
          const click = spring({frame: f - hit, fps, config: {damping: 15, stiffness: 150}, durationInFrames: 26});
          const appear = spring({frame: f - (8 + diag * 8), fps, config: {damping: 200}, durationInFrames: 16});

          // red drawer pulse after the wave finds it
          const pulse = 0.5 + 0.5 * Math.sin((f - hit) / 4.5);

          // settled (good) drawers: push in + go calm silver. bad: stays proud + red.
          const pushIn = isBad ? 0 : click * 4; // px the face recedes when it clicks shut
          const settled = isBad ? 0 : click;

          // isolation dim for the good drawers at the end
          const goodOpacity = appear * (1 - 0.82 * isolate);
          const opacity = isBad ? appear : goodOpacity;

          const ledCalm = BRAND.color.silver;
          const faceBg = isBad
            ? `rgba(192,71,62,${0.10 + 0.26 * click * (0.5 + 0.5 * pulse)})`
            : `linear-gradient(180deg, ${BRAND.color.navy}${settled > 0.5 ? 'D8' : 'F0'}, ${BRAND.color.ink}F0)`;
          const border = isBad
            ? `1px solid rgba(192,71,62,${0.45 + 0.45 * pulse})`
            : `1px solid ${BRAND.color.electric}${settled > 0.5 ? '2A' : '55'}`;

          const status = isBad ? 'NOT CLEARED' : settled > 0.5 ? 'SETTLED' : '· · ·';
          const statusColor = isBad ? RED : settled > 0.5 ? `${BRAND.color.silver}CC` : `${BRAND.color.silver}66`;

          const badGlow = isBad ? 14 + 16 * pulse + 10 * isolate : 0;

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: cellW,
                height: cellH,
                opacity,
                transform: `translateX(${-pushIn}px) scale(${isBad ? 1 + 0.05 * isolate : 1})`,
                background: faceBg,
                border,
                borderRadius: 8,
                boxShadow: isBad
                  ? `0 0 ${badGlow}px ${RED}, inset 0 0 ${8 * click}px rgba(192,71,62,${0.3 * pulse})`
                  : `inset 0 1px 0 ${BRAND.color.electric}14`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                padding: '10px 12px',
                overflow: 'hidden',
              }}
            >
              {/* top: code + LED */}
              <div style={{display: 'flex', alignItems: 'center', gap: 8}}>
                <div
                  style={{
                    width: 9,
                    height: 9,
                    borderRadius: '50%',
                    background: isBad ? RED : settled > 0.5 ? ledCalm : `${BRAND.color.gold}`,
                    boxShadow: isBad ? `0 0 ${6 + 12 * pulse}px ${RED}` : settled > 0.5 ? 'none' : `0 0 8px ${BRAND.color.gold}`,
                    opacity: isBad ? 0.7 + 0.3 * pulse : 1,
                  }}
                />
                <div style={{fontFamily: BRAND.font.body, fontSize: 17, letterSpacing: 1, color: `${BRAND.color.silver}${isBad ? 'FF' : '99'}`}}>
                  {CODE(i)}
                </div>
              </div>
              {/* handle groove */}
              <div
                style={{
                  height: 4,
                  borderRadius: 3,
                  background: isBad
                    ? `linear-gradient(90deg, ${RED}, ${RED}55)`
                    : `linear-gradient(90deg, ${BRAND.color.electric}${settled > 0.5 ? '33' : '77'}, transparent)`,
                }}
              />
              {/* status */}
              <div
                style={{
                  fontFamily: BRAND.font.display,
                  fontSize: isBad ? 20 : 17,
                  letterSpacing: 1,
                  color: statusColor,
                  textShadow: isBad ? `0 0 ${9 * pulse}px ${RED}` : 'none',
                }}
              >
                {status}
              </div>
            </div>
          );
        })}
      </div>

      {/* closing label — masked slide-up, appears once the one line is isolated */}
      <div
        style={{
          position: 'absolute',
          top: top + panelH + height * 0.03,
          left,
          width: panelW,
          textAlign: 'center',
          overflow: 'hidden',
          height: 44,
        }}
      >
        <div
          style={{
            transform: `translateY(${interpolate(f, [142, 168], [44, 0], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px)`,
            opacity: interpolate(f, [142, 162], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            fontFamily: BRAND.font.body,
            fontSize: 26,
            letterSpacing: 2,
            color: `${BRAND.color.silver}DD`,
          }}
        >
          one line{' '}
          <span style={{color: RED, fontWeight: 800}}>·</span> never deleted
        </div>
      </div>

      <VignetteBreath dur={recordsDrawerDuration} />
      <FilmGrain dur={recordsDrawerDuration} />
    </AbsoluteFill>
  );
};
