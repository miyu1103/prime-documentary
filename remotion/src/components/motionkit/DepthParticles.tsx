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

// =====================================================================
// DepthParticles — 視差(パララックス)の奥行きパーティクル・フィールド。
//   正典のネイビー放射グラデを土台に描き、その上へ粒子を screen 合成で重ねる。
//   粒子は 4 枚の奥行きレイヤに分布：手前ほど大きく・ぼけ・速く動き、
//   奥ほど小さく・シャープ・遅く動く（サイズ/ぼかし/移動レートを depth で変える）。
//   フィールド全体をイーズド正弦の「カメラ」パン＋ドリー(ズーム)で揺らし、
//   レイヤ間で視差の分離が見えるようにする。scale による微かなトゥインクル、
//   ごく少数の電気ブルー/ゴールドの明るい粒子で視線を引く。
//
//   Atmospherics.DustMotes との差別化：あちらは上昇する塵の単層フィールド。
//   本部品は複数深度レイヤの視差＋カメラドリフト（奥行き移動）が主眼。
//
//   すべての動きはイージング付き（等速線形禁止）。乱数は remotion `random`
//   （seed 固定）で決定論的。時間は fps から算出。静止フレームを作らない。
//   ブランド色トークンのみ使用。黄縦スイープ/全面黄ウォッシュ/実在肖像/
//   画面内ロゴは生成しない。
// =====================================================================

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// 出入りエンベロープ（先頭で立ち上げ・終端で畳む、必ずイーズド）。
// 任意の dur で interpolate 入力が単調増加になるようフェード幅を dur から算出。
const envelope = (frame: number, dur: number, fps: number): number => {
  const inN = Math.min(sec(fps, 0.5), Math.max(1, Math.floor(dur / 3)));
  const outN = Math.min(sec(fps, 0.5), Math.max(1, Math.floor(dur / 3)));
  const p1 = inN;
  const p2 = Math.max(p1 + 1, dur - outN);
  return interpolate(frame, [0, p1, p2, dur], [0, 1, 1, 0], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// 奥行きレイヤ定義：depth は 0(最奥・小/鋭/遅) → 1(最手前・大/ぼけ/速)。
// サイズ倍率・ぼかし・視差移動レート・基準opacity を depth に紐付ける。
const LAYERS = [
  {depth: 0.0, sizeMul: 0.55, blur: 0.4, parallax: 0.35, op: 0.34},
  {depth: 0.34, sizeMul: 0.9, blur: 1.1, parallax: 0.62, op: 0.42},
  {depth: 0.67, sizeMul: 1.5, blur: 2.4, parallax: 1.0, op: 0.5},
  {depth: 1.0, sizeMul: 2.4, blur: 4.6, parallax: 1.55, op: 0.42},
] as const;

export const DepthParticles: React.FC<{count?: number; dur?: number}> = ({
  count = 90,
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 全体の柔らかな立ち上げ（先頭のポップ防止）と出入りエンベロープ。
  const appear = spring({frame, fps, config: {damping: 24, mass: 1, stiffness: 74}});
  const env = envelope(frame, total, fps);
  const t = frame / fps; // 秒

  // ---- イーズド「カメラ」ドリフト（全レイヤ共通の基準運動）----------------
  // パン：正弦を位置レンジへ interpolate（本質的にイーズド、周回ゆっくり）。
  // ドリー：正弦をズーム倍率へ interpolate（奥行き感の呼吸）。
  const panX = interpolate(Math.sin(t * 0.13), [-1, 1], [-70, 70], {
    easing: Easing.inOut(Easing.sin),
  });
  const panY = interpolate(Math.cos(t * 0.1 + 0.6), [-1, 1], [-46, 46], {
    easing: Easing.inOut(Easing.sin),
  });
  const dolly = interpolate(Math.sin(t * 0.075 + 1.2), [-1, 1], [0.94, 1.12], {
    easing: Easing.inOut(Easing.sin),
  });

  // レイヤごとに粒子数を配分（手前ほど少なめ＝奥に密度、遠近感を強調）。
  const weights = LAYERS.map((_, li) => 1 + (LAYERS.length - 1 - li) * 0.5);
  const wSum = weights.reduce((a, b) => a + b, 0);

  return (
    <AbsoluteFill>
      {/* 土台：正典のネイビー放射グラデ（中心 electric 寄りの淡い持ち上げ→ ink 沈め）。 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(130% 110% at 50% 42%, ${BRAND.color.navy} 0%, ${BRAND.color.navy} 34%, ${BRAND.color.ink} 100%)`,
        }}
      />

      {/* 粒子：screen 合成のオーバーレイ（土台の上に加算的に光る）。 */}
      <AbsoluteFill
        style={{
          mixBlendMode: 'screen',
          pointerEvents: 'none',
          background: 'transparent',
          opacity: appear * env,
        }}
      >
        {LAYERS.map((layer, li) => {
          const layerCount = Math.max(
            1,
            Math.round((count * weights[li]) / wSum),
          );
          // 手前レイヤほど強いモーションブラー（速い動きにブラー）。
          const trailLayers = 2 + li;
          const lag = 0.8 + layer.parallax * 1.1;

          // レイヤ視差オフセット（カメラ運動を parallax レートで拡縮）。
          const lx = panX * layer.parallax;
          const ly = panY * layer.parallax;
          // ドリーはレイヤごとに中心から拡大（手前ほど強く動く）。
          const scaleZ = 1 + (dolly - 1) * (0.5 + layer.parallax * 0.7);

          return (
            <AbsoluteFill
              key={li}
              style={{
                transform: `translate(${lx}px, ${ly}px) scale(${scaleZ})`,
                transformOrigin: '50% 46%',
                willChange: 'transform',
              }}
            >
              <Trail layers={trailLayers} lagInFrames={lag} trailOpacity={0.45}>
                {Array.from({length: layerCount}).map((_, k) => {
                  const i = li * 1000 + k; // レイヤ横断で一意な seed 基底
                  // 決定論的パラメータ（seed 固定・Math.random/Date 不使用）。
                  const rx = random('dp-x' + i); // 横位置 0..1
                  const ry = random('dp-y' + i); // 縦位置 0..1
                  const rs = random('dp-size' + i); // サイズ抽選
                  const rd = random('dp-drift' + i); // 自走ドリフト量
                  const rp = random('dp-phase' + i); // 位相
                  const rt = random('dp-twk' + i); // トゥインクル位相
                  const rc = random('dp-color' + i); // 色抽選
                  const rw = random('dp-wander' + i); // 個別横揺れ位相

                  // ベースサイズ（depth 倍率込み）。手前ほど大きい。
                  const baseSize = (2.4 + rs * 4.2) * layer.sizeMul;

                  // 個々の粒子も微小に自走（正弦＝イーズド、カメラ運動と別位相）。
                  // 循環境界で sin=0 のため位相ラップでもポップしない。
                  const driftSpeed = (0.05 + rd * 0.09) * layer.parallax;
                  const cyc = t * driftSpeed + rp;
                  const ph = cyc - Math.floor(cyc);
                  const warp = 0.11 * Math.sin(ph * Math.PI * 2); // 速度可変
                  const selfY = (ph + warp) * 26 - 13; // ±13px 前後
                  const wander =
                    Math.sin(t * (0.5 + layer.parallax * 0.35) + rw * 6.283) *
                    (5 + layer.parallax * 9);

                  const x = rx * (width + 160) - 80 + wander;
                  const y = ry * (height + 160) - 80 + selfY;

                  // トゥインクルは scale で（opacity 単独禁止）。opacity は下限維持。
                  const tw = 0.5 + 0.5 * Math.sin(t * (1.1 + rt * 1.3) + rt * 6.283);
                  const scale = 0.75 + tw * 0.6; // 0.75..1.35
                  const op = layer.op * (0.55 + tw * 0.45);

                  // ごく少数の明るい電気ブルー/ゴールド粒子で視線を引く。
                  const isElectric = rc > 0.9;
                  const isGold = rc > 0.82 && rc <= 0.9;
                  const color = isElectric
                    ? BRAND.color.electric
                    : isGold
                      ? BRAND.color.gold
                      : BRAND.color.silver;
                  const accent = isElectric || isGold;
                  const glowR = baseSize * (accent ? 3.4 : 2.0);
                  const finalOp = accent ? Math.min(1, op + 0.16) : op;

                  return (
                    <div
                      key={k}
                      style={{
                        position: 'absolute',
                        left: x,
                        top: y,
                        width: baseSize,
                        height: baseSize,
                        marginLeft: -baseSize / 2,
                        marginTop: -baseSize / 2,
                        borderRadius: '50%',
                        background: color,
                        opacity: finalOp,
                        transform: `scale(${scale})`,
                        filter: `blur(${layer.blur}px)`,
                        boxShadow: `0 0 ${glowR}px ${color}`,
                      }}
                    />
                  );
                })}
              </Trail>
            </AbsoluteFill>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
