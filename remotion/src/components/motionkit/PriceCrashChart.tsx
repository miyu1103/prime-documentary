import React, {useMemo} from 'react';
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
// PriceCrashChart — シネマティックな株価/価格ラインチャートのフルスクリーン
//   ・エレクトリックブルーのラインが左→右へ描画（strokeDashoffset ばね）
//   ・ソフトなエリアフィルが同期して左から出現（clip 幅ばね追従）
//   ・クラッシュで先端が急落し、@remotion/motion-blur の Trail で
//     先端グリントにモーションブラー
//   ・最安値にゴールドのクラッシュマーカー＋ crashLabel をマスク切れ上がり
//   ・抑えた軸・薄いグリッド・マスク切れ上がりの label タイトル
//   ・tabular-nums の現在値カウント
//   品質ルール準拠: 全モーション ease(spring/Easing.out(cubic))・opacity単独なし・
//     マスク切れ上がり・決定論(useCurrentFrame+index+remotion random)・3層以上の奥行き。
//   注: 配色は BRAND トークンのみ。クラッシュ警告色は red が無いため gold を採用。
// =====================================================================

const C = BRAND.color;

// 描画プロット領域（1920x1080 基準・余白で軸を抑える）
const PLOT = {left: 268, right: 1652, top: 286, bottom: 812} as const;

// 価格スケール（正規化値 → 表示ドル）
const PRICE_LO = 18.4;
const PRICE_HI = 642.1;

type Pt = {x: number; y: number; v: number};
type Geom = {pts: Pt[]; seg: number[]; cum: number[]; L: number; n: number};

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// 内蔵デフォルト系列: ゆるやかな上昇 → 鋭いクラッシュ → デッドキャットバウンス
const DEFAULT_SERIES: number[] = (() => {
  const n = 30;
  const a: number[] = [];
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    let base: number;
    if (t < 0.6) {
      base = 0.3 + Math.pow(t / 0.6, 1.2) * 0.6; // 0.30 → ~0.90
    } else if (t < 0.76) {
      const u = (t - 0.6) / 0.16;
      base = 0.9 - Math.pow(u, 1.5) * 0.8; // 急落 → ~0.10
    } else {
      const u = (t - 0.76) / 0.24;
      base = 0.11 + Math.sin(u * Math.PI) * 0.13 - u * 0.04; // 弱いリバウンド
    }
    const noise = (random('pcc-seed-' + i) - 0.5) * 0.045;
    a.push(Math.max(0.04, Math.min(0.98, base + noise)));
  }
  return a;
})();

const normalize = (series: number[]): number[] => {
  if (series.length === 0) return [0.5, 0.5];
  let mn = Infinity;
  let mx = -Infinity;
  for (const s of series) {
    if (s < mn) mn = s;
    if (s > mx) mx = s;
  }
  const d = mx - mn;
  if (d < 1e-6) return series.map(() => 0.5);
  return series.map((s) => (s - mn) / d);
};

const buildGeom = (norm: number[]): Geom => {
  const n = norm.length;
  const pts: Pt[] = norm.map((v, i) => ({
    x: PLOT.left + (PLOT.right - PLOT.left) * (n === 1 ? 0 : i / (n - 1)),
    y: PLOT.bottom - v * (PLOT.bottom - PLOT.top),
    v,
  }));
  const seg: number[] = [];
  const cum: number[] = [0];
  let L = 0;
  for (let i = 0; i < n - 1; i++) {
    const d = Math.hypot(pts[i + 1].x - pts[i].x, pts[i + 1].y - pts[i].y);
    seg.push(d);
    L += d;
    cum.push(L);
  }
  return {pts, seg, cum, L, n};
};

// index 空間の進捗 p(0..1) から先端の座標・値・弧長を得る（等ステップ速度＝急落が速い）
const tipAt = (g: Geom, p: number): {pt: Pt; len: number} => {
  const {pts, seg, cum, n} = g;
  if (n === 1) return {pt: pts[0], len: 0};
  const idx = Math.max(0, Math.min(n - 1, p * (n - 1)));
  const i = Math.min(n - 2, Math.floor(idx));
  const f = idx - i;
  const a = pts[i];
  const b = pts[i + 1];
  const pt: Pt = {
    x: a.x + (b.x - a.x) * f,
    y: a.y + (b.y - a.y) * f,
    v: a.v + (b.v - a.v) * f,
  };
  return {pt, len: cum[i] + seg[i] * f};
};

const pathD = (pts: Pt[]): string =>
  pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(2)} ${p.y.toFixed(2)}`).join(' ');

// マスク切れ上がりテキスト（overflow:hidden + 内側 translateY スライドアップ）
const MaskText: React.FC<{
  text: string;
  delay: number;
  size: number;
  color: string;
  font: string;
  weight?: number;
  ls?: number;
}> = ({text, delay, size, color, font, weight = 400, ls = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const cs = spring({frame: frame - delay, fps, config: {damping: 18, mass: 1}});
  const y = interpolate(cs, [0, 1], [118, 0]);
  const o = interpolate(cs, [0, 0.35], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <div style={{overflow: 'hidden', display: 'inline-block', paddingBottom: '0.14em'}}>
      <div
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: font,
          fontSize: size,
          fontWeight: weight,
          letterSpacing: ls,
          color,
          whiteSpace: 'pre',
          lineHeight: 1.02,
        }}
      >
        {text}
      </div>
    </div>
  );
};

// 先端グリント（Trail で高速時にモーションブラー）。自前で frame を読むので Trail が過去フレームを合成できる。
const TipGlint: React.FC<{
  g: Geom;
  drawStart: number;
  drawDur: number;
  peakFrac: number;
}> = ({g, drawStart, drawDur, peakFrac}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = spring({
    frame: frame - drawStart,
    fps,
    durationInFrames: drawDur,
    config: {damping: 200},
  });
  const p = Math.max(0, Math.min(1, draw));
  const {pt} = tipAt(g, p);
  const crashing = p > peakFrac;
  const core = crashing ? C.gold : C.electric;
  const pulse = 1 + Math.sin(frame * 0.3) * 0.06; // 微発光（等速移動ではない）
  return (
    <div style={{position: 'absolute', left: 0, top: 0, transform: `translate(${pt.x}px, ${pt.y}px)`}}>
      <div
        style={{
          position: 'absolute',
          width: 28,
          height: 28,
          marginLeft: -14,
          marginTop: -14,
          borderRadius: '50%',
          background: core,
          boxShadow: `0 0 28px 7px ${core}, 0 0 66px 14px ${core}88`,
          transform: `scale(${pulse})`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          width: 10,
          height: 10,
          marginLeft: -5,
          marginTop: -5,
          borderRadius: '50%',
          background: C.white,
        }}
      />
    </div>
  );
};

export const PriceCrashChart: React.FC<{
  series?: number[];
  label?: string;
  crashLabel?: string;
  dur?: number;
}> = ({series, label = 'INDEX / PRICE (USD)', crashLabel = 'FLASH CRASH', dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const {geom, peakIdx, crashIdx, startV} = useMemo(() => {
    const norm = normalize(series && series.length >= 2 ? series : DEFAULT_SERIES);
    const g = buildGeom(norm);
    let pI = 0;
    let cI = 0;
    for (let i = 0; i < norm.length; i++) {
      if (norm[i] > norm[pI]) pI = i;
      if (norm[i] < norm[cI]) cI = i;
    }
    return {geom: g, peakIdx: pI, peakV: norm[pI], crashIdx: cI, startV: norm[0]};
  }, [series]);

  const {pts, L, n} = geom;
  const peakFrac = n > 1 ? peakIdx / (n - 1) : 1;
  const crashFrac = n > 1 ? crashIdx / (n - 1) : 1;

  // 描画進捗（ばね・index 空間）
  const drawStart = sec(fps, 0.45);
  const drawDur = Math.max(1, Math.round(total * 0.66));
  const draw = spring({frame: frame - drawStart, fps, durationInFrames: drawDur, config: {damping: 200}});
  const p = Math.max(0, Math.min(1, draw));
  const {pt, len} = tipAt(geom, p);

  // 現在値カウント（tabular-nums）
  const price = PRICE_LO + pt.v * (PRICE_HI - PRICE_LO);
  const pct = ((pt.v - startV) / Math.max(0.001, startV)) * 100;
  const up = pct >= 0;

  // クラッシュマーカー出現（p が最安値到達で eased 反応）
  // inputRange は常に厳密増加させる（crashFrac が 1 のとき [1,1] で落ちるのを防ぐ）
  const crashHi = Math.min(1, crashFrac + 0.07);
  const crashLo = Math.min(crashFrac, crashHi - 0.001);
  const mr = interpolate(p, [crashLo, crashHi], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });
  const cpt = pts[crashIdx];

  // シーン入場（translateY と opacity をペア）＋ サブトルな呼吸
  const enter = spring({frame, fps, config: {damping: 200}, durationInFrames: sec(fps, 0.9)});
  const entY = interpolate(enter, [0, 1], [26, 0]);
  const entO = interpolate(enter, [0, 0.6], [0, 1], {extrapolateRight: 'clamp'});
  const breathe = 1 + Math.sin((frame / fps) * 0.7) * 0.004;

  // 中央グロー脈動
  const glowPulse = 0.5 + Math.sin((frame / fps) * 1.1) * 0.14;

  const linePath = pathD(pts);
  const areaPath = `${linePath} L${pts[n - 1].x.toFixed(2)} ${PLOT.bottom} L${pts[0].x.toFixed(2)} ${PLOT.bottom} Z`;
  const dashOffset = L - len;

  // 抑えた価格軸ラベル
  const axisTicks = [0, 0.5, 1];

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* 奥行き層 1: 指定の放射グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${C.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* 奥行き層 2: 漂う微粒子ダスト（決定論・sin ドリフト） */}
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        {Array.from({length: 16}).map((_, i) => {
          const bx = random('pcc-dx-' + i) * 1920;
          const by = 120 + random('pcc-dy-' + i) * 840;
          const dyd = Math.sin(frame / fps + i * 1.7) * 14;
          const sz = 1.5 + random('pcc-ds-' + i) * 2.5;
          const op = 0.05 + random('pcc-do-' + i) * 0.09;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: bx,
                top: by,
                width: sz,
                height: sz,
                borderRadius: '50%',
                background: C.silver,
                opacity: op,
                transform: `translateY(${dyd}px)`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* 奥行き層 3: 中央グロー（脈動） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(48% 42% at 50% 52%, ${C.electric}22 0%, transparent 70%)`,
          opacity: glowPulse,
        }}
      />

      {/* 主役: 入場＋呼吸のラッパー */}
      <AbsoluteFill style={{opacity: entO, transform: `translateY(${entY}px) scale(${breathe})`}}>
        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{position: 'absolute', inset: 0}}
        >
          <defs>
            <linearGradient id="pcc-area" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={C.electric} stopOpacity={0.34} />
              <stop offset="60%" stopColor={C.electric} stopOpacity={0.1} />
              <stop offset="100%" stopColor={C.electric} stopOpacity={0} />
            </linearGradient>
            <clipPath id="pcc-clip">
              <rect x={0} y={0} width={pt.x} height={1080} />
            </clipPath>
          </defs>

          {/* 薄いグリッド（奥行き・抑えた軸） */}
          {[0, 0.25, 0.5, 0.75, 1].map((t, i) => {
            const gy = PLOT.top + (PLOT.bottom - PLOT.top) * t;
            return (
              <line
                key={'h' + i}
                x1={PLOT.left}
                y1={gy}
                x2={PLOT.right}
                y2={gy}
                stroke={C.silver}
                strokeWidth={1}
                opacity={0.08}
              />
            );
          })}
          {Array.from({length: 7}).map((_, i) => {
            const gx = PLOT.left + ((PLOT.right - PLOT.left) * i) / 6;
            return (
              <line
                key={'v' + i}
                x1={gx}
                y1={PLOT.top}
                x2={gx}
                y2={PLOT.bottom}
                stroke={C.silver}
                strokeWidth={1}
                opacity={0.045}
              />
            );
          })}

          {/* ベースライン軸（抑えめ） */}
          <line
            x1={PLOT.left}
            y1={PLOT.bottom}
            x2={PLOT.right}
            y2={PLOT.bottom}
            stroke={C.silver}
            strokeWidth={1.5}
            opacity={0.28}
          />
          <line
            x1={PLOT.left}
            y1={PLOT.top}
            x2={PLOT.left}
            y2={PLOT.bottom}
            stroke={C.silver}
            strokeWidth={1.5}
            opacity={0.18}
          />

          {/* エリアフィル（左からクリップで出現） */}
          <g clipPath="url(#pcc-clip)">
            <path d={areaPath} fill="url(#pcc-area)" />
          </g>

          {/* ライングロー（太いブラー・dash 追従） */}
          <path
            d={linePath}
            fill="none"
            stroke={C.electric}
            strokeWidth={16}
            strokeLinejoin="round"
            strokeLinecap="round"
            strokeDasharray={L}
            strokeDashoffset={dashOffset}
            style={{filter: 'blur(12px)', opacity: 0.5}}
          />
          {/* メインライン（dash で左→右描画） */}
          <path
            d={linePath}
            fill="none"
            stroke={C.electric}
            strokeWidth={4.5}
            strokeLinejoin="round"
            strokeLinecap="round"
            strokeDasharray={L}
            strokeDashoffset={dashOffset}
          />

          {/* クラッシュマーカー（gold・出現 eased） */}
          <line
            x1={cpt.x}
            y1={cpt.y - 152 * mr}
            x2={cpt.x}
            y2={cpt.y}
            stroke={C.gold}
            strokeWidth={2}
            opacity={0.5 * mr}
          />
          <circle
            cx={cpt.x}
            cy={cpt.y}
            r={34 * mr}
            fill="none"
            stroke={C.gold}
            strokeWidth={3}
            opacity={mr}
          />
          <circle
            cx={cpt.x}
            cy={cpt.y}
            r={12 * mr}
            fill={C.gold}
            opacity={mr}
            style={{filter: `drop-shadow(0 0 14px ${C.gold})`}}
          />
        </svg>

        {/* 抑えた価格軸ラベル */}
        {axisTicks.map((t, i) => {
          const gy = PLOT.bottom - t * (PLOT.bottom - PLOT.top);
          const val = PRICE_LO + t * (PRICE_HI - PRICE_LO);
          return (
            <div
              key={'ax' + i}
              style={{
                position: 'absolute',
                left: PLOT.left - 96,
                top: gy - 12,
                width: 80,
                textAlign: 'right',
                fontFamily: BRAND.font.body,
                fontSize: 20,
                fontWeight: 500,
                letterSpacing: 0.5,
                color: C.silver,
                opacity: 0.4,
                fontVariantNumeric: 'tabular-nums',
              }}
            >
              {`$${val.toFixed(0)}`}
            </div>
          );
        })}

        {/* タイトル label（マスク切れ上がり・左上） */}
        <div style={{position: 'absolute', left: PLOT.left, top: 150}}>
          <div style={{marginBottom: 8}}>
            <MaskText
              text="MARKET DATA"
              delay={sec(fps, 0.12)}
              size={22}
              color={C.electric}
              font={BRAND.font.body}
              weight={700}
              ls={7}
            />
          </div>
          <MaskText
            text={label}
            delay={sec(fps, 0.24)}
            size={58}
            color={C.white}
            font={BRAND.font.display}
            weight={400}
            ls={1}
          />
        </div>

        {/* 現在値リードアウト（tabular-nums・右上） */}
        <div
          style={{
            position: 'absolute',
            right: 130,
            top: 154,
            textAlign: 'right',
            transform: `translateX(${interpolate(enter, [0, 1], [34, 0])}px)`,
            opacity: entO,
          }}
        >
          <div
            style={{
              fontFamily: BRAND.font.body,
              fontSize: 20,
              fontWeight: 600,
              letterSpacing: 6,
              color: C.silver,
              opacity: 0.7,
              marginBottom: 6,
            }}
          >
            LAST
          </div>
          <div
            style={{
              fontFamily: BRAND.font.display,
              fontSize: 96,
              lineHeight: 0.9,
              color: C.white,
              fontVariantNumeric: 'tabular-nums',
              textShadow: `0 0 26px ${up ? C.electric : C.gold}aa`,
            }}
          >
            {`$${price.toFixed(2)}`}
          </div>
          <div
            style={{
              marginTop: 10,
              display: 'inline-block',
              padding: '4px 14px',
              borderRadius: 6,
              background: `${up ? C.electric : C.gold}22`,
              border: `1px solid ${up ? C.electric : C.gold}66`,
              fontFamily: BRAND.font.body,
              fontSize: 26,
              fontWeight: 700,
              letterSpacing: 0.5,
              color: up ? C.electric : C.gold,
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {`${up ? '▲' : '▼'} ${Math.abs(pct).toFixed(1)}%`}
          </div>
        </div>

        {/* crashLabel（マスク切れ上がり・マーカー直下） */}
        <div
          style={{
            position: 'absolute',
            left: cpt.x,
            top: cpt.y + 30,
            transform: 'translateX(-50%)',
            overflow: 'hidden',
            paddingBottom: '0.14em',
          }}
        >
          <div
            style={{
              transform: `translateY(${(1 - mr) * 120}%)`,
              opacity: mr,
              fontFamily: BRAND.font.display,
              fontSize: 42,
              letterSpacing: 3,
              color: C.gold,
              whiteSpace: 'nowrap',
              textShadow: `0 0 22px ${C.gold}88`,
            }}
          >
            {crashLabel}
          </div>
        </div>

        {/* 先端グリント（高速時モーションブラー） */}
        <AbsoluteFill style={{pointerEvents: 'none'}}>
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <TipGlint g={geom} drawStart={drawStart} drawDur={drawDur} peakFrac={peakFrac} />
          </Trail>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* ビネット（最前面の締め） */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background: 'radial-gradient(120% 100% at 50% 46%, transparent 52%, rgba(0,0,0,0.66) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
