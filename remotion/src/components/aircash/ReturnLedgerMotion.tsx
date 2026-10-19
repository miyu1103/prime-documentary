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
// ReturnLedgerMotion (Manifest #27 / 幕4・60秒窓補填figure)
//   返還の可視化：政府側(奥・左)から、返還書類の束と帯封された現金束が
//   卓上(2.5Dテーブル)を「実際に滑って」原告(手前・右の手)へ渡っていく。
//   主キネティック＝物体の実移動（奥→手前へ滑走＝x横移動＋y前進＋scale拡大）。
//   束は数frameずつスタッガーで出発し、手前の受け皿へ積み上がる＝返還の量感。
//   走光/暖光は使わず、動きは全て物体移動。Trailで滑走にモーションブラー。
// 品質: 全モーションeased(spring / Easing.inOut(cubic))・opacity単独リビール無し
//   （出現は必ず移動と同時）・マスク切れ上がり文字・≥3レイヤー(暗青)・単一アクセント(gold)・
//   凍らない微シマー・deterministic(useCurrentFrame＋seeded mulberry32のみ)。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);
const BG = BRAND.color.ink;
const GOLD = BRAND.color.gold;
const SILVER = BRAND.color.silver;
const NAVY = BRAND.color.navy;

// deterministic seeded RNG（Math.random禁止）
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

type ItemType = 'bundle' | 'doc';
type ItemSpec = {type: ItemType; departFrac: number; lane: 0 | 1; stack: number};

// 8体：帯封束5＋返還書類3。出発は 0.05D→0.60D に等間隔スタッガー、
// 走行は 0.30D。到着は最遅 ~0.90D → 移動の被覆はビート尺の ~85%。
const ITEMS: ItemSpec[] = [
  {type: 'bundle', departFrac: 0.05, lane: 0, stack: 0},
  {type: 'doc', departFrac: 0.13, lane: 1, stack: 1},
  {type: 'bundle', departFrac: 0.21, lane: 0, stack: 2},
  {type: 'bundle', departFrac: 0.29, lane: 1, stack: 3},
  {type: 'doc', departFrac: 0.37, lane: 0, stack: 4},
  {type: 'bundle', departFrac: 0.45, lane: 1, stack: 5},
  {type: 'doc', departFrac: 0.53, lane: 0, stack: 6},
  {type: 'bundle', departFrac: 0.6, lane: 1, stack: 7},
];
const TRAVEL_FRAC = 0.3;

// --- 現金束（帯封）ベクター。原点中心・幅約140 ---
const CashBundle: React.FC = () => (
  <svg width={150} height={92} viewBox="-75 -46 150 92">
    {/* 束の本体（札の重なり） */}
    <rect x={-62} y={-27} width={124} height={54} rx={6} fill={NAVY} stroke={SILVER} strokeWidth={2} />
    {/* 札の縁の重なり線 */}
    {[-16, -6, 4, 14].map((y) => (
      <line key={y} x1={-56} y1={y} x2={56} y2={y} stroke={SILVER} strokeWidth={1.4} opacity={0.28} />
    ))}
    {/* 帯封（gold・縦帯） */}
    <rect x={-15} y={-31} width={30} height={62} fill={GOLD} opacity={0.92} />
    <rect x={-15} y={-31} width={30} height={62} fill="none" stroke={GOLD} strokeWidth={2} />
    {/* 帯のハイライト */}
    <rect x={-4} y={-31} width={5} height={62} fill={BRAND.color.white} opacity={0.35} />
    {/* 上端のエッジ */}
    <rect x={-62} y={-31} width={124} height={6} rx={3} fill={SILVER} opacity={0.2} />
  </svg>
);

// --- 返還書類（1枚）。原点中心・縦向き ---
const ReturnDoc: React.FC = () => (
  <svg width={104} height={132} viewBox="-52 -66 104 132">
    <rect x={-46} y={-60} width={92} height={120} rx={4} fill={SILVER} fillOpacity={0.16} stroke={SILVER} strokeWidth={2} />
    {/* ヘッダ帯（gold） */}
    <rect x={-46} y={-60} width={92} height={16} rx={4} fill={GOLD} opacity={0.85} />
    {/* 本文行 */}
    {[-30, -18, -6, 6, 18, 30].map((y) => (
      <line key={y} x1={-36} y1={y} x2={y === 30 ? 6 : 36} y2={y} stroke={SILVER} strokeWidth={2} opacity={0.45} />
    ))}
    {/* 返還印（gold seal） */}
    <circle cx={26} cy={40} r={12} fill="none" stroke={GOLD} strokeWidth={2.5} />
    <circle cx={26} cy={40} r={5} fill={GOLD} opacity={0.9} />
  </svg>
);

// --- 受け取る手（シルエット・手のみ／匿名。invariant11） ---
const Palm: React.FC<{flip?: boolean}> = ({flip}) => (
  <g transform={flip ? 'scale(-1,1)' : undefined}>
    {/* 手のひら */}
    <path
      d="M-46,40 L-46,-8 Q-46,-22 -32,-22 L26,-22 Q40,-22 40,-8 L40,40 Z"
      fill={NAVY}
      stroke={SILVER}
      strokeWidth={2.5}
      strokeLinejoin="round"
    />
    {/* 指 */}
    {[-30, -12, 6, 24].map((x, i) => (
      <rect key={x} x={x} y={-52 + (i === 0 || i === 3 ? 8 : 0)} width={14} height={34} rx={7} fill={NAVY} stroke={SILVER} strokeWidth={2.5} />
    ))}
    {/* 親指 */}
    <rect x={38} y={2} width={30} height={14} rx={7} fill={NAVY} stroke={SILVER} strokeWidth={2.5} transform="rotate(24 42 8)" />
  </g>
);

// マスク切れ上がりラベル
const MaskLabel: React.FC<{
  text: string;
  fps: number;
  start: number;
  size: number;
  color: string;
  weight: number;
  letter: number;
  family: string;
}> = ({text, fps, start, size, color, weight, letter, family}) => {
  const frame = useCurrentFrame();
  const cs = spring({frame: frame - sec(fps, start), fps, config: {damping: 16, mass: 0.9}});
  const y = interpolate(cs, [0, 1], [118, 0]);
  const o = interpolate(cs, [0, 0.35], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.16em'}}>
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: family,
          fontWeight: weight,
          fontSize: size,
          letterSpacing: letter,
          color,
          whiteSpace: 'pre',
        }}
      >
        {text}
      </span>
    </span>
  );
};

// =====================================================================
// 滑走する束/書類の隊列（Trailに包む＝useCurrentFrameを内部で読み、
//   TimeShiftされた各層が実際に別位置を描く＝本物のモーションブラー）
// =====================================================================
const Procession: React.FC<{D: number; seed: number}> = ({D, seed}) => {
  const frame = useCurrentFrame();
  const {width: W, height: H, fps} = useVideoConfig();

  // 卓上の座標（fraction→px）
  const startX = 0.07 * W;
  const laneY = [0.31 * H, 0.4 * H];
  // 受け皿（原告手前・右）に積み上がる
  const pileX = 0.63 * W;
  const pileBaseY = 0.78 * H;

  const rnd = mulberry32(seed);
  // 各itemの微小jitter（決定論）
  const jitters = ITEMS.map(() => ({
    x: (rnd() - 0.5) * 22,
    y: (rnd() - 0.5) * 10,
    rot: (rnd() - 0.5) * 10,
  }));

  return (
    <AbsoluteFill>
      {ITEMS.map((it, i) => {
        const j = jitters[i];
        const raw = (frame / D - it.departFrac) / TRAVEL_FRAC;
        // 走行前は非表示（出発と同時に移動しながら出現＝opacity単独リビール回避）
        if (raw <= 0 && frame / D < it.departFrac) {
          // まだ出発していない → 描かない
          return null;
        }
        const p = interpolate(raw, [0, 1], [0, 1], {
          easing: Easing.inOut(Easing.cubic),
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        // 経路：奥左 → 手前右（x横移動＋y前進＋scale拡大＝2.5D接近）
        const sx = startX + it.lane * 0.02 * W;
        const sy = laneY[it.lane];
        const ex = pileX + j.x;
        const ey = pileBaseY - it.stack * 0.026 * H + j.y;

        const px = interpolate(p, [0, 1], [sx, ex]);
        const py = interpolate(p, [0, 1], [sy, ey]);
        const scale = interpolate(p, [0, 1], [0.5, 1.06]);

        // 出現：移動の最初の 12% で立ち上げ（移動と必ず同時）
        const appear = interpolate(raw, [0, 0.12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        // 到着後の微bob（凍結防止・副次／主運動ではない）
        const settled = interpolate(raw, [1, 1.05], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const bob = settled * 2.4 * Math.sin((frame / fps) * ((2 * Math.PI) / 2.6) + i);

        const rot =
          interpolate(p, [0, 1], [j.rot - 6 * it.lane, j.rot * 0.4]) + bob * 0.4;

        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 0,
              top: 0,
              transform: `translate(${px}px, ${py + bob}px) translate(-50%, -50%) scale(${scale}) rotate(${rot}deg)`,
              opacity: appear,
              filter: `drop-shadow(0 ${8 * scale}px ${14 * scale}px rgba(0,0,0,0.55))`,
            }}
          >
            {it.type === 'bundle' ? <CashBundle /> : <ReturnDoc />}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

export const ReturnLedgerMotion: React.FC<{dur?: number; caption?: string}> = ({
  dur,
  caption = 'THE SAVINGS SLIDE BACK',
}) => {
  const frame = useCurrentFrame();
  const {fps, width: W, height: H, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // シーン出入り＋全体の緩い前進パララックス（凍らない・正弦＝イージング）
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 14], [20, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const driftX = 12 * Math.sin((frame / fps) * ((2 * Math.PI) / 8.4));
  const driftY = 7 * Math.sin((frame / fps) * ((2 * Math.PI) / 6.6) + 0.6);

  // 卓上の遠近トラペゾイド
  const farY = 0.28 * H;
  const nearY = 0.94 * H;
  const farL = 0.2 * W;
  const farR = 0.8 * W;
  const nearL = 0.02 * W;
  const nearR = 0.98 * W;

  // 卓上を横切る「送り」の微シマー（副次・主運動ではない）
  const feed = (frame / fps) * ((2 * Math.PI) / 3.2);

  // dust（seeded・副次のドリフト）
  const rnd = mulberry32(3407);
  const dust = Array.from({length: 20}).map(() => ({
    bx: rnd(),
    by: rnd(),
    ph: rnd() * Math.PI * 2,
    sp: 0.4 + rnd() * 0.5,
    r: 1.2 + rnd() * 1.8,
  }));

  // 受け皿マット
  const matX = 0.63 * W;
  const matY = 0.8 * H;

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1: 暗青ラジアル背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 110% at 52% 40%, ${NAVY} 0%, ${BG} 82%)`,
        }}
      />
      {/* L2: 微グリッド（凍らない微ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.07,
          transform: `translateY(${driftY * 0.6}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 74px),
            repeating-linear-gradient(90deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 74px)`,
          maskImage: 'radial-gradient(120% 92% at 52% 46%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 92% at 52% 46%, black 30%, transparent 82%)',
        }}
      />

      <AbsoluteFill style={{opacity: inO * outO, transform: `translate(${driftX}px, ${inY + driftY}px)`}}>
        {/* L3: 卓上（遠近トラペゾイド）＋受け皿＋送りライン */}
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="rlm-table" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={NAVY} stopOpacity={0.4} />
              <stop offset="100%" stopColor={NAVY} stopOpacity={0.95} />
            </linearGradient>
          </defs>

          {/* テーブル天板 */}
          <polygon
            points={`${farL},${farY} ${farR},${farY} ${nearR},${nearY} ${nearL},${nearY}`}
            fill="url(#rlm-table)"
            stroke={`${GOLD}55`}
            strokeWidth={2}
          />
          {/* 天板の暗色オーバーレイ（奥行き・pure black shadow可） */}
          <polygon
            points={`${farL},${farY} ${farR},${farY} ${nearR},${nearY} ${nearL},${nearY}`}
            fill="rgba(0,0,0,0.28)"
          />
          {/* 奥行きの横ライン（遠近） */}
          {Array.from({length: 6}).map((_, i) => {
            const t = (i + 1) / 7;
            const y = farY + (nearY - farY) * t;
            const lx = farL + (nearL - farL) * t;
            const rx = farR + (nearR - farR) * t;
            return (
              <line key={i} x1={lx} y1={y} x2={rx} y2={y} stroke={`${SILVER}18`} strokeWidth={1.5} />
            );
          })}
          {/* 卓上を奥→手前へ流れる送りダッシュ（副次シマー） */}
          {Array.from({length: 5}).map((_, i) => {
            const base = ((Math.sin(feed + i * 1.1) + 1) / 2) * 0.8 + 0.1; // 0.1..0.9
            const y = farY + (nearY - farY) * base;
            const lx = farL + (nearL - farL) * base;
            const rx = farR + (nearR - farR) * base;
            const cxp = (lx + rx) / 2;
            return (
              <circle key={i} cx={cxp} cy={y} r={2.4} fill={GOLD} opacity={0.18 + 0.12 * base} />
            );
          })}

          {/* 受け皿マット（原告側・gold outline） */}
          <ellipse
            cx={matX}
            cy={matY}
            rx={0.19 * W}
            ry={0.07 * H}
            fill={`${GOLD}10`}
            stroke={`${GOLD}66`}
            strokeWidth={2}
          />

          {/* 政府側（奥左）の出所トレイ */}
          <rect
            x={0.03 * W}
            y={0.24 * H}
            width={0.16 * W}
            height={0.11 * H}
            rx={8}
            fill={`${NAVY}`}
            stroke={`${SILVER}44`}
            strokeWidth={2}
          />
        </svg>

        {/* dust（seeded・副次のドリフト・凍結防止） */}
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          {dust.map((d, i) => {
            const t = (frame / fps) * d.sp;
            const x = (d.bx + 0.03 * Math.sin(t + d.ph)) * W;
            const y = (0.28 + d.by * 0.6 + 0.012 * Math.cos(t * 1.3 + d.ph)) * H;
            const o = 0.1 + 0.12 * ((Math.sin(t + d.ph) + 1) / 2);
            return <circle key={i} cx={x} cy={y} r={d.r} fill={GOLD} opacity={o} />;
          })}
        </svg>

        {/* L5: 滑走する束/書類（主キネティック）＋モーションブラー */}
        <Trail layers={6} lagInFrames={1.2} trailOpacity={0.42}>
          <Procession D={D} seed={34} />
        </Trail>

        {/* L6: 受け取る手（原告・手前・シルエット） */}
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          <g
            transform={`translate(${0.55 * W}, ${0.99 * H})`}
            style={{filter: 'drop-shadow(0 -6px 14px rgba(0,0,0,0.5))'}}
          >
            <g transform="translate(-40,0) scale(1.15)">
              <Palm />
            </g>
            <g transform="translate(120,10) scale(1.15)">
              <Palm flip />
            </g>
          </g>
        </svg>

        {/* キャプション（マスク切れ上がり・gold） */}
        <div style={{position: 'absolute', left: 0.045 * W, top: 0.11 * H}}>
          <MaskLabel
            text="RETURNED IN FULL"
            fps={fps}
            start={0.2}
            size={30}
            color={SILVER}
            weight={700}
            letter={5}
            family={BRAND.font.body}
          />
        </div>
        <div style={{position: 'absolute', left: 0.045 * W, top: 0.155 * H}}>
          <MaskLabel
            text={caption}
            fps={fps}
            start={0.5}
            size={64}
            color={GOLD}
            weight={800}
            letter={3}
            family={BRAND.font.display}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
