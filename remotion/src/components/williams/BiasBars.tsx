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
// EP36 williams — BiasBars (code-built motion-graphic · SCENE)
//   NIST(2019)の「偽陽性が一部の顔で桁違いに高い」を honest に可視化。
//   ★事実規律: 捏造した精度%を一切出さない。claim に無い数値は表示しない。
//   画面に焼く数値は grade-A のみ = 「10–100×」「NIST · 2019」だけ（CLM-0005）。
//   2本のバーは "白人の顔" 基準1 に対し "黒人・アジア系の顔" が桁違い長い、という
//   比率のみを見せる（軸の絶対値は出さない）。反証（アジア製で差が消える=学習データ）は
//   ナレ担当・ここは中立な差分表示に徹する。
//   規則: 全モーションにイージング/spring・opacity単独無し・マスク切れ上がり文字・
//   速い伸長に Trail・裏≥3レイヤー・秒はfpsから算出。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const MaskLabel: React.FC<{
  text: string;
  reveal: number;
  size: number;
  weight: number;
  color: string;
  ls?: number;
  font?: string;
}> = ({text, reveal, size, weight, color, ls = 1, font = BRAND.font.body}) => {
  const y = interpolate(reveal, [0, 1], [116, 0]);
  const o = interpolate(reveal, [0, 0.28], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.14em'}}>
      <span
        style={{
          display: 'inline-block',
          transform: `translateY(${y}%)`,
          opacity: o,
          fontFamily: font,
          fontWeight: weight,
          fontSize: size,
          letterSpacing: ls,
          color,
          whiteSpace: 'pre',
        }}
      >
        {text}
      </span>
    </span>
  );
};

export const BiasBars: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const groupO = interpolate(frame, [0, sec(fps, 0.3), total - sec(fps, 0.5), total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = Math.sin(frame * 0.05) * 4;

  // バー領域
  const barLeft = width * 0.20;
  const barMaxW = width * 0.58;
  const rowH = 132; // ラベルとバーが重ならないよう行間を確保
  const topBase = height * 0.36;

  // 基準バー（白人の顔＝短い基準）と、桁違いバー（黒人・アジア系＝長い）
  const baseS = spring({frame: frame - sec(fps, 0.5), fps, config: {damping: 20, stiffness: 90}});
  const highS = spring({frame: frame - sec(fps, 0.85), fps, config: {damping: 18, stiffness: 80}});
  const baseW = interpolate(baseS, [0, 1], [0, barMaxW * 0.10]); // 基準=約1（短い）
  const highW = interpolate(highS, [0, 1], [0, barMaxW * 1.0]); // 桁違い（10–100×を長さで示唆）

  // ラベルreveal
  const head = spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 18}});
  const l1 = spring({frame: frame - sec(fps, 0.55), fps, config: {damping: 18}});
  const l2 = spring({frame: frame - sec(fps, 0.9), fps, config: {damping: 18}});
  // 「10–100×」多倍率チップ（バー着地後にスタンプ）
  const mult = spring({frame: frame - sec(fps, 1.5), fps, config: {damping: 11, mass: 0.9}});
  const multScale = interpolate(mult, [0, 1], [1.6, 1]);
  const multO = interpolate(mult, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
  // 引用（NIST · 2019）
  const cite = spring({frame: frame - sec(fps, 1.9), fps, config: {damping: 20}});

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* レイヤー1: グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 100% at 50% 40%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 66%, #05070d 100%)`,
        }}
      />
      {/* レイヤー2: 微グリッド（ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `repeating-linear-gradient(90deg, ${BRAND.color.electric}20 0px, ${BRAND.color.electric}20 1px, transparent 1px, transparent 90px)`,
          maskImage: 'linear-gradient(180deg, transparent, black 30%, black 70%, transparent)',
          WebkitMaskImage: 'linear-gradient(180deg, transparent, black 30%, black 70%, transparent)',
        }}
      />
      {/* レイヤー3: 主役グロー */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: width * 0.7,
            height: height * 0.4,
            background: `radial-gradient(closest-side, ${BRAND.color.gold}18 0%, transparent 72%)`,
            filter: 'blur(28px)',
            opacity: groupO,
          }}
        />
      </AbsoluteFill>

      {/* 見出し */}
      <AbsoluteFill style={{opacity: groupO, transform: `translateY(${drift * 0.4}px)`}}>
        <div style={{position: 'absolute', left: barLeft, top: height * 0.22}}>
          <MaskLabel
            text="FALSE MATCHES BY WHOSE FACE"
            reveal={head}
            size={30}
            weight={900}
            color={BRAND.color.silver}
            ls={5}
            font={BRAND.font.display}
          />
        </div>

        {/* 基準バー（白人の顔）: ラベル top:0 / バー top:46（明示配置で重なり回避） */}
        <div style={{position: 'absolute', left: barLeft, top: topBase, width: barMaxW, height: 84}}>
          <div style={{position: 'absolute', top: 0, left: 0}}>
            <MaskLabel text="WHITE FACES" reveal={l1} size={26} weight={700} color={BRAND.color.silver} ls={2} />
          </div>
          <div
            style={{
              position: 'absolute',
              top: 46,
              left: 0,
              width: baseW,
              height: 30,
              borderRadius: 4,
              background: `linear-gradient(90deg, ${BRAND.color.silver}cc, ${BRAND.color.silver}66)`,
              boxShadow: `0 0 10px ${BRAND.color.silver}33`,
            }}
          />
        </div>

        {/* 桁違いバー（黒人・アジア系の顔）＋ Trail: ラベル top:0 / バー top:46 */}
        <div style={{position: 'absolute', left: barLeft, top: topBase + rowH, width: barMaxW, height: 84}}>
          <div style={{position: 'absolute', top: 0, left: 0}}>
            <MaskLabel text="BLACK & ASIAN FACES" reveal={l2} size={26} weight={700} color={BRAND.color.white} ls={2} />
          </div>
          <div style={{position: 'absolute', top: 46, left: 0, width: barMaxW, height: 30}}>
            <Trail layers={5} lagInFrames={1.2} trailOpacity={0.4}>
              <div
                style={{
                  width: highW,
                  height: 30,
                  borderRadius: 4,
                  background: `linear-gradient(90deg, ${BRAND.color.gold}, ${BRAND.color.gold}88)`,
                  boxShadow: `0 0 18px ${BRAND.color.gold}77`,
                }}
              />
            </Trail>
          </div>
          {/* 多倍率チップ 10–100×（grade-A・唯一の焼き数値） */}
          <div
            style={{
              position: 'absolute',
              left: highW + 22,
              top: 34,
              transform: `scale(${multScale})`,
              opacity: multO,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: 56,
              color: BRAND.color.gold,
              letterSpacing: 1,
              textShadow: `0 0 26px ${BRAND.color.gold}88`,
              whiteSpace: 'nowrap',
            }}
          >
            10–100× MORE
          </div>
        </div>

        {/* 引用（NIST · 2019） */}
        <div
          style={{
            position: 'absolute',
            left: barLeft,
            top: topBase + rowH + 100,
            opacity: interpolate(cite, [0, 1], [0, 0.9]),
            transform: `translateY(${interpolate(cite, [0, 1], [14, 0])}px)`,
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: 22,
            letterSpacing: 3,
            color: BRAND.color.silver,
          }}
        >
          NIST · 2019 · one-to-one false positives
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
