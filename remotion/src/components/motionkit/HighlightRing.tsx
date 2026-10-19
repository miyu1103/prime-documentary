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
// HighlightRing — 実映像の上に重ねる「手描き風マーカー丸」オーバーレイ
//   ・(cx,cy,r) を 0..1 の画面比率で受け取り、その点を囲む楕円リングを
//     strokeDashoffset の spring で「描き足す」ように出す（等速禁止・全てイージング）。
//   ・実際のペンのように少しだけ描き越し(オーバーシュート)＋各点を乱数で微揺らし
//     → 手描きの活き感。乱数は remotion random(seed) で決定論的（Math.random禁止）。
//   ・背後にぼかしたグローの二重ストローク（同じdashoffsetで一緒に描かれる）。
//   ・描画中の先端に明るいドット＋Trailモーションブラー（速い動き対策）。
//   ・任意の label は overflow:hidden マスクで切り上がり（opacity単独リビール禁止）、
//     リング端から伸びる細いコネクタ線も dashoffset で描き込む。
//   ・描き上がった後もサインの微回転＋微ブレスで“静止しない”。
//   透明背景・pointerEvents:none（映像操作を邪魔しない）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

export const HighlightRing: React.FC<{
  cx: number;
  cy: number;
  r: number;
  label?: string;
  dur?: number;
}> = ({cx, cy, r, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- ピクセル座標（比率→px）。リングは幅基準の半径で楕円化 ----
  const CX = cx * width;
  const CY = cy * height;
  const R = r * width;
  const rx = R;
  const ry = R * 0.9;

  // ---- 手描き風パス（決定論的な乱数で各点を微揺らし＋描き越し）----
  const N = 56;
  const startA = -0.38; // 開始角
  const sweep = Math.PI * 2 + 0.5; // 一周＋少し描き越し
  const pts: {x: number; y: number}[] = [];
  for (let k = 0; k <= N; k++) {
    const t = k / N;
    const a = startA + sweep * t;
    const jit = (random('hl-ring-' + k) - 0.5) * R * 0.055;
    const wob = (random('hl-wob-' + k) - 0.5) * R * 0.03;
    pts.push({
      x: CX + (rx + jit) * Math.cos(a) + wob,
      y: CY + (ry + jit * 0.9) * Math.sin(a),
    });
  }
  const ringPath =
    'M ' +
    pts.map((p) => `${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(' L ');

  // ---- 描き込み進行（spring・イージング）----
  const drawS = spring({
    frame: frame - sec(fps, 0.08),
    fps,
    config: {damping: 30, mass: 1, stiffness: 90},
  });
  const p = interpolate(drawS, [0, 1], [0, 1], {extrapolateRight: 'clamp'});
  const PLEN = 1000;
  const dashOffset = PLEN * (1 - p);

  // ---- 先端ドットの位置（描画中に走る速い要素 → Trailでブラー）----
  const tipIdx = Math.min(N, Math.max(0, Math.floor(p * N)));
  const tip = pts[tipIdx];
  const tipO = interpolate(p, [0, 0.05, 0.9, 1], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ---- 描き上がり後の“生きてる”微回転＋微ブレス（サイン＝非等速）----
  const wobblePhase = random('hl-phase') * Math.PI * 2;
  const settle = interpolate(drawS, [0.4, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rot = Math.sin((frame / fps) * 1.15 + wobblePhase) * 0.85 * settle;
  const breath = 1 + Math.sin((frame / fps) * 0.9 + wobblePhase) * 0.006 * settle;

  // ---- 退出（scaleと併用＝opacity単独禁止）----
  const outStart = total - sec(fps, 0.5);
  const groupO = interpolate(frame, [0, sec(fps, 0.12), outStart, total], [1, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outScale = interpolate(frame, [outStart, total], [1, 1.05], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ---- グローの環境シマー（描画表現ではなく常時の生気）----
  const glowO = 0.34 + Math.sin((frame / fps) * 1.7 + wobblePhase) * 0.08;

  // ---- コネクタ線＋ラベル配置（リング右上端から外へ）----
  const edgeA = -0.62;
  const ex = CX + rx * Math.cos(edgeA);
  const ey = CY + ry * Math.sin(edgeA);
  const cLen = width * 0.055;
  const lx = ex + cLen;
  const ly = ey - cLen * 0.32;

  const connS = spring({
    frame: frame - sec(fps, 0.5),
    fps,
    config: {damping: 26, mass: 0.8, stiffness: 110},
  });
  const connP = interpolate(connS, [0, 1], [0, 1], {extrapolateRight: 'clamp'});
  const CONN_LEN = 100;

  const labelS = spring({
    frame: frame - sec(fps, 0.64),
    fps,
    config: {damping: 18, mass: 0.9, stiffness: 130},
  });
  const labelY = interpolate(labelS, [0, 1], [110, 0]);
  const labelO = interpolate(labelS, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
  const underline = interpolate(labelS, [0.25, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{background: 'transparent', pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          opacity: groupO,
          transform: `rotate(${rot}deg) scale(${breath * outScale})`,
          transformOrigin: `${cx * 100}% ${cy * 100}%`,
        }}
      >
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          style={{position: 'absolute', inset: 0, overflow: 'visible'}}
        >
          <defs>
            <filter id="hl-glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="6" />
            </filter>
          </defs>

          {/* グロー（ぼかした二重ストローク・同じdashoffsetで一緒に描かれる） */}
          <path
            d={ringPath}
            fill="none"
            stroke={BRAND.color.electric}
            strokeWidth={16}
            strokeLinecap="round"
            strokeLinejoin="round"
            pathLength={PLEN}
            strokeDasharray={PLEN}
            strokeDashoffset={dashOffset}
            opacity={glowO}
            filter="url(#hl-glow)"
          />

          {/* 本体ストローク */}
          <path
            d={ringPath}
            fill="none"
            stroke={BRAND.color.electric}
            strokeWidth={5}
            strokeLinecap="round"
            strokeLinejoin="round"
            pathLength={PLEN}
            strokeDasharray={PLEN}
            strokeDashoffset={dashOffset}
          />

          {/* コネクタ線（dashoffsetで描き込み） */}
          {label ? (
            <line
              x1={ex}
              y1={ey}
              x2={lx}
              y2={ly}
              stroke={BRAND.color.silver}
              strokeWidth={2}
              strokeLinecap="round"
              pathLength={CONN_LEN}
              strokeDasharray={CONN_LEN}
              strokeDashoffset={CONN_LEN * (1 - connP)}
              opacity={0.85}
            />
          ) : null}
        </svg>

        {/* 描画中の先端ドット（速い要素 → Trailモーションブラー） */}
        {tipO > 0.01 ? (
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <div
              style={{
                position: 'absolute',
                left: tip.x,
                top: tip.y,
                width: 16,
                height: 16,
                marginLeft: -8,
                marginTop: -8,
                borderRadius: '50%',
                opacity: tipO,
                background: `radial-gradient(circle, ${BRAND.color.white} 0%, ${BRAND.color.electric} 45%, rgba(31,107,255,0) 72%)`,
              }}
            />
          </Trail>
        ) : null}

        {/* ラベル（overflow:hiddenのマスク切り上がり） */}
        {label ? (
          <div
            style={{
              position: 'absolute',
              left: lx + 10,
              top: ly,
              transform: 'translateY(-50%)',
            }}
          >
            <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
              <div
                style={{
                  transform: `translateY(${labelY}%)`,
                  opacity: labelO,
                  color: BRAND.color.white,
                  fontFamily: BRAND.font.display,
                  fontWeight: 900,
                  fontSize: 40,
                  lineHeight: 1.02,
                  letterSpacing: 0.5,
                  textTransform: 'uppercase',
                  whiteSpace: 'nowrap',
                  textShadow: '0 3px 18px rgba(0,0,0,0.85), 0 1px 4px rgba(0,0,0,0.9)',
                }}
              >
                {label}
              </div>
            </div>
            {/* 下線（scaleXで伸びる・ゴールドアクセント） */}
            <div
              style={{
                marginTop: 4,
                height: 3,
                width: '100%',
                background: BRAND.color.gold,
                borderRadius: 2,
                transform: `scaleX(${underline})`,
                transformOrigin: 'left center',
                boxShadow: `0 0 12px ${BRAND.color.gold}aa`,
              }}
            />
          </div>
        ) : null}
      </div>
    </AbsoluteFill>
  );
};
