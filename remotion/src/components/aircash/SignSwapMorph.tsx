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
// SignSwapMorph — 空港の押収主体が別機関へ「交代」する図（EP34 幕5 / #21）。
//   汎用の看板「AIRPORT CASH PROGRAM」が、空港の反転フラップ表示（Solari 式）で
//   一文字ずつ縦スクロールして「DHS / HSI / CBP」へ物理的にモーフ（＝主運動）。
//   同時に右下のオドメーター型「押収継続カウンタ」の桁リールが全編ずっと縦に転がる。
//   ・主運動＝実体の縦移動（フラップ・桁リール）。走光/暖光は不使用（分子外）。
//   ・カウンタは ILLUSTRATIVE（象徴）。未確認の正式名「TIP」は焼き込まない。
//   ・奥行き≥3層（暗青グラデ／金グリッド微ドリフト／ヴィネット）＋単一アクセント gold。
//   全モーション eased/spring・opacity単独なし・fps算出・deterministic（seeded mulberry32）。
// =====================================================================

const BG = '#06080f';
const BACKDROP = `radial-gradient(125% 105% at 50% 40%, ${BRAND.color.navy} 0%, ${BG} 82%)`;
const GOLD = BRAND.color.gold;

const sec = (fps: number, s: number) => Math.round(fps * s);

// 決定論的擬似乱数（Math.random 禁止）。反転フラップの途中グリフ選択に使う。
const mulberry32 = (a: number) => () => {
  a |= 0;
  a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const SEED = 0x726f6c69; // "roli"
const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/'.split('');

// 文字列を中央寄せで固定長へパディング（両ラベルを同じセル数に揃える）。
const padCenter = (s: string, n: number) => {
  if (s.length >= n) return s.slice(0, n);
  const total = n - s.length;
  const left = Math.floor(total / 2);
  return ' '.repeat(left) + s + ' '.repeat(total - left);
};

export type SignSwapMorphProps = {
  dur?: number;
  fromLabel?: string;
  toLabel?: string;
  // ILLUSTRATIVE な押収継続カウンタ（象徴・特定の事実額を主張しない）。
  counterBase?: number;
  counterRate?: number; // 単位/秒（桁リールの転がり速度を決める）
  illustrative?: boolean;
};

// 反転フラップ 1 セル（縦スクロールのリール）。overflow:hidden + translateY で切り上がる。
const FlapCell: React.FC<{
  strip: string[];
  targetIdx: number;
  ty: number;
  x: number;
  y: number;
  w: number;
  h: number;
  fontSize: number;
}> = ({strip, targetIdx, ty, x, y, w, h, fontSize}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: w,
      height: h,
      overflow: 'hidden',
      borderRadius: 7,
      background: `linear-gradient(180deg, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 55%, #000 100%)`,
      border: `2px solid rgba(0,0,0,0.65)`,
      boxShadow: `inset 0 0 14px rgba(0,0,0,0.75)`,
    }}
  >
    <div style={{transform: `translateY(${ty}px)`, willChange: 'transform'}}>
      {strip.map((ch, k) => (
        <div
          key={k}
          style={{
            height: h,
            lineHeight: `${h}px`,
            textAlign: 'center',
            fontFamily: BRAND.font.display,
            fontSize,
            letterSpacing: 1,
            color: k >= targetIdx ? GOLD : BRAND.color.silver,
            textShadow:
              k >= targetIdx
                ? `0 0 18px ${GOLD}aa`
                : '0 2px 6px rgba(0,0,0,0.8)',
          }}
        >
          {ch === ' ' ? ' ' : ch}
        </div>
      ))}
    </div>
    {/* スプリットフラップの中央ヒンジ線 */}
    <div
      style={{
        position: 'absolute',
        left: 0,
        top: h / 2 - 1,
        width: '100%',
        height: 2,
        background: 'rgba(0,0,0,0.85)',
        boxShadow: `0 1px 0 rgba(255,255,255,0.04)`,
      }}
    />
  </div>
);

// オドメーター 1 桁（0..9 の縦リール）。value に対し連続的に転がる＝止まらない実移動。
const DigitReel: React.FC<{
  place: number;
  value: number;
  x: number;
  y: number;
  w: number;
  h: number;
  fontSize: number;
}> = ({place, value, x, y, w, h, fontSize}) => {
  // (value / 10^place) mod 10 は value に対して連続なノコギリ波＝リールが滑らかに回る。
  const pos = ((value / Math.pow(10, place)) % 10 + 10) % 10;
  const ty = -pos * h;
  const digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width: w,
        height: h,
        overflow: 'hidden',
        borderRadius: 6,
        background: `linear-gradient(180deg, ${BRAND.color.ink} 0%, #000 100%)`,
        border: `2px solid rgba(0,0,0,0.6)`,
        boxShadow: `inset 0 0 12px rgba(0,0,0,0.8)`,
      }}
    >
      <div style={{transform: `translateY(${ty}px)`, willChange: 'transform'}}>
        {digits.map((d, k) => (
          <div
            key={k}
            style={{
              height: h,
              lineHeight: `${h}px`,
              textAlign: 'center',
              fontFamily: BRAND.font.display,
              fontSize,
              color: GOLD,
              textShadow: `0 0 14px ${GOLD}88`,
            }}
          >
            {d}
          </div>
        ))}
      </div>
    </div>
  );
};

export const SignSwapMorph: React.FC<SignSwapMorphProps> = ({
  dur,
  fromLabel = 'AIRPORT CASH PROGRAM',
  toLabel = 'DHS / HSI / CBP',
  counterBase = 480000,
  counterRate = 3.7,
  illustrative = true,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;
  const tSec = frame / fps;

  // ---- 看板レイアウト（fps 非依存の空間定数）----
  const cols = Math.max(fromLabel.length, toLabel.length);
  const fromChars = padCenter(fromLabel, cols).split('');
  const toChars = padCenter(toLabel, cols).split('');

  const CELL_W = 78;
  const GAP = 8;
  const CELL_H = 112;
  const PITCH = CELL_W + GAP;
  const boardW = cols * PITCH - GAP;
  const boardX0 = Math.round((width - boardW) / 2);
  const boardY = 348;
  const cellFont = 60;

  // ---- スワップ・タイムライン（全て秒→fps 算出）----
  const SWAP_START = 2.0; // 看板が崩れ始める
  const STAGGER = 0.2; // 列ごとのディレイ（左→右へカスケード）

  // 各列の反転フラップ：spring で縦スクロール（少しアンダーダンプ＝機械的カチッ）。
  const columns = fromChars.map((fc, i) => {
    const tc = toChars[i];
    const rng = mulberry32(SEED + i * 97);
    const scramble = [0, 1, 2].map(() => GLYPHS[Math.floor(rng() * GLYPHS.length)]);
    // 末尾に to を二重化：spring のオーバーシュートでも常に着地文字が見える。
    const strip = [fc, scramble[0], scramble[1], scramble[2], tc, tc];
    const targetIdx = strip.length - 2; // 最初の to（着地インデックス）
    const startF = sec(fps, SWAP_START + i * STAGGER);
    const sp = spring({
      frame: frame - startF,
      fps,
      config: {damping: 12, mass: 0.9, stiffness: 150},
    });
    const ty = interpolate(sp, [0, 1], [0, -targetIdx * CELL_H]);
    return {strip, targetIdx, ty};
  });

  // ---- 押収継続カウンタ（ILLUSTRATIVE・全編ずっと転がる実移動）----
  const counterValue = counterBase + counterRate * tSec;
  const DIGITS = 6;
  const DW = 52;
  const DGAP = 6;
  const DH = 78;
  const digitFont = 62;
  const commaW = 16;
  const groupW = DIGITS * (DW + DGAP) - DGAP + commaW; // カンマ 1 個分
  const counterX0 = Math.round((width - groupW) / 2) + 40;
  const counterY = boardY + CELL_H + 168;

  // ---- 背景の微ドリフト（凍らない微シマー）----
  const gridDrift = interpolate(frame, [0, D], [0, 34], {
    easing: Easing.inOut(Easing.sin),
  });

  // ---- キャプション（マスク切れ上がり）----
  const capSp = spring({frame: frame - sec(fps, 0.3), fps, config: {damping: 16}});
  const capY = interpolate(capSp, [0, 1], [120, 0]);
  const capO = interpolate(capSp, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  const subSp = spring({frame: frame - sec(fps, 0.55), fps, config: {damping: 17}});
  const subY = interpolate(subSp, [0, 1], [100, 0]);
  const subO = interpolate(subSp, [0, 0.3], [0, 1], {extrapolateRight: 'clamp'});

  // カウンタのラベルは押収が「続く」ことをスワップ完了に合わせて強調（scale+translateY）。
  const swapDone = interpolate(
    frame,
    [sec(fps, SWAP_START + cols * STAGGER), sec(fps, SWAP_START + cols * STAGGER + 1.0)],
    [0, 1],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );

  // ---- シーン出入り＋全体パララックス（settle 後も止まらない微運動）----
  const inO = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const outO = interpolate(frame, [D - 12, D], [1, 0], {extrapolateLeft: 'clamp'});
  const inY = interpolate(frame, [0, 14], [20, 0], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const driftX = 12 * Math.sin((frame / fps) * ((2 * Math.PI) / 7.4));
  const driftY = 8 * Math.sin((frame / fps) * ((2 * Math.PI) / 6.1) + 0.5);

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: BACKDROP}} />
      {/* L2 金グリッド（微ドリフト＝凍らない） */}
      <AbsoluteFill
        style={{
          opacity: 0.08,
          transform: `translateY(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px),
            repeating-linear-gradient(90deg, ${GOLD}22 0px, ${GOLD}22 1px, transparent 1px, transparent 76px)`,
          maskImage: 'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 30%, transparent 82%)',
        }}
      />
      {/* L3 ヴィネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, transparent 44%, rgba(0,0,0,0.7) 100%)',
        }}
      />

      <AbsoluteFill
        style={{
          opacity: inO * outO,
          transform: `translate(${driftX}px, ${inY + driftY}px)`,
        }}
      >
        {/* 上部キャプション（マスク切れ上がり） */}
        <div
          style={{
            position: 'absolute',
            top: 150,
            left: 0,
            width: '100%',
            textAlign: 'center',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              transform: `translateY(${capY}%)`,
              opacity: capO,
              fontFamily: BRAND.font.display,
              fontSize: 46,
              letterSpacing: 3,
              color: BRAND.color.white,
            }}
          >
            THE SAME SEIZURES, A DIFFERENT AGENCY
          </div>
        </div>
        <div
          style={{
            position: 'absolute',
            top: 214,
            left: 0,
            width: '100%',
            textAlign: 'center',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              transform: `translateY(${subY}%)`,
              opacity: subO,
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 24,
              letterSpacing: 6,
              color: BRAND.color.silver,
            }}
          >
            SEIZING AGENCY
          </div>
        </div>

        {/* 看板の吊り下げアーム＋プレート土台（奥） */}
        <svg
          width={width}
          height={height}
          style={{position: 'absolute', inset: 0}}
        >
          {/* 吊りアーム */}
          <line
            x1={boardX0 + boardW * 0.32}
            y1={boardY - 60}
            x2={boardX0 + boardW * 0.32}
            y2={boardY - 18}
            stroke={`${BRAND.color.silver}66`}
            strokeWidth={5}
          />
          <line
            x1={boardX0 + boardW * 0.68}
            y1={boardY - 60}
            x2={boardX0 + boardW * 0.68}
            y2={boardY - 18}
            stroke={`${BRAND.color.silver}66`}
            strokeWidth={5}
          />
          {/* プレート土台（セル背後） */}
          <rect
            x={boardX0 - 22}
            y={boardY - 22}
            width={boardW + 44}
            height={CELL_H + 44}
            rx={18}
            fill={BRAND.color.ink}
            stroke={GOLD}
            strokeWidth={3}
            style={{filter: `drop-shadow(0 0 22px ${GOLD}55)`}}
          />
        </svg>

        {/* 看板＝反転フラップ（主運動）。Trail は AbsoluteFill をラップ（inline flex row を直接ラップしない）。 */}
        <Trail layers={5} lagInFrames={1.2} trailOpacity={0.42}>
          <AbsoluteFill>
            {columns.map((c, i) => (
              <FlapCell
                key={i}
                strip={c.strip}
                targetIdx={c.targetIdx}
                ty={c.ty}
                x={boardX0 + i * PITCH}
                y={boardY}
                w={CELL_W}
                h={CELL_H}
                fontSize={cellFont}
              />
            ))}
          </AbsoluteFill>
        </Trail>

        {/* カウンタのラベル（押収は続く） */}
        <div
          style={{
            position: 'absolute',
            top: counterY - 52,
            left: 0,
            width: '100%',
            textAlign: 'center',
            transform: `translateY(${interpolate(swapDone, [0, 1], [24, 0])}px) scale(${interpolate(
              swapDone,
              [0, 1],
              [0.92, 1],
            )})`,
            opacity: interpolate(swapDone, [0, 1], [0.35, 1]),
            fontFamily: BRAND.font.body,
            fontWeight: 700,
            fontSize: 22,
            letterSpacing: 5,
            color: BRAND.color.silver,
          }}
        >
          SEIZURES CONTINUE
        </div>

        {/* オドメーター型 押収継続カウンタ（全編ずっと転がる＝持続する実移動）。Trail は AbsoluteFill をラップ。 */}
        <Trail layers={4} lagInFrames={1.0} trailOpacity={0.4}>
          <AbsoluteFill>
            {Array.from({length: DIGITS}).map((_, j) => {
              // j=0 が最左（最上位桁）。カンマは左から 3 桁目の後ろに挿入。
              const place = DIGITS - 1 - j;
              const commaShift = j >= 3 ? commaW : 0;
              const x = counterX0 + j * (DW + DGAP) + commaShift;
              return (
                <DigitReel
                  key={j}
                  place={place}
                  value={counterValue}
                  x={x}
                  y={counterY}
                  w={DW}
                  h={DH}
                  fontSize={digitFont}
                />
              );
            })}
          </AbsoluteFill>
        </Trail>
        {/* カンマ（静的セパレータ） */}
        <div
          style={{
            position: 'absolute',
            top: counterY + DH - 34,
            left: counterX0 + 3 * (DW + DGAP) - DGAP,
            width: commaW,
            textAlign: 'center',
            fontFamily: BRAND.font.display,
            fontSize: digitFont,
            color: GOLD,
          }}
        >
          ,
        </div>

        {/* ILLUSTRATIVE チップ（特定の事実額を主張しない印） */}
        {illustrative ? (
          <div
            style={{
              position: 'absolute',
              top: counterY + DH + 22,
              left: 0,
              width: '100%',
              textAlign: 'center',
            }}
          >
            <span
              style={{
                display: 'inline-block',
                padding: '5px 14px',
                borderRadius: 6,
                border: `1px solid ${GOLD}88`,
                background: `${GOLD}14`,
                fontFamily: BRAND.font.body,
                fontWeight: 700,
                fontSize: 15,
                letterSpacing: 3,
                color: GOLD,
              }}
            >
              ILLUSTRATIVE
            </span>
          </div>
        ) : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
