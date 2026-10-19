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
// CurtilageShield — 家に密着していた保護グロウが、eased springで外側へ広がり、
//   ドライブウェイとポーチ（＝curtilage）を包む。車の影は保護域の内側に立つ。
//   "CURTILAGE" はマスク切れ上がりで出現。金色のグロウが一度力強く脈打ち保持。
// 品質ルール: 全モーションspring/easing・opacity単独なし・マスク切れ上がり・
//   高速侵入Trail・単一アクセント(gold)・≥3レイヤー・決定論。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);
const BG = '#06080f';
const GOLD = BRAND.color.gold;

const Backdrop: React.FC<{accent: string}> = ({accent}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const drift = interpolate(frame, [0, durationInFrames], [0, 30], {
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
          opacity: 0.08,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 70px),
            repeating-linear-gradient(90deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 70px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 50%, black 30%, transparent 82%)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, transparent 42%, rgba(0,0,0,0.68) 100%)',
        }}
      />
    </>
  );
};

const MaskLabel: React.FC<{
  text: string;
  fps: number;
  start: number;
  size: number;
  color: string;
  weight?: number;
  letter?: number;
  family?: string;
}> = ({text, fps, start, size, color, weight = 800, letter = 6, family}) => {
  const frame = useCurrentFrame();
  const cs = spring({
    frame: frame - sec(fps, start),
    fps,
    config: {damping: 15, mass: 0.9},
  });
  const y = interpolate(cs, [0, 1], [120, 0]);
  const o = interpolate(cs, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.16em'}}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: family ?? BRAND.font.display,
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

export const CurtilageShield: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 保護域の拡張 spring（0=家に密着 -> 1=curtilage全体を包む）
  const expand = spring({
    frame: frame - sec(fps, 0.7),
    fps,
    config: {damping: 18, mass: 1.2},
  });

  // 一度だけ力強く脈打つ（越えた後の保持で微呼吸）
  const pulseCore = spring({
    frame: frame - sec(fps, 1.45),
    fps,
    config: {damping: 9, mass: 0.7},
  });
  const pulse = interpolate(pulseCore, [0, 0.5, 1], [0, 1, 0], {
    extrapolateRight: 'clamp',
  });
  const settled = interpolate(expand, [0.75, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // 保護域が settle 後もはっきり息づく呼吸（±9px＝知覚可能な振幅・正弦＝イージング）
  const breath = Math.sin((frame / fps) * Math.PI * 2 * 0.22) * 9 * settled;
  // 境界を走り続けるダッシュ（正弦駆動＝速度可変のイージング・凍結防止）
  const dashOffset =
    settled * 40 * Math.sin((frame / fps) * ((2 * Math.PI) / 2.4));
  // 全体パララックス（settle後・正弦＝イージング・total非依存）
  const driftX =
    settled * 14 * Math.sin((frame / fps) * ((2 * Math.PI) / 7.2));
  const driftY =
    settled * 9 * Math.sin((frame / fps) * ((2 * Math.PI) / 5.6) + 0.5);

  // 保護ゾーン（家に密着 -> ドライブウェイ＆ポーチを包む角丸矩形）
  // 家＝x 720..1040, 車＝ドライブウェイ右側
  const zoneX0Start = 700;
  const zoneY0Start = 470;
  const zoneX1Start = 1060;
  const zoneY1Start = 830;

  const zoneX0End = 620;
  const zoneY0End = 380;
  const zoneX1End = 1360; // ドライブウェイ端まで
  const zoneY1End = 880;

  const zx0 = interpolate(expand, [0, 1], [zoneX0Start, zoneX0End]) - breath * 0.7;
  const zy0 = interpolate(expand, [0, 1], [zoneY0Start, zoneY0End]) - breath;
  const zx1 = interpolate(expand, [0, 1], [zoneX1Start, zoneX1End]) + breath * 0.7;
  const zy1 = interpolate(expand, [0, 1], [zoneY1Start, zoneY1End]) + breath;
  const zw = zx1 - zx0;
  const zh = zy1 - zy0;

  const glowStrength = 10 + expand * 20 + pulse * 34;
  const zoneStroke = interpolate(expand, [0, 1], [1.5, 3.5]);

  // 車シルエットの登場（保護域内・Trailで滑走）
  const carCs = spring({
    frame: frame - sec(fps, 0.25),
    fps,
    config: {damping: 20, mass: 1},
  });
  const carX = interpolate(carCs, [0, 1], [130, 0]);
  const carO = interpolate(carCs, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});

  // 家の建ち上がり
  const houseCs = spring({
    frame: frame - sec(fps, 0.1),
    fps,
    config: {damping: 17, mass: 1},
  });
  const houseY = interpolate(houseCs, [0, 1], [40, 0]);
  const houseO = interpolate(houseCs, [0, 0.4], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [total - 12, total], [1, 0], {
    extrapolateLeft: 'clamp',
  });

  // 家の頂点（三角屋根）
  const houseL = 720;
  const houseR = 1040;
  const houseTop = 470; // 壁の上端
  const roofPeakY = 380;
  const houseBottom = 830;
  const midX = (houseL + houseR) / 2;

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <Backdrop accent={GOLD} />
      <AbsoluteFill
        style={{
          opacity: inO * outO,
          transform: `translate(${driftX}px, ${driftY}px)`,
        }}
      >
        {/* レイヤー1: 地面ライン */}
        <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
          <line
            x1={220}
            y1={houseBottom}
            x2={1700}
            y2={houseBottom}
            stroke={`${BRAND.color.silver}33`}
            strokeWidth={2}
          />

          {/* レイヤー2: ドライブウェイの帯（家の右） */}
          <g
            opacity={interpolate(houseCs, [0.2, 0.7], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            })}
          >
            <polygon
              points="1060,700 1360,700 1420,830 1060,830"
              fill="#0c1524"
              stroke={`${BRAND.color.silver}2a`}
              strokeWidth={2}
            />
            {/* ドライブウェイの分割線 */}
            {Array.from({length: 3}).map((_, i) => {
              const t = (i + 1) / 4;
              const xTop = 1060 + (1360 - 1060) * t;
              const xBot = 1060 + (1420 - 1060) * t;
              return (
                <line
                  key={i}
                  x1={xTop}
                  y1={700}
                  x2={xBot}
                  y2={830}
                  stroke={`${BRAND.color.silver}1f`}
                  strokeWidth={2}
                />
              );
            })}
          </g>

          {/* レイヤー3: 保護ゾーン（グロウ）— 家密着 -> curtilage全体 */}
          <rect
            x={zx0}
            y={zy0}
            width={zw}
            height={zh}
            rx={34}
            fill={`${GOLD}12`}
            stroke={GOLD}
            strokeWidth={zoneStroke}
            strokeDasharray="10 8"
            strokeDashoffset={dashOffset}
            style={{
              filter: `drop-shadow(0 0 ${glowStrength}px ${GOLD}${
                expand > 0.4 ? 'aa' : '66'
              })`,
            }}
          />
          {/* 脈動の二重リング */}
          <rect
            x={zx0 - pulse * 16}
            y={zy0 - pulse * 16}
            width={zw + pulse * 32}
            height={zh + pulse * 32}
            rx={40}
            fill="none"
            stroke={GOLD}
            strokeWidth={2}
            opacity={pulse * 0.7}
          />

          {/* レイヤー4: 家（三角屋根＋壁＋ドア＋窓） */}
          <g
            opacity={houseO}
            transform={`translate(0, ${houseY})`}
            style={{filter: `drop-shadow(0 0 10px ${BRAND.color.navy})`}}
          >
            {/* 壁 */}
            <rect
              x={houseL}
              y={houseTop}
              width={houseR - houseL}
              height={houseBottom - houseTop}
              fill="#0e1a2c"
              stroke={BRAND.color.silver}
              strokeWidth={3}
            />
            {/* 屋根 */}
            <polygon
              points={`${houseL - 26},${houseTop} ${midX},${roofPeakY} ${
                houseR + 26
              },${houseTop}`}
              fill="#0b1524"
              stroke={BRAND.color.silver}
              strokeWidth={3}
              strokeLinejoin="round"
            />
            {/* ドア（ポーチ側） */}
            <rect
              x={midX - 34}
              y={houseBottom - 130}
              width={68}
              height={130}
              fill="#0a1220"
              stroke={`${BRAND.color.gold}cc`}
              strokeWidth={3}
            />
            {/* 窓 */}
            <rect
              x={houseL + 34}
              y={houseTop + 54}
              width={70}
              height={70}
              fill="#0a1220"
              stroke={`${BRAND.color.electric}aa`}
              strokeWidth={3}
            />
            <rect
              x={houseR - 104}
              y={houseTop + 54}
              width={70}
              height={70}
              fill="#0a1220"
              stroke={`${BRAND.color.electric}aa`}
              strokeWidth={3}
            />
            {/* ポーチの床（家の前・curtilageの一部） */}
            <rect
              x={houseL - 30}
              y={houseBottom}
              width={houseR - houseL + 60}
              height={16}
              fill="#0c1626"
              stroke={`${BRAND.color.silver}33`}
              strokeWidth={2}
            />
          </g>
        </svg>

        {/* 車シルエット（ドライブウェイ内・保護域の中）— Trailで滑走侵入 */}
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          <div
            style={{
              position: 'absolute',
              left: 1120,
              top: 726,
              transform: `translateX(${carX}px)`,
              opacity: carO,
            }}
          >
            <svg width={230} height={96} viewBox="0 0 230 96">
              {/* 車体 */}
              <path
                d="M12 70 L34 44 Q40 34 54 34 L150 34 Q168 34 182 46 L214 56 Q224 60 224 70 L224 78 Q224 82 220 82 L14 82 Q10 82 10 78 Z"
                fill="#0a111e"
                stroke={BRAND.color.silver}
                strokeWidth={3}
                strokeLinejoin="round"
              />
              {/* 窓 */}
              <path
                d="M52 42 L146 42 Q158 42 168 50 L120 50 L120 42 Z"
                fill={`${BRAND.color.electric}55`}
              />
              {/* タイヤ */}
              <circle cx={62} cy={82} r={15} fill="#05090f" stroke={BRAND.color.silver} strokeWidth={3} />
              <circle cx={180} cy={82} r={15} fill="#05090f" stroke={BRAND.color.silver} strokeWidth={3} />
            </svg>
          </div>
        </Trail>

        {/* CURTILAGE ラベル（保護域の外側にマスク切れ上がり） */}
        <div style={{position: 'absolute', left: 630, top: 300}}>
          <MaskLabel
            text="CURTILAGE"
            fps={fps}
            start={1.0}
            size={72}
            color={GOLD}
            weight={800}
            letter={12}
            family={BRAND.font.display}
          />
        </div>
        <div style={{position: 'absolute', left: 634, top: 116}}>
          <MaskLabel
            text="THE HOME'S PROTECTED EXTENSION"
            fps={fps}
            start={0.15}
            size={30}
            color={BRAND.color.silver}
            weight={700}
            letter={4}
            family={BRAND.font.body}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
