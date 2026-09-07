import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {BRAND} from '../brand';

/**
 * ShortThumbYT — 16:9 (1280x720) CTR thumbnail for a YouTube Short's dedicated custom thumbnail.
 *
 * Brand language ported from the long-form selected thumbnails
 * (episodes/[ep]/09_package/thumbnail.selected*.png): dark cinematic hero, a gold accent badge, a
 * heavy white Anton headline of 2-4 huge words, a gold underline bar, and a small
 * PRIME DOCUMENTARY brand mark. Tuned for true-crime / legal CTR: one focal hero, a curiosity-gap
 * headline, and text that stays legible at 320px on a phone.
 *
 * Pure Still (no animation). Render one per Short by overriding defaultProps with --props JSON.
 */

export type ShortThumbYTProps = {
  /** 2-4 word punchy headline. Use \n to force line breaks. */
  headline: string;
  /** Small case label under the headline (e.g. "TERRY v. OHIO - 1968"). Optional. */
  subhead?: string;
  /** staticFile-relative hero still under remotion/public (e.g. shorts/short20/short20_01.png). */
  heroImage: string | null;
  /** Accent hex for the badge + underline. Default brand gold. */
  accent?: string;
  /** Short badge word/verdict, e.g. "UNSOLVED", "9-0", "2014". Optional. */
  badge?: string;
  /** Vertical focal point of the (portrait) hero, 0..100. Default 26 (upper third). */
  focusY?: number;
};

const isAscii = (s: string): boolean => {
  for (let i = 0; i < s.length; i += 1) {
    if (s.charCodeAt(i) > 127) return false;
  }
  return true;
};

export const ShortThumbYT: React.FC<ShortThumbYTProps> = ({
  headline,
  subhead,
  heroImage,
  accent = BRAND.color.gold,
  badge,
  focusY = 26,
}) => {
  const lines = headline.split('\n');
  const longest = Math.max(...lines.map((l) => l.length), 1);
  // Adaptive headline size: keep the longest line within the left ~62% text column (~760px).
  // Anton glyphs are ~0.52em wide; solve for size so longest*0.52*size <= 760.
  const rawSize = 760 / (longest * 0.52);
  const fontSize = Math.max(78, Math.min(178, rawSize));
  const ascii = isAscii(headline);

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* Hero */}
      {heroImage ? (
        <Img
          src={staticFile(heroImage)}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            objectPosition: `62% ${focusY}%`,
            filter: 'brightness(0.66) contrast(1.08) saturate(1.06)',
          }}
        />
      ) : (
        <AbsoluteFill
          style={{
            background: `radial-gradient(120% 90% at 70% 35%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 80%)`,
          }}
        />
      )}

      {/* Legibility scrim: heavy on the left where the text sits, plus a bottom floor. */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `linear-gradient(100deg, ${BRAND.color.ink}f7 0%, ${BRAND.color.ink}e6 32%, ${BRAND.color.ink}80 58%, ${BRAND.color.ink}22 80%, ${BRAND.color.ink}00 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: `linear-gradient(0deg, ${BRAND.color.ink}f0 0%, ${BRAND.color.ink}55 22%, transparent 46%)`,
        }}
      />
      {/* Cinematic vignette */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          boxShadow: `inset 0 0 260px 70px ${BRAND.color.ink}`,
        }}
      />

      {/* Brand mark - top-left */}
      <div
        style={{
          position: 'absolute',
          top: 40,
          left: 56,
          color: BRAND.color.gold,
          fontFamily: BRAND.font.body,
          fontWeight: 700,
          fontSize: 30,
          letterSpacing: 7,
          textShadow: `0 2px 10px ${BRAND.color.ink}`,
        }}
      >
        PRIME DOCUMENTARY
      </div>

      {/* Accent badge - top-left, under the brand mark */}
      {badge ? (
        <div
          style={{
            position: 'absolute',
            top: 92,
            left: 54,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '10px 26px 12px',
            background: accent,
            color: BRAND.color.ink,
            fontFamily: BRAND.font.number,
            fontSize: 46,
            lineHeight: 1,
            letterSpacing: 2,
            boxShadow: `0 12px 34px ${BRAND.color.ink}cc`,
          }}
        >
          {badge}
        </div>
      ) : null}

      {/* Headline block - lower-left */}
      <div
        style={{
          position: 'absolute',
          left: 56,
          bottom: 96,
          maxWidth: 820,
        }}
      >
        {lines.map((l, i) => (
          <div
            key={i}
            style={{
              color: BRAND.color.white,
              fontFamily: BRAND.font.number,
              fontSize,
              lineHeight: 0.98,
              letterSpacing: ascii ? -1 : 0,
              textTransform: 'uppercase',
              textShadow: `0 4px 22px ${BRAND.color.ink}, 0 0 44px ${BRAND.color.ink}`,
              WebkitTextStroke: `2px ${BRAND.color.ink}`,
            }}
          >
            {l}
          </div>
        ))}
        {/* Gold underline bar */}
        <div
          style={{
            marginTop: 18,
            width: Math.min(520, Math.max(220, longest * fontSize * 0.34)),
            height: 14,
            background: accent,
            boxShadow: `0 6px 20px ${BRAND.color.ink}`,
          }}
        />
        {subhead ? (
          <div
            style={{
              marginTop: 16,
              color: BRAND.color.silver,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 27,
              letterSpacing: 3,
              textTransform: 'uppercase',
              textShadow: `0 2px 10px ${BRAND.color.ink}`,
            }}
          >
            {subhead}
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
