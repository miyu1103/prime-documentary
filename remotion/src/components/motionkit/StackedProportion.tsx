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
// MOTIONKIT — StackedProportion
//   1本の大きな横 100% バー（両端角丸）。各セグメントが左→右へ 1つずつ
//   spring で scaleX 成長（各セグメント自身の左端が原点）してスライドイン。
//   各セグメントは抑えた別アクセント。割合(%)はセグメント成長に同期して
//   カウントアップし、リーダーティック付きの直接ラベル（上/下交互）に
//   マスク切れ上がりで出る。抑えたベースライン。title はマスク切れ上がり。
//   values は合計で正規化。
//   品質規約準拠: 全モーションにイージング（等速禁止）/ opacity単独禁止 /
//   text=マスク切れ上がり / 速い入りは Trail でモーションブラー /
//   決定論（useCurrentFrame + index）/ tabular-nums / 常に微動。
// =====================================================================

// 秒→フレーム（フレーム直書き禁止・fps から算出）
const sec = (fps: number, s: number) => Math.round(fps * s);

// 抑えたセグメント配色（BRAND トークンのみ・巡回）
const ACCENT_CYCLE = [
  BRAND.color.electric,
  BRAND.color.gold,
  BRAND.color.silver,
  BRAND.color.white,
] as const;

// パーセント整形（tabular-nums 前提。整数割合は整数・端数は1桁）
const formatPct = (target: number, current: number): string =>
  Number.isInteger(target) ? String(Math.round(current)) : current.toFixed(1);

// マスク切れ上がりの1行テキスト（overflow:hidden + translateY）
const MaskLine: React.FC<{
  children: React.ReactNode;
  reveal: number; // 0→1 (eased spring progress)
  size: number;
  weight: number;
  color: string;
  font: string;
  letterSpacing?: number;
  align?: 'left' | 'center';
}> = ({
  children,
  reveal,
  size,
  weight,
  color,
  font,
  letterSpacing = 0.5,
  align = 'center',
}) => {
  const y = interpolate(reveal, [0, 1], [118, 0]);
  const o = interpolate(reveal, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
        fontFamily: font,
        fontWeight: weight,
        fontSize: size,
        letterSpacing,
        color,
        lineHeight: 1.05,
        textAlign: align,
        fontVariantNumeric: 'tabular-nums',
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          whiteSpace: 'pre',
        }}
      >
        {children}
      </span>
    </span>
  );
};

export const StackedProportion: React.FC<{
  parts: {label: string; value: number; accent?: string}[];
  title?: string;
  dur?: number;
}> = ({parts, title, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- レイアウト定数（全て定数化） ----
  const margin = 220;
  const barLeft = margin;
  const barWidth = width - margin * 2; // 1480 @1920
  const barH = 132;
  const barRadius = barH / 2;
  const barY = Math.round((height - barH) / 2); // 中央
  const tickLen = 42;

  // ---- 正規化（合計で割る） ----
  const sum = Math.max(
    parts.reduce((a, p) => a + Math.max(0, p.value), 0),
    1e-9,
  );
  let cum = 0;
  const segs = parts.map((p, i) => {
    const frac = Math.max(0, p.value) / sum;
    const left = cum * barWidth; // セグメント左端 x（バー内相対）
    const segW = frac * barWidth;
    cum += frac;
    return {
      label: p.label,
      accent: p.accent ?? ACCENT_CYCLE[i % ACCENT_CYCLE.length],
      frac,
      left,
      segW,
      pct: frac * 100,
    };
  });

  // ---- 背景ドリフト/パルス（決してフルスタティックにしない・sin） ----
  const drift = interpolate(frame, [0, total], [0, 34], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  const glowPulse = interpolate(
    Math.sin((frame / fps) * 1.4),
    [-1, 1],
    [0.42, 0.64],
  );

  // シーン全体の出入り（opacity単独禁止 → 微translateY と併用）
  const sceneY = interpolate(frame, [0, 12], [18, 0], {
    extrapolateRight: 'clamp',
  });
  const sceneO = interpolate(frame, [0, 12, total - 12, total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // タイトルのマスク切れ上がり
  const titleReveal = spring({
    frame: frame - sec(fps, 0.14),
    fps,
    config: {damping: 18, mass: 1},
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {/* Layer 1: フルスクリーン・シーン背景（グラデ） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 抑えたグリッド（ドリフト・depth） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 76px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 45%, black 28%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 45%, black 28%, transparent 84%)',
        }}
      />

      {/* Layer 3: アクセントグロー（微パルス・depth） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(62% 46% at 50% 48%, ${BRAND.color.electric}1f 0%, transparent 70%)`,
          opacity: glowPulse,
        }}
      />

      {/* Layer 4: ビネット（depth） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 48%, transparent 44%, rgba(0,0,0,0.62) 100%)',
        }}
      />

      {/* ---- 主役 ---- */}
      <AbsoluteFill
        style={{opacity: sceneO, transform: `translateY(${sceneY}px)`}}
      >
        {/* タイトル（バー上・マスク切れ上がり） */}
        {title ? (
          <div
            style={{
              position: 'absolute',
              left: barLeft,
              top: barY - 168,
              width: barWidth,
              display: 'flex',
              justifyContent: 'flex-start',
            }}
          >
            <MaskLine
              reveal={titleReveal}
              size={54}
              weight={700}
              color={BRAND.color.white}
              font={BRAND.font.display}
              letterSpacing={1.5}
              align="left"
            >
              {title}
            </MaskLine>
          </div>
        ) : null}

        {/* 抑えたベースライン（バー直下・recessive） */}
        <div
          style={{
            position: 'absolute',
            left: barLeft - 10,
            top: barY + barH + 16,
            width: barWidth + 20,
            height: 2,
            backgroundColor: BRAND.color.silver,
            opacity: 0.2,
          }}
        />

        {/* 100% トラック＋セグメント（角丸両端で内側直線端をクリップ） */}
        <div
          style={{
            position: 'absolute',
            left: barLeft,
            top: barY,
            width: barWidth,
            height: barH,
            borderRadius: barRadius,
            overflow: 'hidden',
            // 抑えたトラック（未充填の 100% を示す・depth）
            backgroundColor: BRAND.color.silver,
            boxShadow: 'inset 0 0 0 1px rgba(200,205,214,0.10)',
          }}
        >
          {/* トラック地の抑え（silver をさらに沈める） */}
          <AbsoluteFill
            style={{backgroundColor: '#06080f', opacity: 0.86}}
          />

          {segs.map((s, i) => {
            // スタッガー成長（spring・等速禁止・各自の左端が原点）
            const cs = spring({
              frame: frame - sec(fps, 0.3) - i * sec(fps, 0.16),
              fps,
              config: {damping: 20, mass: 1},
            });
            const grow = interpolate(cs, [0, 1], [0, 1]);
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: s.left,
                  top: 0,
                  width: s.segW,
                  height: barH,
                }}
              >
                {/* 速い伸長に Trail でモーションブラー。scaleX は左端原点 */}
                <Trail layers={4} lagInFrames={1.1} trailOpacity={0.5}>
                  <div
                    style={{
                      width: s.segW,
                      height: barH,
                      transformOrigin: 'left center',
                      transform: `scaleX(${grow})`,
                      background: `linear-gradient(90deg, ${s.accent}f2 0%, ${s.accent} 100%)`,
                    }}
                  />
                </Trail>
              </div>
            );
          })}

          {/* 内側セグメント境界の細いシーム（成長に同期して現れる） */}
          {segs.map((s, i) => {
            if (i === 0) return null;
            const cs = spring({
              frame: frame - sec(fps, 0.3) - i * sec(fps, 0.16),
              fps,
              config: {damping: 20, mass: 1},
            });
            const seamO = interpolate(cs, [0.15, 0.6], [0, 0.55], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            return (
              <div
                key={`seam-${i}`}
                style={{
                  position: 'absolute',
                  left: s.left,
                  top: 0,
                  width: 2,
                  height: barH,
                  backgroundColor: '#06080f',
                  opacity: seamO,
                }}
              />
            );
          })}
        </div>

        {/* リーダーティック＋直接ラベル（上/下交互・マスク切れ上がり） */}
        {segs.map((s, i) => {
          const above = i % 2 === 0;
          const centerX = barLeft + s.left + s.segW / 2;

          // 成長 spring（ラベル/ティックの位相・カウント同期）
          const cs = spring({
            frame: frame - sec(fps, 0.3) - i * sec(fps, 0.16),
            fps,
            config: {damping: 20, mass: 1},
          });
          const grow = interpolate(cs, [0, 1], [0, 1]);

          // ティック伸長（バー端が原点で外側へ伸びる）
          const tickReveal = spring({
            frame: frame - sec(fps, 0.36) - i * sec(fps, 0.16),
            fps,
            config: {damping: 22, mass: 1},
          });
          const tickScale = interpolate(tickReveal, [0, 1], [0, 1]);

          // ラベル本体のマスク切れ上がり
          const labelReveal = spring({
            frame: frame - sec(fps, 0.42) - i * sec(fps, 0.16),
            fps,
            config: {damping: 16, mass: 0.9},
          });

          const shownPct = formatPct(s.pct, s.pct * grow);

          return (
            <React.Fragment key={`lbl-${i}`}>
              {/* リーダーティック（バー端 → ラベル方向） */}
              <div
                style={{
                  position: 'absolute',
                  left: centerX - 1,
                  top: above ? barY - tickLen : barY + barH,
                  width: 2,
                  height: tickLen,
                  backgroundColor: s.accent,
                  opacity: 0.75,
                  transformOrigin: above ? 'bottom center' : 'top center',
                  transform: `scaleY(${tickScale})`,
                }}
              />
              {/* 直接ラベル（ラベル名＋% カウントアップ） */}
              <div
                style={{
                  position: 'absolute',
                  left: centerX,
                  ...(above
                    ? {top: barY - tickLen - 74}
                    : {top: barY + barH + tickLen + 8}),
                  transform: 'translateX(-50%)',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 2,
                }}
              >
                <MaskLine
                  reveal={labelReveal}
                  size={30}
                  weight={600}
                  color={BRAND.color.white}
                  font={BRAND.font.body}
                  letterSpacing={1}
                  align="center"
                >
                  {s.label}
                </MaskLine>
                <MaskLine
                  reveal={labelReveal}
                  size={40}
                  weight={400}
                  color={s.accent}
                  font={BRAND.font.display}
                  letterSpacing={0.5}
                  align="center"
                >
                  {shownPct}%
                </MaskLine>
              </div>
            </React.Fragment>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
