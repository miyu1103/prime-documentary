import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// ProbableCauseMeter — 「単なる勘」がしきい値(=相当な理由)を越えるか否か。
//   outcome='stall': 針が線の直下で止まり、鈍く落ちる（越えられない）。
//   outcome='cross': 証拠チップがスタッガーで積み上がり、針を線の上へ押し上げ、
//                    しきい値が金色にロックする。
// 品質ルール: 全モーションspring/easing・opacity単独なし・マスク切れ上がり・
//   高速侵入はTrailでモーションブラー・単一アクセント・決定論(frame+index)。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);
const BG = '#06080f';

// 暗いグラデ背景＋抑えたグリッド＋ビネット（最低3レイヤー）
const Backdrop: React.FC<{accent: string}> = ({accent}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const drift = interpolate(frame, [0, durationInFrames], [0, 34], {
    easing: Easing.inOut(Easing.sin),
  });
  return (
    <>
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 66px),
            repeating-linear-gradient(90deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 66px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 45%, black 28%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 45%, black 28%, transparent 80%)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 44%, rgba(0,0,0,0.66) 100%)',
        }}
      />
    </>
  );
};

// マスク切れ上がりラベル（overflow:hidden + translateY）
const MaskLabel: React.FC<{
  text: string;
  fps: number;
  start: number;
  size: number;
  color: string;
  weight?: number;
  letter?: number;
  family?: string;
}> = ({text, fps, start, size, color, weight = 700, letter = 2, family}) => {
  const frame = useCurrentFrame();
  const cs = spring({
    frame: frame - sec(fps, start),
    fps,
    config: {damping: 16, mass: 0.9},
  });
  const y = interpolate(cs, [0, 1], [115, 0]);
  const o = interpolate(cs, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: family ?? BRAND.font.body,
          fontWeight: weight,
          fontSize: size,
          letterSpacing: letter,
          color,
          whiteSpace: 'pre',
        }}
      >
        {text}
      </span>
    </span>
  );
};

type Outcome = 'stall' | 'cross';

const CHIPS = ['PLAIN VIEW', 'K-9 ALERT', 'ADMISSION'];

export const ProbableCauseMeter: React.FC<{
  outcome?: Outcome;
  dur?: number;
}> = ({outcome = 'cross', dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // メーター幾何
  const trackW = 210;
  const trackH = 720;
  const trackTop = 180;
  const trackBottom = trackTop + trackH; // 900
  const trackX = 640;
  const thresholdFrac = 0.72; // しきい値の高さ（0=底,1=天）
  const thresholdY = trackBottom - thresholdFrac * trackH;

  // ベースの上昇（spring）— 相当な理由の直下まで
  const baseCs = spring({
    frame: frame - sec(fps, 0.35),
    fps,
    config: {damping: 20, mass: 1.1},
  });

  // チップの積み上がり（cross時のみ針を押し上げる）
  const chipStart = 1.15;
  const chipStep = 0.5;
  const chipInc = 0.115;
  const chipProgress = CHIPS.map((_, i) =>
    spring({
      frame: frame - sec(fps, chipStart + i * chipStep),
      fps,
      config: {damping: 15, mass: 0.7},
    }),
  );

  let fillFrac: number;
  if (outcome === 'cross') {
    const base = interpolate(baseCs, [0, 1], [0, 0.55]);
    const fromChips = chipProgress.reduce((a, p) => a + p * chipInc, 0);
    fillFrac = base + fromChips; // 0.55 -> 0.895 (>0.72)
  } else {
    // 直下で止まり、遅れて鈍く落ちる
    const base = interpolate(baseCs, [0, 1], [0, 0.655]);
    const drop = interpolate(
      frame,
      [sec(fps, 2.0), sec(fps, 2.7)],
      [0, 0.06],
      {
        easing: Easing.inOut(Easing.cubic),
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      },
    );
    fillFrac = base - drop; // ~0.655 -> 0.595
  }

  // 常に微呼吸（凍結防止）
  const breath =
    Math.sin((frame / fps) * Math.PI * 2 * 0.28) *
    0.006 *
    interpolate(baseCs, [0, 1], [0, 1]);
  fillFrac = Math.max(0, Math.min(0.97, fillFrac + breath));

  const crossed = fillFrac >= thresholdFrac;
  // 越えた瞬間からのロック演出用の進捗
  const lockP = crossed
    ? interpolate(fillFrac, [thresholdFrac, thresholdFrac + 0.08], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 0;

  const fillColor = crossed ? BRAND.color.gold : BRAND.color.electric;
  const fillH = fillFrac * trackH;
  const fillTopY = trackBottom - fillH;

  // 針(=fill top)に付くラベル
  const meterLabel = outcome === 'stall' ? 'A HUNCH' : 'PROBABLE CAUSE';

  // シーン出入り（微translateY併用でopacity単独回避）
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const inY = interpolate(frame, [0, 10], [18, 0], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [total - 12, total], [1, 0], {
    extrapolateLeft: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <Backdrop accent={BRAND.color.electric} />
      <AbsoluteFill
        style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}
      >
        {/* 見出し */}
        <div style={{position: 'absolute', top: 96, left: 300}}>
          <MaskLabel
            text="DID IT RISE TO PROBABLE CAUSE?"
            fps={fps}
            start={0.1}
            size={38}
            color={BRAND.color.silver}
            weight={700}
            letter={3}
            family={BRAND.font.display}
          />
        </div>

        <svg
          width={1920}
          height={1080}
          style={{position: 'absolute', inset: 0}}
        >
          {/* メータートラック（外枠） */}
          <rect
            x={trackX}
            y={trackTop}
            width={trackW}
            height={trackH}
            rx={26}
            fill="#0b1220"
            stroke={`${BRAND.color.silver}33`}
            strokeWidth={2}
          />
          {/* 目盛り（抑えた軸） */}
          {Array.from({length: 9}).map((_, i) => {
            const gy = trackTop + (trackH * (i + 1)) / 10;
            return (
              <line
                key={i}
                x1={trackX + 14}
                y1={gy}
                x2={trackX + 40}
                y2={gy}
                stroke={`${BRAND.color.silver}22`}
                strokeWidth={2}
              />
            );
          })}

          {/* 針より下のグロー土台 */}
          <defs>
            <linearGradient id="pcmFill" x1="0" y1="1" x2="0" y2="0">
              <stop offset="0%" stopColor={fillColor} stopOpacity={0.55} />
              <stop offset="100%" stopColor={fillColor} stopOpacity={1} />
            </linearGradient>
          </defs>

          {/* 上昇するフィル */}
          <rect
            x={trackX + 8}
            y={fillTopY}
            width={trackW - 16}
            height={Math.max(0, fillH - 8)}
            rx={18}
            fill="url(#pcmFill)"
            style={{
              filter: `drop-shadow(0 0 ${crossed ? 26 : 14}px ${fillColor}${
                crossed ? 'cc' : '88'
              })`,
            }}
          />
          {/* 針先ライン */}
          <rect
            x={trackX + 8}
            y={fillTopY - 3}
            width={trackW - 16}
            height={6}
            rx={3}
            fill={BRAND.color.white}
            opacity={0.9}
          />

          {/* しきい値ライン（PROBABLE CAUSE） */}
          <line
            x1={trackX - 120}
            y1={thresholdY}
            x2={trackX + trackW + 470}
            y2={thresholdY}
            stroke={crossed ? BRAND.color.gold : BRAND.color.white}
            strokeWidth={crossed ? 4 : 3}
            strokeDasharray="2 10"
            strokeLinecap="round"
            opacity={0.9}
            style={{
              filter: `drop-shadow(0 0 ${
                6 + lockP * 22
              }px ${BRAND.color.gold}${crossed ? 'cc' : '00'})`,
            }}
          />
        </svg>

        {/* しきい値ラベル */}
        <div
          style={{
            position: 'absolute',
            left: trackX - 120,
            top: thresholdY - 52,
          }}
        >
          <MaskLabel
            text="PROBABLE CAUSE"
            fps={fps}
            start={0.5}
            size={34}
            color={crossed ? BRAND.color.gold : BRAND.color.white}
            weight={800}
            letter={4}
            family={BRAND.font.display}
          />
        </div>
        {/* ロック表示 */}
        {crossed ? (
          <div
            style={{
              position: 'absolute',
              left: trackX + trackW + 300,
              top: thresholdY + 10,
              transform: `translateY(${interpolate(lockP, [0, 1], [16, 0])}px)`,
              opacity: lockP,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 3,
              color: BRAND.color.gold,
            }}
          >
            ✓ LOCKED
          </div>
        ) : null}

        {/* 針ラベル（fill topに追従） */}
        <div
          style={{
            position: 'absolute',
            left: trackX - 150,
            top: fillTopY + 8,
            width: 150,
            textAlign: 'right',
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: 22,
            letterSpacing: 2,
            color: crossed ? BRAND.color.gold : BRAND.color.electric,
            opacity: interpolate(baseCs, [0.2, 0.6], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        >
          {meterLabel}
        </div>

        {/* 証拠チップ（cross時のみ・Trailで高速侵入＋スタッガー積み上げ） */}
        {outcome === 'cross' ? (
          <div
            style={{
              position: 'absolute',
              left: trackX + trackW + 90,
              top: trackBottom - 150,
              display: 'flex',
              flexDirection: 'column-reverse',
              gap: 14,
            }}
          >
            {CHIPS.map((c, i) => {
              const p = chipProgress[i];
              const x = interpolate(p, [0, 1], [70, 0]);
              const o = interpolate(p, [0, 0.35], [0, 1], {
                extrapolateRight: 'clamp',
              });
              const s = interpolate(p, [0, 1], [0.9, 1]);
              return (
                <Trail
                  key={i}
                  layers={6}
                  lagInFrames={1.1}
                  trailOpacity={0.5}
                >
                  <div
                    style={{
                      transform: `translateX(${x}px) scale(${s})`,
                      opacity: o,
                      padding: '12px 22px',
                      borderRadius: 10,
                      background: 'rgba(11,26,43,0.9)',
                      border: `2px solid ${BRAND.color.gold}`,
                      boxShadow: `0 0 18px ${BRAND.color.gold}44`,
                      fontFamily: BRAND.font.body,
                      fontWeight: 700,
                      fontSize: 26,
                      letterSpacing: 2,
                      color: BRAND.color.white,
                      whiteSpace: 'nowrap',
                    }}
                  >
                    <span style={{color: BRAND.color.gold, marginRight: 10}}>
                      +
                    </span>
                    {c}
                  </div>
                </Trail>
              );
            })}
          </div>
        ) : (
          // stall時: 「越えられない」注記
          <div
            style={{
              position: 'absolute',
              left: trackX + trackW + 300,
              top: thresholdY + 40,
              transform: `translateY(${interpolate(
                baseCs,
                [0.4, 1],
                [20, 0],
                {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
              )}px)`,
              opacity: interpolate(baseCs, [0.5, 1], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              }),
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 2,
              color: BRAND.color.silver,
            }}
          >
            STALLS BELOW THE LINE
          </div>
        )}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
