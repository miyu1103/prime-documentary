import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  Sequence,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

// =====================================================================
// Figures — ドキュメンタリー用「動く図解」部品集（Bのダーク＋発光トーン）
//   Scene1 StatCounter    数字カウントアップ（ヒーロー数値）
//   Scene2 Timeline       年表：線が伸びて点がスタッガー出現＋キャプション切れ上がり
//   Scene3 BarChart       棒が0から立ち上がる（角丸データ端・値カウント・直接ラベル）
//   Scene4 NetworkDiagram 関係図：エッジが描かれてノードがポップ
// 品質ルール準拠: 全モーションにイージング/spring・opacity単独なし・スタッガー・
//   マスク切れ上がり・単一アクセント＋抑えた軸（dataviz配色ガイド）。
// props で各話のデータ差し替え可能。
// =====================================================================

const INK = '#ffffff';
const INK2 = '#c8d2e6';
const MUTED = '#6b7688';
const BG = '#06080f';

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// 毎フレーム更新のフィルムグレイン
const grain = (frame: number, opacity: number): React.CSSProperties => {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>` +
    `<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 131}'/>` +
    `<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>`;
  return {
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svg)}")`,
    backgroundSize: '200px 200px',
    mixBlendMode: 'overlay',
    opacity,
    pointerEvents: 'none',
  };
};

// 共通背景（暗いグラデ＋うっすらグリッド＋アクセントグロー＋ビネット）
const Backdrop: React.FC<{accent: string}> = ({accent}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const drift = interpolate(frame, [0, durationInFrames], [0, 40], {
    easing: Easing.inOut(Easing.sin),
  });
  return (
    <>
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 120% at 50% 30%, #0e1424 0%, #080b14 50%, ${BG} 100%)`,
        }}
      />
      <AbsoluteFill
        style={{
          opacity: 0.14,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 72px),
            repeating-linear-gradient(90deg, ${accent}22 0px, ${accent}22 1px, transparent 1px, transparent 72px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 45%, rgba(0,0,0,0.66) 100%)',
        }}
      />
    </>
  );
};

// シーンの出入りフェード（opacity単独禁止なので必ず微translateYと併用）
const sceneFade = (frame: number, dur: number) => {
  const o = interpolate(frame, [0, 10, dur - 12, dur], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const y = interpolate(frame, [0, 10], [16, 0], {extrapolateRight: 'clamp'});
  return {opacity: o, y};
};

// マスク切れ上がりの見出し（1文字スタッガー）
const MaskTitle: React.FC<{
  text: string;
  fps: number;
  start: number;
  size: number;
  weight?: number;
  serif?: boolean;
  color?: string;
}> = ({text, fps, start, size, weight = 700, serif, color = INK}) => {
  const frame = useCurrentFrame();
  const chars = Array.from(text);
  const st = Math.max(1, sec(fps, 0.03));
  return (
    <div
      style={{
        display: 'flex',
        fontFamily: serif ? "'Times New Roman', Georgia, serif" : 'Inter, system-ui, sans-serif',
        fontWeight: weight,
        fontSize: size,
        letterSpacing: serif ? 1 : -0.5,
        color,
        lineHeight: 1.05,
      }}
    >
      {chars.map((ch, i) => {
        const cs = spring({frame: frame - sec(fps, start) - i * st, fps, config: {damping: 16, mass: 1}});
        const y = interpolate(cs, [0, 1], [110, 0]);
        const o = interpolate(cs, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
        return (
          <span key={i} style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}>
            <span style={{display: 'inline-block', transform: `translateY(${y}%)`, opacity: o, whiteSpace: 'pre'}}>
              {ch}
            </span>
          </span>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------------
// Scene 1: 数字カウントアップ（ヒーロー数値）
// ---------------------------------------------------------------------
export const StatCounter: React.FC<{
  accent: string;
  value: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  label: string;
  topLabel?: string;
  dur: number;
}> = ({accent, value, prefix = '', suffix = '', decimals = 1, label, topLabel = 'By the numbers', dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {opacity, y} = sceneFade(frame, dur);

  // カウントは easing 付き（等速禁止）
  const p = interpolate(frame, [sec(fps, 0.2), sec(fps, 1.6)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // Thousands separators. EP74 itaewon shipped "11666" beside a NumberTicker showing "79,877":
  // the same film, the same kind of fact, two different readings, because only the ticker groups.
  // A four-figure number without separators is measurably slower to read at speed.
  const shown = (value * p).toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  const barW = interpolate(
    spring({frame: frame - sec(fps, 0.3), fps, config: {damping: 18}}),
    [0, 1],
    [0, 220],
  );

  return (
    <AbsoluteFill
      style={{justifyContent: 'center', alignItems: 'center', opacity, transform: `translateY(${y}px)`}}
    >
      <div style={{fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 500, fontSize: 26, letterSpacing: 8, textTransform: 'uppercase', color: MUTED, marginBottom: 18}}>
        {topLabel}
      </div>
      <div style={{display: 'flex', alignItems: 'baseline', color: INK, fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 800}}>
        <span style={{fontSize: 90, color: accent}}>{prefix}</span>
        <span style={{fontSize: 210, letterSpacing: -6, lineHeight: 0.9, fontVariantNumeric: 'tabular-nums'}}>{shown}</span>
        <span style={{fontSize: 90, color: accent, marginLeft: 8}}>{suffix}</span>
      </div>
      <div style={{width: barW, height: 5, borderRadius: 3, backgroundColor: accent, boxShadow: `0 0 24px ${accent}aa`, marginTop: 20}} />
      {/* WIDTH CEILING (2026-09-01). This line had no width and no wrap, so a long source note
          grew past both frame edges and stayed there for the whole hold. MEASURED on the EP73
          uri master of 11:48: the 246 card read "he Texas Department of State Health Services
          figure ... This film uses no oth" / "umber as fact. (TX-26)" -- the attribution was
          unreadable for its entire six seconds. Same defect the lower-third and the timeline had;
          the fixes for those did not reach this component.
          1400 = 1920 - 2*260, and 260 covers the worst case of the two ken-burns transforms this
          figure still rides (FigureScene pan 46 + scale 1.16 about the centre = 153.6, Drift pan
          17 + scale 1.035 = 33.6, about 250px). Centred content, so the margin is symmetric. */}
      <div style={{marginTop: 22, fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 500, fontSize: 30, letterSpacing: 2, color: INK2, maxWidth: 1400, textAlign: 'center', lineHeight: 1.25}}>
        {label}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// Scene 2: タイムライン（線が伸びる→点スタッガー→キャプション切れ上がり）
// ---------------------------------------------------------------------
export const Timeline: React.FC<{
  accent: string;
  events: {year: string; text: string}[];
  dur: number;
}> = ({accent, events, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const {opacity, y} = sceneFade(frame, dur);

  const x0 = 220;
  const x1 = width - 220;
  const cy = 540;
  // KEEPING THE CAPTIONS ON SCREEN (2026-09-01).
  // The node captions are SVG <text x={0} textAnchor="middle"> centred on their node, and the
  // first and last nodes sit at x=220 and x=width-220. So any caption wider than 440px hangs off
  // the frame -- half of it at each end. SVG text does not wrap, so a long event string just kept
  // going. MEASURED on EP73 uri: at 6:04-6:11 the right-hand node read "the report, and the
  // decision take" with "taken" severed at the frame edge and the left-hand node sat flush at
  // x=0; at 26:47 the same figure read "he cold. A joint federal inquiry follows" (missing the
  // T) and "Statewide Rule 66 adopte" (missing the d), and the first and last dots were half
  // off-frame. 25 films and 83 figures use this component.
  // Two things are needed and neither is optional: wrap the string so one line cannot be wider
  // than the space a node owns, and clamp the anchor so an end node's caption cannot cross the
  // safe margin. Width is approximated from the character count -- there is no text metric in a
  // deterministic render -- with 0.54em, which over-estimates for Inter and therefore errs
  // towards wrapping early rather than late.
  const SAFE = 96;                       // px kept clear at each frame edge
  const nEvents = events.length;         // NOT `n`: that const is declared below this block
  const span = nEvents > 1 ? (x1 - x0) / (nEvents - 1) : x1 - x0;
  const capMax = Math.max(200, Math.min(span - 28, 430));
  const em = (size: number) => size * 0.54;
  const wrap = (text: string, size: number): string[] => {
    const max = Math.max(8, Math.floor(capMax / em(size)));
    const out: string[] = [];
    let line = '';
    for (const w of String(text ?? '').split(' ')) {
      const next = line ? line + ' ' + w : w;
      if (next.length > max && line) {
        out.push(line);
        line = w;
      } else {
        line = next;
      }
    }
    if (line) out.push(line);
    return out.slice(0, 3);              // three lines is already a wall of text on a node
  };
  // dx that pulls a centred line back inside [SAFE, width - SAFE] without moving the node itself
  const clampDx = (ex: number, text: string, size: number) => {
    const half = (text.length * em(size)) / 2;
    const lo = SAFE + half;
    const hi = width - SAFE - half;
    if (lo > hi) return 0;               // a line wider than the frame: leave it centred
    return Math.max(lo, Math.min(hi, ex)) - ex;
  };
  const lineP = interpolate(
    spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 30, mass: 1}}),
    [0, 1],
    [0, 1],
  );
  const lineX = interpolate(lineP, [0, 1], [x0, x1]);
  const n = events.length;

  return (
    <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
      <div style={{position: 'absolute', top: 150, left: 220}}>
        <MaskTitle text="TIMELINE OF THE CASE" fps={fps} start={0.1} size={40} weight={600} color={INK2} />
      </div>
      <svg width={width} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* ベース線（伸びる） */}
        <line x1={x0} y1={cy} x2={lineX} y2={cy} stroke={accent} strokeWidth={2} opacity={0.55} />
        {events.map((e, i) => {
          // n === 1 divided by zero here and put the only node at NaN, which SVG drops silently.
          const ex = n > 1 ? x0 + ((x1 - x0) * i) / (n - 1) : (x0 + x1) / 2;
          const cs = spring({frame: frame - sec(fps, 0.5) - i * sec(fps, 0.18), fps, config: {damping: 14, mass: 0.8}});
          const r = interpolate(cs, [0, 1], [0, 9]);
          const glow = interpolate(cs, [0, 1], [0, 0.9]);
          const capY = interpolate(cs, [0, 1], [24, 0]);
          const up = i % 2 === 0;
          return (
            <g key={i}>
              <circle cx={ex} cy={cy} r={r + 8} fill={accent} opacity={glow * 0.18} />
              <circle cx={ex} cy={cy} r={r} fill={INK} stroke={accent} strokeWidth={3} />
              <g transform={`translate(${ex}, ${up ? cy - 40 - capY : cy + 40 + capY})`} opacity={glow}>
                <text x={clampDx(ex, String(e.year ?? ""), 34)} y={up ? -34 : 34} fill={accent} fontFamily="Inter, system-ui" fontWeight={800} fontSize={34} textAnchor="middle">{e.year}</text>
                {wrap(e.text, 22).map((ln, li) => (
                  <text
                    key={li}
                    x={clampDx(ex, ln, 22)}
                    y={(up ? -6 : 62) + li * 26}
                    fill={INK2}
                    fontFamily="Inter, system-ui"
                    fontWeight={500}
                    fontSize={22}
                    textAnchor="middle"
                  >
                    {ln}
                  </text>
                ))}
              </g>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// Scene 3: 棒グラフ（0から立ち上がり・角丸データ端・値カウント・直接ラベル）
// ---------------------------------------------------------------------
export const BarChart: React.FC<{
  accent: string;
  data: {label: string; value: number}[];
  unit?: string;
  dur: number;
  /**
   * The heading above the bars. It used to be the literal string
   * "FORFEITURE CASES / YEAR", hardcoded here, so EVERY episode drawing a bar chart
   * got a civil-forfeiture caption whatever its subject was. Found 2026-08-27 in the
   * shipped frames of EP73 uri at 14:32-14:36, where bars correctly labelled
   * "Held below 59.4 Hz" and "The nine-minute threshold" sat under a heading about
   * forfeiture cases. `.claude/rules/remotion-motion.md` already forbids hardcoding a
   * specific case into a component; this was the violation.
   * Omitted -> no heading, which is the safe default: silence beats a wrong label.
   */
  title?: string;
}> = ({accent, data, unit = '', dur, title}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const {opacity, y} = sceneFade(frame, dur);

  const max = Math.max(...data.map((d) => d.value));
  const baseY = 820;
  const top = 300;
  const plotH = baseY - top;
  const n = data.length;
  const slot = (width - 440) / n;
  const bw = Math.min(150, slot * 0.5);

  return (
    <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
      {title ? (
        <div style={{position: 'absolute', top: 150, left: 220}}>
          <MaskTitle text={title} fps={fps} start={0.1} size={40} weight={600} color={INK2} />
        </div>
      ) : null}
      <svg width={width} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* ベースライン（抑えた軸） */}
        <line x1={200} y1={baseY} x2={width - 200} y2={baseY} stroke={MUTED} strokeWidth={2} opacity={0.5} />
        {data.map((d, i) => {
          const cx = 220 + slot * i + slot / 2;
          const cs = spring({frame: frame - sec(fps, 0.3) - i * sec(fps, 0.12), fps, config: {damping: 18, mass: 1}});
          const h = interpolate(cs, [0, 1], [0, (d.value / max) * plotH]);
          const shownVal = Math.round(d.value * interpolate(cs, [0, 1], [0, 1]));
          return (
            <g key={i}>
              {/* 棒（角丸データ端はベースラインに接地。上端だけ丸め） */}
              <rect x={cx - bw / 2} y={baseY - h} width={bw} height={h} rx={6} fill={accent} />
              {/* データ端をベースに密着させる被せ（角丸の下側を隠す） */}
              <rect x={cx - bw / 2} y={baseY - Math.min(h, 10)} width={bw} height={Math.min(h, 10)} fill={accent} />
              {/* 値（直接ラベル） */}
              <text x={cx} y={baseY - h - 18} fill={INK} fontFamily="Inter, system-ui" fontWeight={800} fontSize={34} textAnchor="middle" opacity={interpolate(cs, [0.3, 1], [0, 1], {extrapolateLeft: 'clamp'})}>
                {shownVal}{unit}
              </text>
              {/* カテゴリラベル */}
              <text x={cx} y={baseY + 40} fill={INK2} fontFamily="Inter, system-ui" fontWeight={500} fontSize={26} textAnchor="middle">{d.label}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// Scene 4: 関係図（エッジが描かれる→ノードがポップ＋ラベル）
// ---------------------------------------------------------------------
export const NetworkDiagram: React.FC<{
  accent: string;
  nodes: {id: string; x: number; y: number}[];
  edges: [number, number][];
  dur: number;
}> = ({accent, nodes, edges, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const {opacity, y} = sceneFade(frame, dur);

  return (
    <AbsoluteFill style={{opacity, transform: `translateY(${y}px)`}}>
      <div style={{position: 'absolute', top: 120, left: 220}}>
        <MaskTitle text="FOLLOW THE MONEY" fps={fps} start={0.1} size={40} weight={600} color={INK2} />
      </div>
      <svg width={width} height={1080} style={{position: 'absolute', inset: 0}}>
        {/* エッジ：strokeDashoffset で描画 */}
        {edges.map(([a, b], i) => {
          const na = nodes[a];
          const nb = nodes[b];
          const len = Math.hypot(nb.x - na.x, nb.y - na.y);
          const p = interpolate(
            spring({frame: frame - sec(fps, 0.4) - i * sec(fps, 0.1), fps, config: {damping: 26}}),
            [0, 1],
            [0, 1],
          );
          return (
            <line
              key={i}
              x1={na.x} y1={na.y} x2={nb.x} y2={nb.y}
              stroke={accent} strokeWidth={2} opacity={0.5}
              strokeDasharray={len} strokeDashoffset={len * (1 - p)}
            />
          );
        })}
        {/* ノード：ポップ＋ラベル */}
        {nodes.map((nd, i) => {
          const cs = spring({frame: frame - sec(fps, 0.7) - i * sec(fps, 0.12), fps, config: {damping: 13, mass: 0.7}});
          const r = interpolate(cs, [0, 1], [0, 16]);
          const o = interpolate(cs, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
          return (
            <g key={i} opacity={o}>
              <circle cx={nd.x} cy={nd.y} r={r + 14} fill={accent} opacity={0.14} />
              <circle cx={nd.x} cy={nd.y} r={r} fill="#0b1020" stroke={accent} strokeWidth={3} />
              <text x={nd.x} y={nd.y + 48} fill={INK} fontFamily="Inter, system-ui" fontWeight={700} fontSize={26} textAnchor="middle">{nd.id}</text>
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// 親：4シーンを順に流すショーケース
// ---------------------------------------------------------------------
export type FiguresProps = {accent: string};

export const figuresDurationInFrames = (fps: number) => Math.round(fps * 8.8);

export const Figures: React.FC<FiguresProps> = ({accent}) => {
  const {fps} = useVideoConfig();
  const D = sec(fps, 2.2);

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      <Backdrop accent={accent} />

      <Sequence from={0} durationInFrames={D}>
        <StatCounter accent={accent} prefix="$" value={68.8} suffix="B" decimals={1} label="Total civil-forfeiture proceeds, U.S." dur={D} />
      </Sequence>

      <Sequence from={D} durationInFrames={D}>
        <Timeline
          accent={accent}
          dur={D}
          events={[
            {year: '1984', text: 'Reform Act'},
            {year: '2000', text: 'CAFRA passed'},
            {year: '2014', text: 'Record seizures'},
            {year: '2019', text: 'Timbs v. Indiana'},
          ]}
        />
      </Sequence>

      <Sequence from={D * 2} durationInFrames={D}>
        <BarChart
          accent={accent}
          dur={D}
          unit="k"
          data={[
            {label: '2013', value: 38},
            {label: '2015', value: 52},
            {label: '2017', value: 61},
            {label: '2019', value: 74},
          ]}
        />
      </Sequence>

      <Sequence from={D * 3} durationInFrames={D}>
        <NetworkDiagram
          accent={accent}
          dur={D}
          nodes={[
            {id: 'SHELL CO.', x: 500, y: 420},
            {id: 'OFFSHORE BANK', x: 960, y: 300},
            {id: 'OFFICIAL', x: 1420, y: 420},
            {id: 'SEIZED FUND', x: 960, y: 720},
          ]}
          edges={[[0, 1], [1, 2], [1, 3], [0, 3]]}
        />
      </Sequence>

      <AbsoluteFill style={grain(useCurrentFrame(), 0.07)} />
    </AbsoluteFill>
  );
};
