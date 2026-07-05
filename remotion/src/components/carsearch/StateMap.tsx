import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {BRAND} from '../../brand';

// =====================================================================
// StateMap — 簡略化(ロウポリ)の合衆国シルエット。ラベルの下で州セルが
//   バラバラの色/強度でスタッガー点灯（一部electric・一部gold・一部dim）。
//   「州によって扱いが違う／未解決」を表す、完全には収束しない揺らぎ。
// 品質ルール: 全モーションspring/easing・opacity単独なし(scale併用)・
//   マスク切れ上がりラベル・単一の暗背景・決定論(frame+index)。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);
const BG = '#06080f';

// 抽象的な合衆国っぽいブロック配置（地理的正確さは不要）
const MAP = [
  ' ######### ',
  '###########',
  '###########',
  '#########  ',
  ' #######   ',
  '  #####  # ',
  '   ###  #  ',
];

const Backdrop: React.FC<{accent: string}> = ({accent}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const drift = interpolate(frame, [0, durationInFrames], [0, 26], {
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
          opacity: 0.09,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 68px),
            repeating-linear-gradient(90deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 68px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 52%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 52%, black 30%, transparent 82%)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 52%, transparent 44%, rgba(0,0,0,0.66) 100%)',
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
}> = ({text, fps, start, size, color, weight = 800, letter = 5, family}) => {
  const frame = useCurrentFrame();
  const cs = spring({
    frame: frame - sec(fps, start),
    fps,
    config: {damping: 16, mass: 0.9},
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

type Cell = {r: number; c: number; idx: number};

// 決定論的な色カテゴリ（indexのみ・非一様）
const catOf = (idx: number): 'electric' | 'gold' | 'dim' => {
  const k = (idx * 37 + 11) % 100;
  if (k < 38) return 'electric';
  if (k < 66) return 'gold';
  return 'dim';
};

export const StateMap: React.FC<{label?: string; dur?: number}> = ({
  label = 'SMELL = PROBABLE CAUSE?',
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // セル集合を決定論的に構築
  const cols = MAP[0].length;
  const cells: Cell[] = [];
  let idx = 0;
  for (let r = 0; r < MAP.length; r++) {
    for (let c = 0; c < cols; c++) {
      if (MAP[r][c] === '#') {
        cells.push({r, c, idx});
        idx++;
      }
    }
  }

  // レイアウト
  const pitch = 112;
  const size = 94;
  const gridW = cols * pitch;
  const startX = (1920 - gridW) / 2 + pitch * 0.0;
  const startY = 300;

  // 点灯順（対角スイープ＋indexで散らす、決定論）
  const orderKey = (cl: Cell) => cl.r + cl.c + (cl.idx % 3) * 0.6;
  const maxOrder = Math.max(...cells.map(orderKey));

  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [total - 12, total], [1, 0], {
    extrapolateLeft: 'clamp',
  });
  const inY = interpolate(frame, [0, 12], [22, 0], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <Backdrop accent={BRAND.color.electric} />
      <AbsoluteFill
        style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}
      >
        {/* マスク切れ上がりラベル */}
        <div
          style={{
            position: 'absolute',
            top: 130,
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <MaskLabel
            text={label}
            fps={fps}
            start={0.12}
            size={58}
            color={BRAND.color.white}
            weight={800}
            letter={4}
            family={BRAND.font.display}
          />
        </div>
        {/* 副題 */}
        <div
          style={{
            position: 'absolute',
            top: 210,
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <MaskLabel
            text="IT DEPENDS WHERE YOU ARE — STILL UNSETTLED"
            fps={fps}
            start={0.4}
            size={26}
            color={BRAND.color.silver}
            weight={600}
            letter={5}
            family={BRAND.font.body}
          />
        </div>

        <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
          <defs>
            <filter id="smBlur" x="-40%" y="-40%" width="180%" height="180%">
              <feGaussianBlur stdDeviation="6" />
            </filter>
          </defs>
          {cells.map((cl) => {
            const x = startX + cl.c * pitch;
            const y = startY + cl.r * pitch;
            const cat = catOf(cl.idx);

            // 点灯 spring（scale併用でopacity単独回避）
            const order = orderKey(cl);
            const startS = 0.7 + (order / maxOrder) * 1.5;
            const cs = spring({
              frame: frame - sec(fps, startS),
              fps,
              config: {damping: 14, mass: 0.8},
            });
            const scale = interpolate(cs, [0, 1], [0.55, 1]);
            const appear = interpolate(cs, [0, 0.35], [0, 1], {
              extrapolateRight: 'clamp',
            });

            // 収束しない揺らぎ（決定論・cellごと位相）
            const phase = (cl.idx * 1.7) % (Math.PI * 2);
            const shimmer =
              0.5 +
              0.5 * Math.sin((frame / fps) * Math.PI * 2 * 0.5 + phase);

            let color: string;
            let baseInt: number;
            if (cat === 'electric') {
              color = BRAND.color.electric;
              baseInt = 0.55 + 0.45 * shimmer;
            } else if (cat === 'gold') {
              color = BRAND.color.gold;
              baseInt = 0.5 + 0.5 * shimmer;
            } else {
              color = BRAND.color.silver;
              baseInt = 0.16 + 0.12 * shimmer; // dim: ほぼ点かない
            }
            const intensity = cs > 0 ? appear * baseInt : 0;

            const cx = x + size / 2;
            const cy = y + size / 2;
            const glow = cat === 'dim' ? 0 : intensity * 18;

            return (
              <g
                key={cl.idx}
                transform={`translate(${cx} ${cy}) scale(${scale}) translate(${-cx} ${-cy})`}
                opacity={appear}
              >
                {/* グロウ土台 */}
                {glow > 0 ? (
                  <rect
                    x={x - 4}
                    y={y - 4}
                    width={size + 8}
                    height={size + 8}
                    rx={12}
                    fill={color}
                    opacity={intensity * 0.35}
                    filter="url(#smBlur)"
                  />
                ) : null}
                {/* セル本体 */}
                <rect
                  x={x}
                  y={y}
                  width={size}
                  height={size}
                  rx={10}
                  fill={color}
                  fillOpacity={0.1 + intensity * 0.78}
                  stroke={color}
                  strokeOpacity={0.35 + intensity * 0.55}
                  strokeWidth={2}
                />
              </g>
            );
          })}
        </svg>

        {/* 凡例（各色の意味・マスク切れ上がりで散らして出す） */}
        <div
          style={{
            position: 'absolute',
            bottom: 110,
            width: '100%',
            display: 'flex',
            justifyContent: 'center',
            gap: 54,
          }}
        >
          {(
            [
              [BRAND.color.electric, 'YES — P.C.'],
              [BRAND.color.gold, 'FACTOR ONLY'],
              [BRAND.color.silver, 'UNDECIDED'],
            ] as const
          ).map(([col, txt], i) => {
            const cs = spring({
              frame: frame - sec(fps, 1.6 + i * 0.18),
              fps,
              config: {damping: 16, mass: 0.8},
            });
            const ly = interpolate(cs, [0, 1], [24, 0]);
            const lo = interpolate(cs, [0, 0.4], [0, 1], {
              extrapolateRight: 'clamp',
            });
            return (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  transform: `translateY(${ly}px)`,
                  opacity: lo,
                }}
              >
                <span
                  style={{
                    width: 20,
                    height: 20,
                    borderRadius: 5,
                    background: col,
                    boxShadow: `0 0 12px ${col}88`,
                  }}
                />
                <span
                  style={{
                    fontFamily: BRAND.font.body,
                    fontWeight: 700,
                    fontSize: 24,
                    letterSpacing: 2,
                    color: BRAND.color.silver,
                  }}
                >
                  {txt}
                </span>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
