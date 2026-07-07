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
import {mulberry32, easeOutCubic, money} from './util';

// =====================================================================
// EquityTheftTally（★ヒーロー・全米 home equity theft の規模と集積）
//   L1 @remotion/three 化の 2D コンパニオン / Blender L3 ヒーロー未着地時のフォールバック。
//   入力: $780,000,000+ ＋ "Est. — Pacific Legal Foundation"（T11・CLM-0017）
//   モーション:
//     - 走行カウンタ 0 → 780,000,000（cubic-out・等速禁止）＋ slam で Trail
//     - 全米シルエット内にドット（家喪失1件=発光1粒）がカウンタと同期して連続集積
//   持続キャリア: ドット連続集積 ＋ カウンタ加算 ＋ 地図の微パララックス drift（≥8px）
//   深度レイヤー: 暗グラデ背景 / 大気グロー / 全米シルエット地形 / 集積ドット / 見出し+出典
//   数はPLF "Est." 規模の視覚表現であり事実断定しない（invariant11 / §2.2#3 注記）。
// =====================================================================

const {ink, navy, electric, silver, gold, white} = BRAND.color;

const TARGET = 780_000_000; // $780M+（CLM-0017・Est.）
const DOTS = 520; // 視覚密度（"8,000+粒" は Blender hero 側・2D は密度表現）
const SEED = 0x71e3a1;

// 全米シルエット（抽象・低ポリ・地理的厳密さは問わない＝invariant11 の生成抽象表現）
const US_PATH =
  'M118 250 L150 190 L250 150 L360 140 L520 120 L700 108 L1020 96 L1300 104 ' +
  'L1520 122 L1660 150 L1740 176 L1770 214 L1748 246 L1700 250 L1660 244 ' +
  'L1620 262 L1600 300 L1560 322 L1520 316 L1470 344 L1420 360 L1360 380 ' +
  'L1280 372 L1180 392 L1060 400 L940 396 L820 404 L700 392 L560 380 ' +
  'L440 356 L340 330 L250 316 L180 300 L140 284 Z';

export const EquityTheftTally: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // ドット配置（決定論・地図bbox内をシード散布→clipPath でシルエットに切抜き）
  const rnd = mulberry32(SEED);
  const dots = React.useMemo(() => {
    const out: {x: number; y: number; r: number; t: number}[] = [];
    for (let i = 0; i < DOTS; i++) {
      out.push({
        x: 120 + rnd() * 1650,
        y: 110 + rnd() * 300,
        r: 2.2 + rnd() * 2.8,
        t: rnd(), // 集積順の位相
      });
    }
    return out;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 進行（0..1・cubic-out で加速感・等速線形禁止）
  const run = easeOutCubic(interpolate(frame, [10, dur - 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  }));
  const counted = Math.round(TARGET * run);
  const visibleDots = Math.floor(dots.length * run);

  // slam（後半で加算が跳ねる瞬間）に Trail を効かせる
  const slamF = Math.round(dur * 0.72);
  const slam = spring({frame: frame - slamF, fps, config: {damping: 9, mass: 0.7}});
  const slamPunch = 1 + 0.05 * Math.exp(-Math.pow((frame - slamF) / 6, 2));

  // 地図の持続パララックス drift（≥8px）
  const driftX = Math.sin(frame / 34) * 10;
  const driftY = Math.cos(frame / 41) * 6;

  const headline = money(TARGET) + '+';

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 100% at 50% 42%, ${navy} 0%, ${ink} 82%)`,
        overflow: 'hidden',
      }}
    >
      {/* 大気グロー（screen ベッド・単独モーション源にしない） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 40% at 50% 46%, ${electric}22 0%, transparent 70%)`,
          mixBlendMode: 'screen',
          transform: `translate(${driftX * 0.4}px, ${driftY * 0.4}px)`,
        }}
      />

      {/* 全米シルエット地形 ＋ 集積ドット */}
      <AbsoluteFill style={{transform: `translate(${driftX}px, ${driftY}px)`}}>
        <svg
          viewBox="0 0 1920 540"
          width="100%"
          height="100%"
          style={{position: 'absolute', top: '18%', left: 0, overflow: 'visible'}}
        >
          <defs>
            <clipPath id="usclip">
              <path d={US_PATH} />
            </clipPath>
            <linearGradient id="usfill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor={navy} stopOpacity="0.85" />
              <stop offset="1" stopColor={ink} stopOpacity="0.9" />
            </linearGradient>
          </defs>
          {/* 地形本体 */}
          <path d={US_PATH} fill="url(#usfill)" stroke={electric} strokeOpacity="0.5" strokeWidth={2.5} />
          {/* 集積ドット（clip でシルエット内のみ） */}
          <g clipPath="url(#usclip)">
            {dots.map((d, i) => {
              if (i >= visibleDots) return null;
              // 各ドットの pop（直近で出現したものほど強い発光＝連続集積の生気）
              const age = (visibleDots - i) / Math.max(1, dots.length);
              const pop = spring({
                frame: frame - Math.round((i / dots.length) * (dur - 30)) - 10,
                fps,
                config: {damping: 12, mass: 0.5},
              });
              const glow = interpolate(age, [0, 0.12], [1, 0.42], {extrapolateRight: 'clamp'});
              return (
                <circle
                  key={i}
                  cx={d.x}
                  cy={d.y}
                  r={d.r * pop}
                  fill={gold}
                  opacity={0.35 + glow * 0.6}
                  style={{filter: `drop-shadow(0 0 ${4 + glow * 8}px ${gold})`}}
                />
              );
            })}
          </g>
        </svg>
      </AbsoluteFill>

      {/* 走行カウンタ（見出し）＋ slam で Trail 残像 */}
      <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', paddingTop: '7%'}}>
        <Trail layers={6} lagInFrames={0.35} trailOpacity={0.5}>
          <div
            style={{
              fontFamily: BRAND.font.display,
              fontSize: 128,
              letterSpacing: 2,
              color: white,
              textShadow: `0 0 24px ${electric}, 0 6px 18px #000`,
              transform: `scale(${slamPunch})`,
              lineHeight: 1,
            }}
          >
            {headline}
          </div>
        </Trail>
        <div
          style={{
            marginTop: 14,
            fontFamily: BRAND.font.body,
            fontSize: 30,
            letterSpacing: 4,
            color: silver,
            textTransform: 'uppercase',
            opacity: interpolate(frame, [6, 26], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            transform: `translateY(${interpolate(frame, [6, 26], [16, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}px)`,
          }}
        >
          Home equity taken nationwide
        </div>
        {/* 現在集計（連続加算＝紙芝居フリーズ根絶） */}
        <div
          style={{
            marginTop: 6,
            fontFamily: BRAND.font.display,
            fontSize: 44,
            color: gold,
            opacity: 0.9,
            transform: `translateY(${(1 - slam) * 4}px)`,
            textShadow: `0 0 12px ${gold}88`,
          }}
        >
          {money(counted)}
        </div>
      </AbsoluteFill>

      {/* 出典チップ（下部・CLM-0017 Est.） */}
      <div
        style={{
          position: 'absolute',
          bottom: 42,
          left: '50%',
          transform: 'translateX(-50%)',
          fontFamily: BRAND.font.body,
          fontSize: 22,
          letterSpacing: 2,
          color: silver,
          opacity: 0.75,
          border: `1px solid ${silver}44`,
          borderRadius: 4,
          padding: '6px 16px',
        }}
      >
        Est. — Pacific Legal Foundation
      </div>
    </AbsoluteFill>
  );
};
