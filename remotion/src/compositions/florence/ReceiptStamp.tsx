/**
 * ReceiptStamp — an ORIGINAL, Florence-only animation (not a reused template).
 * Story beat: "He had the receipt — proof the fine was paid. It didn't matter."
 * A paper receipt slides in under a hard interrogation light; a green/gold PAID
 * stamp SLAMS down with a real inked overshoot — proof, on record. Then a red
 * WARRANT · ACTIVE mark stamps over the top and overrides it: the PAID stamp
 * dims and is struck through, the machine believing the stale warrant over the
 * proof in the man's hand. No readable fake legal text (short generic words only).
 * Self-contained (no image assets). 180f = 6s.
 */
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../../brand';
import {FilmGrain, VignetteBreath} from '../../components/motionkit';

const RED = '#C0473E';
const RED_HOT = '#FF5A48'; // brighter core for the WARRANT glow so it dominates
const PAID_GREEN = '#3F9E6A'; // confident, clearly-positive inked green
const PAID_GREEN_DEEP = '#2E7C51'; // darker ink for the crisp double-line look
const PAPER = '#ECE6D8'; // warm aged off-white
const PAPER_LOW = '#DAD2BE'; // aged shadow tone at the foot of the page
const PAPER_INK = '#3A342A'; // warm brown-grey "ink" for skeleton lines

export const receiptStampDuration = 180;

// generic receipt lines — no readable fake legal text, just skeleton bars
const LINES = [0.86, 0.62, 0.74, 0.5, 0.68];

export const ReceiptStamp: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // hard light cone breathing in
  const lightIn = interpolate(f, [0, 26], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateRight: 'clamp'});
  const lightFlicker = 0.94 + 0.06 * Math.sin(f / 7);

  // receipt slides in under the light + settles with a spring
  const slide = spring({frame: f - 8, fps, config: {damping: 18, stiffness: 90}, durationInFrames: 40});
  // gentle always-alive paper drift
  const driftY = Math.sin(f / 26) * 3;
  const driftR = Math.sin(f / 34) * 0.5;

  // PAID stamp slam — spring overshoot like a real rubber stamp hitting paper
  const paidHit = 46;
  const paidDrop = spring({frame: f - paidHit, fps, config: {damping: 9, stiffness: 200}, durationInFrames: 30});
  // scale from oversized → 1 (the stamp descending onto the page)
  const paidScale = interpolate(paidDrop, [0, 1], [2.4, 1]);
  const paidOpacity = interpolate(f, [paidHit, paidHit + 5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // ink recoil ring on impact
  const impact = interpolate(f - paidHit, [0, 14], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // WARRANT override slams later and wins
  const warHit = 104;
  const warDrop = spring({frame: f - warHit, fps, config: {damping: 8, stiffness: 220}, durationInFrames: 28});
  const warScale = interpolate(warDrop, [0, 1], [2.8, 1.14]); // settles LARGER than PAID — it dominates
  const warOpacity = interpolate(f, [warHit, warHit + 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const warPulse = 0.5 + 0.5 * Math.sin((f - warHit) / 4.5);
  const warImpact = interpolate(f - warHit, [0, 16], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // PAID is overridden: dims + gets struck through once WARRANT lands
  const override = interpolate(f, [warHit, warHit + 24], [0, 1], {easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const paidDim = 1 - 0.62 * override;
  const strike = interpolate(f, [warHit + 6, warHit + 26], [0, 1], {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // page whole-frame shake on each slam (settles fast)
  const shake = (hit: number, amp: number) => {
    const t = f - hit;
    if (t < 0 || t > 12) return 0;
    return Math.sin(t * 1.9) * amp * Math.max(0, 1 - t / 12);
  };
  const pageShake = shake(paidHit, 3) + shake(warHit, 5);

  const paperW = width * 0.37;
  const paperH = height * 0.72;
  const cx = width / 2;
  const cy = height / 2;

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, justifyContent: 'center', alignItems: 'center'}}>
      {/* deep ground */}
      <AbsoluteFill style={{background: `radial-gradient(80% 80% at 50% 42%, ${BRAND.color.navy}AA, ${BRAND.color.ink} 72%)`}} />

      {/* hard interrogation light cone from top */}
      <div
        style={{
          position: 'absolute',
          top: -height * 0.2,
          left: cx - width * 0.34,
          width: width * 0.68,
          height: height * 1.1,
          opacity: lightIn * lightFlicker * 0.5,
          background: `radial-gradient(60% 55% at 50% 20%, ${BRAND.color.white}22, transparent 60%)`,
          clipPath: 'polygon(38% 0%, 62% 0%, 100% 100%, 0% 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* the receipt / document */}
      <div
        style={{
          position: 'absolute',
          width: paperW,
          height: paperH,
          left: cx - paperW / 2,
          top: cy - paperH / 2,
          transform: `translateX(${pageShake}px) translateY(${interpolate(slide, [0, 1], [height * 0.5, 0]) + driftY}px) rotate(${interpolate(slide, [0, 1], [-4, 0]) + driftR}deg)`,
          opacity: interpolate(f, [8, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
          background: `linear-gradient(168deg, ${PAPER} 0%, #E6DECD 58%, ${PAPER_LOW} 100%)`,
          borderRadius: 5,
          boxShadow: `0 34px 100px #000D, 0 2px 0 #FFFFFF30 inset, 0 -30px 60px #00000022 inset`,
          overflow: 'hidden',
        }}
      >
        {/* fibrous paper texture — faint warm horizontal grain */}
        <div style={{
          position: 'absolute', inset: 0, pointerEvents: 'none', opacity: 0.5,
          backgroundImage: `repeating-linear-gradient(0deg, #00000000 0px, #00000000 2px, ${PAPER_INK}0A 3px, #00000000 4px), repeating-linear-gradient(90deg, #00000000 0px, #FFFFFF00 5px, #FFFFFF14 6px, #00000000 8px)`,
        }} />
        {/* aged edge vignette + warm interrogation glow catching the sheet */}
        <div style={{
          position: 'absolute', inset: 0, pointerEvents: 'none',
          background: `radial-gradient(120% 90% at 50% 8%, ${BRAND.color.white}22, transparent 46%), radial-gradient(130% 120% at 50% 108%, ${PAPER_INK}55, transparent 62%)`,
        }} />
        {/* paper header band */}
        <div style={{height: paperH * 0.12, borderBottom: `2px solid ${PAPER_INK}33`, display: 'flex', alignItems: 'center', padding: '0 8%'}}>
          <div style={{width: 14, height: 14, borderRadius: '50%', background: PAID_GREEN_DEEP}} />
          <div style={{marginLeft: 12, height: 10, width: '40%', borderRadius: 3, background: `${PAPER_INK}CC`}} />
          <div style={{marginLeft: 'auto', height: 8, width: '18%', borderRadius: 3, background: `${PAPER_INK}66`}} />
        </div>
        {/* generic content lines (skeleton bars — no readable text) */}
        <div style={{padding: '9% 8%', display: 'flex', flexDirection: 'column', gap: paperH * 0.055}}>
          {LINES.map((w, i) => (
            <div
              key={i}
              style={{
                height: 9,
                width: `${w * 100}%`,
                borderRadius: 3,
                background: `${PAPER_INK}${i === 3 ? '66' : '44'}`,
                opacity: interpolate(f, [18 + i * 3, 30 + i * 3], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
              }}
            />
          ))}
        </div>
      </div>

      {/* PAID stamp group — slams down, then dims + struck through */}
      <div
        style={{
          position: 'absolute',
          left: cx,
          top: cy - paperH * 0.06,
          transform: `translate(-50%, -50%) translateX(${pageShake}px) rotate(-13deg) scale(${paidScale})`,
          opacity: paidOpacity * paidDim,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            position: 'relative',
            padding: '8px 32px 12px',
            border: `7px solid ${PAID_GREEN}`,
            // inner hairline echoes a real rubber-stamp die; ink fill sits inside
            outline: `2px solid ${PAID_GREEN_DEEP}`,
            outlineOffset: 5,
            borderRadius: 10,
            color: PAID_GREEN_DEEP,
            fontFamily: BRAND.font.display,
            fontSize: 82,
            fontWeight: 900,
            letterSpacing: 3,
            background: `${PAID_GREEN}1E`,
            filter: `saturate(${1 - 0.72 * override}) brightness(${1 - 0.34 * override})`,
            boxShadow: `0 0 ${20 * paidDrop}px ${PAID_GREEN}55, inset 0 0 ${14 * paidDrop}px ${PAID_GREEN_DEEP}33`,
            // uneven ink bleed: soft under-shadow + crisp top edge
            textShadow: `0 0 6px ${PAID_GREEN}66, 1px 2px 0 ${PAID_GREEN_DEEP}88`,
            WebkitTextStroke: `1px ${PAID_GREEN}`,
          }}
        >
          PAID
          {/* struck-through override bar */}
          <div
            style={{
              position: 'absolute',
              left: '2%',
              top: '52%',
              height: 9,
              width: `${strike * 96}%`,
              background: RED,
              boxShadow: `0 0 14px ${RED}, 0 0 6px ${RED_HOT}`,
              transform: 'rotate(-3deg)',
              borderRadius: 4,
            }}
          />
        </div>
      </div>

      {/* PAID impact recoil ring */}
      <div
        style={{
          position: 'absolute',
          left: cx,
          top: cy - paperH * 0.06,
          width: 40,
          height: 40,
          borderRadius: '50%',
          border: `3px solid ${PAID_GREEN}`,
          transform: `translate(-50%, -50%) scale(${1 + impact * 6})`,
          opacity: f >= paidHit ? (1 - impact) * 0.7 : 0,
          pointerEvents: 'none',
        }}
      />

      {/* WARRANT · ACTIVE override — the machine's verdict, slams on top and wins */}
      <div
        style={{
          position: 'absolute',
          left: cx,
          top: cy + paperH * 0.10,
          transform: `translate(-50%, -50%) translateX(${pageShake}px) rotate(7deg) scale(${warScale})`,
          opacity: warOpacity,
          pointerEvents: 'none',
        }}
      >
        {/* soft blood-red halo bleeding onto the page behind the stamp */}
        <div style={{
          position: 'absolute', inset: '-40% -30%',
          background: `radial-gradient(60% 60% at 50% 50%, ${RED}66, transparent 70%)`,
          filter: 'blur(24px)', opacity: 0.5 + 0.35 * warPulse,
        }} />
        <div
          style={{
            position: 'relative',
            padding: '14px 34px',
            border: `8px solid ${RED}`,
            outline: `2px solid ${RED_HOT}`,
            outlineOffset: 5,
            borderRadius: 10,
            color: RED_HOT,
            fontFamily: BRAND.font.display,
            fontSize: 60,
            fontWeight: 900,
            letterSpacing: 3,
            textAlign: 'center',
            background: `rgba(192,71,62,${0.16 + 0.10 * warPulse})`,
            boxShadow: `0 0 ${28 + 30 * warPulse}px ${RED}, 0 0 ${10 + 14 * warPulse}px ${RED_HOT}, inset 0 0 20px ${RED}77`,
            textShadow: `0 0 ${14 + 8 * warPulse}px ${RED_HOT}, 0 0 4px ${RED}`,
            WebkitTextStroke: `1px ${RED}`,
          }}
        >
          <div>WARRANT</div>
          <div style={{fontSize: 32, letterSpacing: 8, marginTop: 4, color: RED, opacity: 0.75 + 0.25 * warPulse}}>ACTIVE</div>
        </div>
      </div>

      {/* WARRANT impact recoil ring */}
      <div
        style={{
          position: 'absolute',
          left: cx,
          top: cy + paperH * 0.12,
          width: 46,
          height: 46,
          borderRadius: '50%',
          border: `3px solid ${RED}`,
          transform: `translate(-50%, -50%) scale(${1 + warImpact * 7})`,
          opacity: f >= warHit ? (1 - warImpact) * 0.8 : 0,
          pointerEvents: 'none',
        }}
      />

      <VignetteBreath dur={receiptStampDuration} />
      <FilmGrain dur={receiptStampDuration} />
    </AbsoluteFill>
  );
};
