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
// KineticCaptions — MOTIONKIT の大きめ下三分の一キネティック字幕。
//   style='wordpop'   単語が1語ずつ spring でポップ＋ちょい上移動＋Trailブラー
//   style='maskslide' 各行が overflow:hidden マスクで切り上がり（スタッガー）
//   style='emphasis'  通常リビール＋ emphasisWords はスケールパンチ＋ゴールド＋グロー
// 品質ルール準拠: 全モーション spring/eased（線形なし）・opacity単独禁止（translateY/scale併用）
//   ・テキストはマスク切り上がり・速い登場は Trail・決定論(useCurrentFrame+index+random)
//   ・保持中も微ブレスで静止させない・タイミングは fps から Math.round(fps*sec)。
//   白ボディ／ゴールド強調／強めのドロップシャドウ／ボトムセーフ配置（背後映像に重ねる想定）。
//
// 実装メモ: @remotion/motion-blur の <Trail> は各レイヤーを AbsoluteFill(絶対配置)で
//   重ねるため、インライン単語を個別に包むとフレックス配置が壊れる。よってレイアウト全体
//   (Inner=AbsoluteFill) を1つの Trail で包み、各レイヤーが同一に重なるようにする。
// =====================================================================

// 秒→フレーム
const secF = (fps: number, s: number): number => Math.round(fps * s);

// 強調語の照合用: 文字・数字以外を落として小文字化
const norm = (w: string): string => w.replace(/[^\p{L}\p{N}]/gu, '').toLowerCase();

// 白ボディの強めドロップシャドウ
const BODY_SHADOW = '0 6px 24px rgba(0,0,0,0.85), 0 2px 6px rgba(0,0,0,0.9)';
// ゴールド強調のグロー付きシャドウ
const goldShadow = (): string =>
  `0 6px 24px rgba(0,0,0,0.85), 0 0 34px ${BRAND.color.gold}99, 0 0 12px ${BRAND.color.gold}66`;

const BODY_SIZE = 66;

// 終端で下へ流しつつフェード（opacity単独にしない）。dur はコンポジション尺。
const exitAt = (
  frame: number,
  fps: number,
  dur: number,
): {exitY: number; exitOpacity: number} => {
  const e = interpolate(frame, [dur - secF(fps, 0.6), dur - secF(fps, 0.1)], [0, 1], {
    easing: Easing.in(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return {exitY: e * 44, exitOpacity: 1 - e};
};

// ---------------------------------------------------------------------
// 単語（wordpop / emphasis 共用）: マスク切り上がり＋スプリングポップ
// ---------------------------------------------------------------------
const Word: React.FC<{
  word: string;
  index: number;
  startFrame: number;
  emphasis: boolean;
  fastPop: boolean;
  dur: number;
}> = ({word, index, startFrame, emphasis, fastPop, dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const local = frame - startFrame;

  const enter = spring({
    frame: local,
    fps,
    config: fastPop
      ? {damping: 12, mass: 0.6, stiffness: 170}
      : {damping: 15, mass: 0.7, stiffness: 140},
  });
  const y = interpolate(enter, [0, 1], [120, 0]); // マスク内 %
  const baseScale = interpolate(enter, [0, 1], [0.72, 1]);
  const op = interpolate(enter, [0, 0.35], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // 決定論的な微小ジッター（着地時に消える回転）
  const jitter = random('kc-word-' + index) - 0.5; // -0.5..0.5
  const settleRot = jitter * 1.6 * (1 - enter);

  // 強調語のスケールパンチ（登場後）
  const punchSpring = emphasis
    ? spring({
        frame: local - secF(fps, 0.16),
        fps,
        config: {damping: 9, mass: 0.5, stiffness: 210},
      })
    : 0;
  const punch = 1 + interpolate(punchSpring, [0, 1], [0, 0.2]);

  // 保持中も止めないブレス
  const breath = 1 + Math.sin((frame + index * 7) / (fps * 0.9)) * 0.014;

  const {exitY, exitOpacity} = exitAt(frame, fps, dur);

  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.16em',
        marginRight: BODY_SIZE * 0.26,
      }}
    >
      <span
        style={{
          display: 'inline-block',
          transform:
            `translateY(${y}%) translateY(${exitY}px) ` +
            `scale(${baseScale * punch * breath}) rotate(${settleRot}deg)`,
          opacity: op * exitOpacity,
          color: emphasis ? BRAND.color.gold : BRAND.color.white,
          whiteSpace: 'pre',
          textShadow: emphasis ? goldShadow() : BODY_SHADOW,
        }}
      >
        {word}
      </span>
    </span>
  );
};

// ---------------------------------------------------------------------
// 行（maskslide 用）: 行まるごとマスク切り上がり
// ---------------------------------------------------------------------
const Line: React.FC<{text: string; startFrame: number; index: number; dur: number}> = ({
  text,
  startFrame,
  index,
  dur,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const local = frame - startFrame;

  const enter = spring({
    frame: local,
    fps,
    config: {damping: 16, mass: 0.85, stiffness: 120},
  });
  const y = interpolate(enter, [0, 1], [112, 0]); // マスク内 %
  const slideX = interpolate(enter, [0, 1], [-20, 0]); // px 微スライド
  const op = interpolate(enter, [0, 0.3], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const breath = 1 + Math.sin((frame + index * 9) / (fps * 0.9)) * 0.01;
  const {exitY, exitOpacity} = exitAt(frame, fps, dur);

  return (
    <div style={{overflow: 'hidden', paddingBottom: '0.14em'}}>
      <div
        style={{
          transform:
            `translateY(${y}%) translateY(${exitY}px) translateX(${slideX}px) scale(${breath})`,
          opacity: op * exitOpacity,
          color: BRAND.color.white,
          whiteSpace: 'pre',
          textShadow: BODY_SHADOW,
        }}
      >
        {text}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------
// レイアウト本体（単一 Trail の子）— スタイル別に行/単語を配置
// ---------------------------------------------------------------------
const Inner: React.FC<{
  lines: string[];
  style: 'wordpop' | 'maskslide' | 'emphasis';
  emphasisSet: Set<string>;
  dur: number;
}> = ({lines, style, emphasisSet, dur}) => {
  const {fps} = useVideoConfig();
  const base = secF(fps, 0.12);

  const rowStyle: React.CSSProperties = {
    display: 'flex',
    flexWrap: 'wrap',
    alignItems: 'flex-end',
    fontFamily: BRAND.font.display,
    fontWeight: 900,
    fontSize: BODY_SIZE,
    lineHeight: 1.04,
    letterSpacing: -0.5,
    textTransform: 'uppercase',
    maxWidth: 1500,
  };

  const container: React.CSSProperties = {
    justifyContent: 'flex-end',
    alignItems: 'flex-start',
    paddingLeft: 120,
    paddingRight: 120,
    paddingBottom: 132,
    gap: 6,
  };

  if (style === 'maskslide') {
    const perLine = secF(fps, 0.14);
    return (
      <AbsoluteFill style={container}>
        {lines.map((text, i) => (
          <div key={i} style={rowStyle}>
            <Line text={text} index={i} startFrame={base + i * perLine} dur={dur} />
          </div>
        ))}
      </AbsoluteFill>
    );
  }

  // wordpop / emphasis — 単語ベース
  const perWord = style === 'wordpop' ? secF(fps, 0.06) : secF(fps, 0.04);
  let running = 0;
  return (
    <AbsoluteFill style={container}>
      {lines.map((text, li) => {
        const words = text.split(/\s+/).filter((w) => w.length > 0);
        return (
          <div key={li} style={rowStyle}>
            {words.map((w, wi) => {
              const gi = running++;
              // 決定論的な微小ディレイ揺らぎ（±1f 前後）
              const delayJitter = Math.round((random('kc-delay-' + gi) - 0.5) * 3);
              const start = base + gi * perWord + delayJitter;
              const emphasis = style === 'emphasis' && emphasisSet.has(norm(w));
              return (
                <Word
                  key={wi}
                  word={w}
                  index={gi}
                  startFrame={start}
                  emphasis={emphasis}
                  fastPop={style === 'wordpop'}
                  dur={dur}
                />
              );
            })}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// 公開コンポーネント
// ---------------------------------------------------------------------
export const KineticCaptions: React.FC<{
  lines: string[];
  style?: 'wordpop' | 'maskslide' | 'emphasis';
  emphasisWords?: string[];
  dur?: number;
}> = ({lines, style = 'wordpop', emphasisWords = [], dur}) => {
  const {durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;
  const emphasisSet = new Set(emphasisWords.map((w) => norm(w)));

  return (
    <AbsoluteFill>
      {/* 速い登場にモーションブラーの尾。保持中の行は微ブレスのみで尾は無視できる。 */}
      <Trail layers={6} lagInFrames={1.1} trailOpacity={0.5}>
        <Inner lines={lines} style={style} emphasisSet={emphasisSet} dur={total} />
      </Trail>
    </AbsoluteFill>
  );
};
