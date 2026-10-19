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
// BrightLine — 暗いグラウンドプレーンを走る発光エレクトリックブルーの継ぎ目。
//   左三分の一に CAR シルエット / 右三分の一に HOUSE シルエット（ベクター）。
//   mode='draw' : 線が L→R に spring で描かれ、グローがランプ
//   mode='hold' : 線が居座り、微かに呼吸（イージング付き・静止禁止）
//   mode='slam' : 線が上からハードに落ちて overshoot spring で着地。
//                 Trail のモーションブラー残像 + 減衰する白フラッシュ。
//                 「the Court said NO」ペイオフ。
//   深度レイヤー: 暗グラデ背景 / パースグリッド地平 / シルエット / グロー継ぎ目。
//   全モーション spring / Easing.out(cubic)。opacity 単独禁止（scale/translate 併用）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const {ink, navy, electric, silver, white} = BRAND.color;

type BrightLineMode = 'draw' | 'hold' | 'slam';

// 左三分の一の CAR シルエット（横向き・単純ベクター）
const CarSilhouette: React.FC<{color: string; opacity: number}> = ({
  color,
  opacity,
}) => (
  <svg
    viewBox="0 0 400 160"
    width={400}
    height={160}
    style={{overflow: 'visible', opacity}}
  >
    <path
      d="M18 118
         C18 108 30 104 44 104
         L96 104
         C112 76 150 60 200 60
         C252 60 292 76 312 104
         L360 108
         C378 110 384 116 384 126
         L384 132 L18 132 Z"
      fill={color}
    />
    <circle cx={118} cy={132} r={26} fill={color} />
    <circle cx={300} cy={132} r={26} fill={color} />
    <circle cx={118} cy={132} r={12} fill={navy} />
    <circle cx={300} cy={132} r={12} fill={navy} />
  </svg>
);

// 右三分の一の HOUSE シルエット（単純ベクター）
const HouseSilhouette: React.FC<{color: string; opacity: number}> = ({
  color,
  opacity,
}) => (
  <svg
    viewBox="0 0 320 220"
    width={320}
    height={220}
    style={{overflow: 'visible', opacity}}
  >
    <path
      d="M160 12 L308 116 L280 116 L280 200 L40 200 L40 116 L12 116 Z"
      fill={color}
    />
    <rect x={132} y={140} width={56} height={60} fill={navy} />
    <rect x={70} y={128} width={40} height={40} fill={navy} />
    <rect x={210} y={128} width={40} height={40} fill={navy} />
  </svg>
);

export const BrightLine: React.FC<{mode?: BrightLineMode; dur?: number}> = ({
  mode = 'draw',
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const seamY = Math.round(height * 0.6);
  const seamThickness = 4;

  // ---- モード別の継ぎ目パラメータ ----
  // drawP: 線の横方向の描き込み割合 (0→1)
  // dropY: 上からの落下量(px, 0 で着地)
  // glow : グロー強度 (0→1)
  // breath: 呼吸スケール(縦厚み/明滅の乗数)
  let drawP = 1;
  let dropY = 0;
  let glow = 1;
  let breath = 1;
  let flash = 0;

  if (mode === 'draw') {
    const s = spring({
      frame: frame - sec(fps, 0.15),
      fps,
      config: {damping: 26, mass: 1},
    });
    drawP = interpolate(s, [0, 1], [0, 1]);
    glow = interpolate(s, [0, 1], [0.15, 1]);
    // 着地後わずかに呼吸を継続（静止禁止）
    breath =
      1 +
      0.06 *
        Math.sin(frame / (fps * 0.9)) *
        interpolate(s, [0.7, 1], [0, 1], {extrapolateLeft: 'clamp'});
  } else if (mode === 'hold') {
    drawP = 1;
    // ゆっくりした呼吸: スケールと明滅を sin で（イージング内包）
    const b = Math.sin(frame / (fps * 1.1));
    breath = 1 + 0.09 * b;
    glow = 0.72 + 0.28 * ((b + 1) / 2);
  } else {
    // slam: 上から一気に落ちて overshoot 着地
    const s = spring({
      frame: frame - sec(fps, 0.1),
      fps,
      config: {damping: 9, mass: 1.1, stiffness: 200},
    });
    dropY = interpolate(s, [0, 1], [-seamY * 0.9, 0]);
    glow = interpolate(s, [0, 0.4, 1], [0.1, 0.6, 1], {
      extrapolateRight: 'clamp',
    });
    // 着地インパクトの白フラッシュ（減衰）
    const impact = sec(fps, 0.42);
    flash = interpolate(frame, [impact, impact + sec(fps, 0.5)], [0.9, 0], {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    breath = 1;
  }

  // 全体のシーンイン/アウト（微 translateY 併用で opacity 単独回避）
  const sceneIn = spring({frame, fps, config: {damping: 200, mass: 0.6}});
  const sceneOut = interpolate(
    frame,
    [total - sec(fps, 0.5), total],
    [1, 0],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp'},
  );
  const sceneOpacity = interpolate(sceneIn, [0, 1], [0, 1]) * sceneOut;
  const sceneY = interpolate(sceneIn, [0, 1], [24, 0]);

  const coreColor = electric;
  const seamWidth = width * 0.92 * drawP;
  const seamLeft = (width - width * 0.92) / 2;

  // グラウンドプレーンのパース・ドリフト（イージング付き横流し）
  const gridDrift = interpolate(frame, [0, total], [0, 60], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- リビール後に効く持続的二次モーション（settle後にランプイン・全編凍結禁止）----
  // sustain: リビール完了後に 0→1 へ（イージング）。以降ずっと大振幅の動きを載せる。
  const sustain = interpolate(frame, [sec(fps, 1.3), sec(fps, 2.0)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // 全体パララックス（正弦＝イージング内包・往復）: 画面幅/高さの約±1.4% / ±1.2%
  const groupX =
    sustain * Math.sin((frame / fps) * ((2 * Math.PI) / 6.2)) * (width * 0.014);
  const groupY =
    sustain *
    Math.sin((frame / fps) * ((2 * Math.PI) / 4.8) + 1.1) *
    (height * 0.012);
  // ゆっくりしたスケール呼吸 1.00↔1.02（上方向のみ＝背景ギャップ無し）
  const groupScale =
    1 +
    sustain *
      0.02 *
      (0.5 + 0.5 * Math.sin((frame / fps) * ((2 * Math.PI) / 5.4)));
  const groupTransform = `translate(${groupX}px, ${groupY}px) scale(${groupScale})`;
  // 継ぎ目を往復する走行グリント（0..1・正弦ping-pong＝イージング・常時移動）
  const glintPos = 0.5 + 0.5 * Math.sin((frame / fps) * ((2 * Math.PI) / 2.6) - Math.PI / 2);

  // 継ぎ目本体（core + bloom）。scaleY で呼吸 / slam の落下は translateY。
  const Seam: React.FC = () => (
    <div
      style={{
        position: 'absolute',
        left: seamLeft,
        top: seamY,
        width: seamWidth,
        height: seamThickness,
        transform: `translateY(${dropY}px) scaleY(${breath})`,
        transformOrigin: 'center',
      }}
    >
      {/* 広いブルーム */}
      <div
        style={{
          position: 'absolute',
          inset: `${-40}px 0`,
          background: `radial-gradient(60% 100% at 50% 50%, ${electric}${Math.round(
            glow * 90,
          )
            .toString(16)
            .padStart(2, '0')} 0%, transparent 70%)`,
          filter: 'blur(14px)',
        }}
      />
      {/* コアライン */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(90deg, transparent 0%, ${coreColor} 8%, ${white} 50%, ${coreColor} 92%, transparent 100%)`,
          borderRadius: seamThickness,
          boxShadow: `0 0 ${18 * glow}px ${electric}, 0 0 ${
            48 * glow
          }px ${electric}aa, 0 0 ${90 * glow}px ${electric}66`,
          opacity: 0.4 + 0.6 * glow,
        }}
      />
      {/* 継ぎ目上に立つ縦グロー（地面反射感） */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: seamThickness,
          height: 120,
          background: `linear-gradient(180deg, ${electric}${Math.round(
            glow * 55,
          )
            .toString(16)
            .padStart(2, '0')} 0%, transparent 100%)`,
          filter: 'blur(8px)',
        }}
      />
      {/* 継ぎ目を往復する走行グリント（リビール後も止まらない持続モーション） */}
      <div
        style={{
          position: 'absolute',
          left: `calc(${(glintPos * 100).toFixed(3)}% - 46px)`,
          top: -20,
          width: 92,
          height: seamThickness + 40,
          background: `radial-gradient(50% 50% at 50% 50%, ${white} 0%, ${electric}88 34%, transparent 72%)`,
          opacity: 0.6 * glow,
          filter: 'blur(3px)',
          mixBlendMode: 'screen',
          pointerEvents: 'none',
        }}
      />
    </div>
  );

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(125% 105% at 50% 42%, ${navy} 0%, #06080f 82%)`,
        opacity: sceneOpacity,
        transform: `translateY(${sceneY}px)`,
      }}
    >
      {/* 持続的二次モーション群（settle後にパララックス＋スケール呼吸） */}
      <AbsoluteFill style={{transform: groupTransform}}>
      {/* Layer 2: パースグリッド地平（グラウンドプレーン） */}
      <AbsoluteFill
        style={{
          top: seamY,
          opacity: 0.16,
          transform: `translateX(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(90deg, ${silver}33 0px, ${silver}33 1px, transparent 1px, transparent 120px),
            repeating-linear-gradient(0deg, ${silver}22 0px, ${silver}22 1px, transparent 1px, transparent 70px)`,
          maskImage:
            'linear-gradient(180deg, black 0%, transparent 60%), radial-gradient(120% 100% at 50% 0%, black 40%, transparent 85%)',
          WebkitMaskImage:
            'linear-gradient(180deg, black 0%, transparent 60%), radial-gradient(120% 100% at 50% 0%, black 40%, transparent 85%)',
          maskComposite: 'intersect',
          WebkitMaskComposite: 'source-in',
        }}
      />

      {/* Layer 3a: CAR シルエット（左三分の一） */}
      <div
        style={{
          position: 'absolute',
          left: width / 6 - 200,
          top: seamY - 132 + dropY * 0.12,
        }}
      >
        <CarSilhouette color={ink} opacity={0.9} />
      </div>

      {/* Layer 3b: HOUSE シルエット（右三分の一） */}
      <div
        style={{
          position: 'absolute',
          left: (width * 5) / 6 - 160,
          top: seamY - 200 + dropY * 0.12,
        }}
      >
        <HouseSilhouette color={ink} opacity={0.9} />
      </div>

      {/* Layer 4: 発光継ぎ目。slam は Trail で残像 */}
      {mode === 'slam' ? (
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          <Seam />
        </Trail>
      ) : (
        <Seam />
      )}

      {/* Layer 5: 白フラッシュ（slam のインパクト・減衰） */}
      {flash > 0 && (
        <AbsoluteFill
          style={{
            background: `radial-gradient(80% 60% at 50% ${
              (seamY / height) * 100
            }%, ${white} 0%, transparent 60%)`,
            opacity: flash,
            mixBlendMode: 'screen',
            pointerEvents: 'none',
          }}
        />
      )}
      </AbsoluteFill>

      {/* ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 45%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
