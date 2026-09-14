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
// DonutReveal — ULTRA-PREMIUM ring/donut chart for Prime Documentary.
//   ・ウェッジが時計回りに1枚ずつ、イージング済みの弧長(strokeDashoffset)
//     でスタッガー掃引 → 速い掃引は Trail でモーションブラー。
//   ・各スライスの割合(%)がカウントアップ(tabular-nums)＋直接ラベルと
//     リーダー線をマスク切れ上がりで提示。
//   ・中央の大きな合計値 or centerLabel をマスク切れ上がり。
//   ・全体は微細な呼吸（スケール＋装飾リングの揺れ回転）で常に生きている。
// 品質ルール: 等速線形なし・opacity単独なし・テキストはマスク切れ上がり・
//   決定論(useCurrentFrame+index)・単一アクセント/ウェッジ(電光/金/銀/抑制系)。
// 色は BRAND トークンのみ。
// =====================================================================

const C = BRAND.color;

// 秒→フレーム（フレーム直書き禁止・fpsから算出）
const sec = (fps: number, s: number) => Math.round(fps * s);

// 上=0°・時計回りで測る極座標 → 画面座標
const polar = (cx: number, cy: number, r: number, deg: number) => {
  const rad = ((deg - 90) * Math.PI) / 180;
  return {x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad)};
};

// マスク切れ上がり（overflow:hidden + translateY、opacity単独禁止なので必ず併用）
const MaskReveal: React.FC<{
  delay: number;
  children: React.ReactNode;
  distance?: number;
  damping?: number;
}> = ({delay, children, distance = 118, damping = 18}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: frame - delay, fps, config: {damping, mass: 1}});
  const y = interpolate(s, [0, 1], [distance, 0]);
  const o = interpolate(s, [0, 0.32], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span style={{display: 'block', overflow: 'hidden', paddingBottom: '0.14em'}}>
      <span style={{display: 'block', transform: `translateY(${y}%)`, opacity: o}}>
        {children}
      </span>
    </span>
  );
};

export const DonutReveal: React.FC<{
  slices: {label: string; value: number; accent?: string}[];
  centerLabel?: string;
  dur?: number;
}> = ({slices, centerLabel, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // ---- 幾何 ------------------------------------------------------------
  const cx = width / 2;
  const cy = height / 2;
  const R = 300; // リング中心半径
  const SW = 92; // リング太さ
  const circ = 2 * Math.PI * R;
  const rOuter = R + SW / 2 + 8; // リーダー線の起点（リング外周直後）
  const kneeR = R + SW / 2 + 78; // リーダー線の膝
  const labelR = R + SW / 2 + 96; // ラベル基準半径

  // ---- 抑制系ファミリー（電光/金/銀/抑制）: 単一アクセント/ウェッジ ----
  const family: {c: string; op: number}[] = [
    {c: C.electric, op: 1},
    {c: C.gold, op: 1},
    {c: C.silver, op: 0.92},
    {c: C.silver, op: 0.5},
  ];

  // ---- 正規化 & 累積弧長 ----------------------------------------------
  const total = slices.reduce((s, d) => s + Math.max(0, d.value), 0) || 1;
  const gapFrac = 0.006; // ウェッジ間の微小ギャップ（プレミアムな余白）
  let acc = 0;
  const arr = slices.map((s, i) => {
    const frac = Math.max(0, s.value) / total;
    const startFrac = acc;
    acc += frac;
    const midTheta = (startFrac + frac / 2) * 360;
    const startLen = (startFrac + gapFrac / 2) * circ;
    const arcLen = Math.max(0, frac - gapFrac) * circ;
    const fam = family[i % family.length];
    const color = s.accent ?? fam.c;
    const colorOp = s.accent ? 1 : fam.op;
    return {
      label: s.label,
      pct: frac * 100,
      color,
      colorOp,
      midTheta,
      startLen,
      arcLen,
    };
  });

  // ---- タイムライン（秒基準・全て定数化） ------------------------------
  const revealStart = sec(fps, 0.35);
  const stagger = sec(fps, 0.16);
  const centerDelay = sec(fps, 0.55);

  // ---- 呼吸（常に生きている・sinイージングで非線形） -------------------
  const breathT = (frame / fps) * Math.PI * 2 * 0.16;
  const breathScale = 1 + 0.009 * Math.sin(breathT);
  const decoSpin = 9 * Math.sin((frame / fps) * Math.PI * 2 * 0.09); // 揺れ回転
  const decoSpin2 = -6 * Math.sin((frame / fps) * Math.PI * 2 * 0.07);
  const glowPulse = 0.5 + 0.5 * Math.sin(breathT * 1.3);

  // ---- シーン出入り（opacity＋微translateY） ---------------------------
  const sceneO = interpolate(frame, [0, 12, D - 14, D], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const sceneY = interpolate(frame, [0, 14], [26, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // ---- 中央値のカウントアップ（等速禁止・cubic out） -------------------
  const centerP = interpolate(frame, [centerDelay, centerDelay + sec(fps, 1.4)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const centerNumber = Math.round(total * centerP).toLocaleString('en-US');
  const centerText = centerLabel ?? centerNumber;

  // 装飾ティックリング（決定論的に生成）
  const ticks = Array.from({length: 72}, (_, i) => i);

  return (
    <AbsoluteFill
      style={{
        opacity: sceneO,
        transform: `translateY(${sceneY}px)`,
        backgroundColor: '#06080f',
      }}
    >
      {/* ---- 奥行きレイヤー1: 指定の全画面グラデ背景 ---- */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${C.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* ---- 奥行きレイヤー2: 微細な同心リングのテクスチャ（ドリフト） ---- */}
      <AbsoluteFill
        style={{
          opacity: 0.5,
          transform: `translateY(${interpolate(frame, [0, D], [0, 26], {
            easing: Easing.inOut(Easing.sin),
          })}px)`,
          backgroundImage: `repeating-radial-gradient(circle at 50% 50%, ${C.electric}12 0px, ${C.electric}12 1px, transparent 1px, transparent 46px)`,
          maskImage: 'radial-gradient(60% 60% at 50% 50%, black 8%, transparent 74%)',
          WebkitMaskImage:
            'radial-gradient(60% 60% at 50% 50%, black 8%, transparent 74%)',
        }}
      />

      {/* ---- 奥行きレイヤー3: 中央のアクセント・グロー（拍動） + ビネット ---- */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(38% 38% at 50% 50%, ${C.electric}22 0%, transparent 70%)`,
          opacity: 0.55 + glowPulse * 0.35,
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(125% 100% at 50% 46%, transparent 42%, rgba(0,0,0,0.6) 100%)',
        }}
      />

      {/* ================= ドーナツ本体（呼吸スケール） ================= */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          transform: `scale(${breathScale})`,
        }}
      >
        {/* 装飾: 揺れ回転する外側ティックリング + 内側ヘアライン */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
        >
          <g transform={`rotate(${decoSpin} ${cx} ${cy})`}>
            {ticks.map((i) => {
              const a = (i / ticks.length) * 360;
              const long = i % 6 === 0;
              const r1 = R + SW / 2 + 26;
              const r2 = r1 + (long ? 16 : 8);
              const p1 = polar(cx, cy, r1, a);
              const p2 = polar(cx, cy, r2, a);
              return (
                <line
                  key={i}
                  x1={p1.x}
                  y1={p1.y}
                  x2={p2.x}
                  y2={p2.y}
                  stroke={C.silver}
                  strokeWidth={long ? 2 : 1}
                  opacity={long ? 0.28 : 0.14}
                />
              );
            })}
          </g>
          <circle
            cx={cx}
            cy={cy}
            r={R - SW / 2 - 20}
            fill="none"
            stroke={C.silver}
            strokeWidth={1}
            opacity={0.12}
            transform={`rotate(${decoSpin2} ${cx} ${cy})`}
            strokeDasharray="2 10"
          />
        </svg>

        {/* トラック（未充填のベースリング） */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
        >
          <circle
            cx={cx}
            cy={cy}
            r={R}
            fill="none"
            stroke={C.silver}
            strokeOpacity={0.08}
            strokeWidth={SW}
          />
        </svg>

        {/* ウェッジ掃引（速い動き → Trail でモーションブラー） */}
        <Trail layers={5} lagInFrames={1.4} trailOpacity={0.32}>
          <svg
            width={width}
            height={height}
            style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
          >
            {arr.map((w, i) => {
              const s = spring({
                frame: frame - revealStart - i * stagger,
                fps,
                config: {damping: 20, mass: 1},
              });
              const grow = interpolate(s, [0, 1], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              return (
                <circle
                  key={i}
                  cx={cx}
                  cy={cy}
                  r={R}
                  fill="none"
                  stroke={w.color}
                  strokeOpacity={w.colorOp}
                  strokeWidth={SW}
                  strokeLinecap="butt"
                  strokeDasharray={`${w.arcLen * grow} ${circ}`}
                  strokeDashoffset={-w.startLen}
                  transform={`rotate(-90 ${cx} ${cy})`}
                  style={{filter: `drop-shadow(0 0 16px ${w.color}55)`}}
                />
              );
            })}
          </svg>
        </Trail>

        {/* リーダー線（strokeDashoffset で描画・イージング） */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}
        >
          {arr.map((w, i) => {
            const s = spring({
              frame: frame - revealStart - i * stagger - sec(fps, 0.28),
              fps,
              config: {damping: 26, mass: 1},
            });
            const p = interpolate(s, [0, 1], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const rightSide = Math.sin((w.midTheta * Math.PI) / 180) >= 0;
            const a = polar(cx, cy, rOuter, w.midTheta);
            const knee = polar(cx, cy, kneeR, w.midTheta);
            const endX = knee.x + (rightSide ? 66 : -66);
            const dLen = Math.hypot(knee.x - a.x, knee.y - a.y) + Math.abs(endX - knee.x);
            return (
              <g key={i}>
                <path
                  d={`M ${a.x} ${a.y} L ${knee.x} ${knee.y} L ${endX} ${knee.y}`}
                  fill="none"
                  stroke={w.color}
                  strokeOpacity={0.7 * w.colorOp}
                  strokeWidth={2}
                  strokeDasharray={dLen}
                  strokeDashoffset={dLen * (1 - p)}
                />
                <circle
                  cx={a.x}
                  cy={a.y}
                  r={interpolate(p, [0.4, 1], [0, 4.5], {extrapolateLeft: 'clamp'})}
                  fill={w.color}
                  opacity={w.colorOp}
                />
              </g>
            );
          })}
        </svg>

        {/* 直接ラベル（名前＋%カウントアップ）: マスク切れ上がり・tabular-nums */}
        {arr.map((w, i) => {
          const s = spring({
            frame: frame - revealStart - i * stagger - sec(fps, 0.3),
            fps,
            config: {damping: 20, mass: 1},
          });
          const grow = interpolate(s, [0, 1], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          });
          const shownPct = (w.pct * grow).toFixed(0);
          const rightSide = Math.sin((w.midTheta * Math.PI) / 180) >= 0;
          const knee = polar(cx, cy, kneeR, w.midTheta);
          const anchorX = knee.x + (rightSide ? 78 : -78);
          const delay = revealStart + i * stagger + sec(fps, 0.34);
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: anchorX,
                top: knee.y,
                transform: `translate(${rightSide ? '0' : '-100%'}, -50%)`,
                textAlign: rightSide ? 'left' : 'right',
                width: 320,
                display: 'flex',
                flexDirection: 'column',
                alignItems: rightSide ? 'flex-start' : 'flex-end',
              }}
            >
              <MaskReveal delay={delay}>
                <span
                  style={{
                    fontFamily: BRAND.font.body,
                    fontSize: 24,
                    fontWeight: 600,
                    letterSpacing: 2,
                    textTransform: 'uppercase',
                    color: C.silver,
                    whiteSpace: 'nowrap',
                  }}
                >
                  {w.label}
                </span>
              </MaskReveal>
              <MaskReveal delay={delay + sec(fps, 0.06)}>
                <span
                  style={{
                    fontFamily: BRAND.font.display,
                    fontSize: 58,
                    lineHeight: 1,
                    color: w.color,
                    opacity: w.colorOp,
                    fontVariantNumeric: 'tabular-nums',
                  }}
                >
                  {shownPct}
                  <span style={{fontSize: 34, color: C.white, marginLeft: 2}}>%</span>
                </span>
              </MaskReveal>
            </div>
          );
        })}

        {/* 中央: 大きな合計 or centerLabel（マスク切れ上がり + 速い登場は Trail） */}
        <div
          style={{
            position: 'absolute',
            left: cx,
            top: cy,
            transform: 'translate(-50%, -50%)',
            textAlign: 'center',
            width: R * 1.5,
          }}
        >
          <Trail layers={4} lagInFrames={1.2} trailOpacity={0.28}>
            <MaskReveal delay={centerDelay} distance={130} damping={16}>
              <span
                style={{
                  fontFamily: BRAND.font.display,
                  fontSize: 118,
                  lineHeight: 0.92,
                  letterSpacing: -2,
                  color: C.white,
                  fontVariantNumeric: 'tabular-nums',
                  display: 'block',
                }}
              >
                {centerText}
              </span>
            </MaskReveal>
          </Trail>
          <MaskReveal delay={centerDelay + sec(fps, 0.18)} distance={90}>
            <span
              style={{
                fontFamily: BRAND.font.body,
                fontSize: 24,
                fontWeight: 600,
                letterSpacing: 8,
                textTransform: 'uppercase',
                color: C.electric,
                display: 'block',
                marginTop: 10,
              }}
            >
              {centerLabel == null ? 'Total' : 'Share'}
            </span>
          </MaskReveal>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
