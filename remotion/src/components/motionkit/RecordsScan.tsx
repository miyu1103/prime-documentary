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
// RecordsScan — "searching the records" scene (ULTRA-PREMIUM DB aesthetic)
//   ・monospace の記録行がマスク切れ上がりでスタッガー出現
//   ・electric のスキャンラインが上→下へイージング走査（グロー＋Trailブラー）
//   ・highlightIndex の行を通過するとロックオン：金の枠が strokeDashoffset で
//     描かれ、その行だけ僅かに拡大、他行はディム
//   ・薄いグリッド＋フリッカーの奥行きレイヤー
//   全モーションにイージング／spring・opacity単独リビール禁止・決定論的。
//   個人情報は出さない（既定は伏字プレースホルダー行を内部生成）。
// =====================================================================

const MONO =
  'ui-monospace, "SF Mono", "SFMono-Regular", "Consolas", "Liberation Mono", monospace';

// 秒→フレーム（fps基準・フレーム直書き禁止）
const sec = (fps: number, s: number) => Math.round(fps * s);

// レイアウト定数（1920x1080）
const PW = 1220; // パネル幅
const PX = (BRAND.video.width - PW) / 2; // パネル左
const ROW_PAD_X = 30;
const ROW_W = PW - ROW_PAD_X * 2;
const HEADER_H = 60;
const ROWS_TOP = HEADER_H + 40; // パネル内の行開始Y
const ROW_H = 70;
const ROW_GAP = 10;

// 伏字ブロック生成（決定論的：remotion random(seed)）
const block = (n: number) => '█'.repeat(Math.max(1, n));

type Row = {id: string; text: string; tail: string; date: string};

const buildRows = (count: number): Row[] =>
  Array.from({length: count}, (_, i) => {
    const idNum = 1000 + Math.floor(random('recid-' + i) * 8999);
    const nameLen = 7 + Math.floor(random('recnm-' + i) * 9); // 7..15
    const tailLen = 3 + Math.floor(random('rectl-' + i) * 4); // 3..6
    const yy = 1990 + Math.floor(random('recyr-' + i) * 33);
    return {
      id: 'REC-' + idNum,
      text: block(nameLen),
      tail: block(tailLen),
      date: `${yy}-██-██`,
    };
  });

// 行の中心Y（パネル内ローカル座標）
const rowCenterY = (i: number) => ROWS_TOP + i * (ROW_H + ROW_GAP) + ROW_H / 2;

// スキャン走査帯（パネル内ローカル座標）
const scanTopFor = () => ROWS_TOP - 26;
const scanBottomFor = (n: number) =>
  ROWS_TOP + n * ROW_H + (n - 1) * ROW_GAP + 26;

// 走査進捗 p（0..1）をイージング付きで返す
const scanProgress = (frame: number, start: number, end: number) =>
  interpolate(frame, [start, end], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

// ---------------------------------------------------------------------
// スキャンビーム（Trail の中で自分のフレームから位置を計算＝実モーションブラー）
// ---------------------------------------------------------------------
const ScanBeam: React.FC<{
  scanStart: number;
  scanEnd: number;
  travelTop: number;
  travelBottom: number;
}> = ({scanStart, scanEnd, travelTop, travelBottom}) => {
  const frame = useCurrentFrame();
  const p = scanProgress(frame, scanStart, scanEnd);
  const y = interpolate(p, [0, 1], [travelTop, travelBottom]);
  return (
    <>
      {/* 走査グロー帯（読み取り光） */}
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: y - 60,
          height: 120,
          background: `linear-gradient(180deg, transparent 0%, ${BRAND.color.electric}22 45%, ${BRAND.color.electric}33 50%, ${BRAND.color.electric}22 55%, transparent 100%)`,
          pointerEvents: 'none',
        }}
      />
      {/* 芯のスキャンライン */}
      <div
        style={{
          position: 'absolute',
          left: 8,
          right: 8,
          top: y,
          height: 2.5,
          background: BRAND.color.electric,
          boxShadow: `0 0 18px 2px ${BRAND.color.electric}, 0 0 44px 6px ${BRAND.color.electric}66`,
          pointerEvents: 'none',
        }}
      />
    </>
  );
};

export const RecordsScan: React.FC<{
  lines?: string[];
  highlightIndex?: number;
  dur?: number;
}> = ({lines, highlightIndex, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const D = dur ?? durationInFrames;

  // 行データ：lines 指定時はそれを中央テキストに（既定は伏字プレースホルダー）
  const rows: Row[] = React.useMemo(() => {
    if (lines && lines.length > 0) {
      return lines.map((t, i) => {
        const idNum = 1000 + Math.floor(random('recid-' + i) * 8999);
        const tailLen = 3 + Math.floor(random('rectl-' + i) * 4);
        const yy = 1990 + Math.floor(random('recyr-' + i) * 33);
        return {id: 'REC-' + idNum, text: t, tail: block(tailLen), date: `${yy}-██-██`};
      });
    }
    return buildRows(9);
  }, [lines]);

  const N = rows.length;
  const hi =
    highlightIndex !== undefined
      ? Math.max(0, Math.min(N - 1, Math.round(highlightIndex)))
      : Math.min(N - 1, Math.max(0, Math.round(N * 0.55)));

  const panelH = ROWS_TOP + N * ROW_H + (N - 1) * ROW_GAP + 34;
  const PY = (BRAND.video.height - panelH) / 2;

  // タイミング（fps基準）
  const startDelay = sec(fps, 0.15);
  const stagger = sec(fps, 0.06);
  const scanStart = sec(fps, 0.75);
  const scanEnd = Math.max(scanStart + sec(fps, 0.8), D - sec(fps, 0.4));

  // 走査帯（ローカル）
  const travelTop = scanTopFor();
  const travelBottom = scanBottomFor(N);

  // 走査進捗と、ハイライト行の通過ターゲット
  const p = scanProgress(frame, scanStart, scanEnd);
  const target =
    (rowCenterY(hi) - travelTop) / (travelBottom - travelTop);
  // ロック量（他行ディム・拡大の駆動）／枠描画の局所進捗
  const lockAmt = interpolate(p, [target - 0.01, target + 0.07], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const boxP = interpolate(p, [target, target + 0.16], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ハイライト枠の寸法（行ローカル）
  const boxPad = 8;
  const boxW = ROW_W + boxPad * 2;
  const boxH = ROW_H + boxPad * 2;
  const perim = 2 * (boxW + boxH);

  // グリッドのドリフト＋フリッカー（装飾・微translateと併用）
  const gridDrift = interpolate(frame, [0, D], [0, 34], {
    easing: Easing.inOut(Easing.sin),
  });
  const flicker =
    0.1 +
    0.04 * Math.sin(frame * 0.9) +
    0.02 * Math.sin(frame * 2.3 + 1.7);

  // ヘッダーの走査インジケータ点滅（装飾）
  const dotPulse = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(frame * 0.35));

  // シーン全体の入り（微translateY＋opacity＝単独opacity回避）
  const introIn = spring({frame, fps, config: {damping: 22, mass: 0.9}});
  const introY = interpolate(introIn, [0, 1], [26, 0]);
  const introO = interpolate(introIn, [0, 0.5], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f'}}>
      {/* depth 1: 全画面バックドロップ */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`,
        }}
      />

      {/* depth 2: 薄いグリッド（ドリフト＋フリッカー） */}
      <AbsoluteFill
        style={{
          opacity: flicker,
          transform: `translateY(${gridDrift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${BRAND.color.electric}22 0px, ${BRAND.color.electric}22 1px, transparent 1px, transparent 68px),
            repeating-linear-gradient(90deg, ${BRAND.color.electric}1a 0px, ${BRAND.color.electric}1a 1px, transparent 1px, transparent 68px)`,
          maskImage:
            'radial-gradient(115% 92% at 50% 45%, black 34%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(115% 92% at 50% 45%, black 34%, transparent 84%)',
          pointerEvents: 'none',
        }}
      />

      {/* depth 3: アンビエントグロー＋ビネット */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(70% 55% at 50% 40%, ${BRAND.color.electric}14 0%, transparent 60%), radial-gradient(120% 100% at 50% 48%, transparent 44%, rgba(0,0,0,0.62) 100%)`,
          pointerEvents: 'none',
        }}
      />

      {/* パネル（レコードインデックス） */}
      <div
        style={{
          position: 'absolute',
          left: PX,
          top: PY,
          width: PW,
          height: panelH,
          transform: `translateY(${introY}px)`,
          opacity: introO,
          borderRadius: 14,
          background: `linear-gradient(180deg, ${BRAND.color.navy}cc 0%, #070b16e6 100%)`,
          border: `1px solid ${BRAND.color.electric}33`,
          boxShadow: `0 30px 80px rgba(0,0,0,0.55), inset 0 1px 0 ${BRAND.color.silver}1a`,
          overflow: 'hidden',
        }}
      >
        {/* ヘッダー行 */}
        <div
          style={{
            position: 'absolute',
            left: ROW_PAD_X,
            right: ROW_PAD_X,
            top: 0,
            height: HEADER_H,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: `1px solid ${BRAND.color.silver}22`,
          }}
        >
          <span
            style={{
              fontFamily: BRAND.font.body,
              fontWeight: 700,
              fontSize: 22,
              letterSpacing: 5,
              textTransform: 'uppercase',
              color: BRAND.color.silver,
            }}
          >
            National Records Index
          </span>
          <span
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              fontFamily: MONO,
              fontSize: 18,
              letterSpacing: 3,
              color: BRAND.color.electric,
            }}
          >
            <span
              style={{
                width: 9,
                height: 9,
                borderRadius: '50%',
                background: BRAND.color.electric,
                opacity: dotPulse,
                boxShadow: `0 0 12px ${BRAND.color.electric}`,
              }}
            />
            SCANNING
          </span>
        </div>

        {/* レコード行 */}
        {rows.map((r, i) => {
          const top = rowCenterY(i) - ROW_H / 2;
          const isHi = i === hi;

          // 入場：マスク切れ上がり（overflow hidden + translateY）
          const ent = spring({
            frame: frame - startDelay - i * stagger,
            fps,
            config: {damping: 18, mass: 0.9},
          });
          const revealY = interpolate(ent, [0, 1], [100, 0]);
          const revealO = interpolate(ent, [0, 0.4], [0, 1], {
            extrapolateRight: 'clamp',
          });

          // ロック演出：主役は拡大／他行はディム
          const scale = isHi ? 1 + 0.05 * lockAmt : 1;
          const dim = isHi ? 1 : interpolate(lockAmt, [0, 1], [1, 0.34]);
          const rowBg = isHi
            ? `linear-gradient(90deg, ${BRAND.color.gold}1f 0%, ${BRAND.color.gold}0d 100%)`
            : `${BRAND.color.electric}0a`;

          return (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: ROW_PAD_X,
                top,
                width: ROW_W,
                height: ROW_H,
                overflow: 'hidden',
                borderRadius: 8,
                zIndex: isHi ? 3 : 1,
                transform: `scale(${scale})`,
                transformOrigin: 'center',
              }}
            >
              <div
                style={{
                  transform: `translateY(${revealY}%)`,
                  opacity: revealO,
                  height: '100%',
                }}
              >
                <div
                  style={{
                    height: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 26,
                    padding: '0 20px',
                    boxSizing: 'border-box',
                    borderRadius: 8,
                    background: rowBg,
                    border: `1px solid ${
                      isHi ? BRAND.color.gold + '55' : BRAND.color.silver + '14'
                    }`,
                    opacity: dim,
                    fontFamily: MONO,
                  }}
                >
                  {/* ステータスドット */}
                  <span
                    style={{
                      width: 8,
                      height: 8,
                      borderRadius: '50%',
                      flex: '0 0 auto',
                      background: isHi
                        ? BRAND.color.gold
                        : BRAND.color.electric,
                      boxShadow: isHi
                        ? `0 0 12px ${BRAND.color.gold}`
                        : 'none',
                    }}
                  />
                  {/* ID */}
                  <span
                    style={{
                      fontSize: 20,
                      letterSpacing: 1,
                      color: BRAND.color.silver,
                      width: 130,
                      flex: '0 0 auto',
                    }}
                  >
                    {r.id}
                  </span>
                  {/* 伏字メイン */}
                  <span
                    style={{
                      fontSize: 22,
                      letterSpacing: 2,
                      color: isHi ? BRAND.color.white : BRAND.color.silver,
                      flex: '1 1 auto',
                      overflow: 'hidden',
                      whiteSpace: 'nowrap',
                      textOverflow: 'clip',
                    }}
                  >
                    {r.text}
                  </span>
                  {/* 伏字テール */}
                  <span
                    style={{
                      fontSize: 22,
                      letterSpacing: 2,
                      color: `${BRAND.color.silver}99`,
                      flex: '0 0 auto',
                    }}
                  >
                    {r.tail}
                  </span>
                  {/* 日付 */}
                  <span
                    style={{
                      fontSize: 19,
                      letterSpacing: 1,
                      color: `${BRAND.color.silver}aa`,
                      width: 128,
                      textAlign: 'right',
                      flex: '0 0 auto',
                    }}
                  >
                    {r.date}
                  </span>
                  {/* ステータスチップ */}
                  <span
                    style={{
                      fontSize: 15,
                      letterSpacing: 2,
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: 4,
                      flex: '0 0 auto',
                      color: isHi ? BRAND.color.ink : BRAND.color.silver,
                      background: isHi
                        ? BRAND.color.gold
                        : `${BRAND.color.silver}1f`,
                    }}
                  >
                    {isHi ? 'MATCH' : 'SEALED'}
                  </span>
                </div>
              </div>
            </div>
          );
        })}

        {/* ハイライト枠（strokeDashoffset で描画） */}
        <svg
          width={PW}
          height={panelH}
          style={{
            position: 'absolute',
            inset: 0,
            pointerEvents: 'none',
            zIndex: 4,
            filter: `drop-shadow(0 0 10px ${BRAND.color.gold}aa)`,
            opacity: boxP > 0 ? 1 : 0,
          }}
        >
          <rect
            x={ROW_PAD_X - boxPad}
            y={rowCenterY(hi) - ROW_H / 2 - boxPad}
            width={boxW}
            height={boxH}
            rx={10}
            fill="none"
            stroke={BRAND.color.gold}
            strokeWidth={2.5}
            strokeDasharray={perim}
            strokeDashoffset={perim * (1 - boxP)}
          />
        </svg>

        {/* スキャンビーム（Trailでモーションブラー） */}
        <div style={{position: 'absolute', inset: 0, zIndex: 2}}>
          <Trail layers={6} lagInFrames={1.4} trailOpacity={0.55}>
            <ScanBeam
              scanStart={scanStart}
              scanEnd={scanEnd}
              travelTop={travelTop}
              travelBottom={travelBottom}
            />
          </Trail>
        </div>
      </div>

      {/* depth 4: 全画面フリッカー膜（微translateで単独opacity回避） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 45% at 50% ${
            42 + 4 * Math.sin(frame * 0.2)
          }%, ${BRAND.color.electric}0f 0%, transparent 70%)`,
          transform: `translateY(${interpolate(
            Math.sin(frame * 0.25),
            [-1, 1],
            [-3, 3],
          )}px)`,
          mixBlendMode: 'screen',
          opacity: 0.6,
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
