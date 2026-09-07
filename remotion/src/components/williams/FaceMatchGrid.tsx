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
// EP36 williams — FaceMatchGrid (code-built motion-graphic · SCENE)
//   顔認識ソフトが「候補顔」を並べ、走査し、1枠を "MATCH?" とリングで指すUI再現。
//   実在の顔は描かない（invariant 11）＝匿名の抽象パネル（ぼやけた放射グラデ）だけ。
//   画面に数値・実在UIを焼かない（"SCANNING" / "MATCH?" は概念語）。
//   規則: 全モーションにイージング/spring・opacity単独リビール無し（scale/translate併用）・
//   スタッガー・速い動き(走査線/リング)に Trail・主役の裏に≥3レイヤー・
//   マスク切れ上がり文字・秒はfpsから算出・決定論(frame+index+random)。
//   None-exists in motionkit（タイルグリッドは既存に無い）→ EP36専用新規（invariant 14適合）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const COLS = 6;
const ROWS = 4;
const N = COLS * ROWS;

// 匿名パネルの色調（cyan寄りの冷色を微妙にばらす・実在顔なし）
const panelTone = (i: number): string => {
  const r = random(`tone-${i}`);
  const hue = 205 + Math.round(r * 24); // 205–229（青〜藍）
  const lig = 26 + Math.round(random(`lig-${i}`) * 14);
  return `hsl(${hue} 38% ${lig}%)`;
};

export const FaceMatchGrid: React.FC<{
  /** 0..N-1 の「一致」枠（既定=決定論的に1つ） */
  matchIndex?: number;
  dur?: number;
}> = ({matchIndex, dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const match = matchIndex ?? 13; // 決め打ちの一致枠（3行目・2列目付近）

  // グループ出入り（translateY併用＝opacity単独禁止）
  const groupO = interpolate(frame, [0, sec(fps, 0.3), total - sec(fps, 0.5), total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const groupY = interpolate(frame, [0, sec(fps, 0.5)], [26, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  // 常時わずかにドリフト（紙芝居回避）
  const drift = Math.sin(frame * 0.05) * 5;

  // グリッド領域
  const areaW = width * 0.62;
  const areaH = height * 0.62;
  const left = (width - areaW) / 2;
  const top = (height - areaH) / 2 + 18;
  const gap = 18;
  const cw = (areaW - gap * (COLS - 1)) / COLS;
  const ch = (areaH - gap * (ROWS - 1)) / ROWS;

  // 走査線（上→下を1回・イージング）と、走査完了→リング点灯
  const scanStart = sec(fps, 0.55);
  const scanEnd = sec(fps, 1.9);
  const scanP = interpolate(frame, [scanStart, scanEnd], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const scanY = top - 10 + scanP * (areaH + 20);

  const ring = spring({frame: frame - scanEnd, fps, config: {damping: 12, mass: 0.9}});
  const ringScale = interpolate(ring, [0, 1], [1.5, 1]);
  const ringGlow = interpolate(ring, [0, 1], [0, 1]);
  const ringPulse = 0.7 + 0.3 * Math.sin((frame - scanEnd) * 0.18);

  const matchRow = Math.floor(match / COLS);
  const matchCol = match % COLS;
  const matchX = left + matchCol * (cw + gap);
  const matchY = top + matchRow * (ch + gap);

  // ラベル "MATCH?"（マスク切れ上がり）
  const labReveal = spring({frame: frame - scanEnd - sec(fps, 0.25), fps, config: {damping: 16}});
  const labY = interpolate(labReveal, [0, 1], [110, 0]);
  const labO = interpolate(labReveal, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* レイヤー1: 冷色グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 100% at 50% 42%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 62%, #05070d 100%)`,
        }}
      />
      {/* レイヤー2: データグリッド（ゆっくりドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.16,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 66px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 66px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 90% at 50% 45%, black 30%, transparent 82%)',
        }}
      />
      {/* レイヤー3: cyanグロー */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: areaW * 0.9,
            height: areaH * 0.7,
            background: `radial-gradient(closest-side, ${BRAND.color.electric}33 0%, transparent 72%)`,
            filter: 'blur(30px)',
            opacity: groupO,
          }}
        />
      </AbsoluteFill>

      {/* レイヤー4: 候補パネル群（匿名・スタッガー scale/translate イン） */}
      <AbsoluteFill style={{opacity: groupO, transform: `translateY(${groupY + drift * 0.5}px)`}}>
        {Array.from({length: N}).map((_, i) => {
          const row = Math.floor(i / COLS);
          const col = i % COLS;
          const x = left + col * (cw + gap);
          const y = top + row * (ch + gap);
          const s = spring({
            frame: frame - sec(fps, 0.15) - i * Math.max(1, sec(fps, 0.03)),
            fps,
            config: {damping: 15, mass: 0.8},
          });
          const pScale = interpolate(s, [0, 1], [0.7, 1]);
          const pOp = interpolate(s, [0, 0.4], [0, 1], {extrapolateRight: 'clamp'});
          const isMatch = i === match;
          // 走査線がこのパネル帯を通過した瞬間だけ明滅
          const bandLit = scanY > y - 6 && scanY < y + ch + 6 ? 1 : 0;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: cw,
                height: ch,
                borderRadius: 10,
                background: panelTone(i),
                border: `1px solid ${BRAND.color.electric}${bandLit ? '99' : '33'}`,
                boxShadow: bandLit ? `0 0 22px ${BRAND.color.electric}66` : 'none',
                transform: `scale(${pScale})`,
                opacity: pOp * (isMatch ? 1 : 0.82),
                overflow: 'hidden',
              }}
            >
              {/* 匿名の「顔らしき」抽象放射（実在顔ではない） */}
              <div
                style={{
                  position: 'absolute',
                  left: '50%',
                  top: '46%',
                  width: '58%',
                  height: '70%',
                  transform: 'translate(-50%,-50%)',
                  borderRadius: '50%',
                  background: `radial-gradient(closest-side, ${BRAND.color.silver}22 0%, transparent 70%)`,
                  filter: 'blur(6px)',
                }}
              />
            </div>
          );
        })}
      </AbsoluteFill>

      {/* レイヤー5: 走査線（Trailでモーションブラー） */}
      {scanP > 0 && scanP < 1 ? (
        <Trail layers={5} lagInFrames={1.2} trailOpacity={0.4}>
          <AbsoluteFill style={{opacity: groupO}}>
            <div
              style={{
                position: 'absolute',
                left: left - 12,
                top: scanY,
                width: areaW + 24,
                height: 3,
                background: `linear-gradient(90deg, transparent, ${BRAND.color.electric}, transparent)`,
                boxShadow: `0 0 26px 4px ${BRAND.color.electric}aa`,
              }}
            />
          </AbsoluteFill>
        </Trail>
      ) : null}

      {/* レイヤー6: 一致リング＋"MATCH?"（Trail・spring・パルス） */}
      <Trail layers={4} lagInFrames={1} trailOpacity={0.4}>
        <AbsoluteFill style={{opacity: groupO}}>
          <div
            style={{
              position: 'absolute',
              left: matchX - 8,
              top: matchY - 8,
              width: cw + 16,
              height: ch + 16,
              borderRadius: 14,
              border: `3px solid ${BRAND.color.gold}`,
              boxShadow: `0 0 30px 6px ${BRAND.color.gold}${ringGlow > 0.5 ? 'aa' : '55'}`,
              transform: `scale(${ringScale})`,
              opacity: ringGlow * ringPulse,
            }}
          />
        </AbsoluteFill>
      </Trail>

      <AbsoluteFill style={{opacity: groupO}}>
        <div
          style={{
            position: 'absolute',
            left: matchX,
            top: matchY + ch + 14,
            width: cw,
            textAlign: 'center',
            overflow: 'hidden',
            paddingBottom: '0.14em',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              transform: `translateY(${labY}%)`,
              opacity: labO,
              fontFamily: BRAND.font.display,
              fontWeight: 900,
              fontSize: 34,
              letterSpacing: 4,
              color: BRAND.color.gold,
              textShadow: `0 0 18px ${BRAND.color.gold}66`,
            }}
          >
            MATCH?
          </div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
