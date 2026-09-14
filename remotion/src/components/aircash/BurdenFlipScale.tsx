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
// BurdenFlipScale — 立証責任の反転（CAFRA）を物理天秤で可視化。
//   天秤の梁が「市民側(左)が沈む＝市民が立証責任を負う」状態から、
//   spring減衰振動で大きく振れ、"government側(右)が沈む" へFLIPする。
//   政府の皿へ象徴質量（帯封束プロキシ）が連続落下し、皿を追って着地し続ける
//   ＝主運動は物体の実移動（走光は補助）。反転後 ">50% — more likely than not"
//   のillustrativeチップがマスク切れ上がりで着地（「51%」の厳密数値は焼込まない）。
// 品質: 全モーションspring/easing・opacity単独なし・マスク切れ上がり・
//   高速落下Trail(AbsoluteFillラップ)・単一アクセント(electric)・≥3レイヤー・
//   決定論(useCurrentFrameのみ／乱数はseeded mulberry32)。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 108% at 50% 40%, ${BRAND.color.navy} 0%, ${BG} 82%)`;

const sec = (fps: number, s: number) => Math.round(fps * s);

// 決定論的な擬似乱数（Math.random禁止）
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

// 天秤の幾何（コンポーネント内定数・数値はここへ集約）
const L = 320; // 梁の半長
const CORD = 150; // 皿を吊る紐の長さ
const PAN_R = 78; // 皿の半径

export type BurdenFlipScaleProps = {
  dur?: number;
  chipMain?: string; // 例: ">50%"（「51%」等の厳密値は禁止）
  chipSub?: string; // 例: "more likely than not"
};

export const BurdenFlipScale: React.FC<BurdenFlipScaleProps> = ({
  dur,
  chipMain = '>50%',
  chipSub = 'more likely than not',
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  const ACCENT = BRAND.color.electric;
  const METAL = BRAND.color.silver;
  const WHITE = BRAND.color.white;
  const NAVY = BRAND.color.navy;

  const cx = width / 2;
  const pivotX = cx;
  const pivotY = Math.round(height * 0.35); // 支点（梁の回転中心）
  const baseY = Math.round(height * 0.86); // 台座

  // --- タイムライン（全て fps 算出） ---
  const flipStart = sec(fps, 2.4);
  const chipStart = sec(fps, 3.5);
  const capStart = sec(fps, 4.5);
  const massStart = sec(fps, 2.0);

  const thStart = -13; // 市民(左)が沈む
  const thEnd = 11; // 政府(右)が沈む

  // 梁の角度（frameの純関数）: 反転springの過減衰オーバーシュート＋settle後の持続微揺れ
  const thetaAt = (f: number) => {
    const s = spring({
      frame: f - flipStart,
      fps,
      config: {damping: 5.5, mass: 1.2, stiffness: 80},
    });
    const base = interpolate(s, [0, 1], [thStart, thEnd]); // >1でオーバーシュート＝実振り
    const settle = interpolate(
      f,
      [flipStart + sec(fps, 2.2), flipStart + sec(fps, 3.0)],
      [0, 1],
      {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
    );
    const sway = 1.3 * settle * Math.sin((f / fps) * ((2 * Math.PI) / 2.6));
    return base + sway;
  };

  const theta = thetaAt(frame);
  const vel = theta - thetaAt(frame - 1); // 角速度→皿の振り遅れ
  const panLag = Math.max(-14, Math.min(14, -vel * 2.4));

  const rad = (theta * Math.PI) / 180;
  const cosr = Math.cos(rad);
  const sinr = Math.sin(rad);
  const leftEnd = {x: pivotX - L * cosr, y: pivotY - L * sinr};
  const rightEnd = {x: pivotX + L * cosr, y: pivotY + L * sinr};
  const rightPanY = rightEnd.y + CORD;

  // 反転の進捗（皿の色・チップの重み演出）
  const flipProg = interpolate(
    spring({frame: frame - flipStart, fps, config: {damping: 5.5, mass: 1.2, stiffness: 80}}),
    [0, 0.6],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // 政府の皿へ落下する象徴質量（帯封束プロキシ）＝主運動（物体の実移動）
  const masses = React.useMemo(() => {
    const rnd = mulberry32(0x5ca1e8);
    return Array.from({length: 7}).map(() => ({
      xOff: (rnd() * 2 - 1) * PAN_R * 0.6,
      period: 0.95 + rnd() * 0.7,
      phase: rnd() * 1.4,
      size: 42 + rnd() * 16,
      rot0: (rnd() * 2 - 1) * 30,
      spin: (rnd() * 2 - 1) * 42,
    }));
  }, []);

  const spawnY = -60; // 画面上端外から落ちてくる（ポップ無し）
  const panSurfaceY = rightPanY - PAN_R * 0.2;

  // 入退場（scale＋translateYと必ず併用＝opacity単独禁止）
  const riseS = spring({frame, fps, config: {damping: 18, mass: 1}});
  const scaleIn = interpolate(riseS, [0, 1], [0.86, 1]);
  const yIn = interpolate(riseS, [0, 1], [70, 0]);
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const outY = interpolate(frame, [D - 12, D], [0, 26], {extrapolateLeft: 'clamp'});

  // 凍らない微シマー（背景グロー・補助のみ）
  const shimmer = interpolate(Math.sin(frame / 11), [-1, 1], [0.82, 1]);

  // チップ（マスク切れ上がり＋scale）
  const chipS = spring({frame: frame - chipStart, fps, config: {damping: 14, mass: 0.9}});
  const chipY = interpolate(chipS, [0, 1], [115, 0]);
  const chipScale = interpolate(chipS, [0, 1], [0.82, 1]);
  const chipO = interpolate(chipS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // キャプション（マスク切れ上がり）
  const capS = spring({frame: frame - capStart, fps, config: {damping: 16, mass: 0.9}});
  const capY = interpolate(capS, [0, 1], [120, 0]);
  const capO = interpolate(capS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // 皿の描画（紐＋浅い受け皿）。政府側は反転後にaccentが乗る。
  const Pan: React.FC<{end: {x: number; y: number}; accentT: number; label: string; labelColor: string}> = ({
    end,
    accentT,
    label,
    labelColor,
  }) => {
    const panY = end.y + CORD;
    const bowlFill = accentT > 0.02 ? `${ACCENT}22` : '#0b1524';
    const rim = accentT > 0.02 ? ACCENT : METAL;
    return (
      <g>
        {/* 台座グロー（accentが乗る側） */}
        {accentT > 0.02 ? (
          <ellipse
            cx={end.x}
            cy={panY + 6}
            rx={PAN_R + 18}
            ry={22}
            fill={ACCENT}
            opacity={0.18 * accentT}
          />
        ) : null}
        <g transform={`translate(${end.x},${end.y}) rotate(${panLag})`}>
          {/* 吊り紐（左右） */}
          <line x1={-PAN_R * 0.62} y1={0} x2={0} y2={CORD} stroke={METAL} strokeWidth={2} opacity={0.7} />
          <line x1={PAN_R * 0.62} y1={0} x2={0} y2={CORD} stroke={METAL} strokeWidth={2} opacity={0.7} />
          <line x1={0} y1={0} x2={0} y2={CORD} stroke={METAL} strokeWidth={3} />
          <circle cx={0} cy={0} r={6} fill={METAL} />
          {/* 受け皿（浅いボウル） */}
          <g transform={`translate(0,${CORD})`}>
            <path
              d={`M${-PAN_R},0 A ${PAN_R} ${PAN_R} 0 0 0 ${PAN_R},0 Z`}
              fill={bowlFill}
              stroke={rim}
              strokeWidth={4}
              strokeLinejoin="round"
            />
            <line x1={-PAN_R} y1={0} x2={PAN_R} y2={0} stroke={rim} strokeWidth={4} />
          </g>
        </g>
        {/* ラベル（皿を追って移動） */}
        <text
          x={end.x}
          y={panY + 118}
          textAnchor="middle"
          fill={labelColor}
          style={{fontFamily: BRAND.font.body, fontWeight: 700, fontSize: 26, letterSpacing: 3}}
        >
          {label}
        </text>
      </g>
    );
  };

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド */}
      <AbsoluteFill
        style={{
          opacity: 0.08,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 76px)`,
          maskImage: 'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
        }}
      />
      {/* L3 政府側(右)の裏グロー（反転で強まる・微シマー） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(24% 30% at ${((rightEnd.x) / width) * 100}% ${
            (rightPanY / height) * 100
          }%, ${ACCENT}${flipProg > 0.5 ? '4a' : '18'} 0%, transparent 66%)`,
          opacity: shimmer,
        }}
      />
      {/* L3b ヴィネット */}
      <AbsoluteFill
        style={{
          background: 'radial-gradient(120% 100% at 50% 50%, transparent 44%, rgba(0,0,0,0.66) 100%)',
        }}
      />

      <AbsoluteFill
        style={{
          opacity: inO * outO,
          transform: `translateY(${yIn + outY}px) scale(${scaleIn})`,
          transformOrigin: '50% 46%',
        }}
      >
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="bfs-metal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={WHITE} />
              <stop offset="52%" stopColor={METAL} />
              <stop offset="100%" stopColor="#7f8794" />
            </linearGradient>
          </defs>

          {/* ---- 台座＋支柱（奥の構造） ---- */}
          <g>
            <ellipse cx={pivotX} cy={baseY + 12} rx={180} ry={26} fill="#0a1524" stroke={`${METAL}44`} strokeWidth={2} />
            <polygon
              points={`${pivotX - 26},${pivotY} ${pivotX + 26},${pivotY} ${pivotX + 74},${baseY} ${pivotX - 74},${baseY}`}
              fill="#0c1626"
              stroke={METAL}
              strokeWidth={3}
              strokeLinejoin="round"
            />
            <rect x={pivotX - 96} y={baseY} width={192} height={22} rx={6} fill="#0b1524" stroke={METAL} strokeWidth={3} />
          </g>

          {/* ---- 梁（支点回りに回転） ---- */}
          <g transform={`rotate(${theta}, ${pivotX}, ${pivotY})`}>
            <rect
              x={pivotX - L}
              y={pivotY - 9}
              width={2 * L}
              height={18}
              rx={9}
              fill="url(#bfs-metal)"
              stroke="#8b93a1"
              strokeWidth={2}
            />
            <circle cx={pivotX - L} cy={pivotY} r={11} fill={NAVY} stroke={METAL} strokeWidth={3} />
            <circle cx={pivotX + L} cy={pivotY} r={11} fill={NAVY} stroke={METAL} strokeWidth={3} />
          </g>
          {/* 支点ハブ */}
          <circle cx={pivotX} cy={pivotY} r={16} fill="#0a1220" stroke={METAL} strokeWidth={4} />
          <circle cx={pivotX} cy={pivotY} r={5} fill={ACCENT} opacity={0.7 + 0.3 * shimmer} />

          {/* ---- 皿（市民＝左 / 政府＝右） ---- */}
          <Pan end={leftEnd} accentT={0} label="CITIZEN" labelColor={METAL} />
          <Pan end={rightEnd} accentT={flipProg} label="GOVERNMENT" labelColor={flipProg > 0.4 ? ACCENT : METAL} />
        </svg>

        {/* 政府の皿へ落下する象徴質量（帯封束）＝主運動・高速なのでTrail（AbsoluteFillをラップ） */}
        <Trail layers={5} lagInFrames={1.0} trailOpacity={0.4}>
          <AbsoluteFill>
            {masses.map((m, i) => {
              if (frame < massStart) return null;
              const tSec = (frame - massStart) / fps;
              const local = tSec - m.phase;
              if (local < 0) return null;
              const cyc = ((local % m.period) + m.period) % m.period;
              const fallDur = m.period * 0.82;
              if (cyc > fallDur) return null;
              const p = cyc / fallDur;
              const y = interpolate(p, [0, 1], [spawnY, panSurfaceY], {
                easing: Easing.in(Easing.quad),
                extrapolateRight: 'clamp',
              });
              const x = rightEnd.x + m.xOff;
              const o = interpolate(p, [0, 0.05, 0.82, 1], [0, 1, 1, 0]);
              const rot = m.rot0 + p * m.spin;
              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: x - m.size / 2,
                    top: y - m.size * 0.28,
                    width: m.size,
                    height: m.size * 0.56,
                    transform: `rotate(${rot}deg)`,
                    opacity: o,
                    borderRadius: 5,
                    background: `linear-gradient(180deg, ${NAVY}, #0a1626)`,
                    border: `2px solid ${METAL}`,
                    boxShadow: `0 0 12px ${ACCENT}55`,
                  }}
                >
                  <div
                    style={{
                      position: 'absolute',
                      left: '50%',
                      top: 0,
                      bottom: 0,
                      width: 8,
                      marginLeft: -4,
                      background: ACCENT,
                      opacity: 0.85,
                    }}
                  />
                </div>
              );
            })}
          </AbsoluteFill>
        </Trail>

        {/* ">50% — more likely than not" illustrativeチップ（マスク切れ上がり＋scale） */}
        <div
          style={{
            position: 'absolute',
            left: cx - 210,
            top: Math.round(height * 0.115),
            width: 420,
            overflow: 'hidden',
            paddingBottom: 10,
          }}
        >
          <div
            style={{
              transform: `translateY(${chipY}%) scale(${chipScale})`,
              transformOrigin: '50% 100%',
              opacity: chipO,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 6,
            }}
          >
            <div
              style={{
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 22,
                letterSpacing: 5,
                color: METAL,
              }}
            >
              STANDARD OF PROOF
            </div>
            <div
              style={{
                display: 'flex',
                alignItems: 'baseline',
                gap: 18,
                padding: '10px 30px',
                borderRadius: 14,
                border: `2px solid ${ACCENT}`,
                background: `${ACCENT}18`,
                boxShadow: `0 0 34px ${ACCENT}55`,
              }}
            >
              <span
                style={{
                  fontFamily: BRAND.font.display,
                  fontWeight: 900,
                  fontSize: 80,
                  lineHeight: 1,
                  color: WHITE,
                }}
              >
                {chipMain}
              </span>
              <span
                style={{
                  fontFamily: BRAND.font.body,
                  fontWeight: 700,
                  fontSize: 30,
                  color: ACCENT,
                }}
              >
                {chipSub}
              </span>
            </div>
            <div
              style={{
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 16,
                letterSpacing: 4,
                color: `${METAL}aa`,
              }}
            >
              CAFRA · ILLUSTRATIVE
            </div>
          </div>
        </div>

        {/* キャプション（マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            left: cx - 460,
            bottom: 84,
            width: 920,
            textAlign: 'center',
            overflow: 'hidden',
            paddingBottom: 8,
          }}
        >
          <div
            style={{
              transform: `translateY(${capY}%)`,
              opacity: capO,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 34,
              letterSpacing: 1,
              color: BRAND.color.silver,
              lineHeight: 1.2,
            }}
          >
            The burden shifts to the government.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
