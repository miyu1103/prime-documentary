import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  random,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';

// =====================================================================
// MOTIONKIT — LowerThird
//   放送用ロワーサード。左からモーションブラー(Trail)付きでスライドイン、
//   ゴールドのアクセントバーが scaleX で伸び、primary(太字)+secondary(抑え)が
//   単語スタッガーのマスク切れ上がりで出現。終端で左へスライドアウト。
//   透明オーバーレイ（全面バックドロップなし）。accent でバー色を上書き可能。
//   品質ルール: 全モーションにイージング/spring（等速禁止）・opacity単独禁止・
//   マスク切れ上がり・決定論的（useCurrentFrame + index + random('seed'+i)）。
// =====================================================================

// 秒→フレーム（fps基準、フレーム直書き禁止）
const sec = (fps: number, s: number) => fps * s;

// 単語単位のマスク切れ上がり（overflow:hidden + 内側translateYスライドアップ）
const WordMask: React.FC<{
  text: string;
  fps: number;
  startFrame: number;
  color: string;
  fontFamily: string;
  fontSize: number;
  fontWeight: number;
  letterSpacing: number;
  seed: string;
}> = ({
  text,
  fps,
  startFrame,
  color,
  fontFamily,
  fontSize,
  fontWeight,
  letterSpacing,
  seed,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');
  const stagger = Math.max(1, sec(fps, 0.05));
  return (
    <div
      style={{
        display: 'flex',
        flexWrap: 'wrap',
        color,
        fontFamily,
        fontSize,
        fontWeight,
        letterSpacing,
        lineHeight: 1.02,
      }}
    >
      {words.map((w, i) => {
        // 決定論的な微ジッター（±0.6フレーム）
        const jitter = (random(seed + i) - 0.5) * 1.2;
        const cs = spring({
          frame: frame - startFrame - i * stagger - jitter,
          fps,
          config: {damping: 16, mass: 0.9},
        });
        const y = interpolate(cs, [0, 1], [118, 0]);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              overflow: 'hidden',
              paddingBottom: '0.14em',
              marginRight: '0.32em',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                transform: `translateY(${y}%)`,
                whiteSpace: 'pre',
              }}
            >
              {w}
            </span>
          </span>
        );
      })}
    </div>
  );
};

export const LowerThird: React.FC<{
  primary: string;
  secondary?: string;
  accent?: string;
  dur?: number;
}> = ({primary, secondary, accent, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const barColor = accent ?? BRAND.color.gold;

  // 入場：左から素早くスライドイン（イージング＝spring、等速禁止）。
  // 移動量は SHORT（-200px）に抑える：以前は -960px から入っていたため、入場の
  // 0.3-0.5秒ものあいだ本文が画面左端で見切れていた（owner 2026-07-06「左端で文字が
  // 見切れる」）。パネルのクリップ開き＋単語マスクの切り上がりで入場感は十分あるので、
  // 大きな横スライドは不要。短い距離なら本文が常に画面内に収まり見切れない。
  const enter = spring({
    frame,
    fps,
    config: {damping: 20, mass: 1.05, stiffness: 140},
  });
  // NO horizontal slide any more: even a -200px slide-in still pushed the left-aligned text past
  // the frame's left edge during entrance, so the first characters were clipped ("OT A BLANK CHECK"
  // instead of "NOT..."). The entrance is now purely the panel wipe-open (clipPath) + the per-word
  // mask rise + a small VERTICAL rise below — none of which ever move the text left of its resting
  // margin, so nothing is ever clipped at the left edge. (owner 2026-07-06/07)
  const enterY = interpolate(enter, [0, 1], [40, 0]);

  // 退場：終端で下へ微ドリフト＋フェード（横に飛ばさない＝切れ目で半分見切れない）。
  // opacity単独を避けるため translateY と併用。
  const exitStart = total - sec(fps, 0.55);
  const exit = spring({
    frame: frame - exitStart,
    fps,
    config: {damping: 200, mass: 1},
  });
  const exitY = interpolate(exit, [0, 1], [0, 46], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const exitO = interpolate(exit, [0, 1], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  const slideX = 0;

  // アイドル：静止させない微ドリフト（sinイージング相当の連続運動）
  const idleY = interpolate(
    Math.sin((frame / fps) * 1.6),
    [-1, 1],
    [-2.2, 2.2],
  );

  // アクセントバー：scaleX で左origin から伸びる（少し遅延）
  const barGrow = spring({
    frame: frame - sec(fps, 0.12),
    fps,
    config: {damping: 22, mass: 1},
  });
  const barScaleX = interpolate(barGrow, [0, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // バーのグロー脈動（発光の連続運動・静止回避）
  const barGlow = interpolate(
    Math.sin((frame / fps) * 2.4),
    [-1, 1],
    [0.45, 0.9],
  );

  // パネル背景の伸び上がり（開幅、opacity単独にしないため clip + translate と併用）
  const panelGrow = spring({
    frame: frame - sec(fps, 0.04),
    fps,
    config: {damping: 26, mass: 1},
  });
  const panelClip = interpolate(panelGrow, [0, 1], [100, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const primaryStart = sec(fps, 0.22);
  const secondaryStart = sec(fps, 0.42);

  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        // オーバーレイ：全面バックドロップなし（透明）
        backgroundColor: 'transparent',
      }}
    >
      <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
        <div
          style={{
            position: 'absolute',
            left: 92,
            top: 92,
            transform: `translate(${slideX}px, ${idleY + exitY + enterY}px)`,
            opacity: exitO * interpolate(enter, [0, 0.35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
            display: 'flex',
            alignItems: 'stretch',
            // WIDTH CEILING (2026-09-01). This element is absolutely positioned with no width, so
            // it shrink-to-fits against its containing block: 1920 - left(92) = 1828px. A long
            // `secondary` therefore wraps at 1828 and the panel becomes 1828 + bar(8) + padding(56)
            // = 1892 wide, starting at x=92 -- a right edge at 1984, i.e. 64px PAST the frame,
            // before any outer transform is applied at all.
            // MEASURED on EP73 uri: bodies of 33-236 characters across 39 beats. The one the reader
            // used as the control, "FIVE THOUSAND TO ONE MILLION" (121 chars, one line), sits fully
            // inside the frame; "SENATE BILL 3" (178 chars, two lines) is cut mid-word at "maps the
            // supply". Every clipped card had a body that wrapped; every clean one did not.
            // 1736 = 1920 - 92*2, so the right edge lands at 1828 and the card carries the same 92px
            // margin on both sides. minWidth: 0 on the panel below is what lets the flex child
            // actually shrink to this instead of overflowing it.
            maxWidth: 1736,
          }}
        >
          {/* アクセントバー：左origin で scaleX 伸長＋発光脈動 */}
          <div
            style={{
              width: 8,
              alignSelf: 'stretch',
              backgroundColor: barColor,
              transform: `scaleX(${barScaleX})`,
              transformOrigin: 'left center',
              borderRadius: 2,
              boxShadow: `0 0 ${18 + barGlow * 16}px ${barColor}`,
              opacity: 0.4 + barGlow * 0.6,
            }}
          />
          {/* パネル：ナビ→インクの半透明ストリップ（クリップで開く） */}
          <div
            style={{
              position: 'relative',
              minWidth: 0,
              overflow: 'hidden',
              clipPath: `inset(0 ${panelClip}% 0 0)`,
              background: `linear-gradient(100deg, ${BRAND.color.navy}E6 0%, ${BRAND.color.ink}D9 100%)`,
              borderLeft: `1px solid ${barColor}55`,
              backdropFilter: 'blur(3px)',
              padding: '18px 30px 20px 26px',
            }}
          >
            <WordMask
              text={primary}
              fps={fps}
              startFrame={primaryStart}
              color={BRAND.color.white}
              fontFamily={BRAND.font.display}
              fontSize={46}
              fontWeight={900}
              letterSpacing={0.5}
              seed="lt-primary-"
            />
            {secondary ? (
              <div style={{marginTop: 8}}>
                <WordMask
                  text={secondary}
                  fps={fps}
                  startFrame={secondaryStart}
                  color={BRAND.color.silver}
                  fontFamily={BRAND.font.body}
                  fontSize={24}
                  fontWeight={500}
                  letterSpacing={1}
                  seed="lt-secondary-"
                />
              </div>
            ) : null}
          </div>
        </div>
      </Trail>
    </AbsoluteFill>
  );
};
