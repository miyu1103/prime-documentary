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
// CarKeyLock — 概念シーン：車型ヘッドの鍵が、家の玄関ドアの錠へ回り込む
//   「最も晒されている所有物(車)が、最も守られた場所(家)への鍵になる」を可視化。
//   ・鍵ヘッド＝車のシルエット（ベクター）
//   ・鍵が挿さり(スライド)→回る(springで回転)＝錠が抵抗して"カチッ"(小オーバーシュート)
//   ・冷たいelectricの輝きが鍵の刃を走る（Trailでモーションブラー）
//   ・暗い背景＋奥行き≥3層・単一アクセント(electric)・凍らない微シマー
// 全モーションeased・opacity単独なし・fps算出・deterministic。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, ${BG} 82%)`;

const sec = (fps: number, s: number) => Math.round(fps * s);

// 車のシルエット（側面）— 鍵のヘッド（bow）として使う。原点中心・幅約200。
const CarBow: React.FC<{fill: string; stroke: string}> = ({fill, stroke}) => (
  <g transform="translate(-100,-52)">
    <path
      d="M6,66
         C6,50 20,48 34,47
         L52,30 C58,20 68,14 84,13
         L128,13 C142,13 152,20 160,32
         L176,47 C190,49 200,52 200,66
         L200,74 C200,80 195,84 189,84
         L173,84
         A17,17 0 0 0 139,84
         L79,84
         A17,17 0 0 0 45,84
         L17,84 C10,84 6,80 6,74 Z"
      fill={fill}
      stroke={stroke}
      strokeWidth={3}
      strokeLinejoin="round"
    />
    {/* 窓 */}
    <path
      d="M60,31 L72,18 L106,18 L106,31 Z M112,18 L126,18 L138,31 L112,31 Z"
      fill={BG}
      opacity={0.55}
    />
    {/* 車輪 */}
    <circle cx={62} cy={84} r={13} fill={BG} stroke={stroke} strokeWidth={3} />
    <circle cx={156} cy={84} r={13} fill={BG} stroke={stroke} strokeWidth={3} />
  </g>
);

export const CarKeyLock: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  const cx = width / 2;
  const cy = height / 2;

  // 錠(keyhole)の位置：家の玄関ドア上
  const lockX = cx + 250;
  const lockY = cy + 20;

  // --- タイムライン（全て fps 算出）---
  // 1) 家が立ち上がる
  const houseS = spring({
    frame: frame - sec(fps, 0.15),
    fps,
    config: {damping: 22, mass: 1},
  });
  const houseY = interpolate(houseS, [0, 1], [60, 0]);
  const houseO = interpolate(houseS, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});

  // 2) 鍵が左から挿し込まれる（スライドイン）
  const insertS = spring({
    frame: frame - sec(fps, 0.7),
    fps,
    config: {damping: 20, mass: 0.9},
  });
  const insertX = interpolate(insertS, [0, 1], [-620, 0]);

  // 3) 鍵が回る（抵抗→カチッ：小オーバーシュートのspring）
  const turnS = spring({
    frame: frame - sec(fps, 1.5),
    fps,
    config: {damping: 9, mass: 0.9, stiffness: 140},
  });
  const turnDeg = interpolate(turnS, [0, 1], [0, 92]);

  // 4) 錠のリングが抵抗してから同期して回る（さらに強いオーバーシュート＝click）
  const lockS = spring({
    frame: frame - sec(fps, 1.62),
    fps,
    config: {damping: 7, mass: 0.8, stiffness: 170},
  });
  const lockDeg = interpolate(lockS, [0, 1], [0, 92]);
  // click時のフラッシュ
  const clickFlash = interpolate(
    lockS,
    [0.55, 0.72, 0.9],
    [0, 0.9, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // 冷たいelectricグリントが刃を走る（挿入〜回転の間）
  const glintP = interpolate(
    frame,
    [sec(fps, 0.9), sec(fps, 1.75)],
    [0, 1],
    {
      easing: Easing.inOut(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );
  const glintActive = frame >= sec(fps, 0.9) && frame <= sec(fps, 1.8);

  // 凍らない微シマー
  const shimmer = interpolate(Math.sin(frame / 10), [-1, 1], [0.82, 1]);
  const metalPulse = interpolate(Math.sin(frame / 13 + 1), [-1, 1], [0.9, 1]);

  // シーン出入り
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 12], [18, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  const METAL = BRAND.color.silver;
  const ACCENT = BRAND.color.electric;

  // 鍵：pivot(keyhole)を基準に回す。刃は左から錠へ伸びる。
  // 鍵全体の座標系：keyhole(lockX,lockY)を原点にしてローカル配置。
  const keyBladeLen = 300; // keyhole から左へ伸びる刃
  const bowCenterX = -keyBladeLen - 120; // ヘッド(車)の中心

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 グリッド */}
      <AbsoluteFill
        style={{
          opacity: 0.09,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 78px),
            repeating-linear-gradient(90deg, ${ACCENT}22 0px, ${ACCENT}22 1px, transparent 1px, transparent 78px)`,
          maskImage: 'radial-gradient(120% 90% at 55% 48%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 55% 48%, black 30%, transparent 82%)',
        }}
      />
      {/* L3 ドア裏のグロー（clickで強まる） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(28% 34% at ${(lockX / width) * 100}% ${
            (lockY / height) * 100
          }%, ${ACCENT}${clickFlash > 0.4 ? '55' : '22'} 0%, transparent 68%)`,
        }}
      />

      <AbsoluteFill style={{opacity: inO * outO, transform: `translateY(${inY}px)`}}>
        <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
          <defs>
            <linearGradient id="ckl-metal" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor={BRAND.color.white} />
              <stop offset="50%" stopColor={METAL} />
              <stop offset="100%" stopColor="#7f8794" />
            </linearGradient>
          </defs>

          {/* ---- L (奥) 家の輪郭 ---- */}
          <g
            transform={`translate(0, ${houseY})`}
            opacity={houseO}
            stroke={METAL}
            strokeWidth={3}
            fill="none"
            strokeLinejoin="round"
          >
            {/* 本体 */}
            <path
              d={`M${cx - 40},${cy + 300}
                  L${cx - 40},${cy - 120}
                  L${cx + 360},${cy - 120}
                  L${cx + 360},${cy + 300} Z`}
              fill={`${BRAND.color.navy}`}
              opacity={0.9}
            />
            {/* 屋根 */}
            <path
              d={`M${cx - 80},${cy - 120}
                  L${cx + 160},${cy - 260}
                  L${cx + 400},${cy - 120} Z`}
              fill="#0d1f33"
            />
            {/* 窓 */}
            <rect
              x={cx + 200}
              y={cy - 60}
              width={110}
              height={110}
              rx={6}
              fill={`${ACCENT}22`}
              stroke={METAL}
              strokeWidth={2}
            />
            <line x1={cx + 255} y1={cy - 60} x2={cx + 255} y2={cy + 50} strokeWidth={2} />
            <line x1={cx + 200} y1={cy - 5} x2={cx + 310} y2={cy - 5} strokeWidth={2} />
          </g>

          {/* ---- 玄関ドア（錠が入る前面） ---- */}
          <g transform={`translate(0, ${houseY})`} opacity={houseO}>
            <rect
              x={lockX - 95}
              y={lockY - 150}
              width={190}
              height={340}
              rx={8}
              fill="#0a1626"
              stroke={METAL}
              strokeWidth={3}
            />
            {/* ドアの枠彫り */}
            <rect
              x={lockX - 72}
              y={lockY - 126}
              width={144}
              height={130}
              rx={4}
              fill="none"
              stroke={METAL}
              strokeWidth={2}
              opacity={0.5}
            />
          </g>

          {/* ---- 錠のリング（抵抗→click回転） ---- */}
          <g transform={`translate(${lockX},${lockY})`}>
            {/* 台座グロー */}
            <circle
              r={54}
              fill={ACCENT}
              opacity={0.1 * metalPulse + clickFlash * 0.4}
            />
            <g transform={`rotate(${lockDeg})`}>
              {/* リング */}
              <circle
                r={44}
                fill="#0a1220"
                stroke={METAL}
                strokeWidth={5}
                opacity={metalPulse}
              />
              {/* ノッチ（回転が見える） */}
              <rect x={-4} y={-46} width={8} height={16} rx={2} fill={ACCENT} />
              {/* keyhole 形 */}
              <circle r={12} cy={-6} fill={BG} stroke={METAL} strokeWidth={3} />
              <path d="M-9,0 L9,0 L5,26 L-5,26 Z" fill={BG} stroke={METAL} strokeWidth={3} />
            </g>
          </g>

          {/* ---- 鍵（車ヘッド）：keyhole を pivot に回転＋挿入スライド ---- */}
          <g
            transform={`translate(${lockX + insertX},${lockY}) rotate(${turnDeg})`}
          >
            {/* 刃（keyhole から左へ） */}
            <g opacity={shimmer}>
              {/* シャフト */}
              <rect
                x={-keyBladeLen}
                y={-11}
                width={keyBladeLen}
                height={22}
                rx={5}
                fill="url(#ckl-metal)"
                stroke="#8b93a1"
                strokeWidth={2}
              />
              {/* 刃の歯 */}
              <path
                d={`M${-keyBladeLen},11
                    l0,26 l20,0 l0,-14 l18,0 l0,20 l20,0 l0,-14 l16,0 l0,16 l22,0 l0,-40 Z`}
                fill="url(#ckl-metal)"
                stroke="#8b93a1"
                strokeWidth={2}
                strokeLinejoin="round"
              />
              {/* 首（bowへ） */}
              <rect
                x={bowCenterX + 90}
                y={-9}
                width={40}
                height={18}
                rx={4}
                fill={METAL}
              />
            </g>

            {/* ヘッド＝車のシルエット */}
            <g transform={`translate(${bowCenterX},0) scale(1.05)`} opacity={metalPulse}>
              {/* 台座リング */}
              <circle r={78} fill="#0c1524" stroke={METAL} strokeWidth={4} />
              <CarBow fill={`${BRAND.color.navy}`} stroke={METAL} />
            </g>
          </g>
        </svg>

        {/* 冷たい electric グリントが刃を走る（Trailでモーションブラー） */}
        {glintActive ? (
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            {(() => {
              // 刃のローカル座標(x: -keyBladeLen..0, y:0) を pivot 回転＋挿入で世界座標へ
              const localX = interpolate(glintP, [0, 1], [-keyBladeLen + 20, -10]);
              const rad = (turnDeg * Math.PI) / 180;
              const px = lockX + insertX + localX * Math.cos(rad);
              const py = lockY + localX * Math.sin(rad);
              return (
                <div
                  style={{
                    position: 'absolute',
                    left: px - 9,
                    top: py - 9,
                    width: 18,
                    height: 18,
                    borderRadius: '50%',
                    background: BRAND.color.white,
                    boxShadow: `0 0 24px 7px ${ACCENT}, 0 0 9px 2px ${BRAND.color.white}`,
                  }}
                />
              );
            })()}
          </Trail>
        ) : null}

        {/* clickの瞬間の閃光リング */}
        {clickFlash > 0.02 ? (
          <div
            style={{
              position: 'absolute',
              left: lockX - 70,
              top: lockY - 70,
              width: 140,
              height: 140,
              borderRadius: '50%',
              border: `3px solid ${ACCENT}`,
              transform: `scale(${interpolate(clickFlash, [0, 0.9], [0.7, 1.5])})`,
              opacity: clickFlash,
              boxShadow: `0 0 40px ${ACCENT}`,
            }}
          />
        ) : null}

        {/* キャプション（マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            left: cx - 520,
            bottom: 96,
            width: 720,
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              transform: `translateY(${interpolate(
                spring({frame: frame - sec(fps, 1.9), fps, config: {damping: 18}}),
                [0, 1],
                [120, 0],
              )}%)`,
              fontFamily: BRAND.font.body,
              fontWeight: 600,
              fontSize: 30,
              letterSpacing: 1,
              color: BRAND.color.silver,
              lineHeight: 1.2,
            }}
          >
            Your car becomes the key to your home.
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
