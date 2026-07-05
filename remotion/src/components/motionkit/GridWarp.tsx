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
// GridWarp — フルスクリーンのプレミアム背景ベッド（"data-space"）。
//   正典グラデ地の上に、遠近ネオングリッドを重ねる Tron/データ空間の質感。
//   ・水平ラインは遠近で間隔が詰まり、視点へ向かって「イーズド」に流れる
//     （フェーズを pow で遠近マッピング＝等速線形ではない）。境界はフェードで
//     継ぎ目なくラップ。
//   ・垂直ラインは消失点（水平線中央）へ収束する。
//   ・グリッド全体をイーズド正弦の変位リップルが横断＝ワープ/呼吸。
//     稜線（クレスト）上でラインが明るく光る。
//   ・柔らかな horizon glow と、リップル稜線を追う可動グロー（Trail で
//     モーションブラー）、微かなスキャンライン。
//   すべての動きはイージング付き（等速線形禁止）。色は BRAND トークンのみ。
//   決定論的：useCurrentFrame + index のみ（Math.random/Date 不使用）。
//   時間は fps から算出。静止フレームを作らない。
//   禁止（本ファイルはいずれも生成しない）：黄縦スイープ/全面黄ウォッシュ/
//   ただのズーム・パン/実在肖像/画面内ロゴ。
// =====================================================================

const TWO_PI = Math.PI * 2;
const PERSP = 2.6; // 遠近べき（大きいほど水平線が地平に密集）
const N_H = 20; // 水平ライン本数
const N_V = 24; // 垂直ライン本数
const SAMPLES = 28; // 1ライン当たりのサンプル点（波を滑らかに）
const CROSS = 1.4; // 横方向の波数（リップルが左右へ横断）
const DEPTHW = 1.1; // 奥行き方向の波数
const CEIL = 0.82; // 天井ミラーの縦圧縮率
const CEIL_OP = 0.3; // 天井ミラーの相対不透明度

// ブランドHEX → rgba（トークン以外の色は生成しない）
const hexToRgba = (hex: string, a: number): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};

const smoothstep = (a: number, b: number, x: number): number => {
  const tt = Math.max(0, Math.min(1, (x - a) / (b - a)));
  return tt * tt * (3 - 2 * tt);
};

// 出入りエンベロープ（先頭で立ち上げ・終端で畳む、必ずイーズド）。
const envelope = (frame: number, dur: number, fps: number): number => {
  const inN = Math.min(Math.round(fps * 0.4), Math.max(1, Math.floor(dur / 3)));
  const outN = Math.min(Math.round(fps * 0.45), Math.max(1, Math.floor(dur / 3)));
  const p1 = inN;
  const p2 = Math.max(p1 + 1, dur - outN);
  return interpolate(frame, [0, p1, p2, dur], [0, 1, 1, 0], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

type Line = {d: string; op: number; sw: number};

// 可動クレストグロー（リップル稜線を奥→手前へ追う柔らかいバンド）。
// Trail が実効するよう、内部で useCurrentFrame を読む独立コンポーネントにする。
const CrestGlow: React.FC<{
  horizon: number;
  floorBottom: number;
  color: string;
}> = ({horizon, floorBottom, color}) => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const t = frame / fps;

  // 0..1 を循環するクレスト位置。pow で手前ほど加速＝イーズド（等速でない）。
  const raw = t * 0.09;
  const cf = raw - Math.floor(raw);
  const pers = Math.pow(cf, PERSP);
  const y = horizon + (floorBottom - horizon) * pers;
  // 端で消える（sin(cf*PI)）→ ラップの継ぎ目を隠す。
  const op = Math.sin(cf * Math.PI) * 0.16;
  const band = Math.max(60, height * 0.14);

  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: y - band / 2,
        height: band,
        background: `radial-gradient(60% 60% at 50% 50%, ${color} 0%, transparent 72%)`,
        opacity: op,
      }}
    />
  );
};

export const GridWarp: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const t = frame / fps;

  // 柔らかな立ち上げ＋出入りエンベロープ（先頭のポップ防止・終端で畳む）。
  const appear = spring({frame, fps, config: {damping: 26, mass: 1, stiffness: 60}});
  const env = envelope(frame, total, fps);
  const gridOpacity = appear * env;

  // 消失点は水平線中央。ごく僅かにイーズド呼吸（静止させない）。
  const centerX =
    width / 2 +
    interpolate(Math.sin(t * 0.2), [-1, 1], [-width * 0.018, width * 0.018], {
      easing: Easing.inOut(Easing.sin),
    });
  const horizon =
    height * 0.45 +
    interpolate(Math.sin(t * 0.15), [-1, 1], [-8, 8], {
      easing: Easing.inOut(Easing.sin),
    });
  const horizonBase = height * 0.45;
  const floorBottom = height * 1.08;
  const halfNear = width * 0.95;
  const warpAmp = height * 0.02;

  // 奥行き流れ：フェーズは単調増加だが速度は正弦で常に変化（イーズド・等速でない）。
  // amp*w (=0.024) < base (=0.05) を守り、逆流せず前進のみ。
  const flowRaw = t * 0.05 + 0.04 * Math.sin(t * 0.6);
  const flow = flowRaw - Math.floor(flowRaw);
  // リップルの横断フェーズ（cycles）。
  const warpTravel = t * 0.12;

  // 遠近マッピングと共有ワープ場（H/V ラインで一致＝整合メッシュ）。
  const perspOf = (frac: number): number =>
    Math.pow(Math.max(0, Math.min(1, frac)), PERSP);
  const warpAt = (lateral: number, pers: number): number =>
    warpAmp *
    (0.25 + pers) *
    Math.sin((lateral * CROSS + pers * DEPTHW - warpTravel) * TWO_PI);
  const px = (lateral: number, pers: number): number =>
    centerX + lateral * halfNear * pers;
  const py = (lateral: number, pers: number): number =>
    horizon + (floorBottom - horizon) * pers + warpAt(lateral, pers);

  // ---- 水平ライン（奥行きインデックス、流れでラップ） ----
  const hLines: Line[] = [];
  for (let i = 0; i < N_H; i++) {
    let frac = i / N_H + flow;
    frac -= Math.floor(frac);
    const pers = perspOf(frac);
    let d = '';
    for (let s = 0; s <= SAMPLES; s++) {
      const lateral = -1.2 + 2.4 * (s / SAMPLES);
      const x = px(lateral, pers);
      const y = py(lateral, pers);
      d += `${x.toFixed(1)},${y.toFixed(1)} `;
    }
    const fHorizon = smoothstep(0.0, 0.14, frac); // 地平で消えて出現
    const fNear = 1 - smoothstep(0.8, 1.0, frac); // 手前端でフェード（ラップ隠し）
    const crest = 0.55 + 0.45 * Math.sin((pers * DEPTHW - warpTravel) * TWO_PI);
    hLines.push({
      d: d.trim(),
      op: 0.5 * fHorizon * fNear * crest,
      sw: 0.6 + pers * 2.4,
    });
  }

  // ---- 垂直ライン（消失点へ収束） ----
  const vLines: Line[] = [];
  for (let j = 0; j < N_V; j++) {
    const lat = -1.1 + (2.2 * j) / (N_V - 1);
    let d = '';
    for (let s = 0; s <= SAMPLES; s++) {
      const fracV = s / SAMPLES;
      const pers = perspOf(fracV);
      const x = px(lat, pers);
      const y = py(lat, pers);
      d += `${x.toFixed(1)},${y.toFixed(1)} `;
    }
    const crestV = 0.6 + 0.4 * Math.sin((lat * CROSS - warpTravel) * TWO_PI);
    vLines.push({d: d.trim(), op: 0.16 * crestV, sw: 1.0});
  }

  const electric = BRAND.color.electric;
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const glowId = `gridwarp-glow-${uid}`;

  const polys = (lines: Line[], widthMul: number, prefix: string) =>
    lines.map((l, i) => (
      <polyline
        key={`${prefix}-${i}`}
        points={l.d}
        fill="none"
        stroke={electric}
        strokeWidth={l.sw * widthMul}
        strokeOpacity={l.op}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    ));

  // メッシュ（ぼかしグロー層＋クリスプ層）を一度だけ組み、床/天井で再利用。
  const mesh = (
    <>
      <g filter={`url(#${glowId})`} opacity={0.7}>
        {polys(hLines, 1.7, 'hg')}
        {polys(vLines, 1.7, 'vg')}
      </g>
      <g>
        {polys(hLines, 1.0, 'hc')}
        {polys(vLines, 1.0, 'vc')}
      </g>
    </>
  );

  const horizonPct = (horizonBase / height) * 100;
  const horizonBreath = interpolate(Math.sin(t * 0.6), [-1, 1], [0.5, 0.92], {
    easing: Easing.inOut(Easing.sin),
  });
  const scanDrift = interpolate(Math.sin(t * 0.5), [-1, 1], [0, 3], {
    easing: Easing.inOut(Easing.sin),
  });
  const scanColor = hexToRgba(electric, 0.5);

  return (
    <AbsoluteFill
      style={{
        // 正典グラデ地（背景ベッドの土台）。
        background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
      }}
    >
      <AbsoluteFill style={{opacity: gridOpacity, pointerEvents: 'none'}}>
        {/* 柔らかな horizon glow（消失点帯を沈み込ませる） */}
        <AbsoluteFill
          style={{
            mixBlendMode: 'screen',
            opacity: horizonBreath,
            background: `radial-gradient(58% 20% at 50% ${horizonPct}%, ${hexToRgba(
              electric,
              0.5,
            )} 0%, transparent 70%)`,
          }}
        />

        {/* 遠近ネオングリッド */}
        <svg
          width={width}
          height={height}
          viewBox={`0 0 ${width} ${height}`}
          style={{position: 'absolute', inset: 0, mixBlendMode: 'screen'}}
        >
          <defs>
            <filter id={glowId} x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation={Math.max(2, height * 0.004)} />
            </filter>
          </defs>
          {/* 床 */}
          <g>{mesh}</g>
          {/* 天井ミラー（水平線を軸に反転・圧縮・減光） */}
          <g
            opacity={CEIL_OP}
            transform={`translate(0 ${horizon}) scale(1 ${-CEIL}) translate(0 ${-horizon})`}
          >
            {mesh}
          </g>
        </svg>

        {/* リップル稜線を追う可動グロー（Trail で実効モーションブラー） */}
        <AbsoluteFill style={{mixBlendMode: 'screen'}}>
          <Trail layers={4} lagInFrames={1.2} trailOpacity={0.5}>
            <CrestGlow
              horizon={horizonBase}
              floorBottom={floorBottom}
              color={hexToRgba(electric, 0.85)}
            />
          </Trail>
        </AbsoluteFill>

        {/* 微かなスキャンライン（イーズド正弦でゆっくりドリフト・静止しない） */}
        <AbsoluteFill
          style={{
            mixBlendMode: 'overlay',
            opacity: 0.06,
            backgroundImage: `repeating-linear-gradient(to bottom, ${scanColor} 0px, ${scanColor} 1px, transparent 1px, transparent 3px)`,
            backgroundPositionY: `${scanDrift}px`,
          }}
        />

        {/* コーナーを沈めるビネット（プレミアムな締まり） */}
        <AbsoluteFill
          style={{
            background: `radial-gradient(120% 100% at 50% 42%, transparent 55%, ${hexToRgba(
              BRAND.color.ink,
              0.55,
            )} 100%)`,
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
