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
// TerminalType — シネマティックなハッカー/記録端末シーン
//   暗い角丸コンソールが translateY+scale の spring でせり上がり、
//   走査線・グロー・CRTフリッカ・グリッドを背後に重ねる。
//   lines を1文字ずつ（フレーム由来のreveal数）タイプ。行ごとにスタッガー。
//   点滅ブロックカーソル・prompt接頭辞・モノスペース（緑/エレクトリック）。
// 品質: 全モーションにイージング/spring・opacity単独reveal禁止（パネルは
//   translateY+scaleで登場）・決定論（useCurrentFrame＋index）・常に微動。
// =====================================================================

// ターミナルグリーン（唯一許可されたリテラル）＋ BRAND トークンのみ
const TERM_GREEN = '#5FE0A0';
const MONO = "'SFMono-Regular','Consolas','Menlo',monospace";
const SCENE_BG = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`;

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// ---------------------------------------------------------------------
// 背後の奥行きレイヤー（グリッド＋グロー＋CRTフリッカ／ビネット）
// ---------------------------------------------------------------------
const DepthLayers: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  // グリッドは常に微ドリフト（sinイージング・等速でない）
  const drift = interpolate(frame, [0, durationInFrames], [0, 46], {
    easing: Easing.inOut(Easing.sin),
  });
  // パネル裏のグローが呼吸する
  const glowPulse = interpolate(
    Math.sin((frame / fps) * 1.4),
    [-1, 1],
    [0.32, 0.6],
  );
  // CRT走査ビーム（縦にゆっくり流れる）
  const beamY = interpolate(
    (frame % sec(fps, 3.4)) / sec(fps, 3.4),
    [0, 1],
    [-8, 108],
    {easing: Easing.inOut(Easing.quad)},
  );
  // 決定論的フリッカ（remotion random をフレームでシード）
  const flicker = 0.86 + random(`crt-${Math.floor(frame / 2)}`) * 0.14;

  return (
    <>
      {/* Layer 1: 遠景グリッド（電光ブルーの微かなライン） */}
      <AbsoluteFill
        style={{
          opacity: 0.16,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}26 0px, ${BRAND.color.electric}26 1px, transparent 1px, transparent 66px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}26 0px, ${BRAND.color.electric}26 1px, transparent 1px, transparent 66px)`,
          maskImage:
            'radial-gradient(120% 90% at 50% 46%, black 22%, transparent 80%)',
          WebkitMaskImage:
            'radial-gradient(120% 90% at 50% 46%, black 22%, transparent 80%)',
        }}
      />
      {/* Layer 2: パネル裏のエレクトリックグロー（呼吸） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 40% at 50% 50%, ${BRAND.color.electric}2e 0%, transparent 62%)`,
          opacity: glowPulse,
          filter: 'blur(8px)',
        }}
      />
      {/* Layer 3: CRT走査線＋縦流れビーム＋フリッカ＋ビネット */}
      <AbsoluteFill
        style={{
          opacity: flicker,
          background: `
            linear-gradient(180deg, transparent ${beamY - 6}%, ${TERM_GREEN}12 ${beamY}%, transparent ${beamY + 6}%),
            repeating-linear-gradient(0deg, rgba(0,0,0,0.28) 0px, rgba(0,0,0,0.28) 1px, transparent 1px, transparent 3px),
            radial-gradient(120% 100% at 50% 46%, transparent 48%, rgba(0,0,0,0.62) 100%)`,
          mixBlendMode: 'multiply',
          pointerEvents: 'none',
        }}
      />
    </>
  );
};

export const TerminalType: React.FC<{
  lines: string[];
  prompt?: string;
  dur?: number;
}> = ({lines, prompt = '> ', dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // パネル登場: translateY + scale の spring（opacity単独禁止）
  const enter = spring({
    frame,
    fps,
    config: {damping: 18, mass: 1.1, stiffness: 120},
  });
  const panelY = interpolate(enter, [0, 1], [130, 0]);
  const panelScale = interpolate(enter, [0, 1], [0.9, 1]);
  const panelOpacity = interpolate(enter, [0, 0.35], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 退場も translateY と併用（純フェード回避）
  const outY = interpolate(
    frame,
    [total - sec(fps, 0.5), total],
    [0, -40],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const outOpacity = interpolate(
    frame,
    [total - sec(fps, 0.4), total],
    [1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // タイピング: prompt を接頭辞に、行を順にカスケードでタイプ（フレーム由来）
  const full = lines.map((l) => prompt + l);
  const cps = 30; // chars/sec
  const framesPerChar = fps / cps;
  const typeStart = sec(fps, 0.55);
  const lineGap = sec(fps, 0.16);

  const starts: number[] = [];
  let acc = typeStart;
  full.forEach((t) => {
    starts.push(acc);
    acc += t.length * framesPerChar + lineGap;
  });

  const reveals = full.map((t, i) =>
    Math.max(0, Math.min(t.length, Math.floor((frame - starts[i]) / framesPerChar))),
  );

  // カーソルが乗る行 = 最初の未完了行（全完了なら最終行）
  let cursorLine = full.findIndex((t, i) => reveals[i] < t.length);
  if (cursorLine === -1) cursorLine = full.length - 1;

  // ブロックカーソルの点滅（フレーム由来・soft floor で燐光を残す）
  const blinkPeriod = sec(fps, 0.5);
  const blinkOn = Math.floor(frame / blinkPeriod) % 2 === 0;
  const cursorOpacity = blinkOn ? 1 : 0.18;

  const fontSize = 34;
  const lineH = 1.62;

  return (
    <AbsoluteFill style={{background: SCENE_BG}}>
      <DepthLayers />

      {/* 主役: 端末パネル（速い登場に Trail で残像＝CRT燐光） */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          opacity: outOpacity,
        }}
      >
        <Trail layers={3} lagInFrames={1.4} trailOpacity={0.32}>
          <div
            style={{
              width: 1240,
              transform: `translateY(${panelY + outY}px) scale(${panelScale})`,
              opacity: panelOpacity,
              borderRadius: 18,
              background:
                'linear-gradient(180deg, rgba(11,26,43,0.94) 0%, rgba(6,8,15,0.96) 100%)',
              border: `1px solid ${BRAND.color.electric}3a`,
              boxShadow: `0 40px 120px rgba(0,0,0,0.6), 0 0 0 1px rgba(0,0,0,0.4), 0 0 80px ${BRAND.color.electric}22, inset 0 1px 0 ${BRAND.color.silver}18`,
              overflow: 'hidden',
            }}
          >
            {/* タイトルバー */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '16px 22px',
                borderBottom: `1px solid ${BRAND.color.electric}22`,
                background: `linear-gradient(180deg, ${BRAND.color.electric}12 0%, transparent 100%)`,
              }}
            >
              <span
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  background: BRAND.color.gold,
                  boxShadow: `0 0 10px ${BRAND.color.gold}aa`,
                }}
              />
              <span
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  background: BRAND.color.silver,
                  opacity: 0.7,
                }}
              />
              <span
                style={{
                  width: 12,
                  height: 12,
                  borderRadius: '50%',
                  background: TERM_GREEN,
                  boxShadow: `0 0 10px ${TERM_GREEN}aa`,
                }}
              />
              <span
                style={{
                  marginLeft: 16,
                  fontFamily: MONO,
                  fontSize: 20,
                  letterSpacing: 3,
                  textTransform: 'uppercase',
                  color: BRAND.color.silver,
                }}
              >
                secure shell — records.db
              </span>
            </div>

            {/* コンソール本文 */}
            <div
              style={{
                position: 'relative',
                padding: '34px 40px 40px',
                fontFamily: MONO,
                fontSize,
                lineHeight: lineH,
                minHeight: 380,
              }}
            >
              {full.map((t, i) => {
                const shown = t.slice(0, reveals[i]);
                const promptShown = shown.slice(0, prompt.length);
                const bodyShown = shown.slice(prompt.length);
                // 行が始動する瞬間に軽い切れ上がり（イージング付き）
                const rise = spring({
                  frame: frame - starts[i],
                  fps,
                  config: {damping: 20, mass: 0.6},
                });
                const ty = interpolate(rise, [0, 1], [10, 0]);
                const isCursorLine = i === cursorLine;
                return (
                  <div
                    key={i}
                    style={{
                      minHeight: fontSize * lineH,
                      whiteSpace: 'pre',
                      transform: `translateY(${ty}px)`,
                    }}
                  >
                    <span
                      style={{
                        color: BRAND.color.electric,
                        textShadow: `0 0 12px ${BRAND.color.electric}66`,
                      }}
                    >
                      {promptShown}
                    </span>
                    <span
                      style={{
                        color: TERM_GREEN,
                        textShadow: `0 0 10px ${TERM_GREEN}55`,
                      }}
                    >
                      {bodyShown}
                    </span>
                    {isCursorLine ? (
                      <span
                        style={{
                          display: 'inline-block',
                          width: '0.6em',
                          height: '1.05em',
                          marginLeft: 2,
                          verticalAlign: '-0.16em',
                          background: TERM_GREEN,
                          opacity: cursorOpacity,
                          boxShadow: `0 0 14px ${TERM_GREEN}88`,
                        }}
                      />
                    ) : null}
                  </div>
                );
              })}

              {/* パネル内スキャンライン（本文の上に薄く重ねる） */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  pointerEvents: 'none',
                  backgroundImage:
                    'repeating-linear-gradient(0deg, rgba(0,0,0,0.16) 0px, rgba(0,0,0,0.16) 1px, transparent 1px, transparent 3px)',
                  mixBlendMode: 'multiply',
                }}
              />
            </div>
          </div>
        </Trail>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
