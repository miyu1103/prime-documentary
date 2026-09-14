/**
 * BodyLine — an ORIGINAL, Florence-only animation (not a reused template).
 * Story beat: "The Constitution draws a line around your body." A single
 * anonymous, faceless FULL STANDING silhouette stands in the dark, rim-lit from
 * the left. A single line of GOLD light draws itself as a protective boundary /
 * aura around the body — the constitutional limit. Then a cold institutional
 * element (a blue scan edge + encroaching shadow) presses in from the side
 * against the gold line. The line flexes, brightens at the contact point — but
 * holds, barely. Dignity vs. the state. No face, no nudity: an abstract
 * silhouette only. Self-contained (no image assets). 180f=6s.
 */
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../../brand';
import {DustMotes, FilmGrain, VignetteBreath} from '../../components/motionkit';

export const bodyLineDuration = 180;

const sec = (fps: number, s: number) => Math.round(fps * s);

// --- geometry (single SVG viewBox so figure / aura / press stay aligned) ---
const vbW = 800, vbH = 800;
const cx = 400;            // figure centre-line
const cyA = 420;           // gold aura centre
const rxA = 196, ryA = 348; // gold aura (a tall mandorla hugging the figure)

// Right-half outline of a dignified standing figure, expressed as [dx, y] from
// the centre-line (dx>=0). Head → neck → broad shoulders → waist → hips → legs →
// feet, ending on the centre-line with a slight upward notch = gap between legs.
const RIGHT: Array<[number, number]> = [
  [0, 112],   // crown (on axis)
  [34, 122],  // crown right (rounds the dome)
  [54, 156],  // head widest
  [50, 196],  // jaw
  [26, 220],  // under-jaw
  [22, 238],  // neck (natural, not pinched)
  [98, 270],  // shoulder
  [92, 340],  // upper arm / chest
  [80, 416],  // waist (mild taper — dignified, not hourglass)
  [88, 482],  // hip
  [84, 542],  // upper thigh
  [60, 620],  // knee
  [48, 696],  // shin
  [42, 740],  // ankle
  [50, 756],  // foot (slight forward)
  [14, 754],  // inner foot (near axis, low)
  [0, 548],   // crotch (axis, high → legs split into two)
];

// Build the closed, symmetric outline points (right side top→bottom, then the
// mirrored left side bottom→top).
const figurePoints = (): Array<[number, number]> => {
  const pts: Array<[number, number]> = [];
  for (const [dx, y] of RIGHT) pts.push([cx + dx, y]);
  for (let i = RIGHT.length - 2; i >= 1; i--) pts.push([cx - RIGHT[i][0], RIGHT[i][1]]);
  return pts;
};

// Closed Catmull-Rom → cubic Bézier: smooth, organic silhouette (no hard joints).
const smoothClosedPath = (pts: Array<[number, number]>): string => {
  const n = pts.length;
  let d = `M ${pts[0][0].toFixed(2)} ${pts[0][1].toFixed(2)} `;
  for (let i = 0; i < n; i++) {
    const p0 = pts[(i - 1 + n) % n];
    const p1 = pts[i];
    const p2 = pts[(i + 1) % n];
    const p3 = pts[(i + 2) % n];
    const b1x = p1[0] + (p2[0] - p0[0]) / 6;
    const b1y = p1[1] + (p2[1] - p0[1]) / 6;
    const b2x = p2[0] - (p3[0] - p1[0]) / 6;
    const b2y = p2[1] - (p3[1] - p1[1]) / 6;
    d += `C ${b1x.toFixed(2)} ${b1y.toFixed(2)} ${b2x.toFixed(2)} ${b2y.toFixed(2)} ${p2[0].toFixed(2)} ${p2[1].toFixed(2)} `;
  }
  return d + 'Z';
};

const FIGURE_D = smoothClosedPath(figurePoints());

export const BodyLine: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // --- timeline anchors (derived from fps) ---
  const figureAt = sec(fps, 0.2); // シルエットが立ち上がる
  const ringFrom = sec(fps, 0.9); // 金の境界線が描かれ始める
  const ringTo = sec(fps, 3.0); // 金の境界線が描き終わる
  const pressFrom = sec(fps, 3.1); // 冷たい institutional な圧が入ってくる
  const pressTo = sec(fps, 4.4); // 圧が境界に達する（以降 hold）

  // 常時の微かな呼吸（シルエット・静止フレームを作らない）
  const bodyBreath = interpolate(Math.sin((f / fps) * 1.1), [-1, 1], [0.995, 1.005], {easing: Easing.inOut(Easing.sin)});
  const bodyDriftY = interpolate(Math.sin((f / fps) * 0.7 + 1.2), [-1, 1], [-4, 4], {easing: Easing.inOut(Easing.sin)});

  // シルエット登場（下からせり上がり + フェード）
  const figS = spring({frame: f - figureAt, fps, config: {damping: 200}, durationInFrames: 30});
  const figOp = figS;
  const figY = (1 - figS) * 46;

  // 金の境界線の描画進捗（0→1, eased）
  const ringP = interpolate(f, [ringFrom, ringTo], [0, 1], {
    easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });

  // 冷たい blue の圧（右外から境界のすぐ外まで押し寄せ、ease-out で減速）
  const pressP = interpolate(f, [pressFrom, pressTo], [0, 1], {
    easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
  });
  // 接触後の微かな震え（保持しているが「barely」）＋境界の押し込み
  const contact = interpolate(f, [pressTo - sec(fps, 0.3), pressTo], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const tremor = contact * Math.sin((f - (pressTo - sec(fps, 0.3))) * 2.3) * 1.6;
  // 接触点で金線がわずかにへこむ（flex）が、破れはしない
  const dent = contact * 8;
  // 接触で金のグローが強まる（持ちこたえる証）
  const holdGlow = interpolate(contact, [0, 1], [10, 32]);

  // 金の境界の右頂点（接触点）。dent で全体がわずかに内側へ押される。
  const auraShift = dent * 0.4;
  const contactX = cx + rxA - auraShift; // 接触点の x（金線上）
  // blue の圧の x 位置（右外 → 接触点にわずかに食い込む）。ease-out で減速。
  const pressX = interpolate(pressP, [0, 1], [vbW + 120, contactX - 3]);

  const svgSize = Math.min(width, height) * 0.94;

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, justifyContent: 'center', alignItems: 'center', overflow: 'hidden'}}>
      {/* L1 背景グラデ（暗い institutional な冷たさ・下方はさらに沈む） */}
      <AbsoluteFill style={{background: `radial-gradient(115% 92% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 66%)`}} />

      {/* L1.5 図形背後の柔らかい保護光（ボリューメトリックな暖かい gold の場） */}
      <AbsoluteFill style={{
        opacity: interpolate(figS, [0, 1], [0, 1]) * interpolate(ringP, [0, 1], [0.18, 0.4]),
        background: `radial-gradient(38% 46% at 50% 44%, ${BRAND.color.gold}22 0%, transparent 68%)`,
        mixBlendMode: 'screen',
      }} />

      {/* L2 冷たい blue の encroaching shadow（右から。境界外で止まる） */}
      <AbsoluteFill style={{
        opacity: pressP * 0.9,
        background: `linear-gradient(90deg, transparent 0%, transparent ${(pressX / vbW) * 100 - 6}%, ${BRAND.color.electric}22 ${(pressX / vbW) * 100}%, ${BRAND.color.electric}55 100%)`,
      }} />

      {/* L3 主役：シルエット + 金の境界 + blue の圧（単一 SVG） */}
      <svg
        viewBox={`0 0 ${vbW} ${vbH}`}
        width={svgSize}
        height={svgSize}
        style={{position: 'absolute', transform: `translateY(${figY + bodyDriftY}px)`, overflow: 'visible'}}
      >
        <defs>
          {/* 図形の陰影：左からのリムライト（左＝白/銀、右＝navy の陰）で立体に */}
          <linearGradient id="bl-body" gradientUnits="userSpaceOnUse" x1={cx - 108} y1="0" x2={cx + 116} y2="0">
            <stop offset="0%" stopColor={BRAND.color.white} />
            <stop offset="13%" stopColor={BRAND.color.silver} />
            <stop offset="42%" stopColor="#3D4658" />
            <stop offset="74%" stopColor="#18233A" />
            <stop offset="100%" stopColor={BRAND.color.navy} />
          </linearGradient>
          {/* 左エッジだけを光らせるリム（右側は透明に落とす） */}
          <linearGradient id="bl-rim" gradientUnits="userSpaceOnUse" x1={cx - 118} y1="0" x2={cx + 60} y2="0">
            <stop offset="0%" stopColor={BRAND.color.white} stopOpacity={0.85} />
            <stop offset="42%" stopColor={BRAND.color.white} stopOpacity={0} />
          </linearGradient>
          {/* 上を少し明るく：顔（頭）まわりへ視線を集める微かな縦の光 */}
          <linearGradient id="bl-vert" gradientUnits="userSpaceOnUse" x1="0" y1="110" x2="0" y2="728">
            <stop offset="0%" stopColor={BRAND.color.white} stopOpacity={0.14} />
            <stop offset="34%" stopColor={BRAND.color.white} stopOpacity={0} />
            <stop offset="100%" stopColor={BRAND.color.ink} stopOpacity={0.35} />
          </linearGradient>
        </defs>

        {/* 金の境界線の下敷きグロー（描画進捗に同期・柔らかい aura） */}
        <ellipse cx={cx - dent * 0.4} cy={cyA} rx={rxA} ry={ryA}
          fill="none" stroke={BRAND.color.gold} strokeWidth={14}
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ringP}
          style={{filter: `blur(${holdGlow * 0.5 + 7}px)`, opacity: ringP * 0.5}} />

        {/* 匿名シルエット（顔なし・全身立像。呼吸でスケール） */}
        <g style={{transform: `translate(${cx}px, ${cyA}px) scale(${bodyBreath})`, transformBox: 'fill-box', transformOrigin: 'center'} as React.CSSProperties} opacity={figOp}>
          <g style={{transform: `translate(${-cx}px, ${-cyA}px)`}}>
            {/* 背後の柔らかい接地シャドウ（暗部側にわずかにずらす） */}
            <path d={FIGURE_D} fill={BRAND.color.ink} opacity={0.55}
              style={{filter: 'blur(16px)', transform: 'translate(10px, 12px)'}} />
            {/* 本体：左リムライトの陰影グラデ */}
            <path d={FIGURE_D} fill="url(#bl-body)" />
            {/* 上下の陰影（頭を明るく・足元を沈める）を乗算的に重ねる */}
            <path d={FIGURE_D} fill="url(#bl-vert)" style={{mixBlendMode: 'overlay'}} />
            {/* 左エッジのリムライト */}
            <path d={FIGURE_D} fill="none" stroke="url(#bl-rim)" strokeWidth={2.6} strokeLinejoin="round" />
          </g>
        </g>

        {/* 金の境界線 本体（描かれていく。接触で dent＋glow） */}
        <ellipse cx={cx - auraShift + tremor} cy={cyA} rx={rxA} ry={ryA}
          fill="none" stroke={BRAND.color.gold} strokeWidth={4}
          strokeLinecap="round"
          pathLength={1} strokeDasharray={1} strokeDashoffset={1 - ringP}
          style={{filter: `drop-shadow(0 0 ${holdGlow}px ${BRAND.color.gold})`}} />

        {/* blue の圧の刃（cold institutional edge。接触点まで押し寄せ食い込む） */}
        <g opacity={pressP} style={{transform: `translateX(${tremor * 0.6}px)`}}>
          <rect x={pressX} y={cyA - ryA - 40} width={7} height={ryA * 2 + 80} fill={BRAND.color.electric}
            style={{filter: `drop-shadow(0 0 18px ${BRAND.color.electric})`}} />
        </g>

        {/* 接触点：金線が明るく灯り持ちこたえる（局所グロー＋白スパーク） */}
        <g opacity={contact} style={{transform: `translateX(${tremor * 0.4}px)`}}>
          <circle cx={contactX} cy={cyA} r={interpolate(contact, [0, 1], [6, 26])} fill={BRAND.color.gold}
            opacity={contact * 0.55} style={{filter: `blur(9px)`, mixBlendMode: 'screen'} as React.CSSProperties} />
          <circle cx={contactX} cy={cyA} r={interpolate(contact, [0, 1], [0, 13])} fill={BRAND.color.white}
            opacity={contact * 0.85} style={{filter: `blur(2.5px)`}} />
        </g>
      </svg>

      {/* L4 大気：微塵・ビネット・グレイン */}
      <DustMotes count={20} color={BRAND.color.silver} />
      <VignetteBreath />
      <FilmGrain />
    </AbsoluteFill>
  );
};
