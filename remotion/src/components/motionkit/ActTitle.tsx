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
// ActTitle — 章/幕タイトルカード（MOTIONKIT）
//   小さな kicker チップが spring でスケールイン →
//   大タイトルが overflow:hidden マスクで単語ごとに切り上がり（スタッガー＋Trail）→
//   ゴールドの下線が左から描かれる → 背後に幕番号(index)がうっすらゴースト。
//   クイックイン → 呼吸を伴う短いホールド → クイックアウト。
//   フルスクリーンのシーン背景＋≥3階層の奥行き。常時わずかに動く（紙芝居回避）。
//   全モーションにイージング/spring・opacity単独リビール無し・決定論的。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const DROP = '0 6px 30px rgba(0,0,0,0.8), 0 2px 8px rgba(0,0,0,0.9)';

// 大タイトル1単語の共通字形スタイル（サイズ確定用の透明サイザーと実描画で厳密一致させる）
const WORD: React.CSSProperties = {
  color: BRAND.color.white,
  fontFamily: BRAND.font.display,
  fontWeight: 900,
  fontSize: 124,
  lineHeight: 1.02,
  letterSpacing: -1,
  textTransform: 'uppercase',
  whiteSpace: 'nowrap',
};

export const ActTitle: React.FC<{
  kicker?: string;
  title: string;
  index?: number;
  dur?: number;
}> = ({kicker, title, index, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- グループの出入り（クイックイン／クイックアウト・translateYと併用で非opacity単独）
  const inEnd = sec(fps, 0.42);
  const outStart = total - sec(fps, 0.45);
  const groupO = interpolate(
    frame,
    [0, sec(fps, 0.28), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const groupY = interpolate(
    frame,
    [0, inEnd, outStart, total],
    [34, 0, 0, -30],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- ホールド中の呼吸（静止しない）
  const breath = Math.sin((frame / fps) * 1.5) * 2.2;
  const bgDrift = interpolate(frame, [0, total], [0, 28], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- kicker チップ（spring スケールイン）
  const ks = spring({
    frame: frame - sec(fps, 0.1),
    fps,
    config: {damping: 12, mass: 0.7, stiffness: 170},
  });
  const kickerScale = interpolate(ks, [0, 1], [0.5, 1]);
  const kickerO = interpolate(ks, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});
  const kickerY = interpolate(ks, [0, 1], [22, 0]);

  // ---- ゴールド下線（左から幅が描かれる・spring）
  const us = spring({
    frame: frame - sec(fps, 0.44),
    fps,
    config: {damping: 22, mass: 1, stiffness: 120},
  });
  const underlineScale = interpolate(us, [0, 1], [0, 1]);
  const underlineO = interpolate(us, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // ---- 背後の幕番号ゴースト
  const gs = spring({
    frame: frame - sec(fps, 0.06),
    fps,
    config: {damping: 26, mass: 1.2, stiffness: 90},
  });
  const ghostScale = interpolate(gs, [0, 1], [1.18, 1]);
  // 背景ゴーストは明確に従属：低opacity・小さめ・タイトルの裏に沈める
  const ghostO = interpolate(gs, [0, 0.5], [0, 0.07], {extrapolateRight: 'clamp'});
  const ghostLabel =
    index === undefined ? '' : String(index).padStart(2, '0');

  // ---- タイトル：単語ごとのマスク切り上がり（スタッガー＋わずかなジッタ）
  const words = title.split(' ');
  const wordStagger = sec(fps, 0.08);
  const titleStart = sec(fps, 0.24);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        overflow: 'hidden',
      }}
    >
      {/* 奥行き1: 薄いグリッド（うっすら電光・ゆっくりドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${bgDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 84px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 84px)`,
          maskImage:
            'radial-gradient(120% 90% at 50% 46%, black 24%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 46%, black 24%, transparent 80%)',
        }}
      />

      {/* 奥行き2: 背後の幕番号ゴースト */}
      {ghostLabel !== '' && (
        <AbsoluteFill
          style={{
            justifyContent: 'center',
            alignItems: 'center',
          }}
        >
          <div
            style={{
              transform: `scale(${ghostScale}) translateY(${-40 + breath * 1.6}px)`,
              opacity: ghostO,
              color: BRAND.color.silver,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: 560,
              lineHeight: 0.9,
              letterSpacing: -20,
              fontVariantNumeric: 'tabular-nums',
              userSelect: 'none',
            }}
          >
            {ghostLabel}
          </div>
        </AbsoluteFill>
      )}

      {/* 奥行き3: 中央の電光グロー */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 40% at 50% 50%, ${BRAND.color.electric}22 0%, transparent 70%)`,
          transform: `translateY(${breath * 0.6}px)`,
        }}
      />

      {/* 奥行き4: タイトル直下のダークスクリム（ゴーストを沈めて白タイトルを立たせる可読性コントラスト） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(42% 34% at 50% 50%, ${BRAND.color.ink}d9 0%, ${BRAND.color.ink}82 46%, transparent 74%)`,
          transform: `translateY(${breath * 0.4}px)`,
        }}
      />

      {/* 前景: kicker + タイトル + 下線 */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 160px',
          opacity: groupO,
          transform: `translateY(${groupY + breath}px)`,
        }}
      >
        {/* kicker チップ：内容にだけフィットする小さなピル（inline-flex / fit-content）。
            Trail(=AbsoluteFill)で包むと全幅バーになるため、ここは直接描画で中央に置く。 */}
        {kicker !== undefined && kicker !== '' && (
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              width: 'fit-content',
              maxWidth: '100%',
              transform: `translateY(${kickerY}px) scale(${kickerScale})`,
              opacity: kickerO,
              marginBottom: 40,
              padding: '12px 30px',
              border: `1.5px solid ${BRAND.color.gold}`,
              borderRadius: 999,
              background: `${BRAND.color.gold}24`,
              color: BRAND.color.gold,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 30,
              letterSpacing: 9,
              textTransform: 'uppercase',
              whiteSpace: 'nowrap',
              boxShadow: `0 0 26px ${BRAND.color.gold}44, 0 4px 18px rgba(0,0,0,0.6)`,
            }}
          >
            {kicker}
          </div>
        )}

        {/* タイトル：単語マスク切り上がり */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: '0 26px',
            maxWidth: 1500,
          }}
        >
          {words.map((w, i) => {
            const jitter = random('act-word-' + i) * sec(fps, 0.05);
            const ws = spring({
              frame: frame - titleStart - i * wordStagger - jitter,
              fps,
              config: {damping: 15, mass: 0.9, stiffness: 130},
            });
            const yy = interpolate(ws, [0, 1], [118, 0]);
            const o = interpolate(ws, [0, 0.25], [0, 1], {
              extrapolateRight: 'clamp',
            });
            return (
              <div
                key={i}
                style={{
                  position: 'relative',
                  overflow: 'hidden',
                  paddingBottom: '0.14em',
                }}
              >
                {/* サイズ確定用の透明サイザー：Trailは絶対配置なので、この単語の
                    実寸(幅/行高)を親の箱に与えないと箱が0×0に潰れ左上へ寄る。 */}
                <div aria-hidden style={{...WORD, visibility: 'hidden'}}>
                  {w}
                </div>
                {/* 実描画：Trail(=AbsoluteFill)がこの単語の箱を満たし、マスク切り上がり */}
                <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
                  <div
                    style={{
                      ...WORD,
                      transform: `translateY(${yy}%)`,
                      opacity: o,
                      textShadow: DROP,
                    }}
                  >
                    {w}
                  </div>
                </Trail>
              </div>
            );
          })}
        </div>

        {/* ゴールド下線（左から描画） */}
        <div style={{marginTop: 30, width: 360, overflow: 'hidden'}}>
          <div
            style={{
              height: 5,
              width: '100%',
              transformOrigin: 'left center',
              transform: `scaleX(${underlineScale})`,
              opacity: underlineO,
              borderRadius: 3,
              background: BRAND.color.gold,
              boxShadow: `0 0 22px ${BRAND.color.gold}aa`,
            }}
          />
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
