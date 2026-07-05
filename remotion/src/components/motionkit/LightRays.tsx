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
// LightRays — 実映像/カットの上に重ねる、透明の「ボリューメトリック god-ray」
//   オーバーレイ。数本の長く柔らかい光のシャフトが、画面外・オフセンターの
//   ソフト光源（左上コーナー）から斜めに扇状に伸び、イーズド正弦で角度と
//   強度がゆらぎ・呼吸する。screen 合成・低不透明度。光を受けて漂う微塵つき。
//
//   ・すべての動きはイージング付き（等速線形禁止／ゆらぎはイーズド正弦）。
//   ・決定論的（useCurrentFrame + index + remotion `random(seed)`。
//     Math.random/Date 不使用）。時間は fps から算出。静止フレームを作らない。
//   ・ブランド色トークンのみ（default は electric/white。color で上書き可）。
//   ・root pointerEvents:'none'／不透明背景なし／画面内ロゴなし。
//   ・禁止＝黄縦スイープ／全面黄ウォッシュ／単一のハードな縦バー。ここでは
//     光源はオフセンターで斜め、シャフトは複数・柔らかく・ボリューメトリック。
// =====================================================================

// 秒→フレーム
const sec = (fps: number, s: number) => Math.round(fps * s);

// 出入りエンベロープ（先頭で立ち上げ・終端で畳む、必ずイーズド）。
// 任意の dur で interpolate の入力が単調増加になるようフェード幅を dur から算出。
const envelope = (frame: number, dur: number, fps: number): number => {
  const inN = Math.min(sec(fps, 0.5), Math.max(1, Math.floor(dur / 3)));
  const outN = Math.min(sec(fps, 0.5), Math.max(1, Math.floor(dur / 3)));
  const p1 = inN;
  const p2 = Math.max(p1 + 1, dur - outN);
  return interpolate(frame, [0, p1, p2, dur], [0, 1, 1, 0], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

// イーズド正弦：sin の生値[-1..1]を Easing.inOut(Easing.sin) で lo..hi へ写像。
// 「等速でない」ゆらぎを明示的に作るためのヘルパ（sin 位相は連続＝ポップなし）。
const easedSine = (
  phase: number,
  lo: number,
  hi: number,
): number =>
  interpolate(Math.sin(phase), [-1, 1], [lo, hi], {
    easing: Easing.inOut(Easing.sin),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

// ---------------------------------------------------------------------
// LightRays 本体
// ---------------------------------------------------------------------
export const LightRays: React.FC<{color?: string; dur?: number}> = ({
  color = BRAND.color.electric,
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // レイヤ全体の柔らかな立ち上げ（先頭のポップ防止）＋出入りエンベロープ
  const appear = spring({
    frame,
    fps,
    config: {damping: 26, mass: 1, stiffness: 62},
  });
  const env = envelope(frame, total, fps);
  const t = frame / fps; // 秒

  // オフセンターのソフト光源：左上コーナー（画面外上方）。単一縦バー回避のため
  // ここから斜め右下へ扇状にシャフトを伸ばす。
  const sourceX = width * 0.17;
  const sourceY = -height * 0.14;

  // シャフト本数と扇の広がり（下向き 0deg 基準／右下へ +角度）。
  const RAYS = 7;
  const fanFrom = 8; // deg
  const fanTo = 52; // deg
  const rayLen = Math.hypot(width, height) * 1.9; // 画面を貫く十分な長さ
  const DUST = 26;

  return (
    <AbsoluteFill
      style={{
        mixBlendMode: 'screen',
        pointerEvents: 'none',
        background: 'transparent',
        opacity: appear * env,
      }}
    >
      {/* 光源のソフトグロー（白コア）— イーズド正弦で息づく（ハード線でない） */}
      <div
        style={{
          position: 'absolute',
          left: sourceX - 460,
          top: sourceY - 460,
          width: 920,
          height: 920,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${BRAND.color.white} 0%, ${color} 34%, transparent 66%)`,
          filter: 'blur(30px)',
          opacity: easedSine(t * 0.9 + 0.4, 0.16, 0.28),
        }}
      />

      {/* 光のシャフト群。緩やかなゆらぎは Trail で微かなモーションブラーを付与。 */}
      <Trail layers={3} lagInFrames={2.2} trailOpacity={0.5}>
        {Array.from({length: RAYS}).map((_, i) => {
          // 決定論的パラメータ（seed 固定・Math.random/Date 不使用）
          const rW = random('ray-w' + i); // 幅
          const rSway = random('ray-sway' + i); // ゆらぎ振幅
          const rSwSpd = random('ray-swspd' + i); // ゆらぎ速度
          const rBrSpd = random('ray-brspd' + i); // 呼吸速度
          const rPh = random('ray-ph' + i); // 位相
          const rBl = random('ray-blur' + i); // ぼかし
          const rOp = random('ray-op' + i); // 基準不透明度

          // 扇状の基準角（下向き基準・右下へ）。単一縦バーにならないよう分散。
          const baseAngle = interpolate(i, [0, RAYS - 1], [fanFrom, fanTo]);

          // 角度ゆらぎ＝イーズド正弦（±1.4..3.4deg・シャフトごとに位相/速度差）。
          const swayAmp = 1.4 + rSway * 2.0;
          const swSpeed = 0.10 + rSwSpd * 0.14;
          const sway = easedSine(
            t * swSpeed + rPh * Math.PI * 2,
            -swayAmp,
            swayAmp,
          );
          const angle = baseAngle + sway;

          // 強度呼吸＝イーズド正弦（opacity 単独でなく幅 scale も併走させる）。
          const brSpeed = 0.16 + rBrSpd * 0.22;
          const breath = easedSine(t * brSpeed + rPh * 6.2, 0.45, 1.0);
          const w = (150 + rW * 200) * (0.86 + breath * 0.24); // 幅も脈動
          const baseOpacity = 0.06 + rOp * 0.07; // 低不透明度
          const op = baseOpacity * breath;
          const blur = 42 + rBl * 60;

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: sourceX,
                top: sourceY,
                width: w,
                height: rayLen,
                marginLeft: -w / 2,
                transformOrigin: '50% 0%',
                transform: `rotate(${angle}deg)`,
                // シャフト：光源側が最も明るく、遠端で透明化（god-ray フェード）。
                background: `linear-gradient(to bottom, ${color} 0%, ${color} 8%, transparent 78%)`,
                filter: `blur(${blur}px)`,
                opacity: op,
                borderRadius: '50% / 8%',
              }}
            />
          );
        })}
      </Trail>

      {/* 光を受けて漂う微塵。位置/速度/明滅は決定論的。上昇ドリフト＋横ゆれ。 */}
      <Trail layers={2} lagInFrames={1.4} trailOpacity={0.5}>
        {Array.from({length: DUST}).map((_, i) => {
          const d0 = random('dust-x' + i); // 横位置
          const d1 = random('dust-spd' + i); // 速度
          const d2 = random('dust-size' + i); // サイズ
          const d3 = random('dust-sway' + i); // 横ゆれ量
          const d4 = random('dust-ph' + i); // 位相
          const d5 = random('dust-tw' + i); // 明滅位相
          const d6 = random('dust-start' + i); // 縦初期位相

          const size = 2 + d2 * 5; // 2..7px
          const speed = 0.4 + d1 * 0.7;
          const swayAmp = 14 + d3 * 40;
          const swayPh = d4 * Math.PI * 2;
          const twPh = d5 * Math.PI * 2;

          // 縦ドリフト：連続位相を正弦でワープ（速度可変＝イーズド／循環でポップなし）。
          const cyc = t * speed * 0.1 + d6;
          const ph = cyc - Math.floor(cyc);
          const warped = ph + 0.12 * Math.sin(ph * Math.PI * 2);
          const y = (1 - warped) * (height + 160) - 80;

          // 塵は光の扇（左→中央寄り）に集めて「光を受ける」印象に。横ゆれは正弦。
          const bandX = d0 * width * 0.72 + width * 0.06;
          const x = bandX + Math.sin(t * 0.8 + swayPh) * swayAmp;

          // 明滅は scale で（opacity 単独禁止）。opacity は下限を保ちつつ併走。
          const tw = 0.5 + 0.5 * Math.sin(t * 1.7 + twPh);
          const scale = 0.7 + tw * 0.7;
          const dustOp = (0.18 + tw * 0.32) * easedSine(t * 0.5 + twPh, 0.7, 1.0);

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: x,
                top: y,
                width: size,
                height: size,
                marginLeft: -size / 2,
                marginTop: -size / 2,
                borderRadius: '50%',
                background: BRAND.color.white,
                opacity: dustOp,
                transform: `scale(${scale})`,
                filter: `blur(${0.6 + (i % 3) * 0.5}px)`,
                boxShadow: `0 0 ${size * 2.4}px ${color}`,
              }}
            />
          );
        })}
      </Trail>
    </AbsoluteFill>
  );
};
