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
// DocHighlight — MOTIONKIT overlay for document stills (evidence/quotes/records).
//   Draws animated marks over 0..1 document regions, staggered per rect:
//     'underline'  下線が左から伸びる（scaleX / transformOrigin left）
//     'box'        枠線が描き込まれる（strokeDashoffset のドローオン）
//     'redact'     黒塗りが左からワイプイン（scaleX / transformOrigin left）
// 品質: 全モーションにイージング/spring（等速禁止）・opacity単独禁止・
//   スタッガー・決定論（useCurrentFrame + index のみ）・速い動きに Trail。
//   背景は透明・root は pointerEvents:'none'（下地の書類に被せるオーバーレイ）。
//   配色は BRAND トークンのみ。
// =====================================================================

type Rect = {x: number; y: number; w: number; h: number};
type Mode = 'underline' | 'box' | 'redact';

// 秒→フレーム（fps 由来。フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.max(1, Math.round(fps * s));

// 常時わずかに脈打つグロー（「完全静止」を作らない）。Easing.inOut で非等速。
const useBreath = (indexPhase: number): number => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const period = sec(fps, 2.2);
  // index ごとに位相をずらして固まらないように（決定論）
  const t = (frame + indexPhase * Math.round(period / 3)) % period;
  return interpolate(t, [0, period / 2, period], [0.35, 0.9, 0.35], {
    easing: Easing.inOut(Easing.sin),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// 共通: この rect の登場進捗（spring・0..1・イージング付き）
const useReveal = (
  delay: number,
  config: {damping: number; mass: number},
): number => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - delay, fps, config});
};

// ---------------------------------------------------------------------
// underline: 左から伸びる下線（scaleX）＋ わずかな rise（opacity単独回避）
// ---------------------------------------------------------------------
const UnderlineBar: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  delay: number;
  phase: number;
}> = ({x, y, w, h, delay, phase}) => {
  const grow = useReveal(delay, {damping: 16, mass: 0.9});
  const breath = useBreath(phase);

  const scaleX = interpolate(grow, [0, 1], [0, 1]);
  const rise = interpolate(grow, [0, 1], [10, 0]); // 下からわずかに上がる
  const barH = Math.max(4, h * 0.07);
  const glow = 8 + breath * 16;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y + h - barH,
        width: w,
        height: barH,
        borderRadius: barH / 2,
        backgroundColor: BRAND.color.electric,
        boxShadow: `0 0 ${glow}px ${BRAND.color.electric}`,
        transform: `translateY(${rise}px) scaleX(${scaleX})`,
        transformOrigin: 'left center',
      }}
    />
  );
};

// ---------------------------------------------------------------------
// redact: 左から黒塗りがワイプイン（scaleX）。細い電光エッジで質感付け。
// ---------------------------------------------------------------------
const RedactBar: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  delay: number;
  phase: number;
}> = ({x, y, w, h, delay, phase}) => {
  const grow = useReveal(delay, {damping: 18, mass: 1});
  const breath = useBreath(phase);

  const scaleX = interpolate(grow, [0, 1], [0, 1]);
  const settle = interpolate(grow, [0, 1], [6, 0]); // 上下方向のわずかな詰め
  const edge = 0.25 + breath * 0.4;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y + settle / 2,
        width: w,
        height: h - settle,
        backgroundColor: BRAND.color.ink,
        borderRight: `2px solid ${BRAND.color.electric}`,
        boxShadow: `inset 0 0 ${6 + breath * 6}px ${BRAND.color.navy}`,
        opacity: 0.9 + edge * 0.1,
        transform: `scaleX(${scaleX})`,
        transformOrigin: 'left center',
      }}
    />
  );
};

// ---------------------------------------------------------------------
// box: 枠線を strokeDashoffset で描き込む（ドローオン）＋ 常時グロー
// ---------------------------------------------------------------------
const BoxDraw: React.FC<{
  x: number;
  y: number;
  w: number;
  h: number;
  delay: number;
  phase: number;
}> = ({x, y, w, h, delay, phase}) => {
  const draw = useReveal(delay, {damping: 24, mass: 1});
  const breath = useBreath(phase);

  const sw = 4;
  const rx = Math.min(10, Math.min(w, h) * 0.1);
  const iw = Math.max(1, w - sw);
  const ih = Math.max(1, h - sw);
  const perim = 2 * (iw + ih);
  const p = interpolate(draw, [0, 1], [0, 1]);
  const dashOffset = perim * (1 - p);
  // opacity単独回避のためコーナーからの微スケールも与える
  const s = interpolate(draw, [0, 1], [0.965, 1]);

  return (
    <svg
      width={w}
      height={h}
      style={{
        position: 'absolute',
        left: x,
        top: y,
        overflow: 'visible',
        transform: `scale(${s})`,
        transformOrigin: 'center center',
      }}
    >
      <rect
        x={sw / 2}
        y={sw / 2}
        width={iw}
        height={ih}
        rx={rx}
        ry={rx}
        fill="none"
        stroke={BRAND.color.gold}
        strokeWidth={sw}
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray={perim}
        strokeDashoffset={dashOffset}
        style={{filter: `drop-shadow(0 0 ${6 + breath * 12}px ${BRAND.color.gold})`}}
      />
    </svg>
  );
};

// ---------------------------------------------------------------------
// 1 rect 分のマーク。速い並進（underline/redact）は Trail でモーションブラー。
// ---------------------------------------------------------------------
const Mark: React.FC<{
  rect: Rect;
  mode: Mode;
  index: number;
  fps: number;
  width: number;
  height: number;
}> = ({rect, mode, index, fps, width, height}) => {
  const delay = index * sec(fps, 0.12);
  const px = {
    x: rect.x * width,
    y: rect.y * height,
    w: rect.w * width,
    h: rect.h * height,
  };

  if (mode === 'box') {
    return (
      <BoxDraw x={px.x} y={px.y} w={px.w} h={px.h} delay={delay} phase={index} />
    );
  }

  const bar =
    mode === 'redact' ? (
      <RedactBar x={px.x} y={px.y} w={px.w} h={px.h} delay={delay} phase={index} />
    ) : (
      <UnderlineBar
        x={px.x}
        y={px.y}
        w={px.w}
        h={px.h}
        delay={delay}
        phase={index}
      />
    );

  // 左からのワイプは速いのでトレイルで残像を付ける
  return (
    <Trail layers={4} lagInFrames={0.9} trailOpacity={0.55}>
      {bar}
    </Trail>
  );
};

// ---------------------------------------------------------------------
// DocHighlight — 公開 API
// ---------------------------------------------------------------------
export const DocHighlight: React.FC<{
  rects: Rect[];
  mode?: Mode;
  dur?: number;
}> = ({rects, mode = 'underline', dur}) => {
  const {fps, width, height, durationInFrames} = useVideoConfig();
  // dur は将来のシーケンス尺制御用（既定は全尺）。参照して固定尺前提を避ける。
  const total = dur ?? durationInFrames;

  return (
    <AbsoluteFill
      style={{backgroundColor: 'transparent', pointerEvents: 'none'}}
    >
      {rects.map((rect, i) => (
        <Mark
          key={`${i}-${total}`}
          rect={rect}
          mode={mode}
          index={i}
          fps={fps}
          width={width}
          height={height}
        />
      ))}
    </AbsoluteFill>
  );
};
