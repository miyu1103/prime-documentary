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
// RegionHighlightMap — MOTIONKIT
//   セル格子で描いた様式化アメリカ地図。州セルが「点灯」する。
//   pattern='varied' : セルごとに electric / gold / dim を非一様に、
//                      決して収束しないシマー（sin位相ずらし）で明滅。
//                      "住む場所によって変わる／未確定" を可視化する。
//   pattern='uniform': 全セルが同位相で一斉に点灯・呼吸する。
//   マスク切り上がりのラベル（任意）。決定論（useCurrentFrame＋セル番号＋
//   remotion random）。全モーションにイージング（等速なし）／点灯は必ず
//   スケール・移動と対で（opacity単独禁止）。奥行き5レイヤー。
// =====================================================================

// 秒→フレーム（フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);
const TAU = Math.PI * 2;

// 0..1 のアルファを2桁hexへ
const ah = (a: number): string => {
  const v = Math.max(0, Math.min(255, Math.round(a * 255)));
  return v.toString(16).padStart(2, '0');
};

// 手描きの US シルエット・マスク（'#' = 陸セル）。外部地理データ不使用。
// 各行はちょうど 22 文字。上辺=北の国境、左上=太平洋岸、中下=テキサスの
// 落ち込み、右下=フロリダの垂れ下がり。
const MASK: readonly string[] = [
  '.####################.',
  '.####################.',
  '.####################.',
  '..###################.',
  '..##################..',
  '...################...',
  '...####...#######.....',
  '....###....#####......',
  '.....#......####......',
  '............###.......',
  '............##........',
] as const;

const COLS = 22;
const ROWS = MASK.length;

type Cell = {c: number; r: number; i: number};
const LAND: readonly Cell[] = (() => {
  const cells: Cell[] = [];
  let i = 0;
  for (let r = 0; r < ROWS; r++) {
    const row = MASK[r];
    for (let c = 0; c < COLS; c++) {
      if (row[c] === '#') {
        cells.push({c, r, i});
        i++;
      }
    }
  }
  return cells;
})();

type CellKind = 'electric' | 'gold' | 'dim';
const colorOf = (kind: CellKind): string =>
  kind === 'gold'
    ? BRAND.color.gold
    : kind === 'dim'
    ? BRAND.color.silver
    : BRAND.color.electric;

export const RegionHighlightMap: React.FC<{
  label?: string;
  pattern?: 'uniform' | 'varied';
  dur?: number;
}> = ({label, pattern = 'varied', dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // シーン出入り（opacity単独禁止 → 微translateYと対）
  const sceneY = interpolate(frame, [0, 12], [16, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sceneO = interpolate(
    frame,
    [0, 12, D - 16, D],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // 地図ジオメトリ
  const CELL = 60;
  const originX = (width - COLS * CELL) / 2;
  const originY = (height - ROWS * CELL) / 2 - 26;

  // レイヤー2: ドリフトするグリッド（イージング付き往復）
  const drift = interpolate(frame, [0, D], [0, 34], {
    easing: Easing.inOut(Easing.sin),
  });

  // レイヤー3: 呼吸するアンビエントグロー（sin=イージング、スケールと対）
  const breathe = 0.5 + 0.5 * Math.sin(frame * 0.03);
  const glowScale = 1 + breathe * 0.09;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#06080f',
        opacity: sceneO,
        transform: `translateY(${sceneY}px)`,
      }}
    >
      {/* レイヤー1: フルスクリーン背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* レイヤー3: アンビエントグロー（地図の裏で明滅） */}
      <AbsoluteFill
        style={{
          transform: `scale(${glowScale})`,
          opacity: 0.5 + breathe * 0.3,
          background: `radial-gradient(38% 46% at 46% 46%, ${BRAND.color.electric}30 0%, transparent 70%),
            radial-gradient(24% 30% at 62% 74%, ${BRAND.color.gold}1f 0%, transparent 72%)`,
        }}
      />

      {/* レイヤー2: ドリフトするグリッド */}
      <AbsoluteFill
        style={{
          opacity: 0.16,
          transform: `translate(${drift * 0.5}px, ${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}26 0px, ${BRAND.color.electric}26 1px, transparent 1px, transparent 70px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}26 0px, ${BRAND.color.electric}26 1px, transparent 1px, transparent 70px)`,
          maskImage:
            'radial-gradient(115% 90% at 50% 46%, black 30%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(115% 90% at 50% 46%, black 30%, transparent 84%)',
        }}
      />

      {/* レイヤー4: セル地図 */}
      <AbsoluteFill>
        {LAND.map(({c, r, i}) => {
          // --- 決定論的な種 ---
          const kSeed = random('cell' + i);
          const kind: CellKind =
            pattern === 'uniform'
              ? 'electric'
              : kSeed < 0.15
              ? 'gold'
              : kSeed < 0.66
              ? 'electric'
              : 'dim';
          const color = colorOf(kind);

          // --- 登場: 対角ウェーブ＋ジッターのスタッガー spring ---
          const step = sec(fps, 0.028);
          const delay = (c + r) * step + random('order' + i) * step * 2;
          const appear = spring({
            frame: frame - sec(fps, 0.15) - delay,
            fps,
            config: {damping: 14, mass: 0.8},
          });
          const sc = interpolate(appear, [0, 1], [0.25, 1]);
          const ty = interpolate(appear, [0, 1], [20, 0]);
          const appLight = interpolate(appear, [0, 0.5], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          // --- 点灯強度: 決して収束しないシマー（sin=イージング） ---
          const base = kind === 'gold' ? 0.55 : kind === 'dim' ? 0.16 : 0.5;
          const amp = kind === 'gold' ? 0.45 : kind === 'dim' ? 0.22 : 0.5;
          const shim =
            pattern === 'uniform'
              ? 0.5 + 0.5 * Math.sin(frame * 0.05) // 全セル同位相＝一斉
              : 0.5 +
                0.5 *
                  Math.sin(
                    frame * (0.035 + random('spd' + i) * 0.06) +
                      random('phase' + i) * TAU,
                  );
          const lit = Math.max(0, Math.min(1, base + amp * shim)) * appLight;

          // 点灯はスケールと対で表現（opacity単独禁止）
          const shimScale = 1 + lit * 0.05;
          const inner = CELL * 0.82;

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: originX + c * CELL,
                top: originY + r * CELL,
                width: CELL,
                height: CELL,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                transform: `translateY(${ty}px) scale(${sc * shimScale})`,
                opacity: interpolate(appear, [0, 0.4], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                }),
              }}
            >
              <div
                style={{
                  width: inner,
                  height: inner,
                  borderRadius: CELL * 0.22,
                  backgroundColor: color + ah(0.12 + lit * 0.55),
                  border: `1px solid ${color}${ah(0.28 + lit * 0.42)}`,
                  boxShadow: `0 0 ${8 + lit * 30}px ${color}${ah(
                    lit * 0.75,
                  )}, inset 0 0 ${lit * 14}px ${color}${ah(lit * 0.4)}`,
                }}
              />
            </div>
          );
        })}
      </AbsoluteFill>

      {/* レイヤー5: ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 55%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* レイヤー6: マスク切り上がりラベル（高速なので Trail でモーションブラー） */}
      {label ? (
        <Trail layers={5} lagInFrames={1.2} trailOpacity={0.5}>
          <div
            style={{
              position: 'absolute',
              left: 0,
              right: 0,
              bottom: 96,
              display: 'flex',
              justifyContent: 'center',
              fontFamily: BRAND.font.display,
              fontSize: 58,
              letterSpacing: 4,
              textTransform: 'uppercase',
              color: BRAND.color.white,
            }}
          >
            {Array.from(label).map((ch, i) => {
              const cs = spring({
                frame: frame - sec(fps, 0.5) - i * sec(fps, 0.035),
                fps,
                config: {damping: 16, mass: 1},
              });
              const y = interpolate(cs, [0, 1], [110, 0]);
              const o = interpolate(cs, [0, 0.3], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              return (
                <span
                  key={i}
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
                      whiteSpace: 'pre',
                    }}
                  >
                    {ch}
                  </span>
                </span>
              );
            })}
          </div>
        </Trail>
      ) : null}
    </AbsoluteFill>
  );
};
