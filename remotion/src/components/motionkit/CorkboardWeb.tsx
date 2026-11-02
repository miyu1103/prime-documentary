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
// CorkboardWeb — 探偵の「陰謀ボード」風モーション部品
//   写真/メモカードが node 座標(0..1)へ、わずかな傾き＋ピンで
//   オーバーシュート・スプリングで落ちて刺さる（スタッガー）。
//   ラベルは overflow:hidden の切れ上がりマスクで出現。
//   その後、赤い糸がリンク間を strokeDashoffset スプリングで描かれ、
//   ゆるいカテナリー(たるみ)＋着弾時のピンと張る微振動をもつ。
//   微細に漂うダスト＋ビネット。全モーションにイージング/スプリング、
//   opacity 単独の演出なし、決定論的（useCurrentFrame+index+random）。
//   色は BRAND トークンのみ（糸だけ抑えた赤 #C0473E を許可）。
// =====================================================================

// 糸の色（唯一許可された非トークンのリテラル）
const STRING = '#C0473E';

// カード寸法
const CARD_W = 236;
const CARD_H = 172;

// 秒→フレーム（fps 基準・フレーム直書き禁止）
const secF = (fps: number, s: number) => Math.round(fps * s);

// カード落下の開始（i番目）
const cardInFrame = (fps: number, i: number) =>
  secF(fps, 0.18) + i * secF(fps, 0.14);

export const CorkboardWeb: React.FC<{
  nodes: {x: number; y: number; label?: string}[];
  links: [number, number][];
  dur?: number;
}> = ({nodes, links, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width: W, height: H, durationInFrames} = useVideoConfig();
  const DUR = dur ?? durationInFrames;

  // 背景グロー/グリッドのゆっくりドリフト（全編 DUR に渡って動き続ける）
  const glowDrift = interpolate(frame, [0, DUR], [-26, 26], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });
  const gridDrift = interpolate(frame, [0, DUR], [0, 46], {
    easing: Easing.inOut(Easing.sin),
    extrapolateRight: 'clamp',
  });

  // ピン位置（カード上端中央）= 糸の結び目
  const pinAt = (n: {x: number; y: number}) => ({
    x: n.x * W,
    y: n.y * H - CARD_H / 2,
  });

  // 全カード着地のおおよそ後に糸を描き始める
  const stringsBase =
    cardInFrame(fps, Math.max(0, nodes.length - 1)) + secF(fps, 0.62);

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {/* --- L0: SCENE backdrop（指定リテラル） --- */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* --- L1: アクセント・グロー（漂う深度光） --- */}
      <AbsoluteFill
        style={{
          transform: `translate(${glowDrift}px, ${glowDrift * -0.4}px)`,
          background: `radial-gradient(48% 42% at 38% 30%, ${BRAND.color.electric}26 0%, transparent 60%),
            radial-gradient(46% 40% at 72% 74%, ${BRAND.color.gold}12 0%, transparent 62%)`,
        }}
      />

      {/* --- L2: 微グリッド（証拠ボードの目地）＋マスク --- */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.silver}55 0px, ${BRAND.color.silver}55 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${BRAND.color.silver}55 0px, ${BRAND.color.silver}55 1px, transparent 1px, transparent 76px)`,
          maskImage:
            'radial-gradient(120% 90% at 50% 46%, black 26%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 46%, black 26%, transparent 84%)',
        }}
      />

      {/* --- L3: カード（写真/メモが刺さる） --- */}
      {nodes.map((n, i) => {
        const cx = n.x * W;
        const cy = n.y * H;
        const start = cardInFrame(fps, i);
        // オーバーシュート・スプリング（ピンで刺さる手応え）
        const s = spring({
          frame: frame - start,
          fps,
          config: {damping: 11, mass: 0.85, stiffness: 135},
        });
        // 上から落下
        const dropY = interpolate(s, [0, 1], [-680, 0]);
        const scale = interpolate(s, [0, 1], [0.9, 1]);
        // translate と併用（opacity 単独禁止）— マスク的な立ち上がり
        const appear = interpolate(s, [0, 0.16], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        // 最終傾き（決定論的ランダム）＋落下時の余分な振れが収まる
        const tiltFinal = interpolate(random(`tilt-${i}`), [0, 1], [-6.5, 6.5]);
        const swing = interpolate(
          s,
          [0, 1],
          [random(`swing-${i}`) > 0.5 ? 16 : -16, 0],
        );
        // 着地後の極小アイドル揺れ（完全静止を避ける）
        const settled = interpolate(s, [0.55, 1], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const idle =
          Math.sin(((frame - start) / fps) * 1.5 + i * 1.7) * 0.7 * settled;
        const rot = tiltFinal + swing + idle;
        // 着地でカードの落影が育つ（深度）
        const sh = interpolate(s, [0, 1], [2, 26], {extrapolateLeft: 'clamp'});

        // ラベル切れ上がり（overflow:hidden マスク・カード着地後）
        const labelS = spring({
          frame: frame - start - secF(fps, 0.18),
          fps,
          config: {damping: 15, mass: 0.8},
        });
        const labelY = interpolate(labelS, [0, 1], [108, 0]);
        const label = (n.label ?? `EXHIBIT ${String(i + 1).padStart(2, '0')}`)
          .toUpperCase();
        const tag = String(i + 1).padStart(2, '0');

        return (
          <Trail key={`card-${i}`} layers={5} lagInFrames={1.1} trailOpacity={0.42}>
            <AbsoluteFill>
              <div
                style={{
                  position: 'absolute',
                  left: cx,
                  top: cy,
                  width: CARD_W,
                  height: CARD_H,
                  marginLeft: -CARD_W / 2,
                  marginTop: -CARD_H / 2,
                  transformOrigin: '50% 0%',
                  transform: `translateY(${dropY}px) rotate(${rot}deg) scale(${scale})`,
                  opacity: appear,
                }}
              >
                {/* ピン（金の頭＋電光リング＋針） */}
                <div
                  style={{
                    position: 'absolute',
                    top: -9,
                    left: '50%',
                    marginLeft: -9,
                    width: 18,
                    height: 18,
                    borderRadius: '50%',
                    background: `radial-gradient(circle at 34% 30%, ${BRAND.color.white} 0%, ${BRAND.color.gold} 45%, #8a6a18 100%)`,
                    boxShadow: `0 0 10px ${BRAND.color.gold}88, 0 4px 6px rgba(0,0,0,0.5)`,
                    border: `1px solid ${BRAND.color.electric}55`,
                    zIndex: 3,
                  }}
                />
                {/* カード本体（暗いシネマ調・銀の縁） */}
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    borderRadius: 6,
                    background: BRAND.color.navy,
                    border: `1px solid ${BRAND.color.silver}3a`,
                    padding: 9,
                    boxShadow: `0 ${sh}px ${sh * 1.7}px rgba(0,0,0,0.55)`,
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 8,
                    overflow: 'hidden',
                  }}
                >
                  {/* 写真面（被写体は伏せた抽象・実在肖像なし） */}
                  <div
                    style={{
                      position: 'relative',
                      flex: 1,
                      borderRadius: 3,
                      overflow: 'hidden',
                      background: `linear-gradient(158deg, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 100%)`,
                      border: `1px solid ${BRAND.color.ink}`,
                    }}
                  >
                    {/* スポットライト（伏せた被写体の示唆） */}
                    <div
                      style={{
                        position: 'absolute',
                        inset: 0,
                        background: `radial-gradient(60% 55% at 50% 36%, ${BRAND.color.silver}30 0%, transparent 62%)`,
                      }}
                    />
                    {/* 走査線（微細ディテール） */}
                    <div
                      style={{
                        position: 'absolute',
                        inset: 0,
                        opacity: 0.22,
                        backgroundImage: `repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 5px)`,
                      }}
                    />
                    {/* 黒塗り（redaction）バー */}
                    <div
                      style={{
                        position: 'absolute',
                        left: '16%',
                        right: '30%',
                        top: '62%',
                        height: 9,
                        background: `${BRAND.color.silver}2a`,
                        borderRadius: 2,
                      }}
                    />
                    <div
                      style={{
                        position: 'absolute',
                        left: '16%',
                        right: '50%',
                        top: '78%',
                        height: 7,
                        background: `${BRAND.color.silver}20`,
                        borderRadius: 2,
                      }}
                    />
                    {/* 証拠番号タグ */}
                    <div
                      style={{
                        position: 'absolute',
                        top: 6,
                        right: 6,
                        padding: '1px 6px',
                        borderRadius: 2,
                        background: BRAND.color.gold,
                        color: BRAND.color.ink,
                        fontFamily: BRAND.font.display,
                        fontSize: 13,
                        letterSpacing: 0.5,
                        lineHeight: 1.3,
                      }}
                    >
                      {tag}
                    </div>
                  </div>
                  {/* ラベル帯（切れ上がりマスク） */}
                  <div
                    style={{
                      height: 22,
                      overflow: 'hidden',
                      borderTop: `1px solid ${BRAND.color.silver}26`,
                      paddingTop: 3,
                    }}
                  >
                    <div
                      style={{
                        transform: `translateY(${labelY}%)`,
                        fontFamily: BRAND.font.body,
                        fontWeight: 700,
                        fontSize: 13,
                        letterSpacing: 1.4,
                        color: BRAND.color.white,
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {label}
                    </div>
                  </div>
                </div>
              </div>
            </AbsoluteFill>
          </Trail>
        );
      })}

      {/* --- L4: 赤い糸（描画＋たるみ＋着弾振動） --- */}
      <AbsoluteFill>
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          <defs>
            <filter id="cw-str-glow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="3.5" />
            </filter>
          </defs>
          {links.map(([a, b], li) => {
            const na = nodes[a];
            const nb = nodes[b];
            if (!na || !nb) return null;
            const pa = pinAt(na);
            const pb = pinAt(nb);
            const dist = Math.hypot(pb.x - pa.x, pb.y - pa.y);

            const lStart = stringsBase + li * secF(fps, 0.12);
            const draw = spring({
              frame: frame - lStart,
              fps,
              config: {damping: 17, mass: 0.9, stiffness: 120},
            });
            const p = interpolate(draw, [0, 1], [0, 1]);

            // 着弾（描き切り）付近からの減衰振動＝ピンと張る余韻
            const landF = lStart + secF(fps, 0.42);
            const tv = (frame - landF) / fps;
            const drawn = interpolate(draw, [0.72, 1], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const vib =
              tv > 0
                ? Math.sin(tv * 2 * Math.PI * 6) * Math.exp(-tv * 6) * 11 * drawn
                : 0;

            // カテナリー（たるみ）＋振動
            const baseSag = 24 + dist * 0.11;
            const sag = baseSag + vib;
            const mx = (pa.x + pb.x) / 2;
            const my = (pa.y + pb.y) / 2 + sag;
            const d = `M ${pa.x} ${pa.y} Q ${mx} ${my} ${pb.x} ${pb.y}`;

            // 2次ベジェ長の近似（弦と制御網の平均）
            const c1 = Math.hypot(mx - pa.x, my - pa.y);
            const c2 = Math.hypot(pb.x - mx, pb.y - my);
            const len = (dist + c1 + c2) / 2;
            const off = len * (1 - p);

            // 結び目（糸の端が張れてから現れる）
            const knot = interpolate(draw, [0.2, 0.55], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            const knotEnd = interpolate(draw, [0.85, 1], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });

            return (
              <g key={`link-${li}`}>
                {/* グロー下地 */}
                <path
                  d={d}
                  fill="none"
                  stroke={STRING}
                  strokeWidth={5}
                  strokeLinecap="round"
                  opacity={0.32 * drawn + 0.12 * p}
                  strokeDasharray={len}
                  strokeDashoffset={off}
                  filter="url(#cw-str-glow)"
                />
                {/* 芯線 */}
                <path
                  d={d}
                  fill="none"
                  stroke={STRING}
                  strokeWidth={2.2}
                  strokeLinecap="round"
                  strokeDasharray={len}
                  strokeDashoffset={off}
                />
                {/* 端の結び目 */}
                <circle cx={pa.x} cy={pa.y} r={4.5 * knot} fill={STRING} />
                <circle cx={pb.x} cy={pb.y} r={4.5 * knotEnd} fill={STRING} />
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>

      {/* --- L5: 漂うダスト（常時ドリフト＝完全静止しない） --- */}
      <AbsoluteFill style={{pointerEvents: 'none'}}>
        {Array.from({length: 28}).map((_, i) => {
          const bx = random(`dx-${i}`);
          const by = random(`dy-${i}`);
          const size = interpolate(random(`ds-${i}`), [0, 1], [1.5, 4]);
          const speed = interpolate(random(`dv-${i}`), [0, 1], [4, 13]);
          // ゆっくり上昇＋横サイン揺れ（画面内をラップ）
          const yRaw = by * H - frame * (speed / fps) * 6;
          const y = ((yRaw % (H + 80)) + (H + 80)) % (H + 80) - 40;
          const x =
            bx * W + Math.sin((frame / fps) * (speed / 8) + i * 1.9) * 26;
          const o = interpolate(random(`do-${i}`), [0, 1], [0.05, 0.2]);
          return (
            <div
              key={`dust-${i}`}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: size,
                height: size,
                borderRadius: '50%',
                background: BRAND.color.silver,
                opacity: o,
                filter: 'blur(0.5px)',
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* --- L6: ビネット（最前面の締め） --- */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.68) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
