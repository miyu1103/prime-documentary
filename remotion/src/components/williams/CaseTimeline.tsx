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
// EP36 williams — CaseTimeline (code-built motion-graphic · SCENE)
//   2018→2024 の事件年表。プレイヘッドが左→右へ掃引し、各ノードが順に点灯。
//   ★焼く数値は grade-A のみ: 2018(NYT裏付・年号A) / JANUARY 2020・~30 HRS(CLM-0001) /
//   APRIL 2021(CLM-0008) / JUNE 2024・AUDIT SINCE 2017・COURT 4 YRS(CLM-0009)。
//   規則: 全モーションにイージング/spring・opacity単独無し・スタッガー・
//   速い掃引に Trail・裏≥3レイヤー・マスク切れ上がり文字・秒はfpsから算出・決定論。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

type Node = {year: number; kicker: string; title: string; chips?: string[]};

const NODES: Node[] = [
  {year: 2018, kicker: '2018', title: 'THE THEFT'},
  {year: 2020, kicker: 'JANUARY 2020', title: 'THE ARREST', chips: ['~30 HRS HELD']},
  {year: 2021, kicker: 'APRIL 2021', title: 'THE LAWSUIT'},
  {year: 2024, kicker: 'JUNE 2024', title: 'THE SETTLEMENT', chips: ['AUDIT SINCE 2017', 'COURT 4 YRS']},
];

const Y0 = 2018;
const Y1 = 2024.4; // 右端に少し余白

export const CaseTimeline: React.FC<{dur?: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  const groupO = interpolate(frame, [0, sec(fps, 0.3), total - sec(fps, 0.5), total], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const drift = Math.sin(frame * 0.05) * 4;

  const axisL = width * 0.12;
  const axisR = width * 0.88;
  const axisW = axisR - axisL;
  const axisY = height * 0.52;
  const xOf = (year: number) => axisL + ((year - Y0) / (Y1 - Y0)) * axisW;

  // 軸線の描画（左→右・イージング）
  const axisDraw = interpolate(frame, [sec(fps, 0.3), sec(fps, 1.1)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // プレイヘッド掃引（軸描画後・各ノードで少しタメ）
  const headStart = sec(fps, 1.0);
  const headEnd = total - sec(fps, 1.2);
  const headP = interpolate(frame, [headStart, headEnd], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const headX = axisL + headP * axisW;

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink}}>
      {/* レイヤー1: グラデ背景 */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(120% 100% at 50% 45%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 64%, #05070d 100%)`,
        }}
      />
      {/* レイヤー2: 微グリッド（ドリフト） */}
      <AbsoluteFill
        style={{
          opacity: 0.12,
          transform: `translateY(${drift}px)`,
          backgroundImage: `repeating-linear-gradient(0deg, ${BRAND.color.electric}18 0px, ${BRAND.color.electric}18 1px, transparent 1px, transparent 72px)`,
          maskImage: 'radial-gradient(120% 90% at 50% 52%, black 35%, transparent 82%)',
          WebkitMaskImage: 'radial-gradient(120% 90% at 50% 52%, black 35%, transparent 82%)',
        }}
      />
      {/* レイヤー3: 軸グロー */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: axisW * 1.05,
            height: 160,
            marginTop: (axisY - height / 2) * 2,
            background: `radial-gradient(closest-side, ${BRAND.color.electric}22 0%, transparent 72%)`,
            filter: 'blur(26px)',
            opacity: groupO,
          }}
        />
      </AbsoluteFill>

      {/* 見出し */}
      <AbsoluteFill style={{opacity: groupO}}>
        <div
          style={{
            position: 'absolute',
            left: axisL,
            top: height * 0.2,
            fontFamily: BRAND.font.display,
            fontWeight: 900,
            fontSize: 32,
            letterSpacing: 5,
            color: BRAND.color.silver,
            opacity: interpolate(spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 18}}), [0, 1], [0, 1]),
          }}
        >
          SIX YEARS, ONE FACE
        </div>

        {/* 軸線（左→右描画） */}
        <div
          style={{
            position: 'absolute',
            left: axisL,
            top: axisY,
            width: axisW * axisDraw,
            height: 3,
            background: `linear-gradient(90deg, ${BRAND.color.electric}, ${BRAND.color.silver}88)`,
            boxShadow: `0 0 14px ${BRAND.color.electric}66`,
            transform: `translateY(${drift * 0.3}px)`,
          }}
        />

        {/* プレイヘッド（Trail） */}
        {headP > 0 && headP < 1 ? (
          <Trail layers={5} lagInFrames={1.2} trailOpacity={0.4}>
            <div
              style={{
                position: 'absolute',
                left: headX - 9,
                top: axisY - 9,
                width: 18,
                height: 18,
                marginTop: 1.5,
                borderRadius: 9,
                background: BRAND.color.white,
                boxShadow: `0 0 22px 8px ${BRAND.color.gold}`,
              }}
            />
          </Trail>
        ) : null}

        {/* ノード群 */}
        {NODES.map((n, i) => {
          const nx = xOf(n.year);
          // プレイヘッドがこのノードに到達したら点灯
          const reachP = (n.year - Y0) / (Y1 - Y0);
          const arrived = headP >= reachP - 0.01;
          const s = spring({
            frame: frame - (headStart + reachP * (headEnd - headStart)),
            fps,
            config: {damping: 12, mass: 0.9},
          });
          const dotScale = interpolate(s, [0, 1], [0.2, 1]);
          const dotGlow = interpolate(s, [0, 1], [0, 1]);
          const labY = interpolate(s, [0, 1], [110, 0]);
          const labO = interpolate(s, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});
          const above = i % 2 === 0; // 上下交互
          return (
            <div key={n.year}>
              {/* ノード点 */}
              <div
                style={{
                  position: 'absolute',
                  left: nx - 11,
                  top: axisY - 11 + 1.5,
                  width: 22,
                  height: 22,
                  borderRadius: 11,
                  background: arrived ? BRAND.color.gold : BRAND.color.navy,
                  border: `2px solid ${BRAND.color.gold}`,
                  boxShadow: dotGlow > 0.3 ? `0 0 20px 5px ${BRAND.color.gold}88` : 'none',
                  transform: `scale(${dotScale})`,
                }}
              />
              {/* コネクタ */}
              <div
                style={{
                  position: 'absolute',
                  left: nx - 1,
                  top: above ? axisY - 64 : axisY + 14,
                  width: 2,
                  height: 50,
                  background: `${BRAND.color.gold}${arrived ? 'aa' : '33'}`,
                }}
              />
              {/* ラベル群（マスク切れ上がり） */}
              <div
                style={{
                  position: 'absolute',
                  left: nx - 150,
                  top: above ? axisY - 190 : axisY + 66,
                  width: 300,
                  textAlign: 'center',
                }}
              >
                <div style={{overflow: 'hidden', paddingBottom: '0.12em'}}>
                  <div
                    style={{
                      transform: `translateY(${labY}%)`,
                      opacity: labO,
                      fontFamily: BRAND.font.body,
                      fontWeight: 700,
                      fontSize: 22,
                      letterSpacing: 2,
                      color: BRAND.color.gold,
                    }}
                  >
                    {n.kicker}
                  </div>
                </div>
                <div style={{overflow: 'hidden', paddingBottom: '0.12em', marginTop: 2}}>
                  <div
                    style={{
                      transform: `translateY(${labY}%)`,
                      opacity: labO,
                      fontFamily: BRAND.font.display,
                      fontWeight: 900,
                      fontSize: 34,
                      letterSpacing: 1,
                      color: BRAND.color.white,
                      textShadow: `0 0 18px ${BRAND.color.gold}44`,
                    }}
                  >
                    {n.title}
                  </div>
                </div>
                {n.chips ? (
                  <div style={{display: 'flex', gap: 8, justifyContent: 'center', flexWrap: 'wrap', marginTop: 8, opacity: labO}}>
                    {n.chips.map((c) => (
                      <span
                        key={c}
                        style={{
                          fontFamily: BRAND.font.body,
                          fontWeight: 700,
                          fontSize: 16,
                          letterSpacing: 1,
                          color: BRAND.color.silver,
                          border: `1px solid ${BRAND.color.silver}55`,
                          borderRadius: 4,
                          padding: '3px 8px',
                        }}
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                ) : null}
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
