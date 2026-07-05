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
// YearSweep — ULTRA-PREMIUM「時の経過」シーン
//   巨大な年号が from → to へオドメーター式に転がり（各桁マスク内スライド・
//   spring・速い転がりは Trail でモーションブラー・全体は Easing.out(cubic)）、
//   その下を水平タイムライン軸の目盛が流れ（イージング・ラップ）、
//   年が横切ると era 目盛が発光。label はマスク切れ上がりで出現。
//   最後は to に着地して一呼吸。
// 品質ルール準拠: 全モーションにイージング/spring・opacity単独なし・
//   スタッガー・マスク切れ上がり・tabular-nums・最低3枚の奥行きレイヤー・
//   色は BRAND トークンのみ・決定論的（useCurrentFrame のみ）。
// =====================================================================

const C = BRAND.color;

// 秒→フレーム（fps 由来・フレーム直書き禁止）
const F = (fps: number, s: number) => Math.round(fps * s);

// 転がりの正規化進行（等速禁止・Easing.out(cubic)）。parent と桁で共有。
const yearAt = (
  frame: number,
  total: number,
  from: number,
  to: number,
): number => {
  const start = Math.round(total * 0.05);
  const end = Math.round(total * 0.72);
  const p = interpolate(frame, [start, end], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return from + (to - from) * p;
};

// ---------------------------------------------------------------------
// 奥行き背景（指定グラデ＋ドリフトするグリッド＋主役グロー＋ビネット）= 4層
// ---------------------------------------------------------------------
const SceneBackdrop: React.FC<{year: number; from: number}> = ({year, from}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  // 決してフルに静止しない: ゆっくり呼吸するドリフト
  const breathe = interpolate(
    Math.sin((frame / fps) * Math.PI * 0.55),
    [-1, 1],
    [-18, 18],
  );
  // 年に連動する低速パララックス（イージングされた year 由来 → 非等速）
  const gap = 96;
  const parallax = -(((year - from) * 26) % gap) + breathe * 0.5;
  const glowPulse = interpolate(
    Math.sin((frame / fps) * Math.PI * 0.8),
    [-1, 1],
    [0.5, 0.72],
  );
  const drift = interpolate(frame, [0, durationInFrames], [0, 26], {
    easing: Easing.inOut(Easing.sin),
  });
  return (
    <>
      {/* 1: 指定シーン背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${C.navy} 0%, #06080f 82%)`,
        }}
      />
      {/* 2: 流れる縦グリッド（奥・低速パララックス） */}
      <AbsoluteFill
        style={{
          opacity: 0.16,
          transform: `translate3d(${parallax}px, ${drift * 0.4}px, 0)`,
          backgroundImage: `repeating-linear-gradient(90deg, ${C.electric}2b 0px, ${C.electric}2b 1px, transparent 1px, transparent ${gap}px)`,
          maskImage:
            'linear-gradient(90deg, transparent 0%, black 22%, black 78%, transparent 100%)',
          WebkitMaskImage:
            'linear-gradient(90deg, transparent 0%, black 22%, black 78%, transparent 100%)',
        }}
      />
      {/* 3: 主役の裏グロー */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 40% at 50% 40%, ${C.electric}3a 0%, transparent 62%)`,
          opacity: glowPulse,
          transform: `translateY(${breathe * 0.3}px)`,
        }}
      />
      {/* 4: ビネット */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(130% 105% at 50% 44%, transparent 46%, ${C.ink}bb 100%)`,
        }}
      />
    </>
  );
};

// ---------------------------------------------------------------------
// 桁ホイール（2桁スタック・frac で連続転がり・マスク内スライド）＋登場スタッガー
// ---------------------------------------------------------------------
const DigitColumn: React.FC<{
  pos: number;
  size: number;
  slotH: number;
  colW: number;
  enterFrame: number;
  fps: number;
}> = ({pos, size, slotH, colW, enterFrame, fps}) => {
  const whole = Math.floor(pos);
  const frac = pos - whole;
  const cur = ((whole % 10) + 10) % 10;
  const nxt = ((((whole + 1) % 10) + 10) % 10) as number;

  // 登場: 下からマスク切れ上がり（translateY と opacity を必ず併用）
  const enter = spring({frame: enterFrame, fps, config: {damping: 17, mass: 1}});
  const enterY = interpolate(enter, [0, 1], [slotH * 1.15, 0]);
  const enterO = interpolate(enter, [0, 0.35], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const glyph: React.CSSProperties = {
    height: slotH,
    width: colW,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: BRAND.font.display,
    fontSize: size,
    lineHeight: 1,
    color: C.white,
    fontVariantNumeric: 'tabular-nums',
    fontFeatureSettings: '"tnum" 1',
    letterSpacing: -2,
    textShadow: `0 0 34px ${C.electric}66, 0 6px 26px ${C.ink}88`,
  };

  return (
    <div style={{width: colW, height: slotH, overflow: 'hidden'}}>
      {/* 登場マスクの中身 */}
      <div style={{transform: `translateY(${enterY}px)`, opacity: enterO}}>
        {/* 転がり: cur→nxt を frac で連続スライド */}
        <div style={{transform: `translateY(${-frac * slotH}px)`}}>
          <div style={glyph}>{cur}</div>
          <div style={glyph}>{nxt}</div>
        </div>
      </div>
    </div>
  );
};

// 巨大年号（Trail の内側で useCurrentFrame を読む → 速い転がりに実モーションブラー）
const YearNumber: React.FC<{
  from: number;
  to: number;
  total: number;
  digitCount: number;
  size: number;
}> = ({from, to, total, digitCount, size}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const year = yearAt(frame, total, from, to);
  const slotH = Math.round(size * 1.06);
  const colW = Math.round(size * 0.58);

  const cols: React.ReactElement[] = [];
  for (let i = 0; i < digitCount; i++) {
    const place = Math.pow(10, digitCount - 1 - i);
    cols.push(
      <DigitColumn
        key={i}
        pos={year / place}
        size={size}
        slotH={slotH}
        colW={colW}
        enterFrame={frame - F(fps, 0.06) - i * F(fps, 0.05)}
        fps={fps}
      />,
    );
  }

  return (
    <div style={{display: 'flex', alignItems: 'flex-end', gap: 2}}>{cols}</div>
  );
};

// ---------------------------------------------------------------------
// 水平タイムライン軸: 固定プレイヘッドの前を目盛が流れる（year がイージング済み）
// era（10年）目盛は年が横切ると発光。端は spatial マスクでフェード。
// ---------------------------------------------------------------------
const TimeAxis: React.FC<{
  year: number;
  width: number;
  axisY: number;
}> = ({year, width, axisY}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const centerX = width / 2;
  const pxPerYear = 148;
  const span = Math.ceil(width / 2 / pxPerYear) + 3;
  const lo = Math.floor(year) - span;
  const hi = Math.ceil(year) + span;

  // プレイヘッドの微パルス（sin＝非等速・静止させない）
  const pulse = interpolate(
    Math.sin((frame / fps) * Math.PI * 1.4),
    [-1, 1],
    [0.86, 1.06],
  );

  const ticks: React.ReactElement[] = [];
  for (let ty = lo; ty <= hi; ty++) {
    const x = centerX + (ty - year) * pxPerYear;
    const isEra = ty % 10 === 0;
    const d = Math.abs(ty - year);
    // 横切りフレア（year==ty でピーク・イージングされた year 由来）
    const flare = interpolate(d, [0, 0.5, 1.4], [1, 0.4, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    if (isEra) {
      const h = interpolate(flare, [0, 1], [56, 104]);
      ticks.push(
        <g key={ty}>
          <line
            x1={x}
            y1={axisY - h}
            x2={x}
            y2={axisY}
            stroke={C.gold}
            strokeWidth={interpolate(flare, [0, 1], [2.4, 4])}
            style={{
              filter: `drop-shadow(0 0 ${interpolate(
                flare,
                [0, 1],
                [4, 22],
              )}px ${C.gold})`,
            }}
          />
          <circle
            cx={x}
            cy={axisY - h}
            r={interpolate(flare, [0, 1], [3.5, 8])}
            fill={C.gold}
          />
          <text
            x={x}
            y={axisY + 44}
            fill={C.silver}
            fontFamily={BRAND.font.body}
            fontWeight={700}
            fontSize={interpolate(flare, [0, 1], [26, 34])}
            textAnchor="middle"
            style={{
              fontVariantNumeric: 'tabular-nums',
              letterSpacing: 2,
              transform: `translateY(${interpolate(flare, [0, 1], [8, 0])}px)`,
              opacity: interpolate(d, [0, span * 0.7, span], [1, 0.55, 0], {
                extrapolateRight: 'clamp',
              }),
            }}
          >
            {ty}
          </text>
        </g>,
      );
    } else {
      ticks.push(
        <line
          key={ty}
          x1={x}
          y1={axisY - interpolate(flare, [0, 1], [22, 40])}
          x2={x}
          y2={axisY}
          stroke={C.silver}
          strokeWidth={1.5}
          opacity={0.42 + flare * 0.35}
        />,
      );
    }
  }

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        maskImage:
          'linear-gradient(90deg, transparent 0%, black 16%, black 84%, transparent 100%)',
        WebkitMaskImage:
          'linear-gradient(90deg, transparent 0%, black 16%, black 84%, transparent 100%)',
      }}
    >
      <svg
        width={width}
        height={1080}
        style={{position: 'absolute', inset: 0}}
      >
        {/* 軸ベースライン */}
        <line
          x1={0}
          y1={axisY}
          x2={width}
          y2={axisY}
          stroke={C.silver}
          strokeWidth={2}
          opacity={0.35}
        />
        {ticks}
        {/* 固定プレイヘッド（現在＝画面中央） */}
        <g
          style={{
            transform: `translateX(${centerX}px) scaleY(${pulse})`,
            transformOrigin: `${centerX}px ${axisY}px`,
          }}
          opacity={0.95}
        >
          <line
            x1={0}
            y1={axisY - 132}
            x2={0}
            y2={axisY + 14}
            stroke={C.electric}
            strokeWidth={3}
            style={{filter: `drop-shadow(0 0 16px ${C.electric})`}}
          />
          <polygon
            points={`0,${axisY - 150} -12,${axisY - 132} 12,${axisY - 132}`}
            fill={C.electric}
          />
        </g>
      </svg>
    </div>
  );
};

// マスク切れ上がりの見出し（1文字スタッガー・BRAND.font.body）
const MaskLabel: React.FC<{
  text: string;
  startFrame: number;
  fps: number;
  size: number;
}> = ({text, startFrame, fps, size}) => {
  const chars = Array.from(text);
  const st = Math.max(1, F(fps, 0.028));
  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        fontFamily: BRAND.font.body,
        fontWeight: 600,
        fontSize: size,
        letterSpacing: 8,
        textTransform: 'uppercase',
        color: C.silver,
      }}
    >
      {chars.map((ch, i) => {
        const cs = spring({
          frame: startFrame - i * st,
          fps,
          config: {damping: 16, mass: 1},
        });
        const y = interpolate(cs, [0, 1], [118, 0]);
        const o = interpolate(cs, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'});
        return (
          <span
            key={i}
            style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.14em'}}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${y}%)`,
                opacity: o,
                whiteSpace: 'pre',
              }}
            >
              {ch}
            </span>
          </span>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------------
// 本体
// ---------------------------------------------------------------------
export const YearSweep: React.FC<{
  from: number;
  to: number;
  label?: string;
  dur?: number;
}> = ({from, to, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const digitCount = Math.max(
    String(Math.abs(Math.floor(from))).length,
    String(Math.abs(Math.floor(to))).length,
  );
  const year = yearAt(frame, total, from, to);
  const size = 300;
  const numberCenterY = height * 0.4;
  const axisY = height * 0.72;

  // 進行（アンダーライン・着地判定に使用。year 由来＝イージング済み）
  const span = to - from;
  const prog = span === 0 ? 1 : (year - from) / span;

  // 着地の一呼吸（roll 終了で spring・その後は微小な呼吸で静止させない）
  const rollEnd = Math.round(total * 0.72);
  const settle = spring({
    frame: frame - rollEnd,
    fps,
    config: {damping: 12, mass: 0.9, stiffness: 130},
  });
  const settleScale = interpolate(settle, [0, 1], [1.055, 1]);
  const breathe = interpolate(
    Math.sin((frame / fps) * Math.PI * 0.9),
    [-1, 1],
    [0.996, 1.004],
  );
  const heroScale = settleScale * breathe;

  // 全体の入り（微 translateY・opacity と併用＝opacity単独禁止）
  const intro = spring({frame, fps, config: {damping: 20, mass: 1}});
  const introY = interpolate(intro, [0, 1], [26, 0]);
  const introO = interpolate(intro, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});

  // アンダーラインの金アクセント（横方向のみ・縦スイープ/全面ウォッシュ禁止）
  const barMax = size * digitCount * 0.42;
  const barW = interpolate(prog, [0, 1], [0, barMax], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      <SceneBackdrop year={year} from={from} />

      <AbsoluteFill style={{opacity: introO, transform: `translateY(${introY}px)`}}>
        {/* 見出し（マスク切れ上がり） */}
        {label ? (
          <div
            style={{
              position: 'absolute',
              top: numberCenterY - size * 0.62,
              left: 0,
              right: 0,
            }}
          >
            <MaskLabel text={label} startFrame={frame - F(fps, 0.35)} fps={fps} size={30} />
          </div>
        ) : null}

        {/* 巨大年号（Trail で速い転がりにモーションブラー・着地で呼吸） */}
        <div
          style={{
            position: 'absolute',
            top: numberCenterY,
            left: 0,
            right: 0,
            display: 'flex',
            justifyContent: 'center',
            transform: `scale(${heroScale})`,
            transformOrigin: '50% 40%',
          }}
        >
          <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
            <YearNumber
              from={from}
              to={to}
              total={total}
              digitCount={digitCount}
              size={size}
            />
          </Trail>
        </div>

        {/* 年号下の金アンダーライン（横伸長のみ） */}
        <div
          style={{
            position: 'absolute',
            top: numberCenterY + size * 0.62,
            left: '50%',
            transform: 'translateX(-50%)',
            width: barW,
            height: 6,
            borderRadius: 4,
            backgroundColor: C.gold,
            boxShadow: `0 0 26px ${C.gold}aa`,
          }}
        />

        {/* 流れるタイムライン軸＋era フレア */}
        <TimeAxis year={year} width={width} axisY={axisY} />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
