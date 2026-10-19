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
// VoteTally — 法廷の評決を可視化するシネマティックSCENE（MOTIONKIT）
//   多数意見(majority)＋反対意見(dissent)の席を、番号順にスタッガーで点灯。
//   多数=ゴールド、反対=抑えたマットレッド('#C0473E')。点灯は spring の
//   スケール(ポップ)と「無点灯→点灯色」への色遷移をペアで行う（opacity単独禁止）。
//   点灯し切った後に、巨大な評決数 "8–1" がマスク切り上がりで出現（tabular-nums）。
//   任意ラベルは下段にマスク切り上がり。フルスクリーンのダーク背景・常時微動。
//   決定論的（useCurrentFrame＋席index・乱数/日時なし）・全モーションにイージング。
//   5–4 / 8–1 / 9–0 のような最高裁評決に使用。
// =====================================================================

// 反対意見の抑えたマットレッド（ブランドトークン外・仕様指定）
const DISSENT_RED = '#C0473E';
// 無点灯の席の下地（深いネイビーグレー）
const SEAT_DARK = '#1B2740';

// 秒→フレーム（fps基準・フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

// 2つのhexを線形補間（点灯色遷移用・純関数）
const hexToRgb = (h: string): readonly [number, number, number] => {
  const s = h.replace('#', '');
  return [
    parseInt(s.slice(0, 2), 16),
    parseInt(s.slice(2, 4), 16),
    parseInt(s.slice(4, 6), 16),
  ] as const;
};
const mixHex = (a: string, b: string, t: number): string => {
  const [ar, ag, ab] = hexToRgb(a);
  const [br, bg, bb] = hexToRgb(b);
  const r = Math.round(ar + (br - ar) * t);
  const g = Math.round(ag + (bg - ag) * t);
  const bl = Math.round(ab + (bb - ab) * t);
  return `rgb(${r}, ${g}, ${bl})`;
};

// マスク切り上がりの数字/文字パーツ（overflow:hidden＋内側translateY＋Trail）
const MaskReveal: React.FC<{
  active: number; // spring 進捗 0..1
  color: string;
  fontSize: number;
  fontFamily: string;
  weight: number;
  letter?: number;
  children: React.ReactNode;
}> = ({active, color, fontSize, fontFamily, weight, letter = 0, children}) => {
  const y = interpolate(active, [0, 1], [118, 0]);
  const o = interpolate(active, [0, 0.26], [0, 1], {extrapolateRight: 'clamp'});
  return (
    <span
      style={{
        display: 'inline-block',
        overflow: 'hidden',
        paddingBottom: '0.14em',
        verticalAlign: 'top',
      }}
    >
      <Trail layers={6} lagInFrames={1.1} trailOpacity={0.45}>
        <span
          style={{
            display: 'inline-block',
            transform: `translateY(${y}%)`,
            opacity: o,
            color,
            fontFamily,
            fontWeight: weight,
            fontSize,
            letterSpacing: letter,
            lineHeight: 1,
            whiteSpace: 'pre',
          }}
        >
          {children}
        </span>
      </Trail>
    </span>
  );
};

export const VoteTally: React.FC<{
  majority: number;
  dissent: number;
  label?: string;
  dur?: number;
}> = ({majority, dissent, label, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames, width, height} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // 席の総数（多数→反対の順に並べる）
  const seatCount = Math.max(1, Math.round(majority) + Math.round(dissent));
  const majCount = Math.max(0, Math.round(majority));

  // タイムライン（すべて fps 由来）
  const seatStart = sec(fps, 0.28); // 最初の席の点灯
  const seatStagger = Math.max(1, sec(fps, 0.11)); // 席ごとのディレイ
  const seatsDone = seatStart + seatCount * seatStagger;
  const numStart = seatsDone + sec(fps, 0.3); // 評決数の出現
  const numStagger = sec(fps, 0.12);
  const labelStart = numStart + sec(fps, 0.42); // ラベル
  const outStart = total - sec(fps, 0.5); // シーン退出

  // シーン全体の出入り（opacity単独禁止 → 微translateYと必ず併用）
  const sceneO = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const sceneY = interpolate(
    frame,
    [0, sec(fps, 0.4), outStart, total],
    [22, 0, 0, 18],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  // 常時わずかな呼吸ドリフト（静止させない）
  const breath = Math.sin((frame / fps) * 1.1) * 3;

  // 席のレイアウト（緩やかなベンチのアーチ）
  const denom = Math.max(1, seatCount - 1);
  const seatR = seatCount <= 9 ? 32 : Math.max(15, Math.round(300 / seatCount));
  const gap = Math.min(156, seatCount <= 1 ? 0 : 1220 / denom);
  const rowW = gap * denom;

  // 席バンド（アーチ）の寸法。席は band 内のローカル座標で絶対配置する。
  const ARCH = 46; // アーチで中央席が持ち上がる量
  const seatsBandH = seatR * 2 + ARCH; // 席バンドの縦の広がり
  const bandW = rowW + seatR * 2; // 端の席の円まで含む幅

  // グループ内の縦の間隔（席バンド→評決数→アンダーライン→ラベル）。
  // グループ全体を flex で縦センタリングするため、順序と間隔だけを定義する。
  const GROUP_GAP = 80; // 席バンドと評決数の間隔（席の“下”に評決数を置く）
  const UNDERLINE_MT = 18; // 評決数→アンダーライン
  const UNDERLINE_H = 4; // アンダーライン高さ
  const LABEL_MT = 34; // アンダーライン→ラベル
  const LABEL_H = 34; // ラベル文字高

  // 評決数のフォントサイズ。基準300。グループ全体が画面高−上下マージン(各80px)に
  // 収まらない場合のみ縮小し、全要素がフレーム内に収まりクリップしないことを保証する。
  const NUM_FS_BASE = 300;
  const EDGE_MARGIN = 80; // 全フレーム端からの最小クリアランス
  const maxGroupH = height - EDGE_MARGIN * 2; // 1080 → 920
  // 数字行の実効高さ ≒ fontSize×1.14（lineHeight1 + paddingBottom0.14em 相当）。
  const fixedH =
    seatsBandH +
    GROUP_GAP +
    UNDERLINE_MT +
    UNDERLINE_H +
    (label ? LABEL_MT + LABEL_H : 0);
  const numFS =
    fixedH + NUM_FS_BASE * 1.14 <= maxGroupH
      ? NUM_FS_BASE
      : Math.max(120, Math.floor((maxGroupH - fixedH) / 1.14));
  const dashFS = Math.round(numFS * 0.7333); // ダッシュは数字より一回り小さく

  // 評決数の spring（多数→ダッシュ→反対の順にスタッガー）
  const majS = spring({
    frame: frame - numStart,
    fps,
    config: {damping: 17, mass: 0.9, stiffness: 130},
  });
  const dashS = spring({
    frame: frame - numStart - numStagger,
    fps,
    config: {damping: 17, mass: 0.9, stiffness: 130},
  });
  const disS = spring({
    frame: frame - numStart - numStagger * 2,
    fps,
    config: {damping: 17, mass: 0.9, stiffness: 130},
  });

  // 評決数の下に描かれるアンダーライン（scaleX spring・中心origin）
  const underlineS = spring({
    frame: frame - numStart - numStagger * 2 - sec(fps, 0.1),
    fps,
    config: {damping: 22, mass: 1, stiffness: 90},
  });
  const underlineX = interpolate(underlineS, [0, 1], [0, 1]);

  // ラベルのマスク切り上がり
  const labelS = spring({
    frame: frame - labelStart,
    fps,
    config: {damping: 18, mass: 0.9, stiffness: 120},
  });
  const labelY = interpolate(labelS, [0, 1], [110, 0]);
  const labelO = interpolate(labelS, [0, 0.3], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // 背景の浮遊ダスト（決定論的・常時ドリフト）
  const DUST = 14;

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      {/* Layer 1: フルスクリーン背景グラデ（指定の SCENE backdrop） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* Layer 2: 抑えたグリッド＋ビネット（奥行き） */}
      <AbsoluteFill
        style={{
          opacity: 0.1,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 96px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 96px)`,
          transform: `translateY(${breath * 1.4}px)`,
          maskImage: 'radial-gradient(120% 85% at 50% 46%, black 24%, transparent 78%)',
          WebkitMaskImage:
            'radial-gradient(120% 85% at 50% 46%, black 24%, transparent 78%)',
        }}
      />

      {/* Layer 3: 決定論的な浮遊ダスト（常時ドリフト・静止しない） */}
      <AbsoluteFill style={{opacity: 0.5}}>
        {new Array(DUST).fill(0).map((_, i) => {
          const bx = random('vt-dust-x' + i) * width;
          const by = random('vt-dust-y' + i) * 1080;
          const size = 1.5 + random('vt-dust-s' + i) * 3;
          const speed = 0.25 + random('vt-dust-v' + i) * 0.5;
          const phase = random('vt-dust-p' + i) * Math.PI * 2;
          const dx = Math.sin((frame / fps) * speed + phase) * 22;
          const dy = Math.cos((frame / fps) * speed * 0.8 + phase) * 16;
          const tw = 0.25 + (Math.sin((frame / fps) * 1.3 + phase) * 0.5 + 0.5) * 0.6;
          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: bx,
                top: by,
                width: size,
                height: size,
                borderRadius: '50%',
                backgroundColor: BRAND.color.silver,
                opacity: tw,
                transform: `translate(${dx}px, ${dy}px)`,
                boxShadow: `0 0 ${size * 3}px ${BRAND.color.electric}66`,
              }}
            />
          );
        })}
      </AbsoluteFill>

      {/* Layer 4: 評決グループ（席バンド→評決数→アンダーライン→ラベル）を
          1つの flex 列として画面中央に縦センタリング。DOM順で評決数は必ず
          席の“下の独立行”になり、justifyContent:center でフレーム端クリップを防ぐ。 */}
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          opacity: sceneO,
          transform: `translateY(${sceneY + breath}px)`,
        }}
      >
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          {/* 席バンド（スタッガー点灯・spring スケール＋色遷移）。band 内ローカル座標。 */}
          <div style={{position: 'relative', width: bandW, height: seatsBandH}}>
            {new Array(seatCount).fill(0).map((_, i) => {
              const isMajority = i < majCount;
              const litColor = isMajority ? BRAND.color.gold : DISSENT_RED;

              // 席位置（緩やかなアーチ：中央がわずかに持ち上がる）
              const u = seatCount <= 1 ? 0.5 : i / denom;
              const cx = seatR + gap * i; // band 内ローカルX（左端の席円の中心=seatR）
              const cy = ARCH + seatR - Math.sin(u * Math.PI) * ARCH; // band 内ローカルY

              // アイドルの微上下（決定論的・静止しない）
              const bob = Math.sin((frame / fps) * 1.5 + i * 0.6) * 2.4;

              // 点灯 spring（overshoot でポップ）
              const cs = spring({
                frame: frame - seatStart - i * seatStagger,
                fps,
                config: {damping: 12, mass: 0.8, stiffness: 150},
              });
              const lit = interpolate(cs, [0, 1], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              // スケールはポップ（overshoot 反映のため cs をそのまま写像）
              const scale = interpolate(cs, [0, 1], [0.5, 1]);
              // 色は「無点灯下地→点灯色」へ遷移（opacity単独ではない）
              const fill = mixHex(SEAT_DARK, litColor, lit);
              const glow = interpolate(cs, [0, 1], [0, seatR * 1.5], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const ringA = Math.round(60 + lit * 140);

              return (
                <div
                  key={i}
                  style={{
                    position: 'absolute',
                    left: cx - seatR,
                    top: cy - seatR + bob,
                    width: seatR * 2,
                    height: seatR * 2,
                    transform: `scale(${scale})`,
                    transformOrigin: 'center center',
                  }}
                >
                  {/* 下地リング（常時見える＝奥行き・静止させない微光） */}
                  <div
                    style={{
                      position: 'absolute',
                      inset: 0,
                      borderRadius: '50%',
                      border: `2px solid rgba(200, 205, 214, ${(ringA / 255).toFixed(3)})`,
                    }}
                  />
                  {/* 点灯ディスク（色遷移＋グロー） */}
                  <div
                    style={{
                      position: 'absolute',
                      inset: 4,
                      borderRadius: '50%',
                      backgroundColor: fill,
                      boxShadow: `0 0 ${glow}px ${litColor}`,
                    }}
                  />
                </div>
              );
            })}
          </div>

          {/* 評決数 "M–D"（tabular-nums・マスク切り上がり）＝席バンドの下の独立行 */}
          <div
            style={{
              display: 'flex',
              alignItems: 'baseline',
              justifyContent: 'center',
              fontVariantNumeric: 'tabular-nums',
              lineHeight: 1,
              marginTop: GROUP_GAP,
            }}
          >
            <MaskReveal
              active={majS}
              color={BRAND.color.gold}
              fontSize={numFS}
              fontFamily={BRAND.font.display}
              weight={900}
              letter={-4}
            >
              {String(Math.round(majority))}
            </MaskReveal>
            <MaskReveal
              active={dashS}
              color={BRAND.color.silver}
              fontSize={dashFS}
              fontFamily={BRAND.font.display}
              weight={900}
              letter={-2}
            >
              {'–'}
            </MaskReveal>
            <MaskReveal
              active={disS}
              color={DISSENT_RED}
              fontSize={numFS}
              fontFamily={BRAND.font.display}
              weight={900}
              letter={-4}
            >
              {String(Math.round(dissent))}
            </MaskReveal>
          </div>

          {/* アンダーライン：scaleX spring（中心origin）で描画 */}
          <div
            style={{
              marginTop: UNDERLINE_MT,
              width: 420,
              height: UNDERLINE_H,
              borderRadius: 2,
              background: `linear-gradient(90deg, ${BRAND.color.gold} 0%, ${BRAND.color.silver} 50%, ${DISSENT_RED} 100%)`,
              transform: `scaleX(${underlineX})`,
              transformOrigin: 'center center',
              boxShadow: `0 0 18px ${BRAND.color.gold}66`,
            }}
          />

          {/* 任意ラベル：マスク切り上がり */}
          {label ? (
            <div
              style={{
                overflow: 'hidden',
                paddingBottom: '0.14em',
                marginTop: LABEL_MT,
              }}
            >
              <div
                style={{
                  transform: `translateY(${labelY}%)`,
                  opacity: labelO,
                  fontFamily: BRAND.font.body,
                  fontWeight: 600,
                  fontSize: LABEL_H,
                  letterSpacing: 6,
                  textTransform: 'uppercase',
                  color: BRAND.color.silver,
                  whiteSpace: 'nowrap',
                }}
              >
                {label}
              </div>
            </div>
          ) : null}
        </div>
      </AbsoluteFill>

      {/* Layer 6: シネマティックなビネット（最前面の抑え） */}
      <AbsoluteFill
        style={{
          pointerEvents: 'none',
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 52%, rgba(0,0,0,0.55) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
