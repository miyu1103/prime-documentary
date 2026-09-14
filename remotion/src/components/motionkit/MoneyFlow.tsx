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
// MoneyFlow — MOTIONKIT  「Follow the money」
//   0..1 座標のノード（口座/主体）が spring でポップ（着地スカッシュ）、
//   ラベルは overflow:hidden + inner translateY のマスク切れ上がり。各エッジは
//   weight で太さが変わる発光ラインとして strokeDashoffset で描き進み、
//   source→target に沿って金色の価値パーティクル（コイン）がイーズド経路で
//   連続的に流れる。各エッジ上をソフトな金グロー先端が Trail で走る。
//   エッジ活性化はスタッガー。dur 未指定なら durationInFrames。
//
// 品質ルール準拠:
//   - 全モーションに easing / spring（等速線形なし）
//   - opacity単独の演出なし（必ず translate/scale と併用）
//   - テキストは overflow:hidden + inner translateY のマスク切れ上がり
//   - 速い動き（コイン流・グロー・ノードポップ）は
//     <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
//   - 完全に決定論的（useCurrentFrame + index + remotion random、Math.random不使用）
//   - 尺は fps から算出、never fully static、フルスクリーン正典背景 + 3層以上の奥行き
//   - 色は BRAND トークンのみ（＋正典背景リテラル #06080f）
// =====================================================================

type MFNode = {x: number; y: number; label?: string};
type MFEdge = {from: number; to: number; weight?: number};
type Pt = {x: number; y: number};

type EdgeGeom = {
  a: Pt;
  b: Pt;
  c: Pt; // 二次ベジェ制御点
  len: number; // 近似弧長
  weight: number;
  startF: number; // このエッジの活性化フレーム
  path: string; // SVG path 文字列
};

// 秒→フレーム
const sec = (fps: number, s: number): number => Math.round(fps * s);

// 二次ベジェ上の点（パラメータ t）
const quad = (a: Pt, c: Pt, b: Pt, t: number): Pt => {
  const mt = 1 - t;
  return {
    x: mt * mt * a.x + 2 * mt * t * c.x + t * t * b.x,
    y: mt * mt * a.y + 2 * mt * t * c.y + t * t * b.y,
  };
};

// 速い部分に掛ける共通モーションブラー設定
const FAST_TRAIL = {layers: 6, lagInFrames: 1.1, trailOpacity: 0.5} as const;

// ノードのポップ開始フレーム（index スタッガー）
const nodeStartF = (fps: number, i: number): number =>
  sec(fps, 0.15) + i * sec(fps, 0.12);

// 正典フルスクリーン背景
const SCENE_BG = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`;

// ---------------------------------------------------------------------
// エッジ本体（strokeDashoffset で描き上げ・太さは weight スケール）
// ---------------------------------------------------------------------
const EdgesBase: React.FC<{edges: EdgeGeom[]}> = ({edges}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {electric, white} = BRAND.color;

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{position: 'absolute', inset: 0}}
    >
      <defs>
        <filter id="mf-edgeglow" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="6" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>
      {edges.map((e, i) => {
        // 描き上げ：滑らかな非バウンド spring
        const draw = spring({
          frame: frame - e.startF,
          fps,
          config: {damping: 44, mass: 1.1, stiffness: 130},
          durationInFrames: sec(fps, 0.7),
        });
        const off = e.len * (1 - draw);
        // 描画中の先端はまだ描かれていないので dash で隠れる
        const glowW = 4 + e.weight * 3;
        const coreW = 1.6 + e.weight * 1.2;
        // 描き上がった後もわずかに脈動（完全静止の回避・sin は eased）
        const pulse =
          0.24 +
          0.12 * Math.sin((frame / fps) * Math.PI * 2 * 0.5 + i) * draw;
        return (
          <g key={i}>
            <path
              d={e.path}
              fill="none"
              stroke={electric}
              strokeWidth={glowW}
              strokeLinecap="round"
              strokeOpacity={pulse}
              strokeDasharray={e.len}
              strokeDashoffset={off}
              filter="url(#mf-edgeglow)"
            />
            <path
              d={e.path}
              fill="none"
              stroke={white}
              strokeWidth={coreW}
              strokeLinecap="round"
              strokeOpacity={0.85}
              strokeDasharray={e.len}
              strokeDashoffset={off}
            />
          </g>
        );
      })}
    </svg>
  );
};

// ---------------------------------------------------------------------
// 金色の価値パーティクル（コイン）ストリーム — Trail 内で frame を読む
//   source→target に沿って連続放出。速度はイーズド（等速禁止）。
// ---------------------------------------------------------------------
const CoinStream: React.FC<{edges: EdgeGeom[]}> = ({edges}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {gold, white, silver} = BRAND.color;
  const speedEase = Easing.inOut(Easing.sin);

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{position: 'absolute', inset: 0}}
    >
      <defs>
        <radialGradient id="mf-coin" cx="38%" cy="34%" r="72%">
          <stop offset="0%" stopColor={white} stopOpacity={0.95} />
          <stop offset="42%" stopColor={gold} stopOpacity={1} />
          <stop offset="100%" stopColor={gold} stopOpacity={0} />
        </radialGradient>
      </defs>
      {edges.map((e, ei) => {
        if (frame < e.startF) return null;
        const local = frame - e.startF;
        const travel = sec(fps, 1.5); // 1回の通過フレーム数
        const count = Math.min(9, Math.max(4, Math.round(4 + e.weight * 2)));
        const baseR = 5 + e.weight * 2;

        return (
          <g key={ei}>
            {Array.from({length: count}).map((_, j) => {
              // ソースから時間差で放出（offset<1）→ その後ループ
              const offset = j / count + random(`mf-po-${ei}-${j}`) * (0.5 / count);
              const phase = local / travel - offset;
              if (phase < 0) return null;
              const tRaw = phase - Math.floor(phase);
              const t = speedEase(tRaw); // 速度をイーズド化（加減速）
              const p = quad(e.a, e.c, e.b, t);
              // 出現/吸収のエンベロープ（移動＋scale＋opacity 併用）
              const env = interpolate(
                tRaw,
                [0, 0.12, 0.86, 1],
                [0, 1, 1, 0],
                {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
              );
              const r = baseR * interpolate(env, [0, 1], [0.35, 1]);
              return (
                <g key={j} transform={`translate(${p.x} ${p.y})`} opacity={env}>
                  <circle r={r * 1.9} fill="url(#mf-coin)" opacity={0.7} />
                  <circle
                    r={r}
                    fill={gold}
                    stroke={silver}
                    strokeWidth={r * 0.16}
                    strokeOpacity={0.6}
                  />
                  <circle
                    cx={-r * 0.28}
                    cy={-r * 0.32}
                    r={r * 0.32}
                    fill={white}
                    opacity={0.9}
                  />
                </g>
              );
            })}
          </g>
        );
      })}
    </svg>
  );
};

// ---------------------------------------------------------------------
// ソフトな金グロー先端が各エッジを走る — Trail 内で frame を読む
// ---------------------------------------------------------------------
const GlowTravel: React.FC<{edges: EdgeGeom[]}> = ({edges}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {gold} = BRAND.color;
  const glideEase = Easing.inOut(Easing.cubic);

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{position: 'absolute', inset: 0}}
    >
      <defs>
        <radialGradient id="mf-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={gold} stopOpacity={0.85} />
          <stop offset="55%" stopColor={gold} stopOpacity={0.35} />
          <stop offset="100%" stopColor={gold} stopOpacity={0} />
        </radialGradient>
      </defs>
      {edges.map((e, ei) => {
        if (frame < e.startF) return null;
        const local = frame - e.startF;
        const travel = sec(fps, 1.9);
        const phase = local / travel;
        const tRaw = phase - Math.floor(phase);
        const t = glideEase(tRaw);
        const p = quad(e.a, e.c, e.b, t);
        const env = interpolate(tRaw, [0, 0.14, 0.82, 1], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const rad = (26 + e.weight * 6) * interpolate(env, [0, 1], [0.5, 1]);
        return (
          <circle
            key={ei}
            cx={p.x}
            cy={p.y}
            r={rad}
            fill="url(#mf-glow)"
            opacity={env}
          />
        );
      })}
    </svg>
  );
};

// ---------------------------------------------------------------------
// ノードマーカー（spring ポップ + 着地スカッシュ + 常時パルス） — Trail 内
// ---------------------------------------------------------------------
const NodeMarkers: React.FC<{pts: Pt[]}> = ({pts}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const {navy, electric, white, gold} = BRAND.color;

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{position: 'absolute', inset: 0}}
    >
      {pts.map((p, i) => {
        const st = nodeStartF(fps, i);
        const pop = spring({
          frame: frame - st,
          fps,
          config: {damping: 12, mass: 0.8, stiffness: 150},
        });
        const grow = Math.max(0, pop);
        // 着地スカッシュ（縦つぶれ→戻り）
        const squash = interpolate(
          grow,
          [0.4, 0.58, 0.8, 1],
          [1, 0.72, 1.1, 1],
          {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
        );
        const r = interpolate(grow, [0, 1], [0, 22], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const appear = interpolate(grow, [0, 0.2], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        // 着地後の常時パルスリング（scale 主体・never static）
        const landed = interpolate(grow, [0.7, 1], [0, 1], {
          extrapolateLeft: 'clamp',
        });
        const pulse = interpolate(
          Math.sin((frame - st) / fps * Math.PI * 2 * 0.9),
          [-1, 1],
          [1, 2.0],
        );
        return (
          <g
            key={i}
            transform={`translate(${p.x} ${p.y}) scale(${1 / squash}, ${squash})`}
            opacity={appear}
          >
            {/* 着地パルスリング */}
            <circle
              r={r * pulse}
              fill="none"
              stroke={gold}
              strokeWidth={2}
              opacity={landed * interpolate(pulse, [1, 2.0], [0.55, 0])}
            />
            {/* 発光ハロー */}
            <circle r={r + 12} fill={electric} opacity={0.16} />
            {/* 本体ディスク（不透明・stroke アクセント） */}
            <circle r={r} fill={navy} stroke={electric} strokeWidth={3} />
            <circle r={r * 0.42} fill={electric} />
            <circle r={r * 0.16} fill={white} />
          </g>
        );
      })}
    </svg>
  );
};

// ---------------------------------------------------------------------
// ノードラベル（HTML・マスク切れ上がり）
// ---------------------------------------------------------------------
const NodeLabels: React.FC<{nodes: MFNode[]; pts: Pt[]}> = ({nodes, pts}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {ink, electric, white} = BRAND.color;

  return (
    <>
      {nodes.map((n, i) => {
        if (!n.label) return null;
        const labelStart = nodeStartF(fps, i) + sec(fps, 0.18);
        const lp = spring({
          frame: frame - labelStart,
          fps,
          config: {damping: 16, mass: 0.9},
        });
        const ly = interpolate(lp, [0, 1], [120, 0]);
        const lo = interpolate(lp, [0, 0.3], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: pts[i].x,
              top: pts[i].y,
              transform: 'translate(-50%, 0)',
              marginTop: 40,
              overflow: 'hidden',
              paddingBottom: '0.16em',
              opacity: lo,
            }}
          >
            <div
              style={{
                transform: `translateY(${ly}%)`,
                whiteSpace: 'nowrap',
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 26,
                letterSpacing: 1.4,
                textTransform: 'uppercase',
                color: white,
                padding: '5px 13px',
                borderRadius: 7,
                background: 'rgba(6,8,15,0.55)',
                border: `1px solid ${electric}55`,
                textShadow: `0 2px 10px ${ink}`,
              }}
            >
              {n.label}
            </div>
          </div>
        );
      })}
    </>
  );
};

// =====================================================================
// 親：フルスクリーン・シーン「Follow the money」
// =====================================================================
export const MoneyFlow: React.FC<{
  nodes: {x: number; y: number; label?: string}[];
  edges: {from: number; to: number; weight?: number}[];
  dur?: number;
}> = ({nodes, edges, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  const {ink, electric, silver, gold, white} = BRAND.color;

  // 0..1 → ピクセル座標
  const pts: Pt[] = nodes.map((n) => ({x: n.x * width, y: n.y * height}));
  const fallback: Pt = {x: width / 2, y: height / 2};

  // エッジ幾何（制御点・弧長・活性化フレーム）
  const edgeGeoms: EdgeGeom[] = edges.map((e, i) => {
    const a = pts[e.from] ?? fallback;
    const b = pts[e.to] ?? fallback;
    const mid = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2};
    const dx = b.x - a.x;
    const dy = b.y - a.y;
    const dist = Math.hypot(dx, dy) || 1;
    // 中点から垂直方向へ弓なり（決定論的に符号決定）
    const nx = -dy / dist;
    const ny = dx / dist;
    const sign = random(`mf-curve-${i}`) > 0.5 ? 1 : -1;
    const bow = dist * 0.16 * sign;
    const c = {x: mid.x + nx * bow, y: mid.y + ny * bow};
    // 近似弧長
    let len = 0;
    let prev = a;
    for (let s = 1; s <= 24; s++) {
      const q = quad(a, c, b, s / 24);
      len += Math.hypot(q.x - prev.x, q.y - prev.y);
      prev = q;
    }
    return {
      a,
      b,
      c,
      len: len || 1,
      weight: e.weight ?? 1,
      startF: sec(fps, 0.6) + i * sec(fps, 0.26),
      path: `M ${a.x} ${a.y} Q ${c.x} ${c.y} ${b.x} ${b.y}`,
    };
  });

  // シーン出入り（opacity単独禁止 → translateY と併用）
  const inP = spring({
    frame,
    fps,
    config: {damping: 200},
    durationInFrames: sec(fps, 0.5),
  });
  const sceneY = interpolate(inP, [0, 1], [24, 0]);
  const outO = interpolate(frame, [D - sec(fps, 0.4), D], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outY = interpolate(frame, [D - sec(fps, 0.4), D], [0, -16], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 奥行きの微アニメ（never static）
  const gridDrift = interpolate(frame, [0, D], [0, 44], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  const glowBreath = 0.5 + 0.5 * Math.sin((frame / fps) * 1.2);

  // 微視差パララックス（sin easing）
  const px = interpolate(
    Math.sin((frame / fps) * Math.PI * 2 * 0.07),
    [-1, 1],
    [-12, 12],
  );
  const py = interpolate(
    Math.cos((frame / fps) * Math.PI * 2 * 0.05),
    [-1, 1],
    [-8, 8],
  );

  // 決定論的な奥行きスペック（微発光の塵）
  const specks = Array.from({length: 60}, (_, i) => ({
    x: random(`mf-sx-${i}`) * width,
    y: random(`mf-sy-${i}`) * height,
    r: 0.6 + random(`mf-sr-${i}`) * 1.7,
    tw: random(`mf-st-${i}`),
  }));

  // キッカー（マスク切れ上がり）
  const kicker = spring({
    frame: frame - sec(fps, 0.1),
    fps,
    config: {damping: 18, mass: 0.9},
  });
  const kickerY = interpolate(kicker, [0, 1], [120, 0]);
  const kickerO = interpolate(kicker, [0, 0.3], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', opacity: outO}}>
      {/* Layer 1: 正典フルスクリーン背景グラデ */}
      <AbsoluteFill style={{background: SCENE_BG}} />

      {/* Layer 2: 奥行きスペック（微発光の塵） */}
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="none"
        style={{position: 'absolute', inset: 0}}
      >
        {specks.map((s, i) => {
          const tw = interpolate(
            Math.sin((frame / fps) * Math.PI * 2 * (0.35 + s.tw) + i),
            [-1, 1],
            [0.12, 0.48],
          );
          const rr = s.r * interpolate(tw, [0.12, 0.48], [0.75, 1.15]);
          return <circle key={i} cx={s.x} cy={s.y} r={rr} fill={silver} opacity={tw} />;
        })}
      </svg>

      {/* Layer 3: グリッド（電光・微ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.14,
          transform: `translateY(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${electric}26 0px, ${electric}26 1px, transparent 1px, transparent 82px),
            repeating-linear-gradient(90deg, ${electric}26 0px, ${electric}26 1px, transparent 1px, transparent 82px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 46%, black 28%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 28%, transparent 84%)',
        }}
      />

      {/* Layer 4: アクセントグロー（常時呼吸） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(48% 44% at 50% 47%, ${electric}44 0%, transparent 64%)`,
          opacity: 0.3 + 0.18 * glowBreath,
          mixBlendMode: 'screen',
        }}
      />

      {/* Layer 5: グラフ平面（微パララックス + シーン出入り） */}
      <AbsoluteFill
        style={{transform: `translate(${px}px, ${py + sceneY + outY}px)`}}
      >
        {/* エッジ本体（描き上げ・weight 太さ） */}
        <EdgesBase edges={edgeGeoms} />

        {/* ソフト金グロー先端（速い → Trail） */}
        <Trail
          layers={FAST_TRAIL.layers}
          lagInFrames={FAST_TRAIL.lagInFrames}
          trailOpacity={FAST_TRAIL.trailOpacity}
        >
          <GlowTravel edges={edgeGeoms} />
        </Trail>

        {/* 金コインの価値ストリーム（速い → Trail） */}
        <Trail
          layers={FAST_TRAIL.layers}
          lagInFrames={FAST_TRAIL.lagInFrames}
          trailOpacity={FAST_TRAIL.trailOpacity}
        >
          <CoinStream edges={edgeGeoms} />
        </Trail>

        {/* ノードマーカー（ポップ → Trail） */}
        <Trail
          layers={FAST_TRAIL.layers}
          lagInFrames={FAST_TRAIL.lagInFrames}
          trailOpacity={FAST_TRAIL.trailOpacity}
        >
          <NodeMarkers pts={pts} />
        </Trail>

        {/* ノードラベル（マスク切れ上がり・非Trail） */}
        <NodeLabels nodes={nodes} pts={pts} />
      </AbsoluteFill>

      {/* Layer 6: キッカー見出し（マスク切れ上がり） */}
      <div
        style={{
          position: 'absolute',
          top: 96,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          opacity: kickerO,
        }}
      >
        <div style={{overflow: 'hidden', paddingBottom: '0.16em'}}>
          <div
            style={{
              transform: `translateY(${kickerY}%)`,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 30,
              letterSpacing: 9,
              textTransform: 'uppercase',
              color: gold,
              textShadow: `0 2px 14px ${ink}`,
            }}
          >
            Follow the Money
          </div>
        </div>
      </div>

      {/* Layer 7: ビネット（縁を締める） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 46%, rgba(0,0,0,0.64) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* 極薄のトップシャイン（白・奥行き補助・opacity単独回避のため微 translate） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(90% 60% at 50% 0%, ${white}0f 0%, transparent 55%)`,
          transform: `translateY(${(-glowBreath * 6).toFixed(2)}px)`,
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
