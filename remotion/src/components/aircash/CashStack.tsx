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
// CashStack＋NumberTicker — 帯封束の山が下から積み上がり、確認済みの丸め金額
//   「$82,000」(約82,000ドル) が着地する。精密値 $82,373 は絶対に焼き込まない。
//   ・束は上からドロップ→spring小オーバーシュートで着地(rigidbody風)・スタッガー
//   ・額はマスク切れ上がり＋着地でスケールポップ(opacity単独禁止)
//   ・着地後も束の山が画面高≥3%/秒でパララックス移動を継続(走光は補助)
//   ・奥行き≥3層(グラデ背景/グリッド/裏グロー)＋奥の淡い束列でパララックス
//   ・単一アクセント=gold・暗ネイビー背景・凍らない微シマー・決定論
// 全モーションeased・fps算出・useCurrentFrameのみ・Math.random不使用(seeded)。
// これは自立するTSX図(後でBlender 3Dヒーローが上に合成され得るが単体で成立)。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(120% 105% at 50% 46%, ${BRAND.color.navy} 0%, ${BG} 82%)`;

const sec = (fps: number, s: number) => Math.round(fps * s);

// 決定論PRNG（Math.random禁止・seeded mulberry32）
const mulberry32 = (a: number) => () => {
  a |= 0;
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

// カンマ区切り（決定論・localeに依存しない）
const withCommas = (n: number) =>
  n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');

// ---- 山のレイアウト（モジュール定数・propsに依存しない） ----
const BW = 210; // 束の幅
const BH = 44; // 束の高さ（帯封の厚み）
const DX = 30; // 2.5D 上面オフセットX
const DY = 18; // 2.5D 上面オフセットY
const STACK_STEP = 40; // 段の重なり（BHより小＝重なり）
const GROUND_Y = 806; // 山の底
const CX = 960; // 中央X（1920/2）

type Slot = {x: number; y: number; level: number};

const buildSlots = (): Slot[] => {
  const jr = mulberry32(0x1337);
  const COLS = [
    {x: -212, n: 4},
    {x: 12, n: 5},
    {x: 236, n: 4},
  ];
  const maxN = 5;
  const slots: Slot[] = [];
  // 段(level)優先で下から積む＝ビルド順=配列順
  for (let level = 0; level < maxN; level++) {
    for (let ci = 0; ci < COLS.length; ci++) {
      if (level < COLS[ci].n) {
        slots.push({
          x: CX + COLS[ci].x + level * -8 + (jr() * 18 - 9),
          y: GROUND_Y - BH / 2 - level * STACK_STEP,
          level,
        });
      }
    }
  }
  return slots;
};
const SLOTS = buildSlots();

// 奥の淡い束列（パララックス用・小さく暗く）
const buildFarSlots = (): Slot[] => {
  const jr = mulberry32(0xbeef);
  const COLS = [
    {x: -150, n: 3},
    {x: 150, n: 3},
  ];
  const slots: Slot[] = [];
  for (let level = 0; level < 3; level++) {
    for (let ci = 0; ci < COLS.length; ci++) {
      if (level < COLS[ci].n) {
        slots.push({
          x: CX + COLS[ci].x + (jr() * 14 - 7),
          y: GROUND_Y - 150 - BH / 2 - level * (STACK_STEP - 6),
          level,
        });
      }
    }
  }
  return slots;
};
const FAR_SLOTS = buildFarSlots();

// 舞う塵（seeded 30粒・additive gold・上昇＝実移動）
const DUST = (() => {
  const r = mulberry32(0x5eed);
  return Array.from({length: 30}, () => ({
    x: r() * 1920,
    baseY: r() * 1120,
    speed: 20 + r() * 48, // px/s 上昇
    size: 2 + r() * 4,
    sway: 8 + r() * 22,
    swayT: 2.6 + r() * 3.2,
    phase: r() * Math.PI * 2,
  }));
})();

// ---- 帯封束の2.5Dベクター（原点=前面中心） ----
const MoneyBundle: React.FC<{shimmer: number}> = ({shimmer}) => {
  const hx = BW / 2;
  const hy = BH / 2;
  return (
    <g strokeLinejoin="round">
      {/* 右側面（暗） */}
      <path
        d={`M${hx},${-hy} L${hx + DX},${-hy - DY} L${hx + DX},${hy - DY} L${hx},${hy} Z`}
        fill={BRAND.color.ink}
        stroke={`${BRAND.color.silver}44`}
        strokeWidth={1.5}
      />
      {/* 上面（切り紙＝明るい・重なった札束の断面） */}
      <path
        d={`M${-hx},${-hy} L${hx},${-hy} L${hx + DX},${-hy - DY} L${-hx + DX},${-hy - DY} Z`}
        fill={BRAND.color.silver}
        fillOpacity={0.26}
        stroke={`${BRAND.color.silver}55`}
        strokeWidth={1.5}
      />
      {/* 上面の札の重なり線 */}
      {[0.28, 0.5, 0.72].map((t, i) => (
        <line
          key={i}
          x1={-hx + DX * t}
          y1={-hy - DY * t}
          x2={hx + DX * t}
          y2={-hy - DY * t}
          stroke={`${BRAND.color.silver}33`}
          strokeWidth={1}
        />
      ))}
      {/* 前面（札束の紙） */}
      <rect
        x={-hx}
        y={-hy}
        width={BW}
        height={BH}
        rx={3}
        fill={BRAND.color.navy}
        stroke={`${BRAND.color.silver}3a`}
        strokeWidth={1.5}
      />
      {/* 前面の札エッジ（横線） */}
      {[0.22, 0.42, 0.62, 0.82].map((t, i) => (
        <line
          key={i}
          x1={-hx + 4}
          y1={-hy + BH * t}
          x2={hx - 4}
          y2={-hy + BH * t}
          stroke={`${BRAND.color.silver}22`}
          strokeWidth={1}
        />
      ))}
      {/* 帯封（gold strap） */}
      <rect
        x={-BW * 0.17}
        y={-hy - 2}
        width={BW * 0.34}
        height={BH + 4}
        rx={2}
        fill={BRAND.color.gold}
        opacity={0.9 * shimmer + 0.1}
      />
      <rect
        x={-BW * 0.17}
        y={-hy - 2}
        width={BW * 0.34}
        height={BH + 4}
        rx={2}
        fill="none"
        stroke={`${BRAND.color.white}66`}
        strokeWidth={1}
      />
      {/* 帯封の$記号 */}
      <text
        x={0}
        y={4}
        textAnchor="middle"
        fontFamily={BRAND.font.display}
        fontSize={26}
        fontWeight={800}
        fill={BRAND.color.ink}
        opacity={0.85}
      >
        $
      </text>
    </g>
  );
};

export const CashStack: React.FC<{
  dur?: number;
  amount?: number;
  caption?: string;
}> = ({dur, amount, caption}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // 事実は固定：確認済みの丸め値だけを着地させる（精密$82,373は焼込み禁止）。
  // 千ドル丸めで表示するため、万一精密値が渡ってもforbidden数値は描かれない。
  const landed = Math.round((amount ?? 82000) / 1000) * 1000;

  const t = frame / fps;

  // ---- 持続パララックス（着地後も山が実移動・走光は補助） ----
  // settleで振幅を上げるが、ビルド中も微ドリフト。峰速度≈73px/s(=6.8%/s)。
  const settle = interpolate(
    frame,
    [sec(fps, 6.4), sec(fps, 7.6)],
    [0.35, 1],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const driftY = settle * 42 * Math.sin((t * 2 * Math.PI) / 3.6);
  const driftX = settle * 24 * Math.sin((t * 2 * Math.PI) / 5.4 + 0.7);

  // ゆるいドリーイン＋微呼吸（補助カメラ運動）
  const dolly =
    interpolate(frame, [0, sec(fps, 7)], [0.94, 1.0], {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }) +
    0.008 * Math.sin((t * 2 * Math.PI) / 6);

  // 凍らない微シマー（帯封の輝き）
  const shimmer = interpolate(Math.sin(frame / 11), [-1, 1], [0.72, 1]);

  // ---- NumberTicker：カウント→着地 ----
  const countStart = sec(fps, 4.4);
  const landFrame = sec(fps, 7.0);
  const cp = interpolate(frame, [countStart, landFrame], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const val =
    frame >= landFrame
      ? landed
      : Math.min(landed, Math.round((cp * landed) / 500) * 500);

  // 額のマスク切れ上がり（translateY）＋着地スケールポップ
  const numS = spring({
    frame: frame - sec(fps, 4.2),
    fps,
    config: {damping: 16, mass: 0.9},
  });
  const numY = interpolate(numS, [0, 1], [130, 0]);
  const numO = interpolate(numS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  const landS = spring({
    frame: frame - landFrame,
    fps,
    config: {damping: 9, mass: 0.7, stiffness: 170},
  });
  const pop = 1 + interpolate(landS, [0, 0.5, 1], [0, 0.12, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const flash = interpolate(landS, [0.15, 0.4, 0.85], [0, 0.9, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // 着地の衝撃で山が軽く沈み込む（rigidbody風・二次モーション）
  const jolt = interpolate(landS, [0, 0.35, 0.7, 1], [0, 10, -3, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ラベル切れ上がり
  const labelS = spring({
    frame: frame - sec(fps, 4.9),
    fps,
    config: {damping: 18, mass: 0.9},
  });
  const labelY = interpolate(labelS, [0, 1], [110, 0]);
  const labelO = interpolate(labelS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // シーン出入り
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 12], [20, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  const GOLD = BRAND.color.gold;
  const startY = -780; // 束の落下開始（画面外上）

  // グロー中心（山のおおよそ中央）を%で
  const glowX = (CX / width) * 100;
  const glowY = ((GROUND_Y - 120) / height) * 100;

  // 束1つを描く（ドロップspring＋着地オーバーシュート）
  const renderBundle = (
    s: Slot,
    i: number,
    baseDelay: number,
    dim: number,
    scale: number,
  ) => {
    const delay = baseDelay + i * Math.round(fps * 0.24);
    const drop = spring({
      frame: frame - delay,
      fps,
      config: {damping: 12, mass: 0.9, stiffness: 130},
    });
    const y = interpolate(drop, [0, 1], [startY, s.y]);
    const o = interpolate(drop, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
    return (
      <g
        key={i}
        transform={`translate(${s.x}, ${y + jolt}) scale(${scale})`}
        opacity={o * dim}
      >
        <MoneyBundle shimmer={shimmer} />
      </g>
    );
  };

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド（ゆっくりドリフト＝凍らない） */}
      <AbsoluteFill
        style={{
          opacity: 0.08,
          transform: `translateY(${interpolate(
            Math.sin((t * 2 * Math.PI) / 9),
            [-1, 1],
            [-14, 14],
          )}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px)`,
          maskImage: 'radial-gradient(120% 92% at 50% 58%, black 28%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 58%, black 28%, transparent 82%)',
        }}
      />
      {/* L3 山の裏グロー（着地でフラッシュ） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(34% 40% at ${glowX}% ${glowY}%, ${GOLD}${
            flash > 0.4 ? '4a' : '22'
          } 0%, transparent 66%)`,
        }}
      />

      <AbsoluteFill
        style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}
      >
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0}}
        >
          {/* 地面ライン */}
          <line
            x1={CX - 520}
            y1={GROUND_Y + BH / 2}
            x2={CX + 560}
            y2={GROUND_Y + BH / 2}
            stroke={`${BRAND.color.silver}2a`}
            strokeWidth={2}
          />

          {/* 奥の淡い束列（パララックス0.45・暗） */}
          <g transform={`translate(${driftX * 0.45}, ${driftY * 0.45})`}>
            {FAR_SLOTS.map((s, i) =>
              renderBundle(s, i, sec(fps, 0.2), 0.32, 0.66),
            )}
          </g>

          {/* 主役の山（パララックス1.0＋ドリー） */}
          <g
            transform={`translate(${driftX}, ${driftY}) translate(${CX}, ${GROUND_Y}) scale(${dolly}) translate(${-CX}, ${-GROUND_Y})`}
          >
            {SLOTS.map((s, i) => renderBundle(s, i, sec(fps, 0.35), 1, 1))}
          </g>
        </svg>

        {/* 舞う塵（Trailでモーションブラー・AbsoluteFillをラップ／上昇=実移動・パララックス1.5） */}
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.4}>
          <AbsoluteFill
            style={{transform: `translate(${driftX * 1.5}px, ${driftY * 1.5}px)`}}
          >
            {DUST.map((p, i) => {
              const range = 1180;
              const yy =
                (((p.baseY - t * p.speed) % range) + range) % range - 60;
              const xx = p.x + p.sway * Math.sin((t * 2 * Math.PI) / p.swayT + p.phase);
              // ループ端のポップ回避（三角フェード・movementと併用）
              const edge = Math.min(yy + 60, range - 60 - yy) / 120;
              const op = Math.max(0, Math.min(1, edge)) * 0.5;
              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: xx,
                    top: yy,
                    width: p.size,
                    height: p.size,
                    borderRadius: '50%',
                    background: BRAND.color.white,
                    boxShadow: `0 0 ${6 + p.size}px ${p.size}px ${GOLD}`,
                    opacity: op,
                    pointerEvents: 'none',
                  }}
                />
              );
            })}
          </AbsoluteFill>
        </Trail>

        {/* 着地の閃光リング（補助） */}
        {flash > 0.02 ? (
          <div
            style={{
              position: 'absolute',
              left: CX - 150,
              top: GROUND_Y - 320,
              width: 300,
              height: 300,
              borderRadius: '50%',
              border: `3px solid ${GOLD}`,
              transform: `scale(${interpolate(flash, [0, 0.9], [0.6, 1.5])})`,
              opacity: flash * 0.8,
              boxShadow: `0 0 44px ${GOLD}`,
              pointerEvents: 'none',
            }}
          />
        ) : null}

        {/* NumberTicker：確認済み丸め額の着地 */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            top: 214,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            transform: `translate(${driftX * 0.5}px, ${driftY * 0.5}px)`,
          }}
        >
          {/* 小ラベル（切れ上がり） */}
          <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
            <div
              style={{
                transform: `translateY(${labelY}%)`,
                opacity: labelO,
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 26,
                letterSpacing: 5,
                color: BRAND.color.silver,
              }}
            >
              APPROX. CASH SEIZED AT THE CHECKPOINT
            </div>
          </div>
          {/* 大額（マスク切れ上がり＋着地ポップ） */}
          <div style={{overflow: 'hidden', paddingBottom: '0.1em'}}>
            <div
              style={{
                transform: `translateY(${numY}%) scale(${pop})`,
                transformOrigin: 'center top',
                opacity: numO,
                fontFamily: BRAND.font.display,
                fontWeight: 800,
                fontSize: 148,
                lineHeight: 1,
                letterSpacing: 2,
                color: GOLD,
                textShadow: `0 0 ${18 + flash * 40}px ${GOLD}aa`,
                display: 'flex',
                alignItems: 'baseline',
              }}
            >
              <span style={{fontSize: 66, marginRight: 6, opacity: 0.85}}>≈</span>
              <span>${withCommas(val)}</span>
            </div>
          </div>
        </div>

        {/* キャプション（マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            left: 0,
            right: 0,
            bottom: 96,
            display: 'flex',
            justifyContent: 'center',
          }}
        >
          <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
            <div
              style={{
                transform: `translateY(${interpolate(
                  spring({frame: frame - sec(fps, 7.4), fps, config: {damping: 18}}),
                  [0, 1],
                  [120, 0],
                )}%)`,
                fontFamily: BRAND.font.body,
                fontWeight: 600,
                fontSize: 30,
                letterSpacing: 1,
                color: BRAND.color.silver,
              }}
            >
              {caption ?? 'Roughly $82,000 in cash — taken at the airport.'}
            </div>
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
