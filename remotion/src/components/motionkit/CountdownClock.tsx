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
// CountdownClock — 緊張感のある mm:ss カウントダウン時計
//   ・巨大 tabular-nums 表示。桁が変わるたびにマスク切れ上がりでスライド反転（spring）
//   ・周囲の細いリングが strokeDashoffset で eased に減っていく
//   ・毎秒の鼓動パルス（scale）＋ソフトグロー
//   ・残り約5秒で色が赤へ移行し、鼓動が速い二連打に
//   ・上部に label をマスク切れ上がりで表示
// 品質ルール準拠: 全モーション eased（等速禁止）／opacity単独禁止／
//   テキストはマスク切れ上がり／useCurrentFrame 決定論／背景3層以上／tabular-nums。
// =====================================================================

const URGENT_RED = '#C0473E'; // 最終数秒だけ許可された抑えた赤
const SCENE_BOTTOM = '#06080f';

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// 16進カラーの線形補間（白→赤などの滑らかな移行に使用）
const hexToRgb = (h: string): readonly [number, number, number] => {
  const n = parseInt(h.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
};
const mixColor = (a: string, b: string, t: number): string => {
  const [ar, ag, ab] = hexToRgb(a);
  const [br, bg, bb] = hexToRgb(b);
  const r = Math.round(ar + (br - ar) * t);
  const g = Math.round(ag + (bg - ag) * t);
  const bl = Math.round(ab + (bb - ab) * t);
  return `rgb(${r}, ${g}, ${bl})`;
};

// 残り秒 → "MMSS" の4桁文字列
const fmtMMSS = (total: number): string => {
  const t = Math.max(0, total);
  const m = Math.min(99, Math.floor(t / 60));
  const s = t % 60;
  return String(m).padStart(2, '0') + String(s).padStart(2, '0');
};

// ---------------------------------------------------------------------
// 1桁セル：値が変わった瞬間だけ、旧数字が上へ抜け・新数字が下から
// せり上がる（overflow:hidden のマスク切れ上がり／spring）。
// ---------------------------------------------------------------------
const DigitCell: React.FC<{
  curr: string;
  prev: string;
  changed: boolean;
  startFrame: number;
  color: string;
  size: number;
}> = ({curr, prev, changed, startFrame, color, size}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const s = changed
    ? spring({
        frame: frame - startFrame,
        fps,
        config: {damping: 14, mass: 0.9, stiffness: 170},
      })
    : 1;

  const inY = interpolate(s, [0, 1], [110, 0]); // 新数字：下→定位置
  const outY = interpolate(s, [0, 1], [0, -110]); // 旧数字：定位置→上へ抜け

  const box: React.CSSProperties = {
    position: 'relative',
    display: 'inline-block',
    width: size * 0.62,
    height: size * 1.04,
    overflow: 'hidden',
  };
  const glyph: React.CSSProperties = {
    position: 'absolute',
    inset: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: BRAND.font.display,
    fontVariantNumeric: 'tabular-nums',
    fontFeatureSettings: '"tnum" 1',
    fontSize: size,
    lineHeight: 1,
    color,
  };

  return (
    <span style={box}>
      {changed ? (
        <span style={{...glyph, transform: `translateY(${outY}%)`}}>{prev}</span>
      ) : null}
      <span style={{...glyph, transform: `translateY(${changed ? inY : 0}%)`}}>
        {curr}
      </span>
    </span>
  );
};

// ---------------------------------------------------------------------
// ラベル：1文字ずつスタッガーでマスク切れ上がり（translateYのみ・opacity単独禁止準拠）
// ---------------------------------------------------------------------
const MaskLabel: React.FC<{
  text: string;
  color: string;
  startFrame: number;
  size: number;
}> = ({text, color, startFrame, size}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const chars = Array.from(text);
  const stg = Math.max(1, sec(fps, 0.035));

  return (
    <div
      style={{
        display: 'flex',
        fontFamily: BRAND.font.body,
        fontWeight: 600,
        fontSize: size,
        letterSpacing: 10,
        textTransform: 'uppercase',
        color,
      }}
    >
      {chars.map((ch, i) => {
        const s = spring({
          frame: frame - startFrame - i * stg,
          fps,
          config: {damping: 16, mass: 0.9},
        });
        const y = interpolate(s, [0, 1], [120, 0]);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              paddingBottom: '0.16em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${y}%)`,
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
// メイン
// ---------------------------------------------------------------------
export const CountdownClock: React.FC<{
  from: number;
  label?: string;
  dur?: number;
}> = ({from, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  const D = dur ?? durationInFrames;
  const totalTicks = Math.max(1, Math.round(from));
  const tickLen = D / totalTicks; // 1秒あたりのフレーム数（尺から算出）

  const progress = interpolate(frame, [0, D], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const currentTick = Math.min(totalTicks, Math.floor(frame / tickLen));
  const tickStartFrame = currentTick * tickLen;
  const remaining = Math.max(0, totalTicks - currentTick);
  const prevRemaining = Math.max(0, totalTicks - Math.max(0, currentTick - 1));

  const currStr = fmtMMSS(remaining);
  const prevStr = fmtMMSS(prevRemaining);
  const changed = [0, 1, 2, 3].map(
    (i) => currentTick >= 1 && currStr[i] !== prevStr[i],
  );

  // 連続的な残り秒（色移行を滑らかに）
  const remainingContinuous = Math.max(0, from * (1 - progress));
  const redMix = interpolate(remainingContinuous, [5, 6.5], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const numColor = mixColor(BRAND.color.white, URGENT_RED, redMix);
  const accentGlow = mixColor(BRAND.color.electric, URGENT_RED, redMix);

  // 毎秒の鼓動（tick境界で1回ドン）＋最終5秒は中間にもう一拍（速い二連打）
  const beat = spring({
    frame: frame - tickStartFrame,
    fps,
    config: {damping: 12, mass: 0.6, stiffness: 200},
  });
  const beat2 = spring({
    frame: frame - (tickStartFrame + tickLen * 0.42),
    fps,
    config: {damping: 12, mass: 0.5, stiffness: 220},
  });
  const basePulse = interpolate(beat, [0, 1], [1.055, 1.0]);
  const extraPulse = redMix * interpolate(beat2, [0, 1], [0.05, 0]);
  const clockScale = basePulse + extraPulse;
  const glowPulse = interpolate(beat, [0, 1], [1, 0.32]); // 拍で強→減衰

  // 消耗リング（strokeDashoffset を eased に増やして削る）
  const ringEase = interpolate(frame, [0, D], [0, 1], {
    easing: Easing.inOut(Easing.sin),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 背景の同心リングの微ドリフト（滑らかな正弦：常時わずかに動く）
  const driftY = Math.sin((frame / (fps * 4)) * Math.PI * 2) * 10;

  // レイアウト定数
  const BOX = 720;
  const R = 300;
  const C = 2 * Math.PI * R;
  const dashoffset = C * ringEase;
  const DIGIT = 190;

  // 消耗アークの先端ドット位置（残り分の弧の先頭）
  const headAng = ((-90 + 360 * (1 - ringEase)) * Math.PI) / 180;
  const headX = BOX / 2 + R * Math.cos(headAng);
  const headY = BOX / 2 + R * Math.sin(headAng);
  const headR = interpolate(beat, [0, 1], [11, 7]);

  // コロン：拍で明滅（scale＋opacityを併用＝opacity単独ではない）
  const colonScale = interpolate(beat, [0, 1], [1.1, 0.9]);
  const colonOpacity = interpolate(beat, [0, 1], [1, 0.42]);

  const digitsRow = (
    <div style={{display: 'flex', alignItems: 'center'}}>
      <DigitCell curr={currStr[0]} prev={prevStr[0]} changed={changed[0]} startFrame={tickStartFrame} color={numColor} size={DIGIT} />
      <DigitCell curr={currStr[1]} prev={prevStr[1]} changed={changed[1]} startFrame={tickStartFrame} color={numColor} size={DIGIT} />
      <span
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: DIGIT * 0.34,
          height: DIGIT * 1.04,
          fontFamily: BRAND.font.display,
          fontSize: DIGIT * 0.9,
          lineHeight: 1,
          color: numColor,
          transform: `scale(${colonScale})`,
          opacity: colonOpacity,
        }}
      >
        :
      </span>
      <DigitCell curr={currStr[2]} prev={prevStr[2]} changed={changed[2]} startFrame={tickStartFrame} color={numColor} size={DIGIT} />
      <DigitCell curr={currStr[3]} prev={prevStr[3]} changed={changed[3]} startFrame={tickStartFrame} color={numColor} size={DIGIT} />
    </div>
  );

  return (
    <AbsoluteFill style={{backgroundColor: SCENE_BOTTOM}}>
      {/* Layer 1: 必須シーン背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, ${SCENE_BOTTOM} 82%)`,
        }}
      />

      {/* Layer 2: 同心テンションリング＋微グリッド（微ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.5,
          transform: `translateY(${driftY}px)`,
          backgroundImage: `
            repeating-radial-gradient(circle at 50% 46%, ${BRAND.color.electric}18 0px, ${BRAND.color.electric}18 1px, transparent 1px, transparent 96px),
            repeating-linear-gradient(0deg, ${BRAND.color.silver}0f 0px, ${BRAND.color.silver}0f 1px, transparent 1px, transparent 120px)`,
          maskImage:
            'radial-gradient(70% 60% at 50% 46%, black 20%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(70% 60% at 50% 46%, black 20%, transparent 82%)',
        }}
      />

      {/* Layer 3: アクセント発光（拍で明滅・screen合成） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(36% 36% at 50% 46%, ${accentGlow} 0%, transparent 70%)`,
          opacity: 0.1 + 0.12 * glowPulse,
          mixBlendMode: 'screen',
        }}
      />

      {/* 中央：ラベル＋時計 */}
      <AbsoluteFill
        style={{
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          gap: 10,
        }}
      >
        {label ? (
          <MaskLabel
            text={label}
            color={mixColor(BRAND.color.silver, URGENT_RED, redMix)}
            startFrame={sec(fps, 0.15)}
            size={30}
          />
        ) : null}

        <div
          style={{
            position: 'relative',
            width: BOX,
            height: BOX,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transform: `scale(${clockScale})`,
            filter: `drop-shadow(0 0 ${16 + 30 * glowPulse}px ${accentGlow})`,
          }}
        >
          <svg
            width={BOX}
            height={BOX}
            viewBox={`0 0 ${BOX} ${BOX}`}
            style={{position: 'absolute', inset: 0}}
          >
            {/* トラック（薄い全周） */}
            <circle
              cx={BOX / 2}
              cy={BOX / 2}
              r={R}
              fill="none"
              stroke={BRAND.color.silver}
              strokeOpacity={0.12}
              strokeWidth={2}
            />
            {/* 消耗アーク（上=12時から時計回りに削れる） */}
            <circle
              cx={BOX / 2}
              cy={BOX / 2}
              r={R}
              fill="none"
              stroke={accentGlow}
              strokeWidth={6}
              strokeLinecap="round"
              strokeDasharray={C}
              strokeDashoffset={dashoffset}
              transform={`rotate(-90 ${BOX / 2} ${BOX / 2})`}
              style={{
                filter: `drop-shadow(0 0 ${6 + 12 * glowPulse}px ${accentGlow})`,
              }}
            />
            {/* 先端ドット（拍で脈動） */}
            <circle cx={headX} cy={headY} r={headR + 8} fill={accentGlow} opacity={0.18} />
            <circle cx={headX} cy={headY} r={headR} fill={BRAND.color.white} />
          </svg>

          {/* 桁の高速反転にモーションブラー（Trail） */}
          <Trail layers={5} lagInFrames={1} trailOpacity={0.45}>
            {digitsRow}
          </Trail>
        </div>
      </AbsoluteFill>

      {/* Layer 4: ビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 42%, rgba(0,0,0,0.62) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
