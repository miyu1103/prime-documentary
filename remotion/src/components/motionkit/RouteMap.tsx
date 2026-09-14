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
// RouteMap — MOTIONKIT
//   ダークな抽象マップ平面の上を、発光するルート線がピン間を点→点で
//   描き進む（strokeDashoffset spring）。線の先端をエレクトリックな
//   グリント(Trail)が走る。各ピンはドロップ(spring+スカッシュ)し、
//   ラベルがマスク切れ上がりでスタッガー表示。マップ全体に微視差パララックス。
//
// 品質ルール準拠:
//   - 全モーションに easing / spring（等速線形なし）
//   - opacity単独の演出なし（必ず translate/scale と併用）
//   - テキストは overflow:hidden + inner translateY のマスク切れ上がり
//   - 速い先端グリントは <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
//   - 完全に決定論的（useCurrentFrame + index + remotion random、Math.random不使用）
//   - 尺は fps から算出、never fully static、フルスクリーン背景 + 3層以上の奥行き
// =====================================================================

type Pin = {x: number; y: number; label?: string};

type Pt = {x: number; y: number};

type Seg = {x: number; y: number; x2: number; y2: number; len: number};

// 秒→フレーム
const sec = (fps: number, s: number): number => Math.round(fps * s);

const lerp = (a: number, b: number, t: number): number => a + (b - a) * t;

export const RouteMap: React.FC<{
  pins: Pin[];
  dur?: number;
}> = ({pins, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // --- ピクセル座標へ写像（0..1 → 画面） ---------------------------------
  const pts: Pt[] = pins.map((p) => ({x: p.x * width, y: p.y * height}));

  // --- ルートの折れ線セグメントと累積長 ---------------------------------
  const segs: Seg[] = [];
  const cumAtPin: number[] = [0];
  let total = 0;
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i];
    const b = pts[i + 1];
    const len = Math.hypot(b.x - a.x, b.y - a.y);
    segs.push({x: a.x, y: a.y, x2: b.x, y2: b.y, len});
    total += len;
    cumAtPin.push(total);
  }
  const totalLen = total || 1;

  // 進捗 t(0..1) におけるルート上の点
  const pointAt = (t: number): Pt => {
    if (segs.length === 0) return pts[0] ?? {x: width / 2, y: height / 2};
    const targetD = t * totalLen;
    let acc = 0;
    for (const s of segs) {
      if (acc + s.len >= targetD) {
        const local = s.len === 0 ? 0 : (targetD - acc) / s.len;
        return {x: lerp(s.x, s.x2, local), y: lerp(s.y, s.y2, local)};
      }
      acc += s.len;
    }
    return pts[pts.length - 1];
  };

  // --- ルート描画 spring（滑らか・非バウンド） ---------------------------
  const drawStart = sec(fps, 0.35);
  const drawFrames = sec(fps, 1.7);
  const draw = spring({
    frame: frame - drawStart,
    fps,
    config: {damping: 42, mass: 1.2, stiffness: 120},
    durationInFrames: drawFrames,
  });
  const dashOffset = totalLen * (1 - draw);
  const tip = pointAt(Math.max(0.0001, Math.min(1, draw)));

  // グリントは描画中は移動、着地後も微パルスで静止させない
  const glintScale =
    interpolate(
      Math.sin((frame / fps) * Math.PI * 2 * 1.6),
      [-1, 1],
      [0.82, 1.18],
    ) * interpolate(draw, [0, 0.06], [0.2, 1], {extrapolateRight: 'clamp'});

  // --- 微視差パララックス（sin easing、決して静止しない） ----------------
  const px = interpolate(
    Math.sin((frame / fps) * Math.PI * 2 * 0.08),
    [-1, 1],
    [-14, 14],
  );
  const py = interpolate(
    Math.cos((frame / fps) * Math.PI * 2 * 0.06),
    [-1, 1],
    [-9, 9],
  );
  const gridDrift = interpolate(frame, [0, D], [0, 46], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });

  // --- シーンの出入り（opacity単独禁止 → translateYと併用） --------------
  const inP = spring({frame, fps, config: {damping: 200}, durationInFrames: sec(fps, 0.5)});
  const sceneY = interpolate(inP, [0, 1], [26, 0]);
  const outO = interpolate(frame, [D - sec(fps, 0.4), D], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outY = interpolate(frame, [D - sec(fps, 0.4), D], [0, -18], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const {ink, navy, electric, silver, gold, white} = BRAND.color;

  // --- 決定論的な奥行きスペック（星/塵） --------------------------------
  const specks = Array.from({length: 54}, (_, i) => ({
    x: random(`sx-${i}`) * width,
    y: random(`sy-${i}`) * height,
    r: 0.6 + random(`sr-${i}`) * 1.8,
    tw: random(`st-${i}`),
  }));

  // --- 抽象化した簡易ランドマス（ハンドオーサリング・地理的正確さ不要） ---
  const landmasses = [
    'M120 260 Q300 180 520 250 Q700 300 640 470 Q540 600 340 560 Q160 520 120 400 Z',
    'M1240 180 Q1470 120 1700 220 Q1860 300 1780 470 Q1660 590 1440 540 Q1250 500 1240 360 Z',
    'M760 620 Q980 560 1180 640 Q1320 700 1240 860 Q1100 970 900 920 Q740 870 760 720 Z',
  ];

  return (
    <AbsoluteFill style={{opacity: outO}}>
      {/* Layer 1: フルスクリーン背景（正典グラデ） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 決定論的な奥行きスペック（微発光の塵） */}
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="none"
        style={{position: 'absolute', inset: 0}}
      >
        {specks.map((s, i) => {
          const tw = interpolate(
            Math.sin((frame / fps) * Math.PI * 2 * (0.4 + s.tw) + i),
            [-1, 1],
            [0.12, 0.5],
          );
          const rr = s.r * interpolate(tw, [0.12, 0.5], [0.75, 1.15]);
          return <circle key={i} cx={s.x} cy={s.y} r={rr} fill={silver} opacity={tw} />;
        })}
      </svg>

      {/* パララックスするマップ平面（グリッド + ランドマス + ルート + ピン） */}
      <AbsoluteFill
        style={{
          transform: `translate(${px}px, ${py}px) translateY(${sceneY + outY}px)`,
        }}
      >
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="none"
          style={{position: 'absolute', inset: 0}}
        >
          <defs>
            <filter id="rm-glow" x="-40%" y="-40%" width="180%" height="180%">
              <feGaussianBlur stdDeviation="7" result="b" />
              <feMerge>
                <feMergeNode in="b" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <filter id="rm-softglow" x="-60%" y="-60%" width="220%" height="220%">
              <feGaussianBlur stdDeviation="16" />
            </filter>
          </defs>

          {/* Layer 3a: 発光ハロー（奥のグロー） */}
          <ellipse
            cx={width * 0.5}
            cy={height * 0.44}
            rx={width * 0.42}
            ry={height * 0.34}
            fill={electric}
            opacity={0.1}
            filter="url(#rm-softglow)"
          />

          {/* Layer 3b: 簡易ランドマス（抽象ベクトル大陸） */}
          <g opacity={0.5} transform={`translate(0 ${gridDrift * 0.15})`}>
            {landmasses.map((d, i) => (
              <path
                key={i}
                d={d}
                fill={electric}
                fillOpacity={0.06}
                stroke={silver}
                strokeOpacity={0.14}
                strokeWidth={1.4}
              />
            ))}
          </g>

          {/* Layer 4: グリッド・グラティキュール（微・ドリフト） */}
          <g
            opacity={0.16}
            transform={`translate(0 ${gridDrift})`}
            style={{
              maskImage: 'radial-gradient(115% 90% at 50% 44%, black 32%, transparent 84%)',
            }}
          >
            {Array.from({length: 17}, (_, i) => {
              const gx = (width / 16) * i;
              return (
                <line
                  key={`v${i}`}
                  x1={gx}
                  y1={-80}
                  x2={gx}
                  y2={height + 80}
                  stroke={electric}
                  strokeWidth={1}
                />
              );
            })}
            {Array.from({length: 11}, (_, i) => {
              const gy = (height / 10) * i;
              return (
                <line
                  key={`h${i}`}
                  x1={0}
                  y1={gy}
                  x2={width}
                  y2={gy}
                  stroke={electric}
                  strokeWidth={1}
                />
              );
            })}
          </g>

          {/* Layer 5: ルート線（グロー下地 + 本線を strokeDashoffset で描画） */}
          {segs.length > 0 && (
            <g>
              <path
                d={routeD(pts)}
                fill="none"
                stroke={electric}
                strokeWidth={9}
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeOpacity={0.28}
                strokeDasharray={totalLen}
                strokeDashoffset={dashOffset}
                filter="url(#rm-glow)"
              />
              <path
                d={routeD(pts)}
                fill="none"
                stroke={white}
                strokeWidth={2.4}
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeDasharray={totalLen}
                strokeDashoffset={dashOffset}
              />
            </g>
          )}
        </svg>

        {/* Layer 6a: 先端グリント（Trail でモーションブラー） */}
        {draw > 0.001 && draw < 0.999 && segs.length > 0 && (
          <AbsoluteFill style={{pointerEvents: 'none'}}>
            <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
              <div
                style={{
                  position: 'absolute',
                  left: tip.x,
                  top: tip.y,
                  width: 26,
                  height: 26,
                  marginLeft: -13,
                  marginTop: -13,
                  borderRadius: '50%',
                  background: `radial-gradient(circle, ${white} 0%, ${electric} 45%, rgba(31,107,255,0) 72%)`,
                  transform: `scale(${glintScale})`,
                  boxShadow: `0 0 22px ${electric}, 0 0 44px ${electric}88`,
                }}
              />
            </Trail>
          </AbsoluteFill>
        )}

        {/* Layer 6b: ピン（ドロップ + スカッシュ）＋ ラベル（マスク切れ上がり） */}
        {pins.map((p, i) => {
          const cx = p.x * width;
          const cy = p.y * height;
          // ルート先端がそのピンに到達する頃に着地させる
          const frac = cumAtPin[i] / totalLen;
          const startF = drawStart + frac * drawFrames;

          const dropRaw = spring({
            frame: frame - startF,
            fps,
            config: {damping: 11, mass: 0.9, stiffness: 140},
          });
          const drop = Math.max(0, dropRaw);
          const dropY = interpolate(drop, [0, 1], [-90, 0], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          // 着地スカッシュ（縦つぶれ→戻り）
          const squash = interpolate(
            drop,
            [0.42, 0.58, 0.8, 1],
            [1, 0.68, 1.12, 1],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
          );
          const sx = 1 / squash;
          const sy = squash;
          const appear = interpolate(drop, [0, 0.18], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });

          // 着地後の常時パルス（never static、scale主体）
          const landed = interpolate(drop, [0.7, 1], [0, 1], {extrapolateLeft: 'clamp'});
          const pulse = interpolate(
            Math.sin((frame - startF) / fps * Math.PI * 2 * 1.1),
            [-1, 1],
            [1, 1.9],
          );

          // ラベル・マスク切れ上がり
          const labelStart = startF + sec(fps, 0.16);
          const labelP = spring({
            frame: frame - labelStart,
            fps,
            config: {damping: 16, mass: 0.9},
          });
          const labelY = interpolate(labelP, [0, 1], [110, 0]);
          const labelO = interpolate(labelP, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: cx,
                top: cy,
                transform: `translate(-50%, -100%) translateY(${dropY}px)`,
                transformOrigin: 'bottom center',
                opacity: appear,
              }}
            >
              {/* ピンのマーカー本体（下端＝地図座標に接地・スカッシュ） */}
              <div
                style={{
                  transform: `scale(${sx}, ${sy})`,
                  transformOrigin: 'bottom center',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <svg width={40} height={52} viewBox="0 0 40 52" style={{display: 'block', overflow: 'visible'}}>
                  {/* 着地パルスリング（scale主体） */}
                  <circle
                    cx={20}
                    cy={44}
                    r={7 * pulse}
                    fill="none"
                    stroke={gold}
                    strokeWidth={2}
                    opacity={landed * interpolate(pulse, [1, 1.9], [0.6, 0])}
                  />
                  {/* しずく型ピン */}
                  <path
                    d="M20 4 C9 4 2 12 2 22 C2 33 14 40 20 50 C26 40 38 33 38 22 C38 12 31 4 20 4 Z"
                    fill={navy}
                    stroke={electric}
                    strokeWidth={2.5}
                  />
                  <circle cx={20} cy={22} r={7} fill={electric} />
                  <circle cx={20} cy={22} r={3} fill={white} />
                  {/* 接地シャドウ */}
                  <ellipse cx={20} cy={50} rx={9} ry={2.4} fill={ink} opacity={0.4} />
                </svg>
              </div>

              {/* ラベル（overflow:hidden + inner translateY のマスク切れ上がり） */}
              {p.label ? (
                <div
                  style={{
                    position: 'absolute',
                    left: '50%',
                    top: '100%',
                    transform: 'translateX(-50%)',
                    marginTop: 6,
                    overflow: 'hidden',
                    paddingBottom: '0.14em',
                    opacity: labelO,
                  }}
                >
                  <div
                    style={{
                      transform: `translateY(${labelY}%)`,
                      whiteSpace: 'nowrap',
                      fontFamily: BRAND.font.body,
                      fontWeight: 700,
                      fontSize: 26,
                      letterSpacing: 1.5,
                      textTransform: 'uppercase',
                      color: white,
                      padding: '4px 12px',
                      borderRadius: 6,
                      background: 'rgba(6,8,15,0.55)',
                      border: `1px solid ${electric}55`,
                      textShadow: `0 2px 10px ${ink}`,
                    }}
                  >
                    {p.label}
                  </div>
                </div>
              ) : null}
            </div>
          );
        })}
      </AbsoluteFill>

      {/* Layer 7: 上からのビネット（奥行き締め） */}
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

// ルート折れ線の SVG path 文字列
const routeD = (pts: Pt[]): string =>
  pts.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
