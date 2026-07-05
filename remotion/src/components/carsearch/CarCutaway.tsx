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
// CarCutaway — 暗背景中央のクリーンなベクター車断面図（横向き）。
//   検索対象ゾーンが staggered spring で一つずつ点灯（各 ~0.25s ずれ）。
//   各ゾーン: マスク切れ上がりラベル + ソフトなクリック・グロー。
//   mode='all'   : 与えられた全ゾーン点灯
//   mode='big'   : 大きい物 → TRUNK / BACK SEAT のみ点灯
//   mode='small' : 小さい物 → 全ゾーン + 小さな CONSOLE / ASHTRAY まで
//   単一アクセント(gold/electric)・抑えたダーク車体。図全体は緩くパララックス。
//   全モーション spring / Easing.out(cubic)。opacity 単独禁止。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const {navy, electric, silver, gold, white} = BRAND.color;

type CutMode = 'all' | 'big' | 'small';

// 車ローカル座標系（viewBox 0..1200 x 0..520）でのゾーン・ホットスポット
type Hotspot = {x: number; y: number; r: number; up: boolean};

const HOTSPOTS: Record<string, Hotspot> = {
  GLOVEBOX: {x: 300, y: 300, r: 30, up: false},
  TRUNK: {x: 1010, y: 250, r: 46, up: true},
  'BACK SEAT': {x: 720, y: 250, r: 46, up: true},
  'A ZIPPED BAG': {x: 560, y: 300, r: 34, up: false},
  BAG: {x: 560, y: 300, r: 34, up: false},
  CONSOLE: {x: 470, y: 288, r: 20, up: false},
  ASHTRAY: {x: 420, y: 296, r: 16, up: false},
  DASH: {x: 340, y: 250, r: 26, up: true},
};

// 未知ゾーン用のフォールバック配置（車内に沿って等間隔）
const fallbackSpot = (i: number): Hotspot => ({
  x: 360 + i * 150,
  y: 300,
  r: 28,
  up: i % 2 === 0,
});

const resolveZones = (zones: string[], mode: CutMode): string[] => {
  const up = zones.map((z) => z.toUpperCase());
  if (mode === 'big') {
    const big = up.filter((z) => z === 'TRUNK' || z === 'BACK SEAT');
    return big.length > 0 ? big : ['TRUNK', 'BACK SEAT'];
  }
  if (mode === 'small') {
    const out = [...up];
    for (const extra of ['CONSOLE', 'ASHTRAY']) {
      if (!out.includes(extra)) out.push(extra);
    }
    return out;
  }
  return up;
};

// マスク切れ上がりラベル（overflow:hidden + translateY 立ち上げ）
const MaskLabel: React.FC<{
  text: string;
  progress: number; // 0→1 (spring)
  color: string;
  size: number;
}> = ({text, progress, color, size}) => {
  const y = interpolate(progress, [0, 1], [110, 0]);
  const o = interpolate(progress, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp',
  });
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          whiteSpace: 'pre',
          fontFamily: BRAND.font.body,
          fontWeight: 700,
          letterSpacing: 2,
          fontSize: size,
          color,
        }}
      >
        {text}
      </span>
    </span>
  );
};

export const CarCutaway: React.FC<{
  zones?: string[];
  mode?: CutMode;
  dur?: number;
}> = ({
  zones = ['GLOVEBOX', 'TRUNK', 'BACK SEAT', 'A ZIPPED BAG'],
  mode = 'all',
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const active = resolveZones(zones, mode);
  const accent = mode === 'big' ? gold : electric;

  // シーンイン/アウト（微 translateY 併用）
  const sceneIn = spring({frame, fps, config: {damping: 200, mass: 0.6}});
  const sceneOut = interpolate(frame, [total - sec(fps, 0.5), total], [1, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
  });
  const sceneOpacity = interpolate(sceneIn, [0, 1], [0, 1]) * sceneOut;

  // 図全体の緩いパララックス・ドリフト（イージング付き・静止禁止）
  const driftX = interpolate(frame, [0, total], [-14, 14], {
    easing: Easing.inOut(Easing.sin),
  });
  const driftY = 6 * Math.sin(frame / (fps * 1.3));
  const introY = interpolate(sceneIn, [0, 1], [40, 0]);

  // SVG 配置: viewBox 1200x520 を画面中央に大きく
  const vbW = 1200;
  const vbH = 520;
  const scale = 1.28;
  const svgW = vbW * scale;
  const svgH = vbH * scale;

  const carBody = '#111a2b'; // 抑えたダーク車体
  const carStroke = silver;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(125% 105% at 50% 42%, ${navy} 0%, #06080f 82%)`,
        opacity: sceneOpacity,
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* 背景グリッド（深度レイヤー） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translate(${driftX * 0.4}px, ${driftY * 0.4}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${silver}22 0px, ${silver}22 1px, transparent 1px, transparent 80px),
            repeating-linear-gradient(90deg, ${silver}22 0px, ${silver}22 1px, transparent 1px, transparent 80px)`,
          maskImage: 'radial-gradient(110% 90% at 50% 50%, black 25%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(110% 90% at 50% 50%, black 25%, transparent 80%)',
        }}
      />

      {/* 車図全体（パララックス） */}
      <div
        style={{
          position: 'relative',
          width: svgW,
          height: svgH,
          transform: `translate(${driftX}px, ${driftY + introY}px)`,
        }}
      >
        <svg
          width={svgW}
          height={svgH}
          viewBox={`0 0 ${vbW} ${vbH}`}
          style={{position: 'absolute', inset: 0, overflow: 'visible'}}
        >
          {/* 車体ベース（横向き・単純シェイプ: body, cabin, trunk） */}
          <g>
            {/* 影のグラウンドライン */}
            <ellipse
              cx={600}
              cy={470}
              rx={520}
              ry={22}
              fill="#000"
              opacity={0.35}
            />
            {/* ボディ下部 */}
            <path
              d="M90 360
                 C90 330 120 320 150 320
                 L1050 320
                 C1090 320 1110 335 1110 360
                 L1110 400 L90 400 Z"
              fill={carBody}
              stroke={carStroke}
              strokeOpacity={0.35}
              strokeWidth={2}
            />
            {/* キャビン + トランク上部（ルーフライン） */}
            <path
              d="M250 320
                 C270 220 360 190 480 188
                 L820 188
                 C930 190 1000 230 1040 320 Z"
              fill={carBody}
              stroke={carStroke}
              strokeOpacity={0.35}
              strokeWidth={2}
            />
            {/* 窓（キャビンの抜け） */}
            <path
              d="M330 300 C345 232 410 214 480 214 L640 214 L640 300 Z"
              fill={navy}
              opacity={0.6}
            />
            <path
              d="M670 214 L800 214 C890 216 950 246 985 300 L670 300 Z"
              fill={navy}
              opacity={0.6}
            />
            {/* トランク仕切り */}
            <line
              x1={950}
              y1={214}
              x2={950}
              y2={320}
              stroke={carStroke}
              strokeOpacity={0.25}
              strokeWidth={2}
            />
            {/* 車輪 */}
            <circle cx={300} cy={400} r={78} fill="#0a0f1a" stroke={carStroke} strokeOpacity={0.4} strokeWidth={3} />
            <circle cx={900} cy={400} r={78} fill="#0a0f1a" stroke={carStroke} strokeOpacity={0.4} strokeWidth={3} />
            <circle cx={300} cy={400} r={34} fill={navy} stroke={carStroke} strokeOpacity={0.3} strokeWidth={2} />
            <circle cx={900} cy={400} r={34} fill={navy} stroke={carStroke} strokeOpacity={0.3} strokeWidth={2} />
          </g>

          {/* ゾーン・ホットスポット（点灯グロー） */}
          {active.map((z, i) => {
            const hs = HOTSPOTS[z] ?? fallbackSpot(i);
            const cs = spring({
              frame: frame - sec(fps, 0.5) - i * sec(fps, 0.25),
              fps,
              config: {damping: 13, mass: 0.7},
            });
            const pop = interpolate(cs, [0, 1], [0, 1]);
            const r = interpolate(cs, [0, 1], [0, hs.r]);
            const glowO = interpolate(cs, [0, 0.5, 1], [0, 0.9, 0.6]);
            return (
              <g key={`${z}-${i}`}>
                {/* ソフトなクリック・グロー */}
                <circle
                  cx={hs.x}
                  cy={hs.y}
                  r={r + 26}
                  fill={accent}
                  opacity={glowO * 0.22}
                />
                {/* リング */}
                <circle
                  cx={hs.x}
                  cy={hs.y}
                  r={r}
                  fill="none"
                  stroke={accent}
                  strokeWidth={3}
                  opacity={pop}
                />
                {/* コア点 */}
                <circle
                  cx={hs.x}
                  cy={hs.y}
                  r={interpolate(cs, [0, 1], [0, 6])}
                  fill={white}
                  opacity={pop}
                />
                {/* 引き出し線 */}
                <line
                  x1={hs.x}
                  y1={hs.up ? hs.y - r : hs.y + r}
                  x2={hs.x}
                  y2={hs.up ? hs.y - r - 40 * pop : hs.y + r + 40 * pop}
                  stroke={accent}
                  strokeWidth={2}
                  opacity={pop * 0.8}
                />
              </g>
            );
          })}
        </svg>

        {/* ラベル層（HTML でマスク切れ上がり）。SVG 座標→ピクセル換算 */}
        {active.map((z, i) => {
          const hs = HOTSPOTS[z] ?? fallbackSpot(i);
          const cs = spring({
            frame: frame - sec(fps, 0.5) - i * sec(fps, 0.25),
            fps,
            config: {damping: 13, mass: 0.7},
          });
          const px = hs.x * scale;
          const labelY = (hs.up ? hs.y - hs.r - 78 : hs.y + hs.r + 48) * scale;
          return (
            <div
              key={`lbl-${z}-${i}`}
              style={{
                position: 'absolute',
                left: px,
                top: labelY,
                transform: 'translateX(-50%)',
                textAlign: 'center',
              }}
            >
              <MaskLabel text={z} progress={cs} color={accent} size={26} />
            </div>
          );
        })}
      </div>

      {/* タイトル（マスク切れ上がり + Trail 残像で速い立ち上がり） */}
      <div style={{position: 'absolute', top: height * 0.12}}>
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          <TitleReveal
            text={
              mode === 'big'
                ? 'WHERE A LARGE ITEM COULD BE'
                : mode === 'small'
                ? 'EVERY PLACE A SMALL ITEM FITS'
                : 'SEARCHABLE ZONES'
            }
            fps={fps}
            accent={accent}
          />
        </Trail>
      </div>

      {/* ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, transparent 48%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};

// 見出しのマスク切れ上がり（1 文字スタッガー）
const TitleReveal: React.FC<{text: string; fps: number; accent: string}> = ({
  text,
  fps,
  accent,
}) => {
  const frame = useCurrentFrame();
  const chars = Array.from(text);
  const st = Math.max(1, sec(fps, 0.02));
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        fontFamily: BRAND.font.display,
        fontSize: 46,
        letterSpacing: 3,
        color: white,
      }}
    >
      {chars.map((ch, i) => {
        const cs = spring({
          frame: frame - sec(fps, 0.15) - i * st,
          fps,
          config: {damping: 16, mass: 1},
        });
        const y = interpolate(cs, [0, 1], [110, 0]);
        const o = interpolate(cs, [0, 0.25], [0, 1], {
          extrapolateRight: 'clamp',
        });
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              paddingBottom: '0.12em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${y}%)`,
                opacity: o,
                whiteSpace: 'pre',
                color: ch === ' ' ? white : i % 7 === 0 ? accent : white,
              }}
            >
              {ch}
            </span>
          </span>
        );
      })}
    </div>
  );
};
