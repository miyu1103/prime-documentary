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

/**
 * ProcessSteps — an ULTRA-PREMIUM "how it worked" numbered flow.
 *
 * Nodes are laid out along a gentle horizontal zig-zag connector. The connector
 * DRAWS forward (strokeDashoffset spring) segment by segment; one step at a time
 * the next numbered node pops with an overshoot spring and a gold index badge,
 * its `title` mask-reveals (overflow:hidden + translateY per glyph) and its
 * `desc` fades-up. Completed steps settle to a calmer state as the flow advances,
 * and a glowing gold pulse travels the connector between steps (motion-blurred
 * Trail). Fully deterministic (useCurrentFrame + index only), every motion eased.
 */

// 秒→フレーム（タイミングは fps から算出。フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

// =====================================================================
// 背景（フルスクリーンSCENE＋奥行き3層以上：グラデ / グリッド / グロー / ビネット）
// =====================================================================
const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  const {durationInFrames, width, height} = useVideoConfig();

  // グリッドは常時ゆっくりドリフト（静止させない）
  const drift = interpolate(frame, [0, durationInFrames], [0, 46], {
    easing: Easing.inOut(Easing.sin),
  });
  // 発光ブロブは左右にゆれる（等速禁止＝sinイージング）
  const glowX = interpolate(
    Math.sin(frame / 70),
    [-1, 1],
    [width * 0.36, width * 0.64],
  );
  const glowY = interpolate(
    Math.sin(frame / 95 + 1.2),
    [-1, 1],
    [height * 0.34, height * 0.5],
  );
  const glowPulse = interpolate(Math.sin(frame / 40), [-1, 1], [0.16, 0.3]);

  return (
    <>
      {/* 層1: 指定のSCENEグラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />
      {/* 層2: 発光グロー（電光ブルー・ゆっくり移動） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(42% 42% at ${glowX}px ${glowY}px, ${BRAND.color.electric}00 0%, ${BRAND.color.electric}00 100%)`,
          backgroundImage: `radial-gradient(38% 46% at ${glowX}px ${glowY}px, ${BRAND.color.electric} 0%, transparent 70%)`,
          opacity: glowPulse,
          filter: 'blur(6px)',
          mixBlendMode: 'screen',
        }}
      />
      {/* 層3: 精密グリッド（電光ブルー・マスクで中央を残す・ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}2a 0px, ${BRAND.color.electric}2a 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}2a 0px, ${BRAND.color.electric}2a 1px, transparent 1px, transparent 76px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
        }}
      />
      {/* 層4: ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(122% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.62) 100%)',
        }}
      />
    </>
  );
};

// =====================================================================
// マスク切れ上がりの見出し（1グリフずつスタッガー：overflow:hidden + translateY）
// =====================================================================
const MaskTitle: React.FC<{
  text: string;
  start: number;
  fps: number;
  size: number;
}> = ({text, start, fps, size}) => {
  const frame = useCurrentFrame();
  const chars = Array.from(text);
  const st = Math.max(1, sec(fps, 0.026));
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        fontFamily: BRAND.font.body,
        fontWeight: 800,
        fontSize: size,
        lineHeight: 1.08,
        letterSpacing: 0.3,
        color: BRAND.color.white,
      }}
    >
      {chars.map((ch, i) => {
        const cs = spring({
          frame: frame - start - i * st,
          fps,
          config: {damping: 16, mass: 1},
        });
        const y = interpolate(cs, [0, 1], [112, 0]);
        const o = interpolate(cs, [0, 0.28], [0, 1], {
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

// =====================================================================
// 番号バッジ（オーバーシュートspringでポップ＋完了で沈静化）— Trail内で使用
// =====================================================================
const Badge: React.FC<{
  index: number;
  start: number;
  nextStart: number | null;
  isLast: boolean;
  fps: number;
  size: number;
  fontSize: number;
}> = ({index, start, nextStart, isLast, fps, size, fontSize}) => {
  const frame = useCurrentFrame();

  // ポップ：低damping springでオーバーシュート
  const cs = spring({
    frame: frame - start,
    fps,
    config: {damping: 9, mass: 0.8, stiffness: 140},
  });
  const scale = 0.2 + cs * 0.8; // cs>1 で 1 を超えて弾む
  const popY = interpolate(cs, [0, 1], [26, 0]);
  const o = interpolate(cs, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // 次ステップ開始で沈静化（グロー・彩度を落として落ち着かせる）
  const calm =
    nextStart == null
      ? 1
      : interpolate(
          frame,
          [nextStart - sec(fps, 0.1), nextStart + sec(fps, 0.5)],
          [1, 0.42],
          {
            easing: Easing.out(Easing.cubic),
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          },
        );

  // 現役ノードはやわらかく呼吸（静止させない・決定論的位相）
  const phase = random(`node-${index}`) * Math.PI * 2;
  const breathe = isLast
    ? interpolate(Math.sin(frame / 26 + phase), [-1, 1], [0.9, 1.1])
    : interpolate(Math.sin(frame / 30 + phase), [-1, 1], [0.94, 1.06]);

  const glow = 0.85 * calm * breathe;
  const ring = interpolate(calm, [0.42, 1], [2, 3]);

  return (
    <div
      style={{
        width: size,
        height: size,
        transform: `translateY(${popY}px) scale(${scale})`,
        opacity: o,
        borderRadius: '50%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: `radial-gradient(60% 60% at 50% 38%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 100%)`,
        border: `${ring}px solid ${BRAND.color.gold}`,
        boxShadow: `0 0 ${34 * glow}px ${BRAND.color.gold}${'88'}, inset 0 0 20px ${BRAND.color.gold}22`,
        color: BRAND.color.gold,
        fontFamily: BRAND.font.display,
        fontSize,
        letterSpacing: 1,
        textShadow: `0 0 18px ${BRAND.color.gold}aa`,
      }}
    >
      {index + 1}
    </div>
  );
};

// =====================================================================
// コネクター上を走る発光パルス（ステップ間・Trailでモーションブラー）
// =====================================================================
const Pulse: React.FC<{
  ax: number;
  ay: number;
  bx: number;
  by: number;
  winStart: number;
  winEnd: number;
}> = ({ax, ay, bx, by, winStart, winEnd}) => {
  const frame = useCurrentFrame();
  if (frame < winStart || frame > winEnd) return null;
  const t = interpolate(frame, [winStart, winEnd], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const x = interpolate(t, [0, 1], [ax, bx]);
  const y = interpolate(t, [0, 1], [ay, by]);
  // 入退場で大きさが伸縮（opacity単独にしない）
  const s = interpolate(t, [0, 0.15, 0.85, 1], [0.2, 1, 1, 0.2], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: 26,
        height: 26,
        transform: `translate(-50%, -50%) scale(${s})`,
        borderRadius: '50%',
        background: `radial-gradient(circle, ${BRAND.color.gold} 0%, ${BRAND.color.gold}00 70%)`,
        boxShadow: `0 0 26px ${BRAND.color.gold}, 0 0 44px ${BRAND.color.gold}88`,
      }}
    />
  );
};

// =====================================================================
// 本体
// =====================================================================
export const ProcessSteps: React.FC<{
  steps: {title: string; desc?: string}[];
  dur?: number;
}> = ({steps, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;
  const n = steps.length;

  // -------------------------------------------------------------------
  // ステップ数に応じてジオメトリ/タイポグラフィを適応させる（3〜5で破綻しない）
  // ノードは中央線の上下に交互配置し、ラベルは「外側」（上ノード→上／下ノード→下）
  // に置く。これで隣接ラベルが必ず別の縦バンドに分かれ、衝突しない。
  // -------------------------------------------------------------------
  const nc = Math.min(Math.max(n, 1), 5); // clamp for scaling only（型/props不変）
  const scl = (a: number, b: number) =>
    interpolate(nc, [3, 5], [a, b], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
  const badgeSize = Math.round(scl(112, 84));
  const badgeFont = Math.round(scl(48, 38));
  const titleSize = Math.round(scl(36, 28));
  const descSize = Math.round(scl(22, 18));
  const amp = scl(78, 96); // ステップが増えるほど上下バンドを広げて分離
  const gapBadge = 20; // バッジ端〜ラベルの隙間

  // 横方向は端に余白を取り、端のラベル（幅textW）が画面外に出ないようにする
  const padX = 300;
  const usableW = width - padX * 2;
  const baseY = height * 0.5;
  const pos = steps.map((_, i) => {
    const x = n === 1 ? width / 2 : padX + (usableW * i) / (n - 1);
    const above = i % 2 === 0; // 偶数=上ノード、奇数=下ノード
    const y = baseY + (above ? -amp : amp);
    // 微小なフロートで常時わずかに動かす（決定論的）
    const fy = Math.sin(frame / 34 + i * 0.9) * 3;
    return {x, y: y + fy, above};
  });

  // タイミング（全て fps から算出）
  const intro = sec(fps, 0.35);
  const perStep = n > 0 ? Math.max(sec(fps, 0.6), Math.floor((D - intro) / n)) : D;
  const startOf = (i: number) => intro + i * perStep;

  // 各ラベルの横幅を境界付け：隣は上下逆バンドなので同バンド（i と i+2, 間隔2slot）
  // にも触れない幅に収める。単語は自身の列内で折り返す。
  const slot = n > 1 ? usableW / (n - 1) : usableW;
  const textW = Math.min(340, Math.max(230, slot * (n <= 3 ? 0.62 : 1.0)));

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      <Backdrop />

      {/* コネクター（セグメントごとに strokeDashoffset spring で前進描画） */}
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{position: 'absolute', inset: 0}}
      >
        {pos.map((p, i) => {
          if (i === 0) return null;
          const a = pos[i - 1];
          const len = Math.hypot(p.x - a.x, p.y - a.y);
          const segStart = startOf(i) - sec(fps, 0.55);
          const draw = spring({
            frame: frame - segStart,
            fps,
            config: {damping: 30, mass: 1},
          });
          const off = len * (1 - draw);
          // 描画済みラインは微かに脈動（静止させない）
          const linePulse = interpolate(
            Math.sin(frame / 22 + i),
            [-1, 1],
            [0.4, 0.7],
          );
          return (
            <g key={i}>
              {/* グロー下地 */}
              <line
                x1={a.x}
                y1={a.y}
                x2={p.x}
                y2={p.y}
                stroke={BRAND.color.electric}
                strokeWidth={9}
                strokeLinecap="round"
                strokeDasharray={len}
                strokeDashoffset={off}
                opacity={0.18 * linePulse * 2}
                style={{filter: 'blur(5px)'}}
              />
              {/* 芯線 */}
              <line
                x1={a.x}
                y1={a.y}
                x2={p.x}
                y2={p.y}
                stroke={BRAND.color.electric}
                strokeWidth={2.5}
                strokeLinecap="round"
                strokeDasharray={len}
                strokeDashoffset={off}
                opacity={linePulse}
              />
            </g>
          );
        })}
      </svg>

      {/* コネクター上を走る発光パルス（Trailでモーションブラー） */}
      <AbsoluteFill>
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          {pos.map((p, i) => {
            if (i === 0) return <React.Fragment key={i} />;
            const a = pos[i - 1];
            const winStart = startOf(i) - sec(fps, 0.5);
            const winEnd = startOf(i) - sec(fps, 0.02);
            return (
              <Pulse
                key={i}
                ax={a.x}
                ay={a.y}
                bx={p.x}
                by={p.y}
                winStart={winStart}
                winEnd={winEnd}
              />
            );
          })}
        </Trail>
      </AbsoluteFill>

      {/* ノード：番号バッジ（Trailでポップをブラー）＋タイトル切れ上がり＋説明フェードアップ */}
      {pos.map((p, i) => {
        const s = startOf(i);
        const nextStart = i < n - 1 ? startOf(i + 1) : null;
        const isLast = i === n - 1;

        // desc：translateY＋opacityで持ち上げる（opacity単独禁止）
        const descStart = s + sec(fps, 0.24);
        const dcs = spring({
          frame: frame - descStart,
          fps,
          config: {damping: 200, mass: 1},
        });
        const descY = interpolate(dcs, [0, 1], [20, 0]);
        const descO = interpolate(dcs, [0, 1], [0, 0.92]);

        return (
          <React.Fragment key={i}>
            {/* バッジ */}
            <div
              style={{
                position: 'absolute',
                left: p.x,
                top: p.y,
                transform: 'translate(-50%, -50%)',
              }}
            >
              <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
                <Badge
                  index={i}
                  start={s}
                  nextStart={nextStart}
                  isLast={isLast}
                  fps={fps}
                  size={badgeSize}
                  fontSize={badgeFont}
                />
              </Trail>
            </div>

            {/* テキストブロック（ノードの外側：上ノードは上／下ノードは下）。
                自前の縦ゾーンに収まり、隣接ラベルは必ず逆バンドで衝突しない。 */}
            <div
              style={{
                position: 'absolute',
                left: p.x,
                top: p.above
                  ? p.y - badgeSize / 2 - gapBadge
                  : p.y + badgeSize / 2 + gapBadge,
                width: textW,
                transform: p.above
                  ? 'translate(-50%, -100%)'
                  : 'translateX(-50%)',
                textAlign: 'center',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: p.above ? 'flex-end' : 'flex-start',
                alignItems: 'center',
              }}
            >
              <MaskTitle
                text={steps[i].title}
                start={s + sec(fps, 0.06)}
                fps={fps}
                size={titleSize}
              />
              {steps[i].desc ? (
                <div
                  style={{
                    marginTop: 12,
                    maxWidth: textW,
                    transform: `translateY(${descY}px)`,
                    opacity: descO,
                    fontFamily: BRAND.font.body,
                    fontWeight: 500,
                    fontSize: descSize,
                    lineHeight: 1.32,
                    letterSpacing: 0.2,
                    color: BRAND.color.silver,
                    overflowWrap: 'break-word',
                    wordBreak: 'normal',
                  }}
                >
                  {steps[i].desc}
                </div>
              ) : null}
            </div>
          </React.Fragment>
        );
      })}
    </AbsoluteFill>
  );
};
