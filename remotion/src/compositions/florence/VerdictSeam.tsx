/**
 * VerdictSeam — an ORIGINAL, Florence-only animation (not a reused template).
 * Story beat: "Five to four — safety won. But read that fifth vote closely, and
 * the victory has a seam in it." Five gold tally marks and four silver marks
 * tally up, then collapse into a heavy "5–4". A stamp slams down: CONSTITUTIONAL.
 * Then a hairline CRACK draws itself across the stamp (the concurrences narrowing
 * it) — a faint warm light glows in the gap — and the seam holds. Restrained,
 * weighty. Self-contained (no image assets). No real names / PII / logos. 180f=6s.
 */
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../../brand';
import {FilmGrain, VignetteBreath, LightRays} from '../../components/motionkit';

export const verdictSeamDuration = 180;

// 秒→フレーム（フレーム直書きを避け fps から算出）
const sec = (fps: number, s: number) => Math.round(fps * s);

export const VerdictSeam: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // --- timeline anchors (all derived from fps) ---
  const marksStart = sec(fps, 0.1); // タリーマークが立ち上がり始める
  const collapseAt = sec(fps, 1.5); // マークが中央の 5–4 へ collapse
  const numAt = sec(fps, 1.55); // 大きな "5–4" が springs in
  const stampAt = sec(fps, 2.6); // CONSTITUTIONAL が slam down
  const crackFrom = sec(fps, 3.7); // 亀裂が描かれ始める
  const crackTo = sec(fps, 5.2); // 亀裂が描き終わる

  // 常時わずかに息づくグローバル呼吸（静止フレームを作らない）
  const breath = interpolate(Math.sin((f / fps) * 0.9), [-1, 1], [0.985, 1.015], {
    easing: Easing.inOut(Easing.sin),
  });

  // 大きな 5–4 の登場（overshoot spring）
  const numSpring = spring({frame: f - numAt, fps, config: {damping: 13, stiffness: 130}, durationInFrames: 30});
  const numScale = interpolate(numSpring, [0, 1], [0.7, 1]);
  const numY = interpolate(numSpring, [0, 1], [26, 0]);

  // スタンプの叩き込み（強い overshoot、素早く settle）
  const stampS = spring({frame: f - stampAt, fps, config: {damping: 11, stiffness: 200, mass: 0.9}, durationInFrames: 26});
  const stampScale = interpolate(stampS, [0, 1], [1.55, 1]);
  const stampOpacity = interpolate(f, [stampAt, stampAt + 4], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // 着地の瞬間に画面がわずかに沈む（インパクト）
  const impact = spring({frame: f - stampAt, fps, config: {damping: 9, stiffness: 240}, durationInFrames: 20});
  const impactY = (1 - impact) * 6;

  // 亀裂の描画進捗（0→1, eased）。faint light はやや遅れて追従。
  const crackP = interpolate(f, [crackFrom, crackTo], [0, 1], {
    easing: Easing.inOut(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const gapLight = interpolate(f, [crackFrom + sec(fps, 0.2), crackTo + sec(fps, 0.2)], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  // 描き終わりで一度だけ微かに震え、その後 seam が「保持」される
  const settle = interpolate(f, [crackTo, crackTo + sec(fps, 0.5)], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const seamShake = settle * Math.sin((f - crackTo) * 1.9) * 1.2;

  // 中央 5–4 はスタンプ着地でわずかに引くが、最終タリーとして常に明瞭に読める床を保つ
  const numFade = interpolate(f, [stampAt - 6, stampAt + 10], [1, 0.86], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  // レイアウト
  const cx = width / 2;
  const stampW = width * 0.5;
  const stampH = height * 0.2;
  const stampTop = height * 0.56;

  // 亀裂パス — CONSTITUTIONAL の文字を横断する hairline の破断線。帯の縦中央付近を
  // 走らせ、鋭く折れる。pathLength=1 正規化 + strokeDashoffset 1→0 で「裂けていく」。
  const midY = stampTop + stampH * 0.52;
  const jag = (fx: number, fy: number) => `${cx + stampW * fx} ${midY + stampH * fy}`;
  const crackPath = `M ${jag(-0.55, 0.05)}
    L ${jag(-0.40, -0.11)}
    L ${jag(-0.25, 0.07)}
    L ${jag(-0.10, -0.09)}
    L ${jag(0.05, 0.10)}
    L ${jag(0.20, -0.07)}
    L ${jag(0.36, 0.09)}
    L ${jag(0.55, -0.05)}`;

  // 5 本の金マーク（left cluster）と 4 本の銀マーク（right cluster）
  const goldMarks = 5;
  const silverMarks = 4;
  const clusterY = height * 0.34;

  const renderTally = (n: number, baseX: number, color: string, glow: string, seedOff: number) => (
    Array.from({length: n}).map((_, i) => {
      const appear = spring({frame: f - (marksStart + (seedOff + i) * 3), fps, config: {damping: 200}, durationInFrames: 16});
      // collapse: 中央 (cx) へ寄せてフェード
      const gone = interpolate(f, [collapseAt, collapseAt + sec(fps, 0.5)], [0, 1], {
        easing: Easing.inOut(Easing.cubic), extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
      });
      const x = interpolate(gone, [0, 1], [baseX + i * 26, cx]);
      const y = clusterY + (1 - appear) * -22;
      const op = appear * (1 - gone);
      const sc = interpolate(gone, [0, 1], [1, 0.4]);
      return (
        <div key={`m${seedOff}-${i}`} style={{
          position: 'absolute', left: x, top: y, width: 8, height: 66, marginLeft: -4,
          borderRadius: 4, background: color, opacity: op,
          transform: `translateY(${(1 - appear) * 18}px) scaleY(${appear}) scale(${sc})`,
          boxShadow: `0 0 14px ${glow}`,
        }} />
      );
    })
  );

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, justifyContent: 'center', alignItems: 'center', overflow: 'hidden'}}>
      {/* L1 背景グラデ */}
      <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 42%, ${BRAND.color.navy} 0%, ${BRAND.color.ink} 70%)`}} />
      {/* L1b 薄いグリッド（法廷の記録感） */}
      <AbsoluteFill style={{opacity: 0.07, backgroundImage: `linear-gradient(${BRAND.color.electric}55 1px, transparent 1px), linear-gradient(90deg, ${BRAND.color.electric}55 1px, transparent 1px)`, backgroundSize: '54px 54px'}} />

      {/* L2 大気オーバーレイ（gold の god-ray で「barely held」の緊張） */}
      <LightRays color={BRAND.color.gold} />
      <VignetteBreath />

      {/* L3 主役スタック */}
      <AbsoluteFill style={{transform: `translateY(${impactY}px) scale(${breath})`}}>
        {/* タリーマーク（左=金5, 右=銀4） */}
        {renderTally(goldMarks, cx - width * 0.24, BRAND.color.gold, `${BRAND.color.gold}88`, 0)}
        {renderTally(silverMarks, cx + width * 0.10, BRAND.color.silver, `${BRAND.color.silver}55`, 6)}

        {/* 大きな 5–4 の判決 */}
        <div style={{
          position: 'absolute', left: 0, right: 0, top: height * 0.29,
          display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 10,
          opacity: numFade, transform: `translateY(${numY}px) scale(${numScale})`,
        }}>
          {/* 5 = majority, solid gold */}
          <span style={{
            fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 176, color: BRAND.color.gold,
            textShadow: `0 0 34px ${BRAND.color.gold}88, 0 4px 10px #00000066`,
          }}>5</span>
          <span style={{
            fontFamily: BRAND.font.display, fontSize: 118, color: BRAND.color.silver, margin: '0 8px',
            transform: 'translateY(-14px)', opacity: 0.9,
          }}>–</span>
          {/* 4 = dissent, solid silver — same weight, equally intentional (a real final tally) */}
          <span style={{
            fontFamily: BRAND.font.display, fontWeight: 900, fontSize: 176, color: BRAND.color.silver,
            textShadow: `0 0 26px ${BRAND.color.silver}77, 0 4px 10px #00000066`,
          }}>4</span>
        </div>

        {/* スタンプ: CONSTITUTIONAL */}
        <div style={{
          position: 'absolute', left: cx - stampW / 2, top: stampTop, width: stampW, height: stampH,
          transform: `translateY(${seamShake}px) rotate(-3deg) scale(${stampScale})`, opacity: stampOpacity,
          border: `5px solid ${BRAND.color.gold}`, borderRadius: 10,
          display: 'flex', justifyContent: 'center', alignItems: 'center',
          boxShadow: `0 0 40px ${BRAND.color.gold}33, inset 0 0 26px ${BRAND.color.gold}22`,
          background: `${BRAND.color.navy}44`,
        }}>
          <span style={{
            fontFamily: BRAND.font.display, fontSize: 72, letterSpacing: 6, color: BRAND.color.gold,
            textShadow: `0 0 22px ${BRAND.color.gold}55`,
          }}>CONSTITUTIONAL</span>
        </div>

        {/* 亀裂（SEAM）— gap に welling する暖色光を下敷きに、その上に細い裂け目 */}
        <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0, pointerEvents: 'none'}}>
          {/* 1) 広く滲む暖色のグロー（裂け目から漏れる光。crack より少し遅れて灯る） */}
          <path d={crackPath} fill="none" stroke={BRAND.color.gold} strokeWidth={16}
            strokeLinecap="round" strokeLinejoin="round"
            pathLength={1} strokeDasharray={1} strokeDashoffset={1 - crackP}
            style={{filter: 'blur(12px)', opacity: gapLight * 0.9}} />
          {/* 2) 近接のホットな暖色コア（gap の芯） */}
          <path d={crackPath} fill="none" stroke="#FFE7A8" strokeWidth={6}
            strokeLinecap="round" strokeLinejoin="round"
            pathLength={1} strokeDasharray={1} strokeDashoffset={1 - crackP}
            style={{filter: 'blur(3px)', opacity: gapLight * 0.85}} />
          {/* 3) 影側（裂けた縁の下唇に落ちる陰） */}
          <path d={crackPath} fill="none" stroke="#000000" strokeWidth={5}
            strokeLinecap="round" strokeLinejoin="round"
            pathLength={1} strokeDasharray={1} strokeDashoffset={1 - crackP}
            style={{opacity: crackP * 0.5, transform: 'translateY(2px)'}} />
          {/* 4) hairline 本体（描かれていく鋭い裂け目） */}
          <path d={crackPath} fill="none" stroke="#FFF6E0" strokeWidth={2.6}
            strokeLinecap="round" strokeLinejoin="round"
            pathLength={1} strokeDasharray={1} strokeDashoffset={1 - crackP}
            style={{opacity: 0.95}} />
        </svg>
      </AbsoluteFill>

      {/* L4 グレイン（最前面） */}
      <FilmGrain />
    </AbsoluteFill>
  );
};
