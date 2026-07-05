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
// MOTIONKIT — RadialGauge
//   ULTRA-PREMIUM な計器風フル円弧ダイヤル（ProbableCauseMeter の横メーターとは別物）。
//   ・目盛り付きの円弧（major＋minor tick）に沿って、針が 0→value/max まで
//     オーバーシュートして整定する spring で掃引 → 高速掃引は Trail でブラー。
//   ・アクティブ円弧は上昇に応じて electric→gold にカラー遷移し、柔らかいグロー。
//   ・中央の大きな tabular-nums 読取り値がカウントアップ。
//   ・label は overflow:hidden＋translateY のマスク切れ上がり。
//   ・整定後も針は微小なジッター/ブレスで常に生きている（凍結禁止）。
// 品質ルール: 等速線形なし・opacity単独なし・テキストはマスク切れ上がり・
//   決定論(useCurrentFrame のみ)・単一アクセント・色は BRAND トークンのみ。
// =====================================================================

const C = BRAND.color;
const SCENE_BG = '#06080f';

// 秒→フレーム（フレーム直書き禁止・fps から算出）
const sec = (fps: number, s: number): number => Math.round(fps * s);

// 極座標: deg は上(12時)=0・時計回り。screen座標へ。
const polar = (cx: number, cy: number, r: number, deg: number) => {
  const rad = ((deg - 90) * Math.PI) / 180;
  return {x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad)};
};

// SVG 円弧パス（start→end を時計回りに）
const arcPath = (
  cx: number,
  cy: number,
  r: number,
  startDeg: number,
  endDeg: number,
): string => {
  const a = polar(cx, cy, r, startDeg);
  const b = polar(cx, cy, r, endDeg);
  const large = Math.abs(endDeg - startDeg) > 180 ? 1 : 0;
  return `M ${a.x} ${a.y} A ${r} ${r} 0 ${large} 1 ${b.x} ${b.y}`;
};

// 16進カラーの線形補間（electric→gold のフィル用・決定論）
const parseHex = (h: string): [number, number, number] => {
  const s = h.replace('#', '');
  return [
    parseInt(s.slice(0, 2), 16),
    parseInt(s.slice(2, 4), 16),
    parseInt(s.slice(4, 6), 16),
  ];
};
const toHex = (n: number): string =>
  Math.max(0, Math.min(255, Math.round(n))).toString(16).padStart(2, '0');
const lerpColor = (a: string, b: string, t: number): string => {
  const A = parseHex(a);
  const B = parseHex(b);
  return `#${toHex(A[0] + (B[0] - A[0]) * t)}${toHex(
    A[1] + (B[1] - A[1]) * t,
  )}${toHex(A[2] + (B[2] - A[2]) * t)}`;
};

// マスク切れ上がり（overflow:hidden + translateY、opacity単独禁止なので必ず併用）
const MaskReveal: React.FC<{
  delay: number;
  children: React.ReactNode;
  distance?: number;
  damping?: number;
}> = ({delay, children, distance = 118, damping = 18}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping, mass: 1}});
  const y = interpolate(s, [0, 1], [distance, 0]);
  const o = interpolate(s, [0, 0.32], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{display: 'block', overflow: 'hidden', paddingBottom: '0.14em'}}
    >
      <span
        style={{display: 'block', transform: `translateY(${y}%)`, opacity: o}}
      >
        {children}
      </span>
    </span>
  );
};

export const RadialGauge: React.FC<{
  value: number;
  max?: number;
  label?: string;
  dur?: number;
}> = ({value, max = 100, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // ---- 幾何 ------------------------------------------------------------
  const cx = width / 2; // 960
  const cy = height / 2 - 20; // 520：下側に読取り値の余白
  const R = 360; // 円弧半径
  const TW = 20; // 円弧の太さ
  const START = 225; // 開始角（左下・7:30）
  const SWEEP = 270; // 掃引角（下開き・時計回り 270°）
  const needleLen = R - 34;
  const tailLen = 54; // カウンターウェイト側
  const baseHalf = 10; // 針の根元の半幅

  // ---- 目標値（0..1） --------------------------------------------------
  const safeMax = max === 0 ? 1 : max;
  const target = Math.max(0, Math.min(1, value / safeMax));

  // ---- タイムライン（秒基準・全て定数化） ------------------------------
  const sweepStart = sec(fps, 0.3);
  const countStart = sec(fps, 0.35);
  const countEnd = sec(fps, 1.7);
  const tickStart = sec(fps, 0.14);
  const tickStep = sec(fps, 0.014);

  // ---- 針の掃引: オーバーシュート整定 spring（等速禁止・過減衰でない） ----
  const sweepSpring = spring({
    frame: frame - sweepStart,
    fps,
    config: {damping: 12, mass: 1, stiffness: 120},
  });

  // ---- 整定後の微ジッター/ブレス（決定論・凍結防止） -------------------
  const arrived = interpolate(frame, [countEnd, countEnd + sec(fps, 0.4)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const t = frame / fps;
  const jitterDeg =
    arrived *
    (0.55 * Math.sin(t * Math.PI * 2 * 0.55) +
      0.22 * Math.sin(t * Math.PI * 2 * 1.7));

  // 針の現在割合（わずかなオーバーシュートを許容→実計器の跳ね返り）
  const needleFrac = Math.max(0, Math.min(1.03, target * sweepSpring));
  const arcFrac = Math.max(0, Math.min(1, target * sweepSpring));
  const needleDeg = START + needleFrac * SWEEP + jitterDeg;

  // アクティブ色（上昇に応じて electric→gold）とグロー
  const activeColor = lerpColor(C.electric, C.gold, arcFrac);
  const glowPulse = 0.5 + 0.5 * Math.sin(t * Math.PI * 2 * 0.35);
  const glowBlur = 14 + arcFrac * 26 + glowPulse * 8;

  // ---- 読取り値カウントアップ（cubic out・等速禁止） -------------------
  const countP = interpolate(frame, [countStart, countEnd], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const shownValue = Math.round(value * countP).toLocaleString('en-US');

  // ---- 全体の呼吸（sin・非線形） --------------------------------------
  const breathScale = 1 + 0.006 * Math.sin(t * Math.PI * 2 * 0.16);

  // ---- 背景ドリフト ----------------------------------------------------
  const drift = interpolate(frame, [0, D], [0, 22], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });

  // ---- シーン出入り（opacity＋微translateY） ---------------------------
  const sceneO = interpolate(frame, [0, 12, D - 14, D], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sceneY = interpolate(frame, [0, 14], [24, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // ---- 目盛り（major/minor）：長さが伸びて出る（opacity単独禁止） -----
  const N = 50; // 分割数（minor 単位）
  const ticks = Array.from({length: N + 1}, (_, i) => {
    const f = i / N;
    const isMajor = i % 5 === 0;
    const isLabeled = i % 10 === 0;
    return {i, f, deg: START + f * SWEEP, isMajor, isLabeled};
  });

  // 針ベクトル
  const rad = ((needleDeg - 90) * Math.PI) / 180;
  const ux = Math.cos(rad);
  const uy = Math.sin(rad);
  const perpX = -uy;
  const perpY = ux;
  const tip = {x: cx + ux * needleLen, y: cy + uy * needleLen};
  const tail = {x: cx - ux * tailLen, y: cy - uy * tailLen};
  const b1 = {x: cx + perpX * baseHalf, y: cy + perpY * baseHalf};
  const b2 = {x: cx - perpX * baseHalf, y: cy - perpY * baseHalf};
  const needlePts = `${tail.x},${tail.y} ${b1.x},${b1.y} ${tip.x},${tip.y} ${b2.x},${b2.y}`;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: SCENE_BG,
        opacity: sceneO,
        transform: `translateY(${sceneY}px)`,
      }}
    >
      {/* ---- 奥行き1: 指定の全画面グラデ背景 ---- */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${C.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* ---- 奥行き2: 微細な同心リング（electric・ゆっくりドリフト） ---- */}
      <AbsoluteFill
        style={{
          opacity: 0.5,
          transform: `translateY(${drift}px)`,
          backgroundImage: `repeating-radial-gradient(circle at 50% 47%, ${C.electric}12 0px, ${C.electric}12 1px, transparent 1px, transparent 44px)`,
          maskImage:
            'radial-gradient(62% 62% at 50% 47%, black 6%, transparent 76%)',
          WebkitMaskImage:
            'radial-gradient(62% 62% at 50% 47%, black 6%, transparent 76%)',
        }}
      />

      {/* ---- 奥行き3: 中央アクセントグロー（値に応じて色/強度が上昇・拍動） ---- */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 40% at 50% 47%, ${activeColor}2e 0%, transparent 70%)`,
          opacity: 0.45 + arcFrac * 0.4 + glowPulse * 0.12,
        }}
      />

      {/* ---- 奥行き4: ビネット ---- */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(125% 100% at 50% 47%, transparent 42%, rgba(0,0,0,0.62) 100%)',
        }}
      />

      {/* ================= ダイヤル本体（呼吸スケール） ================= */}
      <AbsoluteFill style={{transform: `scale(${breathScale})`}}>
        {/* 目盛りと数値 */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
        >
          {/* トラック円弧（未充填） */}
          <path
            d={arcPath(cx, cy, R, START, START + SWEEP)}
            fill="none"
            stroke={C.silver}
            strokeOpacity={0.14}
            strokeWidth={TW}
            strokeLinecap="round"
          />

          {/* 目盛り（長さが伸びて出る・スタッガー） */}
          {ticks.map((tk) => {
            const s = spring({
              frame: frame - tickStart - tk.i * tickStep,
              fps,
              config: {damping: 22, mass: 0.7},
            });
            const grow = interpolate(s, [0, 1], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const len = (tk.isMajor ? 30 : 16) * grow;
            const rIn = R + TW / 2 + 8;
            const rOut = rIn + len;
            const p1 = polar(cx, cy, rIn, tk.deg);
            const p2 = polar(cx, cy, rOut, tk.deg);
            const active = tk.f <= arcFrac + 0.0001;
            return (
              <line
                key={tk.i}
                x1={p1.x}
                y1={p1.y}
                x2={p2.x}
                y2={p2.y}
                stroke={active ? activeColor : C.silver}
                strokeOpacity={active ? 0.95 : tk.isMajor ? 0.4 : 0.22}
                strokeWidth={tk.isMajor ? 3 : 1.5}
                strokeLinecap="round"
              />
            );
          })}

          {/* 目盛り数値（major の一部） */}
          {ticks
            .filter((tk) => tk.isLabeled)
            .map((tk) => {
              const s = spring({
                frame: frame - tickStart - tk.i * tickStep - sec(fps, 0.1),
                fps,
                config: {damping: 20, mass: 0.8},
              });
              const grow = interpolate(s, [0, 1], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const rLbl = R + TW / 2 + 66;
              const p = polar(cx, cy, rLbl, tk.deg);
              const active = tk.f <= arcFrac + 0.0001;
              const num = Math.round(tk.f * safeMax).toLocaleString('en-US');
              return (
                <text
                  key={`l-${tk.i}`}
                  x={p.x}
                  y={p.y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill={active ? activeColor : C.silver}
                  fillOpacity={active ? 0.95 : 0.5}
                  fontFamily={BRAND.font.body}
                  fontSize={24}
                  fontWeight={700}
                  style={{
                    fontVariantNumeric: 'tabular-nums',
                    transform: `translateY(${(1 - grow) * 10}px)`,
                    transformOrigin: `${p.x}px ${p.y}px`,
                    opacity: grow,
                  }}
                >
                  {num}
                </text>
              );
            })}
        </svg>

        {/* アクティブ円弧（electric→gold・グロー） */}
        {arcFrac > 0.001 ? (
          <svg
            width={width}
            height={height}
            style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
          >
            <path
              d={arcPath(cx, cy, R, START, START + arcFrac * SWEEP)}
              fill="none"
              stroke={activeColor}
              strokeWidth={TW}
              strokeLinecap="round"
              style={{filter: `drop-shadow(0 0 ${glowBlur}px ${activeColor}bb)`}}
            />
          </svg>
        ) : null}

        {/* 針（高速掃引は Trail でモーションブラー） */}
        <Trail layers={6} lagInFrames={1.2} trailOpacity={0.3}>
          <svg
            width={width}
            height={height}
            style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
          >
            <polygon
              points={needlePts}
              fill={C.white}
              style={{filter: `drop-shadow(0 0 12px ${activeColor}aa)`}}
            />
            {/* 針先の輝点 */}
            <circle cx={tip.x} cy={tip.y} r={7} fill={activeColor} />
          </svg>
        </Trail>

        {/* ハブ（中心軸） */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
        >
          <circle
            cx={cx}
            cy={cy}
            r={28}
            fill={C.navy}
            stroke={C.silver}
            strokeOpacity={0.5}
            strokeWidth={2}
          />
          <circle cx={cx} cy={cy} r={14} fill={SCENE_BG} />
          <circle cx={cx} cy={cy} r={6} fill={activeColor} />
        </svg>

        {/* 中央の読取り値（カウントアップ・tabular-nums）＋ /max ＋ label */}
        <div
          style={{
            position: 'absolute',
            left: cx,
            top: cy + 150,
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            width: R * 1.6,
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'baseline',
              justifyContent: 'center',
              gap: 6,
            }}
          >
            <span
              style={{
                fontFamily: BRAND.font.display,
                fontSize: 150,
                lineHeight: 0.9,
                letterSpacing: -2,
                color: C.white,
                fontVariantNumeric: 'tabular-nums',
                textShadow: `0 0 34px ${activeColor}66`,
              }}
            >
              {shownValue}
            </span>
            <span
              style={{
                fontFamily: BRAND.font.body,
                fontSize: 42,
                fontWeight: 700,
                color: C.silver,
                opacity: 0.7,
                fontVariantNumeric: 'tabular-nums',
              }}
            >
              /{Math.round(safeMax).toLocaleString('en-US')}
            </span>
          </div>

          {label ? (
            <div style={{marginTop: 8}}>
              <MaskReveal delay={sec(fps, 0.7)} distance={110}>
                <span
                  style={{
                    fontFamily: BRAND.font.body,
                    fontSize: 30,
                    fontWeight: 600,
                    letterSpacing: 8,
                    textTransform: 'uppercase',
                    color: C.electric,
                    display: 'block',
                  }}
                >
                  {label}
                </span>
              </MaskReveal>
            </div>
          ) : null}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
