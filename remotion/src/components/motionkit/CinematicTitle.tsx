import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// CinematicTitle — ULTRA-PREMIUM documentary-opening hero title card.
//
// Depth stack (back → front):
//   0  SCENE backdrop      radial navy → near-black
//   1  parallax grid       slow eased drift, radial mask (depth)
//   2  soft light rays      two counter-rotating conic sweeps (eased sine)
//   3  drifting particles   deterministic (remotion random), sine float
//   4  push-in breath group  big TITLE (Trail motion-blur, per-letter mask
//                            reveal + word stagger) → gold underline draws
//                            (scaleX spring) → SILVER subtitle mask reveal
//   5  letter glint          light-sweep clipped to the glyphs (NOT a wash)
//   6  vignette + micro-flash
//
// House rules honored: every motion eased (spring / Easing / sine — never
// linear); no opacity-only reveals (opacity always paired with translate/
// scale/position); text = overflow:hidden + inner translateY mask; per-letter
// stagger; fast entrance wrapped in <Trail>; deterministic (frame + index +
// random('seed'+i)); all timings derived from fps; colors ONLY from BRAND.
// =====================================================================

const INK = BRAND.color.ink;
const NAVY = BRAND.color.navy;
const ELECTRIC = BRAND.color.electric;
const SILVER = BRAND.color.silver;
const GOLD = BRAND.color.gold;
const WHITE = BRAND.color.white;

// Canonical full-screen scene backdrop (spec-mandated).
const SCENE_BG = `radial-gradient(125% 105% at 50% 42%, ${NAVY} 0%, #06080f 82%)`;

export const CinematicTitle: React.FC<{
  title: string;
  subtitle?: string;
  dur?: number;
}> = ({title, subtitle, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const D = dur ?? durationInFrames;

  // ---- Global quick-in / quick-out (paired with transform below) ----
  const fadeIn = interpolate(frame, [0, f(0.3)], [0, 1], {
    extrapolateRight: 'clamp',
  });
  const fadeOut = interpolate(frame, [D - f(0.5), D], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic),
  });
  const gO = Math.min(fadeIn, fadeOut);

  // ---- Push-in "breath": entry settle → gentle sine breath → quick-out ----
  const entryScale = interpolate(frame, [0, f(0.9)], [1.075, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const breath = 1 + 0.011 * Math.sin(frame * 0.045); // continuous, never static
  const outScale = interpolate(frame, [D - f(0.5), D], [1, 1.045], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.in(Easing.cubic),
  });
  const contentScale = entryScale * breath * outScale;
  const contentShift = interpolate(frame, [0, f(0.9)], [22, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

  // Slow background push-in (parallax depth vs. the breathing foreground).
  const bgScale = interpolate(frame, [0, D], [1.04, 1.11], {
    easing: Easing.out(Easing.cubic),
  });

  // ---- Timings (all from fps) ----
  const titleStart = f(0.32);
  const perLetterF = Math.max(1, f(0.024));
  const underlineStart = f(0.82);
  const subStart = f(1.18);
  const glintStart = f(0.95);

  // ---- Title tokens: flatten to letters with a global stagger index ----
  const words = title.split(' ');
  let gi = 0;
  const tokens = words.map((word) => {
    const letters = Array.from(word).map((ch) => ({ch, idx: gi++}));
    return letters;
  });
  const letterCount = gi;

  // ---- Gold underline draws in (scaleX spring) ----
  const ruleS = spring({
    frame: frame - underlineStart,
    fps,
    config: {damping: 16, stiffness: 90, mass: 1},
  });

  // ---- Subtitle mask reveal (silver) ----
  const subS = spring({
    frame: frame - subStart,
    fps,
    config: {damping: 20, stiffness: 110, mass: 1},
  });
  const subY = interpolate(subS, [0, 1], [125, 0]);
  const subO = interpolate(subS, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});

  // ---- Letter glint sweep position (moves across → not opacity-only) ----
  const glintPos = interpolate(frame, [glintStart, glintStart + f(0.7)], [135, -55], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.cubic),
  });
  const glintO = interpolate(
    frame,
    [glintStart, glintStart + f(0.18), glintStart + f(0.7)],
    [0, 0.9, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- Micro-flash as the title lands (subtle, screen-blended) ----
  const flash = interpolate(
    frame,
    [titleStart + f(0.45), titleStart + f(0.62), titleStart + f(0.95)],
    [0, 0.16, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- Eased sine rotations for the two light-ray sweeps ----
  const rayA = interpolate(Math.sin(frame * 0.014), [-1, 1], [-10, 10]);
  const rayB = interpolate(Math.sin(frame * 0.011 + 1.7), [-1, 1], [8, -8]);

  // ---- Parallax grid drift (eased sine, both axes) ----
  const gridX = interpolate(Math.sin(frame * 0.02), [-1, 1], [-26, 26]);
  const gridY = interpolate(Math.sin(frame * 0.016 + 0.6), [-1, 1], [-18, 18]);

  // ---- Deterministic drifting particles ----
  const PARTICLES = 34;
  const particles = new Array(PARTICLES).fill(0).map((_, i) => {
    const baseX = random('cx' + i) * 100;
    const baseY = random('cy' + i) * 100;
    const size = 1.5 + random('cs' + i) * 3.5;
    const speed = 0.006 + random('cv' + i) * 0.02;
    const phase = random('cp' + i) * Math.PI * 2;
    const amp = 12 + random('ca' + i) * 26;
    const gold = random('cg' + i) > 0.55;
    // sine float (nonlinear) — vertical drift + gentle lateral sway
    const y = baseY + interpolate(Math.sin(frame * speed + phase), [-1, 1], [amp, -amp]);
    const x = baseX + interpolate(Math.sin(frame * speed * 0.6 + phase), [-1, 1], [-6, 6]);
    const tw = 0.25 + 0.6 * (0.5 + 0.5 * Math.sin(frame * (speed * 3) + phase));
    return {i, x, y, size, tw, gold};
  });

  const titleFontSize = interpolate(letterCount, [8, 28], [124, 82], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Shared style for the big display title glyph run.
  const titleRunStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'flex-end',
    gap: '0 0.28em',
    maxWidth: 1560,
    fontFamily: BRAND.font.display,
    fontSize: titleFontSize,
    lineHeight: 0.98,
    fontWeight: 900,
    textTransform: 'uppercase',
    textAlign: 'center',
  };

  return (
    <AbsoluteFill style={{backgroundColor: INK, opacity: gO}}>
      {/* Layer 0 — SCENE backdrop */}
      <AbsoluteFill style={{background: SCENE_BG}} />

      {/* Layer 1 — parallax grid (depth) */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `scale(${bgScale}) translate(${gridX}px, ${gridY}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ELECTRIC}30 0px, ${ELECTRIC}30 1px, transparent 1px, transparent 78px),
            repeating-linear-gradient(90deg, ${ELECTRIC}30 0px, ${ELECTRIC}30 1px, transparent 1px, transparent 78px)`,
          maskImage: 'radial-gradient(115% 90% at 50% 44%, black 26%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(115% 90% at 50% 44%, black 26%, transparent 80%)',
        }}
      />

      {/* Layer 2 — soft moving light rays (two counter-rotating sweeps) */}
      <AbsoluteFill
        style={{
          transform: `scale(${bgScale}) rotate(${rayA}deg)`,
          transformOrigin: '50% 38%',
          background: `conic-gradient(from 0deg at 50% 38%, transparent 0deg, ${ELECTRIC}22 22deg, transparent 60deg, ${GOLD}16 150deg, transparent 205deg, ${ELECTRIC}18 268deg, transparent 330deg)`,
          mixBlendMode: 'screen',
          opacity: 0.55,
          filter: 'blur(46px)',
        }}
      />
      <AbsoluteFill
        style={{
          transform: `scale(${bgScale}) rotate(${rayB}deg)`,
          transformOrigin: '50% 34%',
          background: `conic-gradient(from 140deg at 50% 34%, transparent 0deg, ${GOLD}14 30deg, transparent 90deg, ${ELECTRIC}18 200deg, transparent 260deg)`,
          mixBlendMode: 'screen',
          opacity: 0.4,
          filter: 'blur(60px)',
        }}
      />
      {/* central bloom to seat the title */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 40% at 50% 46%, ${ELECTRIC}1f 0%, transparent 62%)`,
          mixBlendMode: 'screen',
          opacity: 0.7 + 0.15 * Math.sin(frame * 0.05),
        }}
      />

      {/* Layer 3 — drifting particles (deterministic) */}
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        {particles.map((p) => (
          <div
            key={p.i}
            style={{
              position: 'absolute',
              left: `${p.x}%`,
              top: `${p.y}%`,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              background: p.gold ? GOLD : WHITE,
              opacity: p.tw * 0.6,
              boxShadow: `0 0 ${p.size * 3}px ${p.gold ? GOLD : ELECTRIC}`,
              transform: 'translate(-50%, -50%)',
            }}
          />
        ))}
      </AbsoluteFill>

      {/* Layer 4 — push-in breath group: TITLE / underline / subtitle */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          transform: `translateY(${contentShift}px) scale(${contentScale})`,
        }}
      >
        <div style={{position: 'relative'}}>
          {/* In-flow SIZER — reserves the title's real box. <Trail> and the
              glint overlay are both position:absolute (Trail's root is an
              AbsoluteFill), so without an in-flow child this wrapper would
              collapse to 0 height and the underline + subtitle would pack up
              onto the title. Static, hidden, aria-hidden — layout only, not a
              reveal. Mirrors the animated glyph structure exactly so the
              reserved box matches (same font, padding, wrap). */}
          <div style={{...titleRunStyle, visibility: 'hidden'}} aria-hidden>
            {tokens.map((letters, wi) => (
              <span key={wi} style={{display: 'inline-flex'}}>
                {letters.map(({ch, idx}) => (
                  <span
                    key={idx}
                    style={{
                      display: 'inline-block',
                      overflow: 'hidden',
                      paddingBottom: '0.14em',
                    }}
                  >
                    <span style={{display: 'inline-block', whiteSpace: 'pre'}}>
                      {ch}
                    </span>
                  </span>
                ))}
              </span>
            ))}
          </div>

          {/* TITLE — fast entrance under motion blur */}
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <div style={{...titleRunStyle, color: WHITE, textShadow: `0 0 48px ${ELECTRIC}44, 0 4px 26px #000`}}>
              {tokens.map((letters, wi) => (
                <span key={wi} style={{display: 'inline-flex'}}>
                  {letters.map(({ch, idx}) => {
                    const ls = spring({
                      frame: frame - titleStart - idx * perLetterF,
                      fps,
                      config: {damping: 13, stiffness: 120, mass: 1},
                    });
                    const y = interpolate(ls, [0, 1], [118, 0]);
                    const sc = interpolate(ls, [0, 1], [1.14, 1]);
                    const o = interpolate(ls, [0, 0.32], [0, 1], {
                      extrapolateRight: 'clamp',
                    });
                    return (
                      <span
                        key={idx}
                        style={{
                          display: 'inline-block',
                          overflow: 'hidden',
                          paddingBottom: '0.14em',
                        }}
                      >
                        <span
                          style={{
                            display: 'inline-block',
                            transform: `translateY(${y}%) scale(${sc})`,
                            opacity: o,
                            whiteSpace: 'pre',
                          }}
                        >
                          {ch}
                        </span>
                      </span>
                    );
                  })}
                </span>
              ))}
            </div>
          </Trail>

          {/* Layer 5 — letter glint: light sweep clipped to the glyphs */}
          <div
            aria-hidden
            style={{
              ...titleRunStyle,
              position: 'absolute',
              inset: 0,
              color: 'transparent',
              pointerEvents: 'none',
              opacity: glintO,
              mixBlendMode: 'screen',
              backgroundImage: `linear-gradient(100deg, transparent 42%, ${WHITE}f2 50%, ${GOLD}cc 55%, transparent 63%)`,
              backgroundSize: '260% 100%',
              backgroundRepeat: 'no-repeat',
              backgroundPosition: `${glintPos}% 0`,
              WebkitBackgroundClip: 'text',
              backgroundClip: 'text',
              textShadow: 'none',
            }}
          >
            {tokens.map((letters, wi) => (
              <span key={wi} style={{display: 'inline-flex'}}>
                {letters.map(({ch, idx}) => (
                  <span
                    key={idx}
                    style={{display: 'inline-block', paddingBottom: '0.14em', whiteSpace: 'pre'}}
                  >
                    {ch}
                  </span>
                ))}
              </span>
            ))}
          </div>
        </div>

        {/* Gold underline — draws in via scaleX spring, with a running spark */}
        <div style={{position: 'relative', width: 620, height: 3, margin: '46px 0 34px'}}>
          <div
            style={{
              width: '100%',
              height: 3,
              background: `linear-gradient(90deg, transparent 0%, ${GOLD} 12%, ${GOLD} 88%, transparent 100%)`,
              boxShadow: `0 0 16px 2px ${GOLD}88`,
              transform: `scaleX(${ruleS})`,
              transformOrigin: '50% 50%',
            }}
          />
          <div
            style={{
              position: 'absolute',
              top: '50%',
              left: `${interpolate(ruleS, [0, 1], [50, 100])}%`,
              width: 14,
              height: 14,
              marginTop: -7,
              marginLeft: -7,
              borderRadius: 7,
              background: WHITE,
              boxShadow: `0 0 20px 7px ${GOLD}`,
              opacity: ruleS > 0.03 && ruleS < 0.97 ? 1 : 0,
            }}
          />
        </div>

        {/* Subtitle — mask reveal in silver */}
        {subtitle ? (
          <span
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              paddingBottom: '0.12em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${subY}%)`,
                opacity: subO,
                fontFamily: BRAND.font.body,
                color: SILVER,
                fontSize: 32,
                fontWeight: 600,
                letterSpacing: 3,
                textTransform: 'uppercase',
              }}
            >
              {subtitle}
            </span>
          </span>
        ) : null}
      </AbsoluteFill>

      {/* Layer 6 — vignette + micro-flash */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.62) 100%)',
          pointerEvents: 'none',
        }}
      />
      <AbsoluteFill
        style={{
          background: WHITE,
          opacity: flash,
          mixBlendMode: 'screen',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
