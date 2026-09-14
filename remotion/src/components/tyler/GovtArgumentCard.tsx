import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';
import {mulberry32} from './util';

// =====================================================================
// GovtArgumentCard（★ヒーロー・郡の最強論が崩れる感情ペイオフ）
//   L3 Cycles rigid-body 破断シムの 2D コンパニオン / hero 未着地時フォールバック。
//   入力: 郡の余剰保持正当化論（OL4・CLM-0006 関連。逐語引用でなく論旨要約ラベル）
//   モーション:
//     mode='stack'   : 積層カードが下から spring で組上がり、微 push で呼吸（等速禁止）
//     mode='collapse': 13:20 構造破断。各カードが破片へ分裂し、Trail + overshoot で飛散、
//                      全体 zoompunch。以後は崩壊粒子ドリフト + 残響振動が持続。
//   深度レイヤー: 暗背景 / 光柱ベッド / 積層カード（破片） / 粉塵パーティクル / 見出し
//   全モーション spring / cubic。opacity 単独禁止（scale/translate/rotate 併用）。
// =====================================================================

const {ink, navy, electric, silver, gold, white} = BRAND.color;

type Mode = 'stack' | 'collapse';

// 郡の主張（論旨要約・逐語でない・画面テキストは図データとして許容）
const CLAIMS = ['THE DEBT WAS OWED', 'THE STATUTE ALLOWED THE SALE', 'TITLE PASSED TO THE COUNTY', 'THE SURPLUS WAS FORFEIT'];

const SHARDS = 5; // 各カードの破片数
const SEED = 0x0c0113;

export const GovtArgumentCard: React.FC<{dur: number; mode?: Mode}> = ({dur, mode = 'collapse'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const collapseF = mode === 'collapse' ? Math.round(dur * 0.5) : dur + 999;
  // 崩壊進行（0..1・cubic-out）
  const col = interpolate(frame, [collapseF, collapseF + 26], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const colEased = 1 - Math.pow(1 - col, 3);

  // zoompunch（崩壊着火の瞬間だけ全体を寄せる）
  const punch = 1 + 0.06 * Math.exp(-Math.pow((frame - collapseF) / 5, 2));

  // 残響振動（崩壊後の持続・減衰）
  const ring = col > 0 ? Math.sin(frame / 3) * 3 * Math.exp(-(frame - collapseF) / 30) : 0;

  const rnd = mulberry32(SEED);
  // 破片ごとの飛散ベクトル（決定論）
  const shardVecs = React.useMemo(() => {
    const r = mulberry32(SEED + 7);
    return CLAIMS.map(() =>
      Array.from({length: SHARDS}, () => ({
        dx: (r() - 0.5) * 900,
        dy: -120 - r() * 520,
        rot: (r() - 0.5) * 140,
        delay: r() * 6,
      }))
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 粉塵（崩壊後ドリフト・持続キャリア）
  const dust = React.useMemo(
    () => Array.from({length: 46}, () => ({x: rnd(), y: rnd(), r: 1 + rnd() * 2.5, ph: rnd()})),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const cardW = 720;
  const cardH = 116;
  const gap = 20;
  const baseY = 560;

  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${navy} 0%, ${ink} 85%)`, overflow: 'hidden'}}>
      {/* 光柱ベッド（screen・単独モーション源にしない） */}
      <AbsoluteFill
        style={{
          background: `conic-gradient(from 210deg at 50% 20%, transparent, ${electric}18, transparent 40%)`,
          mixBlendMode: 'screen',
          opacity: 0.6,
        }}
      />

      {/* 見出し */}
      <div
        style={{
          position: 'absolute',
          top: 84,
          width: '100%',
          textAlign: 'center',
          fontFamily: BRAND.font.body,
          fontSize: 28,
          letterSpacing: 6,
          textTransform: 'uppercase',
          color: silver,
          opacity: interpolate(frame, [4, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
        }}
      >
        The county&apos;s argument
      </div>

      {/* 積層カード（破片） */}
      <AbsoluteFill style={{transform: `scale(${punch}) translateY(${ring}px)`}}>
        {CLAIMS.map((claim, ci) => {
          // 組上がり（stack）
          const rise = spring({frame: frame - ci * 8 - 8, fps, config: {damping: 16}});
          const y = baseY - ci * (cardH + gap);
          // 組上がり後の微 push 呼吸（持続・等速でない sin）
          const breathe = Math.sin((frame - ci * 5) / 26) * 3;
          const vecs = shardVecs[ci];
          return (
            <div key={ci} style={{position: 'absolute', left: '50%', top: 0}}>
              {vecs.map((v, si) => {
                const shardW = cardW / SHARDS;
                const sx = -cardW / 2 + si * shardW;
                const t = Math.max(0, Math.min(1, (colEased * 30 - v.delay) / 24));
                const te = 1 - Math.pow(1 - t, 2);
                const tx = sx + v.dx * te;
                const ty = y + breathe * (1 - te) + v.dy * te + (te * te) * 260; // 放物: 上昇→落下
                const rot = v.rot * te;
                const op = interpolate(te, [0.6, 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
                const shard = (
                  <div
                    style={{
                      position: 'absolute',
                      left: tx,
                      top: ty,
                      width: shardW - 2,
                      height: cardH,
                      transform: `scale(${rise}) rotate(${rot}deg)`,
                      transformOrigin: 'center',
                      background: `linear-gradient(180deg, ${navy} 0%, ${ink} 100%)`,
                      borderTop: `2px solid ${electric}`,
                      borderBottom: `1px solid ${electric}55`,
                      overflow: 'hidden',
                      opacity: op,
                      boxShadow: `0 6px 24px #000a, inset 0 0 30px ${electric}22`,
                    }}
                  >
                    {/* 破片スライスに対応する文字部分（clip） */}
                    <div
                      style={{
                        position: 'absolute',
                        left: -si * shardW,
                        top: 0,
                        width: cardW,
                        height: cardH,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontFamily: BRAND.font.display,
                        fontSize: 46,
                        letterSpacing: 1,
                        color: te > 0.15 ? silver : white,
                        textShadow: `0 0 14px ${electric}`,
                      }}
                    >
                      {claim}
                    </div>
                  </div>
                );
                // 飛散中の破片には Trail（速い動きのモーションブラー）
                return te > 0.02 ? (
                  <Trail key={si} layers={6} lagInFrames={0.35} trailOpacity={0.5}>
                    {shard}
                  </Trail>
                ) : (
                  <React.Fragment key={si}>{shard}</React.Fragment>
                );
              })}
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 粉塵パーティクル（崩壊後ドリフト・持続キャリア） */}
      {col > 0 && (
        <AbsoluteFill style={{opacity: interpolate(col, [0, 0.3], [0, 0.8], {extrapolateRight: 'clamp'})}}>
          {dust.map((d, i) => {
            const t = (frame - collapseF) / fps;
            const px = (d.x * 1920 + Math.sin((frame + i * 13) / 40) * 30) % 1920;
            const py = d.y * 1080 - t * (20 + d.ph * 40);
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: px,
                  top: py,
                  width: d.r,
                  height: d.r,
                  borderRadius: '50%',
                  background: gold,
                  opacity: 0.4 + d.ph * 0.3,
                  filter: `blur(${0.5 + d.ph}px)`,
                }}
              />
            );
          })}
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
