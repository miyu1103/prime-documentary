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
// ReportThresholdMeter — 現金申告義務の閾値メーター（CLM-0024）
//   国内線(DOMESTIC)は「上限なし・申告義務なし」＝針が右端 NO LIMIT まで
//   走り切り、下のバーが端まで伸びる。国際線(INTERNATIONAL)は $10,000 超
//   のみ申告義務＝ゲートで硬く止まる。対比で「国内は青天井」を可視化。
//
//   主運動＝(1)ダイヤルの針が左端$0→右端 NO LIMIT へ大きくスイープ
//          (2)DOMESTIC バーが右へ伸長
//          (3)無制限バー上を現金シェブロンが左→右へ持続的に流れ続ける
//   ＝いずれも「物体の実移動」。走光/グロウは補助のみ。
//
//   品質: 全モーション spring/Easing・opacity単独なし（translateY/scale併走）・
//   テキストは overflow:hidden + translateY マスク切上り・高速針は Trail で
//   モーションブラー・暗紺背景＋奥行き≥3層・単一アクセント(gold)・
//   凍らない微シマー・fps算出・deterministic(useCurrentFrame + mulberry32)。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 105% at 50% 40%, ${BRAND.color.navy} 0%, ${BG} 82%)`;
const GOLD = BRAND.color.gold;

const sec = (fps: number, s: number) => Math.round(fps * s);

// seeded PRNG（Math.random 禁止・決定論）
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

// 極座標→直交（トップ半円ダイヤル：deg 180=左端/$0, 0=右端/NO LIMIT）
const arcPoint = (gx: number, gy: number, r: number, deg: number) => {
  const rad = (deg * Math.PI) / 180;
  return {x: gx + r * Math.cos(rad), y: gy - r * Math.sin(rad)};
};

// deg1→deg2 を折れ線でサンプルして path 文字列にする（arc-flag 曖昧回避）
const arcPath = (
  gx: number,
  gy: number,
  r: number,
  deg1: number,
  deg2: number,
  steps = 48,
) => {
  let d = '';
  for (let i = 0; i <= steps; i++) {
    const deg = deg1 + ((deg2 - deg1) * i) / steps;
    const p = arcPoint(gx, gy, r, deg);
    d += `${i === 0 ? 'M' : 'L'}${p.x.toFixed(2)},${p.y.toFixed(2)}`;
  }
  return d;
};

export type ReportThresholdMeterProps = {
  dur?: number;
  // 事実は固定（CLM-0024）。既定値のみ許可＝国内無制限 / 国際$10,000。
  intlThreshold?: string;
  domesticLabel?: string;
};

export const ReportThresholdMeter: React.FC<ReportThresholdMeterProps> = ({
  dur,
  intlThreshold = '$10,000',
  domesticLabel = 'NO LIMIT',
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;
  const t = frame / fps;

  // ---- ダイヤル幾何 ----
  const gx = width / 2;
  const gy = height * 0.46;
  const R = 250;
  const DEG_ZERO = 180; // 左端 = $0
  const DEG_MAX = 6; // 右端 = NO LIMIT
  const DEG_GATE = 128; // $10,000 ゲート位置（左寄り）

  // ---- タイムライン（全て fps 算出）----
  // ダイヤルの円弧トラックが描かれる
  const dialIn = spring({
    frame: frame - sec(fps, 0.2),
    fps,
    config: {damping: 20, mass: 0.9},
  });

  // 主運動1: 針の大スイープ（$0 → NO LIMIT）。国内は上限に達しても止まらない。
  const sweep = spring({
    frame: frame - sec(fps, 0.5),
    fps,
    config: {damping: 16, mass: 1, stiffness: 90},
  });
  // スイープ後も針は「青天井」を突き続ける生きた揺れ（正弦＝速度可変イージング・実角移動）
  const sustain = interpolate(frame, [sec(fps, 2.8), sec(fps, 3.4)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const hunt = sustain * 7 * Math.sin(t * ((2 * Math.PI) / 2.1)); // ±7°の実移動
  const needleDeg =
    interpolate(sweep, [0, 1], [DEG_ZERO, DEG_MAX]) + hunt;
  const needleActive =
    frame >= sec(fps, 0.5) && frame <= sec(fps, D / fps); // 常時（sweep+hunt）
  const needleTip = arcPoint(gx, gy, R - 18, needleDeg);
  // 針が掃いた扇形（針に連動して育つ・塗り）
  const wedge =
    `M${gx},${gy} ` +
    arcPath(gx, gy, R - 40, DEG_ZERO, needleDeg, 40).slice(1) +
    ` L${gx},${gy} Z`;

  // ---- バー幾何 ----
  const bx0 = width * 0.16;
  const bx1 = width * 0.84;
  const barW = bx1 - bx0;
  const domY = height * 0.66;
  const intlY = height * 0.8;
  const barH = 34;
  const gateT = 0.22; // 国際線ゲート＝バーの22%地点（$10,000）

  // 主運動2: DOMESTIC バー伸長（右端まで＝無制限）
  const domGrow = spring({
    frame: frame - sec(fps, 2.6),
    fps,
    config: {damping: 20, mass: 1, stiffness: 80},
  });
  const domFill = interpolate(domGrow, [0, 1], [0, barW]);

  // INTERNATIONAL バー伸長（ゲートで硬く停止）
  const intlGrow = spring({
    frame: frame - sec(fps, 3.6),
    fps,
    config: {damping: 22, mass: 1, stiffness: 80},
  });
  const intlFill = interpolate(intlGrow, [0, 1], [0, barW * gateT]);
  // ゲート壁の着弾フラッシュ（$10,000 で止まる衝撃）
  const gateHit = interpolate(intlGrow, [0.7, 0.9, 1], [0, 1, 0.35], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ---- 持続主運動3: 無制限バー上を流れる現金シェブロン（実移動・Trail）----
  const flowReveal = interpolate(domGrow, [0.35, 0.8], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rand = mulberry32(20240034);
  const N_FLOW = 7;
  const chevrons = Array.from({length: N_FLOW}).map((_, i) => {
    const phase = rand();
    const speed = 0.34 + rand() * 0.06; // 周回/秒
    const p = (t * speed + phase) % 1; // 0→1 を左→右
    const x = bx0 + p * domFill; // 伸長済み範囲内を走る
    // 端でのフェード（実体の出入り・opacity単独ではなく位置移動が主）
    const edge = Math.min(p, 1 - p) * 6;
    const o = flowReveal * Math.min(1, edge) * 0.9;
    return {x, y: domY + barH / 2, o};
  });

  // ---- 微シマー（凍らない）----
  const shimmer = interpolate(Math.sin(frame / 11), [-1, 1], [0.86, 1]);
  const goldPulse = interpolate(Math.sin(frame / 15 + 1), [-1, 1], [0.9, 1]);

  // ---- シーン出入り（opacity は translateY と併走）----
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {
    extrapolateLeft: 'clamp',
  });
  const inY = interpolate(frame, [0, 12], [22, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // ---- テキスト・マスク切上り ----
  const domLabelY = interpolate(
    spring({frame: frame - sec(fps, 3.4), fps, config: {damping: 17}}),
    [0, 1],
    [120, 0],
  );
  const intlLabelY = interpolate(
    spring({frame: frame - sec(fps, 4.4), fps, config: {damping: 17}}),
    [0, 1],
    [120, 0],
  );
  const titleY = interpolate(
    spring({frame: frame - sec(fps, 0.15), fps, config: {damping: 16}}),
    [0, 1],
    [120, 0],
  );

  const gatePos = arcPoint(gx, gy, R - 40, DEG_GATE);
  const gateEnd = arcPoint(gx, gy, R + 6, DEG_GATE);

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド */}
      <AbsoluteFill
        style={{
          opacity: 0.08,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
        }}
      />
      {/* L3 ダイヤル裏のグロー（針が右へ進むほど強まる） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(26% 30% at 50% ${
            (gy / height) * 100
          }%, ${GOLD}${sweep > 0.6 ? '3a' : '18'} 0%, transparent 66%)`,
        }}
      />

      <AbsoluteFill
        style={{
          opacity: inO * outO,
          transform: `translateY(${inY}px)`,
        }}
      >
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="rtm-dom" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={`${GOLD}55`} />
              <stop offset="100%" stopColor={GOLD} />
            </linearGradient>
          </defs>

          {/* ---- ダイヤルの円弧トラック（奥） ---- */}
          <g opacity={interpolate(dialIn, [0, 0.5], [0, 1], {extrapolateRight: 'clamp'})}>
            <path
              d={arcPath(gx, gy, R, DEG_ZERO, DEG_MAX)}
              fill="none"
              stroke={`${BRAND.color.silver}44`}
              strokeWidth={16}
              strokeLinecap="round"
            />
            {/* 目盛り */}
            {Array.from({length: 11}).map((_, i) => {
              const deg = DEG_ZERO + ((DEG_MAX - DEG_ZERO) * i) / 10;
              const a = arcPoint(gx, gy, R - 26, deg);
              const b = arcPoint(gx, gy, R - 6, deg);
              return (
                <line
                  key={i}
                  x1={a.x}
                  y1={a.y}
                  x2={b.x}
                  y2={b.y}
                  stroke={`${BRAND.color.silver}66`}
                  strokeWidth={i === 10 ? 4 : 2}
                />
              );
            })}
          </g>

          {/* ---- 針が掃いた扇形（針に連動して育つ） ---- */}
          <path d={wedge} fill={`${GOLD}1c`} opacity={dialIn} />
          {/* 進んだ弧のハイライト */}
          <path
            d={arcPath(gx, gy, R, DEG_ZERO, needleDeg)}
            fill="none"
            stroke={GOLD}
            strokeWidth={6}
            strokeLinecap="round"
            opacity={0.85 * goldPulse}
            style={{filter: `drop-shadow(0 0 ${8 + sweep * 10}px ${GOLD}aa)`}}
          />

          {/* ---- $10,000 国際線ゲート・マーカー（ダイヤル上） ---- */}
          <g opacity={interpolate(dialIn, [0.4, 0.9], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}>
            <line
              x1={gatePos.x}
              y1={gatePos.y}
              x2={gateEnd.x}
              y2={gateEnd.y}
              stroke={BRAND.color.silver}
              strokeWidth={3}
              strokeDasharray="5 4"
            />
            <circle cx={gateEnd.x} cy={gateEnd.y} r={5} fill={BRAND.color.silver} />
          </g>

          {/* ---- 右端 NO LIMIT ピン ---- */}
          {(() => {
            const nl = arcPoint(gx, gy, R + 6, DEG_MAX);
            return (
              <circle
                cx={nl.x}
                cy={nl.y}
                r={7}
                fill={GOLD}
                opacity={interpolate(sweep, [0.75, 1], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                })}
                style={{filter: `drop-shadow(0 0 10px ${GOLD})`}}
              />
            );
          })()}

          {/* ---- 針（pivot=ダイヤル中心） ---- */}
          <g opacity={shimmer}>
            <line
              x1={gx}
              y1={gy}
              x2={needleTip.x}
              y2={needleTip.y}
              stroke={GOLD}
              strokeWidth={6}
              strokeLinecap="round"
              style={{filter: `drop-shadow(0 0 6px ${GOLD}aa)`}}
            />
            {/* 針の尾（反対側の小片） */}
            {(() => {
              const tail = arcPoint(gx, gy, -34, needleDeg);
              return (
                <line
                  x1={gx}
                  y1={gy}
                  x2={tail.x}
                  y2={tail.y}
                  stroke={`${BRAND.color.silver}cc`}
                  strokeWidth={5}
                  strokeLinecap="round"
                />
              );
            })()}
            <circle cx={gx} cy={gy} r={16} fill="#0c1524" stroke={GOLD} strokeWidth={4} />
            <circle cx={gx} cy={gy} r={5} fill={GOLD} />
          </g>

          {/* ================= バー（下段） ================= */}
          {/* --- DOMESTIC トラック --- */}
          <rect
            x={bx0}
            y={domY}
            width={barW}
            height={barH}
            rx={barH / 2}
            fill="#0c1524"
            stroke={`${BRAND.color.silver}33`}
            strokeWidth={2}
          />
          {/* DOMESTIC 伸長フィル（右端まで＝無制限） */}
          <rect
            x={bx0}
            y={domY}
            width={Math.max(0, domFill)}
            height={barH}
            rx={barH / 2}
            fill="url(#rtm-dom)"
            style={{filter: `drop-shadow(0 0 ${10 * goldPulse}px ${GOLD}88)`}}
          />
          {/* 無制限を示す先端の → 矢羽（フィル先端に付く） */}
          {domGrow > 0.9 ? (
            <path
              d={`M${bx0 + domFill - 4},${domY + 4} L${bx0 + domFill + 22},${
                domY + barH / 2
              } L${bx0 + domFill - 4},${domY + barH - 4}`}
              fill="none"
              stroke={GOLD}
              strokeWidth={5}
              strokeLinejoin="round"
              strokeLinecap="round"
              opacity={goldPulse}
            />
          ) : null}

          {/* --- INTERNATIONAL トラック --- */}
          <rect
            x={bx0}
            y={intlY}
            width={barW}
            height={barH}
            rx={barH / 2}
            fill="#0c1524"
            stroke={`${BRAND.color.silver}33`}
            strokeWidth={2}
          />
          {/* INTERNATIONAL 伸長フィル（ゲートで停止） */}
          <rect
            x={bx0}
            y={intlY}
            width={Math.max(0, intlFill)}
            height={barH}
            rx={barH / 2}
            fill={`${BRAND.color.silver}aa`}
          />
          {/* $10,000 ゲート壁 */}
          <g>
            <rect
              x={bx0 + barW * gateT - 3}
              y={intlY - 14}
              width={6}
              height={barH + 28}
              rx={3}
              fill={GOLD}
              style={{
                filter: `drop-shadow(0 0 ${6 + gateHit * 22}px ${GOLD})`,
              }}
            />
            {/* ゲート衝撃リング */}
            {gateHit > 0.02 ? (
              <circle
                cx={bx0 + barW * gateT}
                cy={intlY + barH / 2}
                r={interpolate(gateHit, [0, 1], [8, 40])}
                fill="none"
                stroke={GOLD}
                strokeWidth={3}
                opacity={gateHit}
              />
            ) : null}
          </g>
        </svg>

        {/* ---- 現金シェブロン流（無制限バー上を左→右へ持続移動・Trail） ---- */}
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.45}>
          <AbsoluteFill style={{pointerEvents: 'none'}}>
            {chevrons.map((c, i) => (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: c.x - 11,
                  top: c.y - 12,
                  opacity: c.o,
                }}
              >
                <svg width={22} height={24} viewBox="0 0 22 24">
                  <path
                    d="M3 3 L15 12 L3 21"
                    fill="none"
                    stroke={BRAND.color.white}
                    strokeWidth={4}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
            ))}
          </AbsoluteFill>
        </Trail>

        {/* ---- 高速な針先のグリント（Trail・スイープ中のみ） ---- */}
        {needleActive && sweep < 0.98 ? (
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <AbsoluteFill style={{pointerEvents: 'none'}}>
              <div
                style={{
                  position: 'absolute',
                  left: needleTip.x - 9,
                  top: needleTip.y - 9,
                  width: 18,
                  height: 18,
                  borderRadius: '50%',
                  background: BRAND.color.white,
                  boxShadow: `0 0 22px 7px ${GOLD}, 0 0 8px 2px ${BRAND.color.white}`,
                }}
              />
            </AbsoluteFill>
          </Trail>
        ) : null}

        {/* ---- テキスト（マスク切上り） ---- */}
        {/* タイトル */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            top: height * 0.12,
            width: '100%',
            textAlign: 'center',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              transform: `translateY(${titleY}%)`,
              fontFamily: BRAND.font.display,
              fontWeight: 800,
              fontSize: 40,
              letterSpacing: 6,
              color: BRAND.color.white,
            }}
          >
            CASH REPORTING THRESHOLD
          </div>
        </div>

        {/* DOMESTIC ラベル */}
        <div
          style={{
            position: 'absolute',
            left: bx0,
            top: domY - 46,
            overflow: 'hidden',
            width: barW,
          }}
        >
          <div
            style={{
              transform: `translateY(${domLabelY}%)`,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 26,
              letterSpacing: 2,
              color: GOLD,
            }}
          >
            {`DOMESTIC · ${domesticLabel} — NO REPORTING REQUIRED`}
          </div>
        </div>

        {/* INTERNATIONAL ラベル */}
        <div
          style={{
            position: 'absolute',
            left: bx0,
            top: intlY + barH + 12,
            overflow: 'hidden',
            width: barW,
          }}
        >
          <div
            style={{
              transform: `translateY(${intlLabelY}%)`,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 26,
              letterSpacing: 2,
              color: BRAND.color.silver,
            }}
          >
            {`INTERNATIONAL · REPORT REQUIRED OVER ${intlThreshold}`}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
