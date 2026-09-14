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
// HeadlineStack — 報道モンタージュSCENE（MOTIONKIT）
//   新聞クリッピング風のカードが1枚につき見出し1本を太いセリフ体で載せ、
//   左右交互からわずかな傾き＋オーバーシュートspring＋モーションブラー(Trail)で
//   飛び込み、決定論的な散らばり座標/回転でフレーム上に積層/散乱する。
//   最新カードが最前面で拡大し、古いカードは奥へ退いて減光・微ブラー。
//   上部に控えめな kicker "PRESS COVERAGE"、背景に漂うダスト。
//   フルスクリーンのSCENE背景＋≥3階層の奥行き。常時わずかに動く（紙芝居回避）。
//   全モーションにイージング/spring・opacity単独リビール無し・text=マスク切り上がり・
//   決定論的（useCurrentFrame + index + random）。上品な報道モンタージュ（回転新聞の
//   安っぽさは禁止）。
// =====================================================================

// クリッピング見出しの太いセリフ体（house style を踏襲）
const SERIF = "'Georgia', 'Times New Roman', 'Times', serif";

// 秒→フレーム（fps基準・フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

// 汎用の報道タグ（ブランドロゴではない一般的な報道記述子・決定論的に選択）
const TAGS = ['FRONT PAGE', 'EXCLUSIVE', 'THE WIRE', 'NATIONAL', 'BULLETIN', 'REPORT'];

export const HeadlineStack: React.FC<{
  headlines: string[];
  dur?: number;
}> = ({headlines, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const items = headlines.filter((h) => h && h.trim().length > 0);
  const n = items.length;

  // ---- カデンス（すべて fps 由来の定数・カードの飛び込み間隔）
  const inStart = sec(fps, 0.3);
  const outDur = sec(fps, 0.5);
  const tail = sec(fps, 0.7); // 最終カードのホールド確保
  const cadence =
    n > 1
      ? Math.max(
          sec(fps, 0.32),
          Math.min(sec(fps, 0.7), (total - inStart - tail) / n),
        )
      : sec(fps, 0.4);
  const starts = items.map((_, i) => inStart + i * cadence);
  const outStart = total - outDur;

  // ---- シーン全体の出入り（opacity単独禁止 → 微translateYと必ず併用）
  const fieldO = interpolate(
    frame,
    [0, sec(fps, 0.26), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const fieldY = interpolate(
    frame,
    [0, sec(fps, 0.4), outStart, total],
    [26, 0, 0, -22],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // ---- 常時の呼吸ドリフト（静止させない）
  const breath = Math.sin((frame / fps) * 1.05) * 3;
  const bgDrift = interpolate(frame, [0, total], [0, 30], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- kicker "PRESS COVERAGE"（マスク切り上がり＋spring・常駐）
  const ks = spring({
    frame: frame - sec(fps, 0.12),
    fps,
    config: {damping: 16, mass: 0.9, stiffness: 130},
  });
  const kickerY = interpolate(ks, [0, 1], [130, 0]);
  const kickerO = interpolate(ks, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  const kickerUnderline = interpolate(
    spring({frame: frame - sec(fps, 0.3), fps, config: {damping: 22, stiffness: 110}}),
    [0, 1],
    [0, 1],
  );

  // ---- 決定論的な浮遊ダスト（常時ドリフト・静止しない）
  const DUST = 18;

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* 奥行き1: フルスクリーンSCENE背景グラデ（指定値） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* 奥行き2: 抑えたグリッド（うっすら電光・ゆっくりドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          transform: `translateY(${bgDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 90px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 90px)`,
          maskImage:
            'radial-gradient(120% 88% at 50% 46%, black 24%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 88% at 50% 46%, black 24%, transparent 80%)',
        }}
      />

      {/* 奥行き3: 中央の電光グロー（最新カードの裏で発光） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(48% 42% at 50% 50%, ${BRAND.color.electric}22 0%, transparent 70%)`,
          transform: `translateY(${breath * 0.6}px)`,
        }}
      />

      {/* 奥行き4: 決定論的な浮遊ダスト（常時ドリフト） */}
      <AbsoluteFill style={{opacity: 0.5}}>
        {new Array(DUST).fill(0).map((_, i) => {
          const bx = random('hs-dust-x' + i) * width;
          const by = random('hs-dust-y' + i) * height;
          const size = 1.4 + random('hs-dust-s' + i) * 3.1;
          const speed = 0.24 + random('hs-dust-v' + i) * 0.5;
          const phase = random('hs-dust-p' + i) * Math.PI * 2;
          const dx = Math.sin((frame / fps) * speed + phase) * 24;
          const dy = Math.cos((frame / fps) * speed * 0.8 + phase) * 18;
          const tw = 0.22 + (Math.sin((frame / fps) * 1.25 + phase) * 0.5 + 0.5) * 0.6;
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
                boxShadow: `0 0 ${size * 3}px ${BRAND.color.electric}66`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* 前景: 見出しカードのスタック */}
      <AbsoluteFill
        style={{
          opacity: fieldO,
          transform: `translateY(${fieldY + breath}px)`,
        }}
      >
        {items.map((h, i) => {
          const start = starts[i];

          // ---- 飛び込み（左右交互・オーバーシュートspring）
          const fromLeft = i % 2 === 0;
          const e = spring({
            frame: frame - start,
            fps,
            config: {damping: 13, mass: 1, stiffness: 120},
          });
          const enterX =
            interpolate(e, [0, 1], [fromLeft ? -1700 : 1700, 0]);
          const enterO = interpolate(e, [0, 0.3], [0, 1], {
            extrapolateRight: 'clamp',
          });
          const enterScale = interpolate(e, [0, 1], [0.9, 1]);

          // ---- 決定論的な散らばり座標・回転・サイズ・タグ
          const scx = (random('hs-x' + i) - 0.5) * 760;
          const scy = (random('hs-y' + i) - 0.5) * 360;
          const baseRot = (random('hs-r' + i) - 0.5) * 9; // 静止時の傾き（±4.5°）
          const enterRot = interpolate(
            e,
            [0, 1],
            [fromLeft ? -15 : 15, baseRot],
          ); // 飛び込み時に大きく傾いて着地でオーバーシュート
          const cardW = 560 + random('hs-w' + i) * 300; // 560–860
          const tag = TAGS[Math.floor(random('hs-tag' + i) * TAGS.length) % TAGS.length];
          const accent = i % 2 === 0 ? BRAND.color.electric : BRAND.color.gold;

          // ---- 奥行き退避（新しいカードが来るたびに滑らかに奥へ・減光・微ブラー）
          const times: number[] = [start];
          const depths: number[] = [0];
          for (let j = i + 1; j < n; j++) {
            times.push(starts[j]);
            depths.push(j - i);
          }
          const depth =
            times.length > 1
              ? interpolate(frame, times, depths, {
                  easing: Easing.inOut(Easing.cubic),
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                })
              : 0;
          const recedeScale = Math.max(0.6, 1 - depth * 0.07);
          const recedeDim = Math.max(0.3, 1 - depth * 0.16);
          const recedeY = -depth * 12; // 奥へ引きつつわずかに上へ収まる
          const recedeBlur = Math.min(4.2, depth * 0.95);

          // ---- 常時の微回転ブレス（静止しない）
          const cardBreath = Math.sin((frame / fps) * 0.6 + i * 1.3) * 0.5;

          const scale = enterScale * recedeScale;
          const rot = enterRot + cardBreath;
          const tx = scx + enterX;
          const ty = scy + recedeY + breath * (0.4 + (i % 3) * 0.2);

          // ---- 見出し語のマスク切り上がり（overflow:hidden + 内側translateY・スタッガー）
          const words = h.trim().split(/\s+/);
          const wordStart = start + sec(fps, 0.16);
          const wordStagger = Math.max(1, sec(fps, 0.045));
          const headSize = cardW < 680 ? 44 : 50;

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: '50%',
                top: '50%',
                width: cardW,
                zIndex: i,
                opacity: enterO * recedeDim,
                transform: `translate(-50%, -50%) translate(${tx}px, ${ty}px) rotate(${rot}deg) scale(${scale})`,
                transformOrigin: 'center center',
                filter: recedeBlur > 0.05 ? `blur(${recedeBlur}px)` : undefined,
              }}
            >
              {/* 飛び込みの速いエントランスをモーションブラー(Trail)で包む */}
              <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
                <div
                  style={{
                    background: BRAND.color.white,
                    padding: '34px 40px 38px',
                    borderRadius: 4,
                    borderTop: `4px solid ${accent}`,
                    boxShadow: `0 30px 70px rgba(0,0,0,0.55), 0 8px 20px rgba(0,0,0,0.4)`,
                  }}
                >
                  {/* メタ行: 報道タグチップ ＋ 罫線 */}
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 14,
                      marginBottom: 18,
                    }}
                  >
                    <span
                      style={{
                        padding: '4px 12px',
                        background: `${accent}1f`,
                        color: accent,
                        fontFamily: BRAND.font.body,
                        fontWeight: 700,
                        fontSize: 17,
                        letterSpacing: 3,
                        textTransform: 'uppercase',
                        borderRadius: 3,
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {tag}
                    </span>
                    <span
                      style={{
                        flex: 1,
                        height: 2,
                        background: `${BRAND.color.navy}33`,
                        transformOrigin: 'left center',
                        transform: `scaleX(${interpolate(e, [0.15, 1], [0, 1], {
                          extrapolateLeft: 'clamp',
                          extrapolateRight: 'clamp',
                        })})`,
                      }}
                    />
                  </div>

                  {/* 見出し本文: 語ごとのマスク切り上がり（太いセリフ体） */}
                  <div
                    style={{
                      display: 'flex',
                      flexWrap: 'wrap',
                      gap: '0.04em 0.28em',
                      fontFamily: SERIF,
                      fontWeight: 700,
                      fontSize: headSize,
                      lineHeight: 1.12,
                      letterSpacing: 0.1,
                      color: BRAND.color.ink,
                    }}
                  >
                    {words.map((w, wi) => {
                      const ws = spring({
                        frame: frame - wordStart - wi * wordStagger,
                        fps,
                        config: {damping: 18, mass: 0.85, stiffness: 140},
                      });
                      const wy = interpolate(ws, [0, 1], [118, 0]);
                      const wo = interpolate(ws, [0, 0.28], [0, 1], {
                        extrapolateRight: 'clamp',
                      });
                      return (
                        <span
                          key={wi}
                          style={{
                            display: 'inline-block',
                            overflow: 'hidden',
                            paddingBottom: '0.1em',
                            verticalAlign: 'top',
                          }}
                        >
                          <span
                            style={{
                              display: 'inline-block',
                              transform: `translateY(${wy}%)`,
                              opacity: wo,
                              whiteSpace: 'pre',
                            }}
                          >
                            {w}
                          </span>
                        </span>
                      );
                    })}
                  </div>

                  {/* 疑似本文バー（クリッピングの体裁・scaleXで描画） */}
                  <div style={{marginTop: 22, display: 'grid', gap: 9}}>
                    {[0, 1, 2].map((b) => {
                      const bw = 0.62 + random('hs-bar' + i + '-' + b) * 0.34;
                      const bs = interpolate(
                        e,
                        [0.35 + b * 0.12, 0.7 + b * 0.12],
                        [0, 1],
                        {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
                      );
                      return (
                        <span
                          key={b}
                          style={{
                            height: 6,
                            width: `${bw * 100}%`,
                            borderRadius: 3,
                            background: `${BRAND.color.navy}22`,
                            transformOrigin: 'left center',
                            transform: `scaleX(${bs})`,
                          }}
                        />
                      );
                    })}
                  </div>
                </div>
              </Trail>
            </div>
          );
        })}
      </AbsoluteFill>

      {/* 前面: kicker "PRESS COVERAGE"（マスク切り上がり＋ゴールド下線） */}
      <AbsoluteFill
        style={{
          justifyContent: 'flex-start',
          alignItems: 'center',
          paddingTop: 96,
          pointerEvents: 'none',
        }}
      >
        <div style={{display: 'inline-block', textAlign: 'center'}}>
          <div style={{overflow: 'hidden', paddingBottom: '0.12em'}}>
            <div
              style={{
                transform: `translateY(${kickerY}%)`,
                opacity: kickerO,
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 26,
                letterSpacing: 12,
                textTransform: 'uppercase',
                color: BRAND.color.silver,
                whiteSpace: 'nowrap',
              }}
            >
              Press Coverage
            </div>
          </div>
          <div style={{marginTop: 14, height: 3, overflow: 'hidden'}}>
            <div
              style={{
                height: '100%',
                width: '100%',
                background: BRAND.color.gold,
                borderRadius: 2,
                transformOrigin: 'center',
                transform: `scaleX(${kickerUnderline})`,
                boxShadow: `0 0 18px ${BRAND.color.gold}99`,
              }}
            />
          </div>
        </div>
      </AbsoluteFill>

      {/* 前面: シネマティックなビネット（最前面の抑え） */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background:
            'radial-gradient(120% 100% at 50% 48%, transparent 50%, rgba(0,0,0,0.6) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
