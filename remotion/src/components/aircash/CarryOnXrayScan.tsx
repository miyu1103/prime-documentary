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
// CarryOnXrayScan — 空港TSAのX線モニタ。機内持ち込みバッグがスキャンベルト上を
//   左→右へ「実移動」し、その中の“密な現金塊(帯封束)”がX線像として現れる。
//   バッグが検査トンネル中央に来た瞬間、検知レティクル(コーナー括弧)が大きく開いた
//   状態から現金塊へ収束し「DENSE MASS DETECTED」が切れ上がる。
//   ・主運動＝バッグ＋現金塊の横断移動（§7: 物体の実移動が主。走光/X線グロウは補助）
//   ・X線ルック＝electricのスキャンライン走査＋グロウ（auxiliary）
//   ・ベルトのトレッドが連続スクロール／ローラー回転／微塵が舞う（凍らない）
//   ・暗紺背景＋奥行き≥3層・単一アクセント(electric)・微シマー・決定論。
// 全モーションeased(spring/Easing)・opacity単独なし・fps算出・deterministic。
// mulberry32(seeded)で微塵のみ変化（Math.random禁止）。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(128% 108% at 50% 46%, ${BRAND.color.navy} 0%, ${BG} 84%)`;

const sec = (fps: number, s: number) => Math.round(fps * s);

// 決定論的な擬似乱数（微塵の初期配置にのみ使用）
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const TAU = Math.PI * 2;

type CarryOnXrayScanProps = {
  dur?: number;
  // 検知ラベル（事実の精密数値は焼き込まない：金額は#1側で扱う）
  caption?: string;
  header?: string;
};

export const CarryOnXrayScan: React.FC<CarryOnXrayScanProps> = ({
  dur,
  caption = 'DENSE MASS DETECTED',
  header = 'TSA CHECKPOINT · CARRY-ON X-RAY',
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;
  const t = frame / fps; // 秒（連続・尺非依存＝長ホールドでも止まらない補助モーション用）

  const ACCENT = BRAND.color.electric;
  const METAL = BRAND.color.silver;

  const beltY = Math.round(height * 0.62); // ベルト上面のワールドY
  const cx = width / 2;

  // 検査トンネル（X線窓）ワールド矩形
  const sx0 = cx - 470;
  const sx1 = cx + 470;
  const syTop = beltY - 340;
  const syBot = beltY + 26;

  // ---- 主運動：バッグ＋現金塊がベルト上を左→右へ横断（beat全編）----
  // startX/endX は画面外。inOut cubic で加減速するが中央では最速＝60%以上を
  // 画面高2.5%/秒(≈27px/s)を大きく超える速度で移動（総移動≈2520px/尺）。
  const startX = -320;
  const endX = width + 320;
  const travel = interpolate(frame, [0, Math.max(1, D)], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const bagX = interpolate(travel, [0, 1], [startX, endX]);

  // バッグが中央(トンネル中心)に最接近する瞬間 ≒ travel=0.5（D*0.5付近）
  const detectStart = Math.round(D * 0.44);

  // 検知レティクルの収束（大きく開いた枠→現金塊へキュッと締まる：小オーバーシュート）
  const detectS = spring({
    frame: frame - detectStart,
    fps,
    config: {damping: 12, mass: 0.8, stiffness: 150},
  });
  // 現金塊のX線グロウが検知でパルス（scaleと必ず併走＝opacity単独禁止）
  const glowPulse = interpolate(
    spring({frame: frame - detectStart, fps, config: {damping: 8, mass: 0.7}}),
    [0, 0.5, 1],
    [0, 1, 0.55],
    {extrapolateRight: 'clamp'},
  );
  // 検知フラッシュ（一瞬）
  const flash = interpolate(detectS, [0.4, 0.6, 0.85], [0, 0.9, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 凍らない微シマー（補助）
  const shimmer = interpolate(Math.sin(t * TAU * 0.55), [-1, 1], [0.82, 1]);
  const xrayBreath = interpolate(Math.sin(t * TAU * 0.33 + 1), [-1, 1], [0.86, 1]);

  // スキャンライン（トンネル内を縦に往復走査＝X線ルック・auxiliary）
  const scanY = interpolate(
    (t / 1.7) % 1,
    [0, 0.5, 1],
    [syTop + 20, syBot - 20, syTop + 20],
    {easing: Easing.inOut(Easing.sin)},
  );

  // ベルトのトレッド連続スクロール（バッグと同方向・左→右）
  const treadGap = 46;
  const treadShift = (t * 150) % treadGap;
  const beltX0 = 150;
  const beltX1 = width - 150;
  const treadCount = Math.ceil((beltX1 - beltX0) / treadGap) + 2;

  // ローラー回転（両端・連続）
  const rollerDeg = (t * 220) % 360;

  // 舞う微塵（seeded・上昇＋横スウェイ・additive）
  const motes = React.useMemo(() => {
    const rnd = mulberry32(0x51ca7);
    return Array.from({length: 24}).map(() => ({
      x: sx0 + rnd() * (sx1 - sx0),
      y: rnd(),
      spd: 22 + rnd() * 26,
      amp: 8 + rnd() * 16,
      ph: rnd() * TAU,
      r: 1.4 + rnd() * 1.8,
    }));
  }, [sx0, sx1]);

  // シーン出入り（移動と併走＝opacity単独でない）
  const inO = interpolate(frame, [0, 12], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 14, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 14], [26, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // ヘッダの切れ上がり（マスク）
  const headS = spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 18}});
  const headY = interpolate(headS, [0, 1], [120, 0]);
  // キャプションの切れ上がり（検知で出現）
  const capS = spring({
    frame: frame - (detectStart + sec(fps, 0.15)),
    fps,
    config: {damping: 16, mass: 0.9},
  });
  const capY = interpolate(capS, [0, 1], [120, 0]);

  // ---- バッグ内ローカル座標系（div内SVG viewBox 460x360）----
  // 現金塊(帯封束)のローカル中心と、検知レティクルの収束サイズ
  const cashCX = 230;
  const cashCY = 196;
  const hw = interpolate(detectS, [0, 1], [212, 108]); // 半幅：大きく開く→締まる
  const hh = interpolate(detectS, [0, 1], [156, 74]); // 半高
  const bracket = 26; // コーナー括弧の腕長
  const reticleO = interpolate(detectS, [0, 0.25], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 現金束（4段の帯封ブロック）をローカルに配置
  const bricks = [
    {x: 152, y: 150, w: 156, h: 22},
    {x: 152, y: 176, w: 156, h: 22},
    {x: 152, y: 202, w: 156, h: 22},
    {x: 158, y: 228, w: 144, h: 20},
  ];

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド（X線モニタの格子・faint） */}
      <AbsoluteFill
        style={{
          opacity: 0.1 * xrayBreath,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 74px),
            repeating-linear-gradient(90deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 74px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 50%, black 34%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 50%, black 34%, transparent 84%)',
        }}
      />
      {/* L3 X線トンネルのグロウ（teal系→brand electric・auxiliary・検知で強まる） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 42% at 50% ${
            ((beltY - 150) / height) * 100
          }%, ${ACCENT}${flash > 0.4 ? '3a' : '1c'} 0%, transparent 66%)`,
        }}
      />

      <AbsoluteFill
        style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}
      >
        {/* ---- ベース SVG：検査機・ベルト・スキャンライン・微塵 ---- */}
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="cox-belt" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#101c2e" />
              <stop offset="100%" stopColor="#0a1320" />
            </linearGradient>
            <linearGradient id="cox-machine" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#13223a" />
              <stop offset="100%" stopColor="#0b1526" />
            </linearGradient>
            <clipPath id="cox-tunnel">
              <rect x={sx0} y={syTop} width={sx1 - sx0} height={syBot - syTop} rx={20} />
            </clipPath>
            <clipPath id="cox-beltclip">
              <rect x={beltX0} y={beltY} width={beltX1 - beltX0} height={30} />
            </clipPath>
          </defs>

          {/* 検査機の筐体（トンネル） */}
          <rect
            x={sx0 - 40}
            y={syTop - 40}
            width={sx1 - sx0 + 80}
            height={syBot - syTop + 80}
            rx={30}
            fill="url(#cox-machine)"
            stroke={METAL}
            strokeWidth={3}
            opacity={0.96}
          />
          {/* トンネル開口（X線窓） */}
          <rect
            x={sx0}
            y={syTop}
            width={sx1 - sx0}
            height={syBot - syTop}
            rx={20}
            fill="#060d18"
            stroke={`${ACCENT}88`}
            strokeWidth={2}
          />

          {/* トンネル内：スキャンライン走査＋舞う微塵（clip） */}
          <g clipPath="url(#cox-tunnel)">
            {/* スキャンライン（electric・白コア・auxiliary） */}
            <rect
              x={sx0}
              y={scanY - 2}
              width={sx1 - sx0}
              height={4}
              fill={BRAND.color.white}
              opacity={0.85 * xrayBreath}
            />
            <rect
              x={sx0}
              y={scanY - 26}
              width={sx1 - sx0}
              height={52}
              fill={ACCENT}
              opacity={0.16 * xrayBreath}
            />
            {/* 微塵（seeded・上昇＋横スウェイ・additive） */}
            {motes.map((m, i) => {
              const span = syBot - syTop;
              const yy =
                syTop + ((m.y * span - t * m.spd) % span + span) % span;
              const xx = m.x + m.amp * Math.sin(t * TAU * 0.2 + m.ph);
              return (
                <circle
                  key={i}
                  cx={xx}
                  cy={yy}
                  r={m.r}
                  fill={BRAND.color.white}
                  opacity={0.22 * shimmer}
                />
              );
            })}
          </g>

          {/* ベルト本体 */}
          <rect
            x={beltX0}
            y={beltY}
            width={beltX1 - beltX0}
            height={30}
            fill="url(#cox-belt)"
            stroke={`${METAL}44`}
            strokeWidth={2}
          />
          {/* ベルトのトレッド（左→右へ連続スクロール） */}
          <g clipPath="url(#cox-beltclip)">
            {Array.from({length: treadCount}).map((_, i) => {
              const x = beltX0 - treadGap + i * treadGap + treadShift;
              return (
                <line
                  key={i}
                  x1={x}
                  y1={beltY + 2}
                  x2={x + 14}
                  y2={beltY + 28}
                  stroke={`${METAL}33`}
                  strokeWidth={3}
                />
              );
            })}
          </g>
          {/* 両端ローラー（回転・連続） */}
          {[beltX0, beltX1].map((rx, i) => (
            <g key={i} transform={`translate(${rx},${beltY + 15})`}>
              <circle r={20} fill="#0b1524" stroke={METAL} strokeWidth={3} />
              <g transform={`rotate(${rollerDeg})`}>
                <line x1={-14} y1={0} x2={14} y2={0} stroke={`${METAL}aa`} strokeWidth={3} />
                <line x1={0} y1={-14} x2={0} y2={14} stroke={`${METAL}aa`} strokeWidth={3} />
              </g>
            </g>
          ))}

          {/* ステータスLED（検知で赤→electric点灯・auxiliary） */}
          <circle
            cx={sx1 + 8}
            cy={syTop - 8}
            r={9}
            fill={ACCENT}
            opacity={0.25 + flash * 0.7 + 0.12 * Math.sin(t * TAU * 1.4)}
          />
        </svg>

        {/* ---- 主役：バッグ＋現金塊がベルト上を横断（Trailでモーションブラー） ----
             Trailは AbsoluteFill をラップ（inline flex row禁止）。中の絶対配置div内SVGが
             左→右へ translateX で実移動する。検知レティクルもバッグ内ローカルに描くので
             移動する塊へロックし続ける（＝レティクルも動く物体）。 */}
        <Trail layers={7} lagInFrames={1.15} trailOpacity={0.42}>
          <AbsoluteFill>
            <div
              style={{
                position: 'absolute',
                left: bagX - 230,
                top: beltY - 300, // ローカルy=300 がベルト上面に一致
                width: 460,
                height: 360,
              }}
            >
              <svg width={460} height={360} viewBox="0 0 460 360">
                {/* バッグ影（ベルト接地） */}
                <ellipse cx={230} cy={300} rx={150} ry={12} fill="#000" opacity={0.32} />

                {/* ハンドル（テレスコピック） */}
                <g stroke={`${ACCENT}cc`} strokeWidth={9} strokeLinecap="round" opacity={shimmer}>
                  <line x1={182} y1={92} x2={182} y2={48} />
                  <line x1={278} y1={92} x2={278} y2={48} />
                </g>
                <rect x={176} y={40} width={108} height={14} rx={7} fill={`${ACCENT}cc`} />

                {/* バッグ本体（X線半透明シルエット） */}
                <rect
                  x={100}
                  y={90}
                  width={260}
                  height={172}
                  rx={26}
                  fill={`${ACCENT}22`}
                  stroke={`${ACCENT}bb`}
                  strokeWidth={3}
                />
                {/* バッグの補強リブ（X線らしい内部線） */}
                <line x1={100} y1={150} x2={360} y2={150} stroke={`${ACCENT}44`} strokeWidth={2} />
                <line x1={230} y1={90} x2={230} y2={262} stroke={`${ACCENT}2e`} strokeWidth={2} />

                {/* 車輪 */}
                <circle cx={140} cy={278} r={18} fill="#06101d" stroke={`${ACCENT}aa`} strokeWidth={3} />
                <circle cx={320} cy={278} r={18} fill="#06101d" stroke={`${ACCENT}aa`} strokeWidth={3} />

                {/* ★密な現金塊（帯封束）＝X線で最も明るい高密度ブロック */}
                <g
                  style={{
                    filter: `drop-shadow(0 0 ${8 + glowPulse * 26}px ${ACCENT})`,
                  }}
                >
                  {bricks.map((b, i) => (
                    <g key={i}>
                      <rect
                        x={b.x}
                        y={b.y}
                        width={b.w}
                        height={b.h}
                        rx={3}
                        fill={BRAND.color.white}
                        opacity={0.86 + glowPulse * 0.14}
                      />
                      {/* 帯封（バンド） */}
                      <rect
                        x={b.x + b.w * 0.42}
                        y={b.y}
                        width={b.w * 0.16}
                        height={b.h}
                        fill={ACCENT}
                        opacity={0.9}
                      />
                    </g>
                  ))}
                </g>

                {/* 検知レティクル（コーナー括弧・大きく開く→収束）— 現金塊にロック */}
                <g opacity={reticleO} stroke={ACCENT} strokeWidth={4} fill="none" strokeLinecap="round">
                  {/* 左上 */}
                  <path d={`M${cashCX - hw},${cashCY - hh + bracket} L${cashCX - hw},${cashCY - hh} L${cashCX - hw + bracket},${cashCY - hh}`} />
                  {/* 右上 */}
                  <path d={`M${cashCX + hw - bracket},${cashCY - hh} L${cashCX + hw},${cashCY - hh} L${cashCX + hw},${cashCY - hh + bracket}`} />
                  {/* 右下 */}
                  <path d={`M${cashCX + hw},${cashCY + hh - bracket} L${cashCX + hw},${cashCY + hh} L${cashCX + hw - bracket},${cashCY + hh}`} />
                  {/* 左下 */}
                  <path d={`M${cashCX - hw + bracket},${cashCY + hh} L${cashCX - hw},${cashCY + hh} L${cashCX - hw},${cashCY + hh - bracket}`} />
                </g>
              </svg>
            </div>
          </AbsoluteFill>
        </Trail>

        {/* 検知フラッシュ・リング（一瞬・トンネル中心） */}
        {flash > 0.02 ? (
          <div
            style={{
              position: 'absolute',
              left: cx - 90,
              top: beltY - 150 - 90,
              width: 180,
              height: 180,
              borderRadius: '50%',
              border: `3px solid ${ACCENT}`,
              transform: `scale(${interpolate(flash, [0, 0.9], [0.7, 1.5])})`,
              opacity: flash,
              boxShadow: `0 0 44px ${ACCENT}`,
              pointerEvents: 'none',
            }}
          />
        ) : null}

        {/* ヘッダ（マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            left: 96,
            top: 88,
            width: 900,
            overflow: 'hidden',
            paddingBottom: '0.2em',
          }}
        >
          <div
            style={{
              transform: `translateY(${headY}%)`,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 30,
              letterSpacing: 5,
              color: METAL,
            }}
          >
            {header}
          </div>
        </div>

        {/* 検知キャプション（マスク切れ上がり＋electricアクセント） */}
        <div
          style={{
            position: 'absolute',
            left: 96,
            bottom: 92,
            width: 1200,
            overflow: 'hidden',
            paddingBottom: '0.16em',
          }}
        >
          <div
            style={{
              transform: `translateY(${capY}%)`,
              fontFamily: BRAND.font.display,
              fontWeight: 800,
              fontSize: 62,
              letterSpacing: 3,
              lineHeight: 1.05,
              color: BRAND.color.white,
              textShadow: `0 0 26px ${ACCENT}`,
            }}
          >
            <span style={{color: ACCENT}}>X-RAY · </span>
            {caption}
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
