import React from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  random,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// GlitchCut — 短いデジタル・グリッチのトランジション・オーバーレイ。
//   ドキュメンタリーの緊張の一拍（ゲーマー的なミームではない）を狙う、
//   抑制の効いた ULTRA-PREMIUM な演出。実映像/カットの継ぎ目に重ねる。
//
//   構成要素（すべて1本のイーズド・エンベロープ env で駆動、山は中央）:
//     ・RGB スプリット・スライス … electric/gold のクロマ収差バー
//       （brand トークンのみ。赤/シアンは使わず electric×gold で色ズレを表現）
//     ・水平ディスプレイスメント帯 … 決定論的にジッターして横ズレするバンド
//     ・スキャンライン       … 微細な走査線が連続ドリフト（静止しない）
//     ・ink フラッシュ       … 中央付近の一瞬の暗転（シャッター/カットの一拍）
//
//   規約: 透明背景・root pointerEvents:'none'・screen 合成。乱数は remotion
//   `random`（seed 固定・Math.random/Date 不使用）で決定論的。時間は fps 算出。
//   グリッチの「跳ね」は離散で良いが、その振幅は必ずイーズドな env で駆動する
//   （生の等速線形リビールは作らない）。run 中は常に動く（静止フレーム無し）。
//   brand トークン外の色・黄縦スイープ・全面黄ウォッシュ・画面内ロゴ・実在
//   肖像は生成しない。
// =====================================================================

// 秒→フレーム
const sec = (fps: number, s: number): number => Math.round(fps * s);

// brand HEX → rgba（トークン以外の色は生成しない）
const hexToRgba = (hex: string, a: number): string => {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
};

// 帯数（画面を水平にスライスする本数）
const BANDS = 9;

export const GlitchCut: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = Math.max(2, dur ?? durationInFrames);

  const t = frame / fps; // 秒

  // メイン・エンベロープ: 0 → 1 → 0（山は中央 total/2）。三角だが cubic で
  // 立ち上がり/畳みをイーズド化。これがすべてのグリッチ振幅を駆動する。
  const env = interpolate(frame, [0, total * 0.5, total], [0, 1, 0], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ink フラッシュ: 中央やや手前で一瞬だけ暗転する鋭いスパイク（イーズド）。
  const flashN = Math.max(1, sec(fps, 0.09));
  const flashCenter = total * 0.46;
  const flashRaw = interpolate(Math.abs(frame - flashCenter), [0, flashN], [1, 0], {
    easing: Easing.out(Easing.quad),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const flash = flashRaw * flashRaw; // 鋭くする

  // グリッチの離散ステップ（跳ねは離散で良い）。~fps/14 フレームごとに更新。
  const STEP = Math.max(1, Math.round(fps / 14));

  // スキャンラインの連続ドリフト（正弦＝イーズド・常時可動→静止しない）。
  const scanDrift = Math.sin(t * 5.5) * 2.2;
  const scanOpacity = env * 0.5;

  // 1帯ぶんの色ストリップ（データ状の破線バー）を生成するヘルパ。
  const strip = (
    color: string,
    offsetX: number,
    phase: number,
  ): React.CSSProperties => ({
    position: 'absolute',
    inset: 0,
    transform: `translateX(${offsetX}px)`,
    backgroundImage: `repeating-linear-gradient(90deg, ${hexToRgba(
      color,
      0,
    )} 0px, ${hexToRgba(color, 0.5)} 7px, ${hexToRgba(color, 0.5)} 46px, ${hexToRgba(
      color,
      0,
    )} 53px)`,
    backgroundPositionX: `${phase}px`,
  });

  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        background: 'transparent',
        overflow: 'hidden',
      }}
    >
      {/* --- RGB スプリット・スライス + 水平ディスプレイスメント帯 --- */}
      {/* 速い横跳ねに Trail でモーションブラーを付与。screen 合成。 */}
      <Trail layers={3} lagInFrames={1.2} trailOpacity={0.5}>
        <AbsoluteFill style={{mixBlendMode: 'screen'}}>
          {Array.from({length: BANDS}).map((_, i) => {
            const bandTop = (i / BANDS) * height;
            const bandH = height / BANDS + 1; // 継ぎ目を1px重ねる

            // 帯ごとに位相をずらした離散ティック（同時に全部跳ねない）。
            const tick = Math.floor((frame + i * 5) / STEP);
            const seed = i + '-' + tick;

            // この帯がこのティックでグリッチするか（山＝env が高いほど発火しやすい）。
            const active = random('gact-' + seed) < 0.3 + 0.55 * env ? 1 : 0;

            // 横ズレ（離散ジャンプ）: 振幅はイーズドな env で駆動。
            const jr = random('gdx-' + seed) * 2 - 1;
            const dx = jr * (10 + 70 * Math.pow(env, 1.2)) * active;

            // クロマ収差量: active 時に大きく、非 active 時も微小な正弦で常時ゆらぐ
            // （＝静止しない）。electric を右、gold を左へ逆方向オフセット。
            const chroma =
              active * (6 + 22 * env) * (0.45 + random('gch-' + seed) * 0.55) +
              1.4 * Math.sin(t * 6.2 + i);

            // 帯の可視度: env がある限り常に微présence（active でさらに強調）。
            const bandOp = env * (0.22 + 0.5 * active);

            // 破線の位相（帯ごと固定シードで散らす）。
            const phE = random('gphE-' + i) * 120;
            const phG = random('gphG-' + i) * 120;
            const phS = random('gphS-' + i) * 120;

            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: 0,
                  top: bandTop,
                  width: '100%',
                  height: bandH,
                  overflow: 'hidden',
                  opacity: bandOp,
                  transform: `translateX(${dx}px)`,
                  mixBlendMode: 'screen',
                }}
              >
                {/* electric（右へ） / gold（左へ）で色ズレ、silver は中央核 */}
                <div style={strip(BRAND.color.electric, chroma, phE)} />
                <div style={strip(BRAND.color.gold, -chroma, phG)} />
                <div
                  style={{
                    ...strip(BRAND.color.silver, 0, phS),
                    opacity: 0.55,
                  }}
                />
              </div>
            );
          })}
        </AbsoluteFill>
      </Trail>

      {/* --- スキャンライン（微細な走査線が連続ドリフト） --- */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'screen',
          opacity: scanOpacity,
          backgroundImage: `repeating-linear-gradient(0deg, ${hexToRgba(
            BRAND.color.silver,
            0,
          )} 0px, ${hexToRgba(BRAND.color.silver, 0)} 2px, ${hexToRgba(
            BRAND.color.silver,
            0.1,
          )} 3px, ${hexToRgba(BRAND.color.silver, 0)} 4px)`,
          backgroundPositionY: `${scanDrift}px`,
        }}
      />

      {/* --- 中央のクロマ・グロー（緊張の核。ハード線でない放射） --- */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'screen',
          opacity: 0.16 * env,
          background: `radial-gradient(60% 30% at 50% 50%, ${hexToRgba(
            BRAND.color.electric,
            0.5,
          )} 0%, transparent 70%)`,
        }}
      />

      {/* --- ink フラッシュ（一瞬の暗転＝シャッター/カットの一拍） --- */}
      <AbsoluteFill
        style={{
          background: hexToRgba(BRAND.color.ink, 0.5 * flash),
        }}
      />
    </AbsoluteFill>
  );
};
