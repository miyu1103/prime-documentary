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
// PinDropMap — 「これは N か所で起きた」用の様式化マップ（MOTIONKIT）
//   様式化されたマップ平面（外部地理データ不使用の抽象大陸ブロブ＋緯経線グリッド）に、
//   複数のピンがスタッガーで落下（オーバーシュートspringでバウンド）→
//   着地ごとに拡がる波紋リング（ループして静止しない）→
//   ピン間を電光アークが strokeDashoffset で順に描かれ →
//   ラベルは overflow:hidden の translateY マスク切り上がりで出る。
//   フルスクリーンのシーン背景＋≥3階層の奥行き。常時わずかにドリフト（紙芝居回避）。
//   全モーションにイージング/spring・opacity単独リビール無し・決定論的（frame+index+random）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

// マップ平面の描画領域（px・1920x1080基準）
const MAP_L = 236;
const MAP_T = 150;
const MAP_W = 1448;
const MAP_H = 792;

const DROP = '0 6px 26px rgba(0,0,0,0.82), 0 2px 8px rgba(0,0,0,0.9)';

type Pin = {x: number; y: number; label?: string};

export const PinDropMap: React.FC<{
  pins: Pin[];
  dur?: number;
}> = ({pins, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- 0..1 座標 → px（マップ領域内にクランプ）
  const px = (p: Pin) => MAP_L + Math.min(1, Math.max(0, p.x)) * MAP_W;
  const py = (p: Pin) => MAP_T + Math.min(1, Math.max(0, p.y)) * MAP_H;

  // ---- グループの出入り（クイックイン／クイックアウト・translateY併用で非opacity単独）
  const inEnd = sec(fps, 0.4);
  const outStart = total - sec(fps, 0.5);
  const groupO = interpolate(
    frame,
    [0, sec(fps, 0.26), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const groupY = interpolate(
    frame,
    [0, inEnd, outStart, total],
    [30, 0, 0, -26],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // ---- ホールド中の呼吸ドリフト（静止しない）
  const breath = Math.sin((frame / fps) * 1.4) * 2.4;
  const gridDrift = interpolate(frame, [0, total], [0, 26], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- マップ平面のゆっくりした登場（scaleと併用の非opacity単独）
  const plane = spring({
    frame: frame - sec(fps, 0.06),
    fps,
    config: {damping: 30, mass: 1.2, stiffness: 90},
  });
  const planeScale = interpolate(plane, [0, 1], [1.06, 1]);
  const planeO = interpolate(plane, [0, 0.5], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // ---- 抽象大陸ブロブ（決定論的に配置・外部地理データ不使用）
  const blobs = React.useMemo(
    () =>
      Array.from({length: 6}, (_, i) => ({
        cx: MAP_L + (0.12 + random('blob-x-' + i) * 0.76) * MAP_W,
        cy: MAP_T + (0.14 + random('blob-y-' + i) * 0.72) * MAP_H,
        rx: 120 + random('blob-rx-' + i) * 230,
        ry: 80 + random('blob-ry-' + i) * 150,
        rot: random('blob-rot-' + i) * 180,
      })),
    [],
  );

  // ---- タイミング定数
  const pinStart = sec(fps, 0.38);
  const pinStagger = sec(fps, 0.16);
  const settle = sec(fps, 0.42); // 着地までの目安（波紋開始基準）
  const arcStart = sec(fps, 0.6);
  const arcStagger = sec(fps, 0.14);
  const ripplePeriod = sec(fps, 1.35);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        overflow: 'hidden',
      }}
    >
      {/* 奥行き1: マップ平面（ドット・オーシャン＋緯経線グリッド＋抽象大陸ブロブ） */}
      <AbsoluteFill
        style={{
          opacity: planeO,
          transform: `scale(${planeScale}) translateY(${breath * 0.5}px)`,
        }}
      >
        {/* ドット・オーシャン */}
        <AbsoluteFill
          style={{
            opacity: 0.16,
            transform: `translateY(${gridDrift}px)`,
            backgroundImage: `radial-gradient(${BRAND.color.electric}88 1.4px, transparent 1.6px)`,
            backgroundSize: '34px 34px',
            maskImage:
              'radial-gradient(118% 92% at 50% 46%, black 26%, transparent 82%)',
            WebkitMaskImage:
              'radial-gradient(118% 92% at 50% 46%, black 26%, transparent 82%)',
          }}
        />
        {/* 緯経線グリッド */}
        <AbsoluteFill
          style={{
            opacity: 0.12,
            transform: `translateY(${-gridDrift * 0.6}px)`,
            backgroundImage: `
              repeating-linear-gradient(0deg, ${BRAND.color.silver}33 0px, ${BRAND.color.silver}33 1px, transparent 1px, transparent 96px),
              repeating-linear-gradient(90deg, ${BRAND.color.silver}33 0px, ${BRAND.color.silver}33 1px, transparent 1px, transparent 96px)`,
            maskImage:
              'radial-gradient(120% 90% at 50% 46%, black 20%, transparent 80%)',
            WebkitMaskImage:
              'radial-gradient(120% 90% at 50% 46%, black 20%, transparent 80%)',
          }}
        />
        {/* 抽象大陸ブロブ（緩やかにドリフト） */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0}}
        >
          {blobs.map((b, i) => {
            const drift = Math.sin((frame / fps) * 0.6 + i) * 6;
            return (
              <g
                key={i}
                transform={`translate(${b.cx}, ${b.cy + drift}) rotate(${b.rot})`}
              >
                <ellipse
                  rx={b.rx}
                  ry={b.ry}
                  fill={BRAND.color.electric}
                  opacity={0.07}
                />
                <ellipse
                  rx={b.rx}
                  ry={b.ry}
                  fill="none"
                  stroke={BRAND.color.electric}
                  strokeWidth={1.5}
                  opacity={0.16}
                />
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>

      {/* 奥行き2: 中央の電光グロー */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(48% 42% at 50% 48%, ${BRAND.color.electric}22 0%, transparent 70%)`,
          transform: `translateY(${breath * 0.7}px)`,
        }}
      />

      {/* 奥行き3: アーク＋波紋＋ピン頭（フルスクリーンSVG） */}
      <AbsoluteFill
        style={{opacity: groupO, transform: `translateY(${groupY + breath}px)`}}
      >
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0}}
        >
          {/* ピン間の電光アーク（順に描画される） */}
          {pins.slice(1).map((p, k) => {
            const a = pins[k];
            const b = p;
            const ax = px(a);
            const ay = py(a);
            const bx = px(b);
            const by = py(b);
            const mx = (ax + bx) / 2;
            const my = (ay + by) / 2 - Math.hypot(bx - ax, by - ay) * 0.24;
            const len = Math.hypot(bx - ax, by - ay) * 1.2 + 40;
            const s = spring({
              frame: frame - arcStart - k * arcStagger,
              fps,
              config: {damping: 26, mass: 1, stiffness: 120},
            });
            return (
              <path
                key={k}
                d={`M ${ax} ${ay} Q ${mx} ${my} ${bx} ${by}`}
                fill="none"
                stroke={BRAND.color.electric}
                strokeWidth={2}
                strokeLinecap="round"
                opacity={0.42}
                strokeDasharray={len}
                strokeDashoffset={len * (1 - s)}
              />
            );
          })}

          {/* 波紋リング（着地後にループ・拡大＝非opacity単独） */}
          {pins.map((p, i) => {
            const cx = px(p);
            const cy = py(p);
            const land = pinStart + i * pinStagger + settle;
            const rings = [0, 1].map((kk) => {
              const t0 = frame - land - kk * (ripplePeriod / 2);
              if (t0 < 0) return null;
              const tt = (t0 % ripplePeriod) / ripplePeriod;
              const eased = Easing.out(Easing.cubic)(tt);
              const r = interpolate(eased, [0, 1], [10, 96]);
              const o = interpolate(
                tt,
                [0, 0.12, 1],
                [0, 0.5, 0],
                {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
              );
              return (
                <circle
                  key={kk}
                  cx={cx}
                  cy={cy}
                  r={r}
                  fill="none"
                  stroke={BRAND.color.electric}
                  strokeWidth={2}
                  opacity={o}
                />
              );
            });
            return <g key={i}>{rings}</g>;
          })}

          {/* ピン頭（オーバーシュートspringで落下＋バウンド） */}
          {pins.map((p, i) => {
            const cx = px(p);
            const cy = py(p);
            const jitter = random('pin-j-' + i) * sec(fps, 0.05);
            const ps = spring({
              frame: frame - pinStart - i * pinStagger - jitter,
              fps,
              config: {damping: 9, mass: 0.9, stiffness: 150}, // 低damping=オーバーシュート
            });
            const drop = interpolate(ps, [0, 1], [-260, 0]); // 上から落下（overshootで沈む）
            const scl = interpolate(ps, [0, 1], [0.4, 1]);
            const o = interpolate(ps, [0, 0.22], [0, 1], {
              extrapolateRight: 'clamp',
            });
            // 落下ハイライト（落ちる間だけ縦に伸びる残像感）
            const speed = Math.max(0, 1 - Math.abs(1 - ps) * 2);
            return (
              <g key={i} opacity={o}>
                {/* 接地シャドウ（固定・呼吸） */}
                <ellipse
                  cx={cx}
                  cy={cy + 4}
                  rx={interpolate(ps, [0, 1], [4, 16])}
                  ry={interpolate(ps, [0, 1], [1.5, 5])}
                  fill="#000"
                  opacity={0.4}
                />
                <g transform={`translate(${cx}, ${cy + drop}) scale(${scl})`}>
                  {/* グロー */}
                  <circle r={26} fill={BRAND.color.electric} opacity={0.16} />
                  {/* リング */}
                  <circle
                    r={15}
                    fill={BRAND.color.navy}
                    stroke={BRAND.color.electric}
                    strokeWidth={3}
                  />
                  {/* ゴールドのコア（単一アクセント） */}
                  <circle
                    r={6}
                    fill={BRAND.color.gold}
                    opacity={0.9 + speed * 0.1}
                  />
                </g>
              </g>
            );
          })}
        </svg>

        {/* ラベル：マスク切り上がり（overflow:hidden + translateY・Trail） */}
        {pins.map((p, i) => {
          if (!p.label) return null;
          const cx = px(p);
          const cy = py(p);
          const ls = spring({
            frame: frame - pinStart - i * pinStagger - settle * 0.5,
            fps,
            config: {damping: 15, mass: 0.9, stiffness: 130},
          });
          const yy = interpolate(ls, [0, 1], [118, 0]);
          const lo = interpolate(ls, [0, 0.25], [0, 1], {
            extrapolateRight: 'clamp',
          });
          // 右にはみ出す場合は左寄せに
          const flipLeft = cx > width - 320;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: cx,
                top: cy - 74,
                transform: `translateX(${flipLeft ? '-100%' : '0'})`,
                pointerEvents: 'none',
              }}
            >
              <div style={{overflow: 'hidden', paddingBottom: '0.16em'}}>
                <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
                  <div
                    style={{
                      transform: `translateY(${yy}%)`,
                      opacity: lo,
                      padding: '8px 18px',
                      marginLeft: flipLeft ? 0 : 24,
                      marginRight: flipLeft ? 24 : 0,
                      borderRadius: 8,
                      background: `${BRAND.color.ink}cc`,
                      border: `1px solid ${BRAND.color.electric}66`,
                      color: BRAND.color.white,
                      fontFamily: BRAND.font.body,
                      fontWeight: 700,
                      fontSize: 30,
                      letterSpacing: 1.5,
                      whiteSpace: 'nowrap',
                      textShadow: DROP,
                      boxShadow: `0 0 20px ${BRAND.color.electric}22`,
                    }}
                  >
                    {p.label}
                  </div>
                </Trail>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 前景ビネット（奥行きの締め） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 46%, rgba(0,0,0,0.62) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
