import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';

// =====================================================================
// ForcefulCut — 力強い入場トランジション集（クロスフェード/黄縦ワイプに非ず）
//   mode:
//     push      = 1.14→1.0 スケールスルー＋わずかなスライド
//     slide     = ±画面外→0 の水平スライド（from で向き指定）
//     zoompunch = 1.35→1.0 の高速パンチイン
//     whip      = 高速水平移動が0にスナップ（ウィップパン）＋重いブラー
//   すべて spring でeased＋減衰ブラー(blur 16→0px, 最初の~9f)。
//   whip は Trail も併用して残像を強調。deterministic(useCurrentFrame)。
// =====================================================================

type Mode = 'push' | 'slide' | 'zoompunch' | 'whip';
type From = 'left' | 'right';

export const ForcefulCut: React.FC<{
  mode: Mode;
  from?: From;
  children: React.ReactNode;
}> = ({mode, from = 'left', children}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const dir = from === 'left' ? -1 : 1;

  // 入場スプリング（約10-12フレームで収束する強めの設定）
  const s = spring({
    frame,
    fps,
    config: {damping: 15, mass: 0.7, stiffness: 200},
    durationInFrames: 12,
  });

  // 減衰ブラー：16→0px を最初の ~9 フレームで
  const blurPx = interpolate(frame, [0, 9], [16, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  let transform = '';
  let useTrail = false;

  if (mode === 'push') {
    const scale = interpolate(s, [0, 1], [1.14, 1]);
    const tx = interpolate(s, [0, 1], [dir * 120, 0]);
    transform = `translateX(${tx}px) scale(${scale})`;
  } else if (mode === 'slide') {
    const tx = interpolate(s, [0, 1], [dir * width, 0]);
    transform = `translateX(${tx}px)`;
  } else if (mode === 'zoompunch') {
    const scale = interpolate(s, [0, 1], [1.35, 1]);
    transform = `scale(${scale})`;
  } else {
    // whip: 画面幅×1.15 の高速水平移動が0にスナップ
    const tx = interpolate(s, [0, 1], [dir * width * 1.15, 0]);
    transform = `translateX(${tx}px)`;
    useTrail = true;
  }

  const content = (
    <AbsoluteFill
      style={{
        transform,
        filter: blurPx > 0.05 ? `blur(${blurPx}px)` : undefined,
        willChange: 'transform, filter',
      }}
    >
      {children}
    </AbsoluteFill>
  );

  // whip は入場中だけ Trail を巻いて残像を強調（収束後は素の描画）
  if (useTrail && s < 0.995) {
    return (
      <AbsoluteFill>
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          {content}
        </Trail>
      </AbsoluteFill>
    );
  }

  return <AbsoluteFill>{content}</AbsoluteFill>;
};
