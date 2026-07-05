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
// StampReveal — ラバースタンプ「判決」リビール（MOTIONKIT）
//   ・text（例 'GUILTY' / 'CONVICTED' / 'SEALED'）が巨大スケールから
//     高速オーバーシュートspring＋わずかな回転で叩き込まれる（SLAM）。
//   ・落下中は @remotion/motion-blur の Trail でモーションブラー。
//   ・接触フレームで画面全体にインパクトシェイク（減衰・非等速）。
//   ・接触点から決定論的なダスト粒子が飛散＋リング状の衝撃波が拡大。
//   ・color の粗い二重アウトラインのスタンプ枠（既定 '#C0473E' の色あせた赤）。
//   ・着地後は微かなブレスで“静止しない”。
//   全モーションにイージング/spring・opacity単独リビール無し・決定論的
//   （useCurrentFrame + index + remotion random(seed)。Math.random/Date 禁止）。
//   フルスクリーンのシーン背景＋≥3階層の奥行き。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

const DUST_COUNT = 26;

export const StampReveal: React.FC<{
  text: string;
  color?: string;
  dur?: number;
}> = ({text, color = '#C0473E', dur}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // ---- タイムライン（全て fps から算出） ----
  const slamStart = sec(fps, 0.1);
  const contact = slamStart + sec(fps, 0.24); // 叩き込み接触フレーム

  // ---- SLAM：巨大スケール→1 の高速オーバーシュートspring（低damping＝跳ね） ----
  const slamS = spring({
    frame: frame - slamStart,
    fps,
    config: {damping: 9, mass: 0.8, stiffness: 150},
  });
  const slamScale = interpolate(slamS, [0, 1], [5.2, 1]); // spring>1 で 1 を割り込み跳ねる
  const slamRot = interpolate(slamS, [0, 1], [-14, -4]); // 着地時のわずかな傾き
  const slamO = interpolate(
    frame,
    [slamStart, slamStart + sec(fps, 0.06)],
    [0, 1],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- 着地後の落ち着き＆ブレス（サイン＝非等速・常時わずかに動く） ----
  const settle = interpolate(slamS, [0.6, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const breathPhase = random('stamp-breath') * Math.PI * 2;
  const breathScale = 1 + Math.sin((frame / fps) * 1.4 + breathPhase) * 0.006 * settle;
  const breathRot = Math.sin((frame / fps) * 1.0 + breathPhase) * 0.5 * settle;

  // ---- インパクトシェイク（接触後に減衰・画面全体） ----
  const shakeEnv = interpolate(
    frame,
    [contact, contact + sec(fps, 0.34)],
    [1, 0],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const shakeAmt = frame >= contact ? shakeEnv : 0;
  const shakeX = Math.sin((frame - contact) * 2.7) * 15 * shakeAmt;
  const shakeY = Math.cos((frame - contact) * 3.3) * 13 * shakeAmt;
  const shakeR = Math.sin((frame - contact) * 2.1) * 0.7 * shakeAmt;

  // ---- 背景の奥行きドリフト（常時のゆっくりした生気） ----
  const bgDrift = interpolate(frame, [0, total], [0, 26], {
    easing: Easing.inOut(Easing.sin),
  });
  const glowPulse = 0.16 + Math.sin((frame / fps) * 1.6 + breathPhase) * 0.05;

  // ---- 衝撃波リング（接触点から拡大・二重） ----
  const ringT = interpolate(frame, [contact, contact + sec(fps, 0.5)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const ringT2 = interpolate(
    frame,
    [contact + sec(fps, 0.08), contact + sec(fps, 0.62)],
    [0, 1],
    {easing: Easing.out(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- 前景グループの退出（scaleと併用＝opacity単独禁止） ----
  const outStart = total - sec(fps, 0.4);
  const groupO = interpolate(frame, [0, sec(fps, 0.06), outStart, total], [0, 1, 1, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const outScale = interpolate(frame, [outStart, total], [1, 0.96], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const finalScale = slamScale * breathScale * outScale;
  const finalRot = slamRot + breathRot;

  // 粗い二重アウトラインの「インク欠け」マスク（枠だけに適用） ----
  const roughMask =
    'repeating-linear-gradient(38deg, #000 0 15px, transparent 15px 17px), ' +
    'repeating-linear-gradient(128deg, #000 0 21px, transparent 21px 22px)';

  const shockRing = (t: number, base: number, w0: number) => {
    if (t <= 0 || t >= 1) return null;
    const size = interpolate(t, [0, 1], [base, base + 620]);
    const o = interpolate(t, [0, 0.12, 1], [0, 0.5, 0]);
    const bw = interpolate(t, [0, 1], [w0, 1]);
    return (
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '50%',
          width: size,
          height: size,
          marginLeft: -size / 2,
          marginTop: -size / 2,
          borderRadius: '50%',
          border: `${bw}px solid ${color}`,
          opacity: o,
          boxShadow: `0 0 26px ${color}66`,
        }}
      />
    );
  };

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        overflow: 'hidden',
      }}
    >
      {/* シェイク対象：背景〜前景を包む。scale で外周を隠しつつ揺らす */}
      <AbsoluteFill
        style={{
          transform: `translate(${shakeX}px, ${shakeY}px) rotate(${shakeR}deg) scale(1.045)`,
        }}
      >
        {/* 奥行き1: 薄いグリッド（うっすら電光・ゆっくりドリフト） */}
        <AbsoluteFill
          style={{
            opacity: 0.09,
            transform: `translateY(${bgDrift}px)`,
            backgroundImage: `
              repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 88px),
              repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 88px)`,
            maskImage: 'radial-gradient(120% 90% at 50% 46%, black 22%, transparent 80%)',
            WebkitMaskImage: 'radial-gradient(120% 90% at 50% 46%, black 22%, transparent 80%)',
          }}
        />

        {/* 奥行き2: 中央の電光グロー（サインでパルス＝常時わずかに動く） */}
        <AbsoluteFill
          style={{
            background: `radial-gradient(46% 40% at 50% 50%, ${BRAND.color.electric} 0%, transparent 70%)`,
            opacity: glowPulse,
            transform: `translateY(${-bgDrift * 0.4}px)`,
          }}
        />

        {/* 奥行き3: 環境ダストモート（低速に漂う・常時わずかに動く） */}
        <AbsoluteFill>
          {new Array(14).fill(0).map((_, i) => {
            const bx = random('mote-x' + i);
            const by = random('mote-y' + i);
            const sp = 0.5 + random('mote-s' + i) * 0.8;
            const ph = random('mote-p' + i) * Math.PI * 2;
            const dx = Math.sin((frame / fps) * sp + ph) * 20;
            const dy = Math.cos((frame / fps) * sp * 0.8 + ph) * 16;
            const sz = 2 + random('mote-z' + i) * 4;
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: `${bx * 100}%`,
                  top: `${by * 100}%`,
                  width: sz,
                  height: sz,
                  marginLeft: dx,
                  marginTop: dy,
                  borderRadius: '50%',
                  background: BRAND.color.silver,
                  opacity: 0.06 + random('mote-o' + i) * 0.06,
                  filter: 'blur(0.5px)',
                }}
              />
            );
          })}
        </AbsoluteFill>

        {/* 前景: スタンプ＋衝撃波＋ダスト飛散 */}
        <AbsoluteFill
          style={{
            justifyContent: 'center',
            alignItems: 'center',
            opacity: groupO,
          }}
        >
          {/* 衝撃波リング（接触点＝中央から拡大） */}
          {shockRing(ringT, 60, 9)}
          {shockRing(ringT2, 40, 6)}

          {/* ダスト粒子の飛散（決定論的・translate+scaleで飛ぶ＝opacity単独禁止） */}
          {new Array(DUST_COUNT).fill(0).map((_, i) => {
            const a = random('dust-a' + i) * Math.PI * 2;
            const d0 = 110 + random('dust-d' + i) * 300;
            const startJit = random('dust-j' + i) * sec(fps, 0.04);
            const start = contact + startJit;
            const life = sec(fps, 0.5) + random('dust-l' + i) * sec(fps, 0.2);
            const t = interpolate(frame, [start, start + life], [0, 1], {
              easing: Easing.out(Easing.cubic),
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            });
            if (frame < start || t >= 1) return null;
            const dist = d0 * t;
            const px = Math.cos(a) * dist;
            const py = Math.sin(a) * dist + t * t * 60; // わずかな落下ドリフト
            const o = interpolate(t, [0, 0.12, 1], [0, 0.9, 0], {
              easing: Easing.out(Easing.quad),
            });
            const psz = 4 + random('dust-z' + i) * 12;
            const psc = interpolate(t, [0, 1], [1, 0.2], {
              easing: Easing.out(Easing.cubic),
            });
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: '50%',
                  top: '50%',
                  width: psz,
                  height: psz,
                  marginLeft: -psz / 2,
                  marginTop: -psz / 2,
                  borderRadius: '50%',
                  background: color,
                  opacity: o,
                  transform: `translate(${px}px, ${py}px) scale(${psc})`,
                }}
              />
            );
          })}

          {/* スタンプ本体（落下中は Trail でモーションブラー） */}
          <Trail layers={6} lagInFrames={1.2} trailOpacity={0.45}>
            <div
              style={{
                position: 'relative',
                transform: `scale(${finalScale}) rotate(${finalRot}deg)`,
                opacity: slamO,
                padding: '38px 74px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {/* 粗い二重アウトライン枠（インク欠けマスク・テキストとは別レイヤー） */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  border: `7px solid ${color}`,
                  borderRadius: 10,
                  boxShadow: `inset 0 0 0 5px transparent, inset 0 0 0 8px ${color}`,
                  maskImage: roughMask,
                  WebkitMaskImage: roughMask,
                  opacity: 0.92,
                }}
              />
              {/* 二重枠の内側ライン（ギャップを空けた薄い罫） */}
              <div
                style={{
                  position: 'absolute',
                  inset: 12,
                  border: `2px solid ${color}`,
                  borderRadius: 6,
                  maskImage: roughMask,
                  WebkitMaskImage: roughMask,
                  opacity: 0.78,
                }}
              />
              {/* テキスト（色あせたインクのスタンプ字面） */}
              <div
                style={{
                  position: 'relative',
                  color,
                  fontFamily: BRAND.font.display,
                  fontWeight: 900,
                  fontSize: 150,
                  lineHeight: 1,
                  letterSpacing: 4,
                  textTransform: 'uppercase',
                  whiteSpace: 'nowrap',
                  opacity: 0.94,
                  maskImage: roughMask,
                  WebkitMaskImage: roughMask,
                  textShadow: `0 2px 0 ${color}44`,
                }}
              >
                {text}
              </div>
            </div>
          </Trail>
        </AbsoluteFill>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
