import React from 'react';
import {Img, staticFile} from 'remotion';

/**
 * LottieMotion — NON-BREAKING PLACEHOLDER (Status: design / assumptions).
 *
 * Renders a Lottie "light motion part" (arrow, line, icon, map pin, UI motion,
 * chapter ornament). Lottie is NOT the main video generator — only accents.
 *
 * IMPORTANT: `@remotion/lottie` is NOT installed yet. To avoid breaking the
 * build, this file imports ONLY existing deps ('react' / 'remotion') and draws
 * a type-safe fallback: if `src` ends with `.json`/`.lottie` we show a labeled
 * placeholder box; if it points to an image (e.g. a `.preview.png`) we show it.
 *
 * Phase 4 (Codex) — swap to real Lottie:
 *   1) cd remotion && npm i @remotion/lottie lottie-web
 *   2) Replace the fallback below with:
 *        import {Lottie} from '@remotion/lottie';
 *        import {useEffect, useState} from 'react';
 *        // fetch JSON once from staticFile(src), then:
 *        // <Lottie animationData={data} loop={loop} playbackRate={speed} style={style} />
 *   3) Implement `tint` via Lottie color-key replacement or a CSS filter, mapped
 *      to BRAND colors (remotion/src/brand.ts).
 *   4) Keep using this component ONLY from MotionDemo. Do NOT edit Root.tsx or
 *      existing compositions here.
 *
 * Props are kept stable so the Phase-4 swap is drop-in.
 */
export type LottieMotionProps = {
  /** Path under remotion/public, e.g. "assets/lottie/LT-0001__arrow_draw.json". */
  src: string;
  /** Loop the animation (used by the real <Lottie> in Phase 4). */
  loop?: boolean;
  /** Playback speed multiplier (used by the real <Lottie> in Phase 4). */
  speed?: number;
  /** Brand tint to recolor a monochrome Lottie (applied for real in Phase 4). */
  tint?: string;
  /** Extra styles for the wrapper. */
  style?: React.CSSProperties;
};

const isImageSrc = (src: string): boolean =>
  /\.(png|jpe?g|gif|webp|svg)$/i.test(src);

export const LottieMotion: React.FC<LottieMotionProps> = ({
  src,
  loop = true,
  speed = 1,
  tint,
  style,
}) => {
  const file = staticFile(src);

  const wrapperStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '100%',
    height: '100%',
    ...style,
  };

  // Fallback A: an actual image (e.g. a preview frame) — render it directly.
  if (isImageSrc(src)) {
    return (
      <div style={wrapperStyle}>
        <Img
          src={file}
          style={{
            maxWidth: '100%',
            maxHeight: '100%',
            // CSS approximation of `tint` until real recoloring lands.
            filter: tint ? 'saturate(0.2)' : undefined,
          }}
        />
      </div>
    );
  }

  // Fallback B: a Lottie JSON/dotLottie — render a type-safe placeholder box.
  // (No @remotion/lottie import here, so the build stays green.)
  return (
    <div style={wrapperStyle}>
      <div
        style={{
          border: `2px dashed ${tint ?? '#1F6BFF'}`,
          borderRadius: 8,
          padding: '12px 16px',
          color: tint ?? '#1F6BFF',
          fontFamily: '"Trebuchet MS", Arial, sans-serif',
          fontSize: 18,
          textAlign: 'center',
          opacity: 0.9,
        }}
      >
        <div style={{fontWeight: 700}}>Lottie placeholder</div>
        <div style={{fontSize: 13, opacity: 0.8, marginTop: 4}}>{src}</div>
        <div style={{fontSize: 12, opacity: 0.6, marginTop: 6}}>
          loop={String(loop)} speed={speed}
        </div>
      </div>
    </div>
  );
};

export default LottieMotion;
