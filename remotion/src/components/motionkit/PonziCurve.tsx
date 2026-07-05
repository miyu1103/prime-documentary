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
// MOTIONKIT — PonziCurve
//   概念的な「詐欺の曲線」。GOLD の破線＝約束されたリターン（指数関数）が
//   strokeDashoffset の spring で上へ描かれ、その傍らを SILVER/electric の
//   実線＝実際の価値が低く追従する。ピーク付近で乖離（ギャップ）が広がり、
//   peakLabel がマスク切れ上がりで出現。直後、実際の曲線が 0 へ COLLAPSE：
//   @remotion/motion-blur の Trail でブラーを引きながら垂直に落下し、底で
//   赤い collapseLabel マーカーが弾ける。
//   準拠: 全モーション eased（線形禁止）/ opacity 単独禁止（必ず translate|scale 併用）
//   / テキストは overflow:hidden + translateY のマスク切れ上がり / 速い落下は Trail
//   / 決定論（useCurrentFrame + index、乱数なし）/ 秒は fps から算出 /
//   フルスクリーン・シーン背景＋奥行き 4 層 / 常時わずかに動く（グリッドドリフト・
//   グロー呼吸）。単一構図・単一アクセント体系（gold=約束 / electric=実際 / red=崩壊）。
//   崩壊マーカーの赤は BRAND 外だが、当リポジトリの既定の危険色運用
//   （VoteTally.tsx の抑えたマットレッド #C0473E）に準拠。
// =====================================================================

// 秒→フレーム（フレーム直書き禁止・fps から算出）
const sec = (fps: number, s: number) => Math.round(fps * s);

// カラー体系（gold=約束 / electric=実際 / silver=軸 / red=崩壊）
const PROMISE = BRAND.color.gold;
const ACTUAL = BRAND.color.electric;
const AXIS = BRAND.color.silver;
// 抑えたマット危険赤（既存 VoteTally.tsx の DISSENT_RED 運用に準拠）
const DANGER = '#C0473E';

// 指定のフルスクリーン・シーン背景
const SCENE_BG = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`;

// 速い落下に掛ける共通モーションブラー設定
const FAST_TRAIL = {layers: 7, lagInFrames: 1.15, trailOpacity: 0.5} as const;

// 値曲線: 約束されたリターン（指数のホッケースティック / 0..1 にクランプ）
const promisedV = (t: number): number =>
  Math.min(0.98, 0.05 * (Math.exp(3.6 * t) - 1));

// 値曲線: 実際の価値（低く緩やかに上昇し、ピークで頭打ち）
const T_PEAK = 0.82; // 実際の曲線がピークを迎える時間位置
const PEAK_V = 0.34; // 実際のピーク値
const actualV = (t: number): number => PEAK_V * Math.pow(t / T_PEAK, 0.72);

type Pt = {x: number; y: number};
const toPath = (pts: Pt[]): string =>
  pts
    .map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(2)} ${p.y.toFixed(2)}`)
    .join(' ');
const polyLen = (pts: Pt[]): number => {
  let L = 0;
  for (let i = 1; i < pts.length; i++) {
    L += Math.hypot(pts[i].x - pts[i - 1].x, pts[i].y - pts[i - 1].y);
  }
  return L;
};

// マスク切れ上がりの直接ラベル（overflow:hidden + translateY / opacity は併用）
const MaskLabel: React.FC<{
  text: string;
  reveal: number; // 0→1（eased spring progress）
  size: number;
  weight: number;
  color: string;
  font?: string;
  letterSpacing?: number;
  glow?: string;
}> = ({
  text,
  reveal,
  size,
  weight,
  color,
  font = BRAND.font.body,
  letterSpacing = 0.5,
  glow,
}) => {
  const y = interpolate(reveal, [0, 1], [118, 0]);
  const o = interpolate(reveal, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.16em',
        fontFamily: font,
        fontWeight: weight,
        fontSize: size,
        letterSpacing,
        color,
        lineHeight: 1.06,
        textShadow: glow ? `0 0 22px ${glow}, 0 2px 8px rgba(0,0,0,0.8)` : undefined,
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
        {text}
      </span>
    </span>
  );
};

// ---------------------------------------------------------------------
// 実際の曲線の「崩壊」= 垂直落下（Trail の内側で frame を読む → ラグ複製がアニメ）
// ---------------------------------------------------------------------
const Plunge: React.FC<{
  px: number;
  topY: number;
  botY: number;
  collapseStart: number;
  width: number;
  height: number;
}> = ({px, topY, botY, collapseStart, width, height}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // 落下: spring（わずかにオーバーシュート＝底で叩きつける）
  const pp = spring({
    frame: frame - collapseStart,
    fps,
    config: {damping: 13, mass: 0.9, stiffness: 120},
  });
  const headY = interpolate(pp, [0, 1], [topY, botY]);
  // 落下ヘッドの発光（速度に応じて明滅＝完全静止しない）
  const speed = interpolate(pp, [0, 0.15, 0.7, 1], [0, 1, 1, 0.2], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
    >
      {/* 落下する崖: 頂点から現在のヘッドまで（伸長する縦線＝Trail でブラー） */}
      <line
        x1={px}
        y1={topY}
        x2={px}
        y2={headY}
        stroke={ACTUAL}
        strokeWidth={7}
        strokeLinecap="round"
        style={{filter: `drop-shadow(0 0 ${8 + 16 * speed}px ${ACTUAL})`}}
      />
      {/* 落下ヘッド（先端の光弾） */}
      <circle
        cx={px}
        cy={headY}
        r={10 + 6 * speed}
        fill={BRAND.color.white}
        style={{filter: `drop-shadow(0 0 ${14 + 20 * speed}px ${ACTUAL})`}}
      />
    </svg>
  );
};

// ---------------------------------------------------------------------
// 親コンポーネント
// ---------------------------------------------------------------------
export const PonziCurve: React.FC<{
  peakLabel?: string;
  collapseLabel?: string;
  dur?: number;
}> = ({peakLabel = 'Paper profits', collapseLabel = 'Collapse', dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- プロット定数（全て定数化） ----
  const plotLeft = 250;
  const plotRight = width - 210; // 1710
  const plotBottom = height - 230; // 850
  const plotTop = 210;
  const plotW = plotRight - plotLeft;
  const plotH = plotBottom - plotTop;
  const xOf = (t: number) => plotLeft + t * plotW;
  const yOf = (v: number) => plotBottom - v * plotH;

  // ---- 曲線サンプリング（width/height 依存のみ→決定論・メモ化） ----
  const N = 90;
  const promisedPts = React.useMemo<Pt[]>(() => {
    const pts: Pt[] = [];
    const t1 = 0.96;
    for (let i = 0; i <= N; i++) {
      const t = (t1 * i) / N;
      pts.push({x: xOf(t), y: yOf(promisedV(t))});
    }
    return pts;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [width, height]);
  const actualPts = React.useMemo<Pt[]>(() => {
    const pts: Pt[] = [];
    for (let i = 0; i <= N; i++) {
      const t = (T_PEAK * i) / N;
      pts.push({x: xOf(t), y: yOf(actualV(t))});
    }
    return pts;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [width, height]);

  const promisedPath = toPath(promisedPts);
  const actualPath = toPath(actualPts);
  const actualLen = polyLen(actualPts);

  // 主要点
  const peakPt = {x: xOf(T_PEAK), y: yOf(PEAK_V)}; // 実際のピーク（崩壊起点）
  const promisedEnd = promisedPts[promisedPts.length - 1];
  const gapTopY = yOf(promisedV(T_PEAK)); // 同じ x での約束側の高さ（乖離上端）

  // ---- タイムライン（秒→フレーム、崩壊は total 基準で末尾に確保） ----
  const gridStart = sec(fps, 0.1);
  const axisStart = sec(fps, 0.15);
  const drawStartP = sec(fps, 0.28);
  const drawStartA = sec(fps, 0.42);
  const legendStart = sec(fps, 1.25);
  const peakLabelStart = sec(fps, 1.5);
  const gapStart = sec(fps, 1.75);
  const collapseStart = Math.max(sec(fps, 2.1), total - sec(fps, 1.35));
  const markerStart = collapseStart + sec(fps, 0.42);
  const outStart = total - sec(fps, 0.45);

  // ---- 奥行きの常時モーション（決して完全静止しない） ----
  const drift = interpolate(frame, [0, total], [-20, 20], {
    easing: Easing.inOut(Easing.sin),
  });
  const glowPulse = 0.42 + 0.2 * Math.sin((frame / fps) * 1.3);
  const promiseGlow = 0.5 + 0.5 * Math.sin((frame / fps) * 2.1);

  // ---- 描画進捗（spring・線形禁止） ----
  const axisDraw = spring({
    frame: frame - axisStart,
    fps,
    config: {damping: 30, mass: 1},
  });
  const promisedDraw = spring({
    frame: frame - drawStartP,
    fps,
    config: {damping: 32, mass: 1},
  });
  const actualDraw = spring({
    frame: frame - drawStartA,
    fps,
    config: {damping: 30, mass: 1},
  });
  const gapDraw = spring({
    frame: frame - gapStart,
    fps,
    config: {damping: 26, mass: 1},
  });

  // ラベルのマスク切れ上がり
  const peakReveal = spring({
    frame: frame - peakLabelStart,
    fps,
    config: {damping: 16, mass: 0.9},
  });
  const legendPromiseReveal = spring({
    frame: frame - legendStart,
    fps,
    config: {damping: 17, mass: 0.9},
  });
  const legendActualReveal = spring({
    frame: frame - legendStart - sec(fps, 0.12),
    fps,
    config: {damping: 17, mass: 0.9},
  });
  const collapseReveal = spring({
    frame: frame - markerStart,
    fps,
    config: {damping: 15, mass: 0.8},
  });

  // 崩壊マーカーの弾け（scale pop）＋衝撃リング（scale 併用＝opacity 単独でない）
  const markerPop = interpolate(collapseReveal, [0, 1], [0.2, 1]);
  const ringP = interpolate(
    frame,
    [markerStart, markerStart + sec(fps, 0.55)],
    [0, 1],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );
  const ringScale = interpolate(ringP, [0, 1], [0.3, 2.6]);
  const ringO = interpolate(ringP, [0, 1], [0.9, 0]);

  // 崩壊ヘッドの現在位置（マーカー点灯や乖離ハイライトの同期に使用）
  const plungeP = spring({
    frame: frame - collapseStart,
    fps,
    config: {damping: 13, mass: 0.9, stiffness: 120},
  });
  const gapEmphasis = interpolate(
    frame,
    [gapStart, collapseStart],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // シーン出入り（scale 併用＝opacity 単独でない）
  const sceneO = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const sceneScale = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [1.035, 1, 1, 1.02],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );
  const sceneY = interpolate(frame, [0, sec(fps, 0.3)], [22, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // 補助線（グリッド）
  const hGrid = [0.25, 0.5, 0.75];
  const vGrid = [0.25, 0.5, 0.75];

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* Layer 1: フルスクリーン・シーン背景（グラデ） */}
      <AbsoluteFill style={{background: SCENE_BG}} />

      {/* Layer 2: 抑えた大グリッド（ドリフト＝常時可変） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACTUAL}22 0px, ${ACTUAL}22 1px, transparent 1px, transparent 78px),
            repeating-linear-gradient(90deg, ${ACTUAL}22 0px, ${ACTUAL}22 1px, transparent 1px, transparent 78px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
        }}
      />

      {/* Layer 3: アクセントグロー（呼吸で常時可変） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(58% 46% at 62% 40%, ${ACTUAL}1f 0%, transparent 70%)`,
          opacity: glowPulse,
          mixBlendMode: 'screen',
        }}
      />

      {/* Layer 4: ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.64) 100%)',
        }}
      />

      {/* ---- 主役: 詐欺の曲線 ---- */}
      <AbsoluteFill
        style={{
          opacity: sceneO,
          transform: `translateY(${sceneY}px) scale(${sceneScale})`,
        }}
      >
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          style={{position: 'absolute', inset: 0}}
        >
          <defs>
            <linearGradient id="pc-actual" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor={AXIS} />
              <stop offset="100%" stopColor={ACTUAL} />
            </linearGradient>
            {/* 約束カーブの描き上げ = 左→右へ広がる矩形クリップ（幾何学的リビール）。
                破線の流れ(dashoffset)と描き上げを両立させるため clipPath を使用。 */}
            <clipPath id="pc-clip-promise">
              <rect
                x={plotLeft}
                y={0}
                width={Math.max(0, plotW * promisedDraw)}
                height={height}
              />
            </clipPath>
          </defs>

          {/* 抑えた補助グリッド（recessive・左→右へ描き込み / スタッガー） */}
          {hGrid.map((v, i) => {
            const y = yOf(v);
            const p = interpolate(
              spring({
                frame: frame - gridStart - i * sec(fps, 0.06),
                fps,
                config: {damping: 28, mass: 1},
              }),
              [0, 1],
              [0, 1],
            );
            return (
              <line
                key={`h${i}`}
                x1={plotLeft}
                y1={y}
                x2={plotRight}
                y2={y}
                stroke={AXIS}
                strokeOpacity={0.1}
                strokeWidth={1}
                strokeDasharray={plotW}
                strokeDashoffset={plotW * (1 - p)}
              />
            );
          })}
          {vGrid.map((t, i) => {
            const x = xOf(t);
            const p = interpolate(
              spring({
                frame: frame - gridStart - i * sec(fps, 0.06),
                fps,
                config: {damping: 28, mass: 1},
              }),
              [0, 1],
              [0, 1],
            );
            return (
              <line
                key={`v${i}`}
                x1={x}
                y1={plotBottom}
                x2={x}
                y2={plotTop}
                stroke={AXIS}
                strokeOpacity={0.08}
                strokeWidth={1}
                strokeDasharray={plotH}
                strokeDashoffset={plotH * (1 - p)}
              />
            );
          })}

          {/* 軸（L字・recessive・描き込み） */}
          <line
            x1={plotLeft}
            y1={plotTop}
            x2={plotLeft}
            y2={plotBottom}
            stroke={AXIS}
            strokeOpacity={0.32}
            strokeWidth={2}
            strokeDasharray={plotH}
            strokeDashoffset={plotH * (1 - axisDraw)}
          />
          <line
            x1={plotLeft}
            y1={plotBottom}
            x2={plotRight}
            y2={plotBottom}
            stroke={AXIS}
            strokeOpacity={0.32}
            strokeWidth={2}
            strokeDasharray={plotW}
            strokeDashoffset={plotW * (1 - axisDraw)}
          />

          {/* 乖離（ギャップ）: 実際ピークと約束の間を結ぶ縦線＋端キャップ。
              崩壊直前に強調（opacity と幅・グローを併用） */}
          <g opacity={interpolate(gapDraw, [0, 0.5], [0, 1], {extrapolateRight: 'clamp'})}>
            <line
              x1={peakPt.x}
              y1={peakPt.y}
              x2={peakPt.x}
              y2={interpolate(gapDraw, [0, 1], [peakPt.y, gapTopY])}
              stroke={PROMISE}
              strokeOpacity={0.35 + 0.4 * gapEmphasis}
              strokeWidth={2}
              strokeDasharray="2 9"
              style={{filter: `drop-shadow(0 0 ${6 * gapEmphasis}px ${PROMISE})`}}
            />
            {/* 端キャップ（上=約束 / 下=実際） */}
            <circle cx={peakPt.x} cy={gapTopY} r={4} fill={PROMISE} opacity={gapDraw} />
            <circle cx={peakPt.x} cy={peakPt.y} r={4} fill={ACTUAL} opacity={gapDraw} />
          </g>

          {/* 約束されたリターン: GOLD 破線・指数。矩形クリップで左→右に描き上がり、
              破線は dashoffset で流れ続ける（常時可変・opacity 単独リビールでない） */}
          <path
            d={promisedPath}
            fill="none"
            stroke={PROMISE}
            strokeWidth={5}
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray={`14 12`}
            strokeDashoffset={-frame * 0.6}
            clipPath="url(#pc-clip-promise)"
            style={{filter: `drop-shadow(0 0 ${8 + 8 * promiseGlow}px ${PROMISE}aa)`}}
          />

          {/* 実際の価値: SILVER→electric の実線（低く追従） */}
          <path
            d={actualPath}
            fill="none"
            stroke="url(#pc-actual)"
            strokeWidth={6}
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeDasharray={actualLen}
            strokeDashoffset={actualLen * (1 - actualDraw)}
            style={{filter: `drop-shadow(0 0 10px ${ACTUAL}88)`}}
          />

          {/* 約束の終端マーカー（右上・発光） */}
          <circle
            cx={promisedEnd.x}
            cy={promisedEnd.y}
            r={interpolate(promisedDraw, [0.8, 1], [0, 8], {
              extrapolateLeft: 'clamp',
            })}
            fill={PROMISE}
            style={{filter: `drop-shadow(0 0 16px ${PROMISE})`}}
          />

          {/* 実際のピークマーカー（崩壊起点・崩壊前のみ点灯） */}
          <circle
            cx={peakPt.x}
            cy={peakPt.y}
            r={interpolate(actualDraw, [0.85, 1], [0, 9], {
              extrapolateLeft: 'clamp',
            }) * (1 - Math.min(1, plungeP * 1.4))}
            fill={BRAND.color.white}
            style={{filter: `drop-shadow(0 0 14px ${ACTUAL})`}}
          />

          {/* 崩壊の底: 衝撃リング（赤・scale＋opacity 併用） */}
          {ringP > 0 ? (
            <circle
              cx={peakPt.x}
              cy={plotBottom}
              r={26 * ringScale}
              fill="none"
              stroke={DANGER}
              strokeWidth={4}
              opacity={ringO}
            />
          ) : null}

          {/* 崩壊マーカー（赤いダイヤ・pop） */}
          <g
            transform={`translate(${peakPt.x} ${plotBottom}) scale(${markerPop})`}
            opacity={interpolate(collapseReveal, [0, 0.3], [0, 1], {
              extrapolateRight: 'clamp',
            })}
          >
            <rect
              x={-13}
              y={-13}
              width={26}
              height={26}
              transform="rotate(45)"
              fill={DANGER}
              stroke={BRAND.color.white}
              strokeWidth={2}
              style={{filter: `drop-shadow(0 0 14px ${DANGER})`}}
            />
          </g>
        </svg>

        {/* 崩壊の落下（速い → Trail でモーションブラー / Trail 内で frame を読む） */}
        {frame >= collapseStart ? (
          <Trail
            layers={FAST_TRAIL.layers}
            lagInFrames={FAST_TRAIL.lagInFrames}
            trailOpacity={FAST_TRAIL.trailOpacity}
          >
            <Plunge
              px={peakPt.x}
              topY={peakPt.y}
              botY={plotBottom}
              collapseStart={collapseStart}
              width={width}
              height={height}
            />
          </Trail>
        ) : null}

        {/* peakLabel: ピーク（約束）の見出し（マスク切れ上がり・上部左の空きへ） */}
        <div style={{position: 'absolute', left: plotLeft + 12, top: 132}}>
          <div style={{marginBottom: 10}}>
            <MaskLabel
              text="THE PROMISE"
              reveal={peakReveal}
              size={22}
              weight={700}
              color={PROMISE}
              letterSpacing={7}
              glow={`${PROMISE}66`}
            />
          </div>
          <MaskLabel
            text={peakLabel}
            reveal={peakReveal}
            size={72}
            weight={400}
            color={BRAND.color.white}
            font={BRAND.font.display}
            letterSpacing={1}
            glow="rgba(0,0,0,0.6)"
          />
        </div>

        {/* 直接ラベル: 約束（曲線右上・gold） */}
        <div
          style={{
            position: 'absolute',
            left: promisedEnd.x - 250,
            top: promisedEnd.y - 6,
            textAlign: 'right',
            width: 234,
          }}
        >
          <MaskLabel
            text="PROMISED RETURNS"
            reveal={legendPromiseReveal}
            size={26}
            weight={700}
            color={PROMISE}
            letterSpacing={1.5}
            glow={`${PROMISE}55`}
          />
        </div>

        {/* 直接ラベル: 実際（ピーク上・electric） */}
        <div
          style={{
            position: 'absolute',
            left: peakPt.x - 300,
            top: peakPt.y - 58,
            textAlign: 'right',
            width: 280,
          }}
        >
          <MaskLabel
            text="ACTUAL VALUE"
            reveal={legendActualReveal}
            size={26}
            weight={700}
            color={ACTUAL}
            letterSpacing={1.5}
            glow={`${ACTUAL}55`}
          />
        </div>

        {/* collapseLabel: 崩壊マーカー（赤・底・マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            left: peakPt.x,
            top: plotBottom + 34,
            transform: 'translateX(-50%)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <MaskLabel
            text={collapseLabel}
            reveal={collapseReveal}
            size={54}
            weight={400}
            color={DANGER}
            font={BRAND.font.display}
            letterSpacing={2}
            glow={`${DANGER}88`}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
