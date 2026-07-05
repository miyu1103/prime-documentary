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
// EvidenceCard — 証拠／展示カードのシネマティックSCENE（MOTIONKIT）
//   ダークな「写真/展示」プレースホルダー枠が、わずかな傾き付きで overshoot
//   spring とモーションブラー Trail でスラムイン → 微振動して着地。
//   ゴールドの角チップ tag（既定 'EXHIBIT A'）がスタンプ的インパクトで
//   スケールイン（overshoot + settle）。枠の下に caption がマスク切り上がり。
//   ペーパークリップ/ピンのアクセントと柔らかいドロップシャドウ。常時わずかに
//   呼吸（紙芝居回避）。実画像は読み込まず抽象的なブループリント充填で表現。
//   フルスクリーンのシーン背景＋≥3階層の奥行き。全モーションにイージング/spring・
//   opacity単独リビール無し・決定論的（useCurrentFrame + index + random）。
// =====================================================================

// 秒→フレーム（fps基準・フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

const DROP = '0 40px 90px rgba(0,0,0,0.62), 0 12px 30px rgba(0,0,0,0.55)';

export const EvidenceCard: React.FC<{
  tag?: string;
  caption?: string;
  dur?: number;
}> = ({tag = 'EXHIBIT A', caption, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- タイムライン（すべて fps 由来）
  const slamStart = sec(fps, 0.08); // カードのスラムイン開始
  const tagStart = sec(fps, 0.46); // タグチップのスタンプ開始
  const capStart = sec(fps, 0.62); // キャプションのマスク切り上がり開始
  const clipStart = sec(fps, 0.34); // ペーパークリップの着地開始
  const outStart = total - sec(fps, 0.5); // シーン退出開始

  // ---- 常時わずかな呼吸（静止しない）
  const breath = Math.sin((frame / fps) * 1.2) * 3;
  const breathRot = Math.sin((frame / fps) * 0.9) * 0.35; // deg
  const bgDrift = interpolate(frame, [0, total], [0, 30], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- シーン全体の出入り（opacity単独禁止 → 微translateYと必ず併用）
  const sceneO = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const sceneY = interpolate(
    frame,
    [0, sec(fps, 0.4), outStart, total],
    [24, 0, 0, 20],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // ---- カードのスラムイン（overshoot spring・傾き→着地）
  const cardS = spring({
    frame: frame - slamStart,
    fps,
    config: {damping: 11, mass: 1.05, stiffness: 150},
  });
  const cardScale = interpolate(cardS, [0, 1], [1.14, 1]);
  const cardY = interpolate(cardS, [0, 1], [-120, 0]);
  const cardRot = interpolate(cardS, [0, 1], [-6.5, -1.6]); // deg：わずかな傾きで着地
  const cardO = interpolate(cardS, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  // 着地直後の微振動（減衰する残響・spring settle を補強）
  const settleFrame = frame - slamStart - sec(fps, 0.34);
  const settle =
    settleFrame > 0
      ? Math.sin(settleFrame * 0.9) * Math.exp(-settleFrame * 0.14) * 1.4
      : 0;

  // ---- タグチップのスタンプ（overshoot → settle）
  const tagS = spring({
    frame: frame - tagStart,
    fps,
    config: {damping: 9, mass: 0.7, stiffness: 210},
  });
  const tagScale = interpolate(tagS, [0, 0.55, 1], [1.5, 0.92, 1]); // 押し込み→着地
  const tagY = interpolate(tagS, [0, 1], [-16, 0]);
  const tagO = interpolate(tagS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // ---- ペーパークリップの着地（spring・上から差し込む）
  const clipS = spring({
    frame: frame - clipStart,
    fps,
    config: {damping: 14, mass: 0.9, stiffness: 160},
  });
  const clipY = interpolate(clipS, [0, 1], [-70, 0]);
  const clipO = interpolate(clipS, [0, 0.35], [0, 1], {extrapolateRight: 'clamp'});

  // ---- キャプションのマスク切り上がり
  const capS = spring({
    frame: frame - capStart,
    fps,
    config: {damping: 18, mass: 0.9, stiffness: 130},
  });
  const capY = interpolate(capS, [0, 1], [118, 0]);
  const capO = interpolate(capS, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  const underlineS = spring({
    frame: frame - capStart - sec(fps, 0.14),
    fps,
    config: {damping: 22, mass: 1, stiffness: 110},
  });
  const underlineX = interpolate(underlineS, [0, 1], [0, 1]);

  // ---- カードの寸法
  const CARD_W = 980;
  const CARD_H = 620;

  // 決定論的な浮遊ダスト（背景の奥行き・常時ドリフト）
  const DUST = 14;

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* Layer 1: フルスクリーン背景グラデ（指定の SCENE backdrop） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 抑えたグリッド＋ビネットマスク（奥行き・ゆっくりドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${bgDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 90px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 90px)`,
          maskImage:
            'radial-gradient(120% 88% at 50% 46%, black 22%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 88% at 50% 46%, black 22%, transparent 80%)',
        }}
      />

      {/* Layer 3: 中央の電光グロー（カード裏の発光・呼吸） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(42% 40% at 50% 46%, ${BRAND.color.electric}22 0%, transparent 70%)`,
          transform: `translateY(${breath * 0.6}px)`,
        }}
      />

      {/* Layer 4: 決定論的な浮遊ダスト（常時ドリフト・静止しない） */}
      <AbsoluteFill style={{opacity: 0.45}}>
        {new Array(DUST).fill(0).map((_, i) => {
          const bx = random('ec-dust-x' + i) * width;
          const by = random('ec-dust-y' + i) * height;
          const size = 1.4 + random('ec-dust-s' + i) * 3;
          const speed = 0.24 + random('ec-dust-v' + i) * 0.5;
          const phase = random('ec-dust-p' + i) * Math.PI * 2;
          const dx = Math.sin((frame / fps) * speed + phase) * 20;
          const dy = Math.cos((frame / fps) * speed * 0.8 + phase) * 15;
          const tw = 0.25 + (Math.sin((frame / fps) * 1.3 + phase) * 0.5 + 0.5) * 0.6;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: bx,
                top: by,
                width: size,
                height: size,
                borderRadius: '50%',
                backgroundColor: BRAND.color.silver,
                opacity: tw,
                transform: `translate(${dx}px, ${dy}px)`,
                boxShadow: `0 0 ${size * 3}px ${BRAND.color.electric}55`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* Layer 5: 証拠カード（スラムイン＋Trail・傾き着地・前景ヒーロー） */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          opacity: sceneO,
          transform: `translateY(${sceneY}px)`,
        }}
      >
        <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
          <div
            style={{
              position: 'relative',
              width: CARD_W,
              height: CARD_H,
              opacity: cardO,
              transform: `translateY(${cardY + breath}px) rotate(${
                cardRot + breathRot + settle
              }deg) scale(${cardScale})`,
              transformOrigin: '50% 50%',
              borderRadius: 10,
              padding: 20,
              background:
                'linear-gradient(160deg, #12203a 0%, #0b1626 60%, #0a1220 100%)',
              border: `1px solid ${BRAND.color.silver}33`,
              boxShadow: DROP,
            }}
          >
            {/* 写真エリア：抽象ブループリント充填のプレースホルダー（実画像なし） */}
            <div
              style={{
                position: 'relative',
                width: '100%',
                height: '100%',
                borderRadius: 5,
                overflow: 'hidden',
                background: `
                  radial-gradient(80% 120% at 26% 18%, ${BRAND.color.electric}2e 0%, transparent 55%),
                  radial-gradient(70% 90% at 82% 88%, ${BRAND.color.navy} 0%, transparent 60%),
                  linear-gradient(140deg, #0e1a2e 0%, #070c16 100%)`,
                border: `1px solid ${BRAND.color.electric}22`,
                boxShadow: 'inset 0 0 120px rgba(0,0,0,0.7)',
              }}
            >
              {/* ブループリントの細グリッド */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  opacity: 0.5,
                  backgroundImage: `
                    repeating-linear-gradient(0deg, ${BRAND.color.electric}1f 0px, ${BRAND.color.electric}1f 1px, transparent 1px, transparent 44px),
                    repeating-linear-gradient(90deg, ${BRAND.color.electric}1f 0px, ${BRAND.color.electric}1f 1px, transparent 1px, transparent 44px)`,
                  maskImage:
                    'radial-gradient(120% 120% at 50% 40%, black 40%, transparent 92%)',
                  WebkitMaskImage:
                    'radial-gradient(120% 120% at 50% 40%, black 40%, transparent 92%)',
                }}
              />
              {/* 抽象的な計測ライン（決定論・わずかにドリフト） */}
              <svg
                width="100%"
                height="100%"
                viewBox="0 0 940 580"
                preserveAspectRatio="none"
                style={{position: 'absolute', inset: 0, opacity: 0.55}}
              >
                {new Array(5).fill(0).map((_, i) => {
                  const y0 = 90 + i * 96;
                  const dphase = random('ec-line' + i) * Math.PI * 2;
                  const dy = Math.sin((frame / fps) * 0.6 + dphase) * 8;
                  return (
                    <line
                      key={i}
                      x1={40}
                      y1={y0 + dy}
                      x2={900}
                      y2={y0 - dy}
                      stroke={BRAND.color.electric}
                      strokeWidth={1.5}
                      strokeDasharray="10 14"
                      opacity={0.4}
                    />
                  );
                })}
                <circle
                  cx={470}
                  cy={290}
                  r={150}
                  fill="none"
                  stroke={BRAND.color.silver}
                  strokeWidth={1.5}
                  strokeDasharray="4 12"
                  opacity={0.35}
                />
                <line
                  x1={470}
                  y1={40}
                  x2={470}
                  y2={540}
                  stroke={BRAND.color.gold}
                  strokeWidth={1.5}
                  opacity={0.28}
                />
              </svg>
              {/* コーナーのレジストレーションマーク（4隅） */}
              {[
                [26, 26, 1, 1],
                [914, 26, -1, 1],
                [26, 554, 1, -1],
                [914, 554, -1, -1],
              ].map(([cx, cy, sx, sy], i) => (
                <svg
                  key={i}
                  width={30}
                  height={30}
                  viewBox="0 0 30 30"
                  style={{
                    position: 'absolute',
                    left: `${((cx as number) / 940) * 100}%`,
                    top: `${((cy as number) / 580) * 100}%`,
                    transform: `translate(-50%, -50%) scale(${sx}, ${sy})`,
                    opacity: 0.6,
                  }}
                >
                  <path
                    d="M2 2 L14 2 M2 2 L2 14"
                    stroke={BRAND.color.silver}
                    strokeWidth={2}
                    fill="none"
                  />
                </svg>
              ))}
              {/* 前面のガラス反射（斜めのハイライト） */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  background:
                    'linear-gradient(120deg, rgba(255,255,255,0.09) 0%, transparent 28%, transparent 72%, rgba(255,255,255,0.04) 100%)',
                  pointerEvents: 'none',
                }}
              />
            </div>

            {/* タグチップ（ゴールド・左上角・スタンプインパクト） */}
            <div
              style={{
                position: 'absolute',
                top: -26,
                left: -22,
                transform: `translateY(${tagY}px) scale(${tagScale}) rotate(-3deg)`,
                opacity: tagO,
                transformOrigin: 'left center',
                padding: '12px 26px',
                borderRadius: 6,
                background: `${BRAND.color.gold}1c`,
                border: `2px solid ${BRAND.color.gold}`,
                color: BRAND.color.gold,
                fontFamily: BRAND.font.display,
                fontWeight: 900,
                fontSize: 34,
                letterSpacing: 5,
                textTransform: 'uppercase',
                whiteSpace: 'nowrap',
                boxShadow: `0 0 26px ${BRAND.color.gold}44, 0 8px 20px rgba(0,0,0,0.5)`,
                textShadow: `0 0 14px ${BRAND.color.gold}55`,
              }}
            >
              {tag}
            </div>

            {/* ペーパークリップのアクセント（右上・上から差し込む） */}
            <svg
              width={64}
              height={140}
              viewBox="0 0 64 140"
              style={{
                position: 'absolute',
                top: -46,
                right: 96,
                transform: `translateY(${clipY}px) rotate(8deg)`,
                opacity: clipO,
                filter: 'drop-shadow(0 6px 10px rgba(0,0,0,0.55))',
              }}
            >
              <path
                d="M32 14 C16 14 16 14 16 40 L16 104 C16 122 48 122 48 104 L48 34 C48 22 30 22 30 34 L30 100"
                fill="none"
                stroke={BRAND.color.silver}
                strokeWidth={7}
                strokeLinecap="round"
              />
            </svg>
          </div>
        </Trail>

        {/* キャプション：枠の下・マスク切り上がり＋ゴールド下線 */}
        {caption !== undefined && caption !== '' && (
          <div
            style={{
              marginTop: 54,
              display: 'inline-block',
              maxWidth: CARD_W,
              transform: `translateY(${breath * 0.5}px)`,
            }}
          >
            <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
              <div
                style={{
                  transform: `translateY(${capY}%)`,
                  opacity: capO,
                  fontFamily: BRAND.font.body,
                  fontWeight: 600,
                  fontSize: 34,
                  lineHeight: 1.28,
                  letterSpacing: 1,
                  textAlign: 'center',
                  color: BRAND.color.white,
                }}
              >
                {caption}
              </div>
            </div>
            {/* 下線：scaleX spring（中央origin）で描画 */}
            <div
              style={{
                marginTop: 18,
                height: 3,
                borderRadius: 2,
                backgroundColor: BRAND.color.gold,
                transform: `scaleX(${underlineX})`,
                transformOrigin: 'center',
                boxShadow: `0 0 16px ${BRAND.color.gold}aa`,
              }}
            />
          </div>
        )}
      </AbsoluteFill>

      {/* Layer 6: シネマティックなビネット（最前面の抑え） */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 52%, rgba(0,0,0,0.56) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
