import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {Trail} from '@remotion/motion-blur';
import {BRAND} from '../../brand';
import {mulberry32} from './util';

// =====================================================================
// OralArgQuestionTally（口頭弁論の質問往復）
//   入力: 弁論の質問数（CLM-0009 関連。総数は象徴・断定しない）
//   モーション: 上段=Justices の 9 席（弧）／下段=Advocate。質問が発火するたび
//     席から下へ光が飛び（Trail）、下部タリーが方向性充填（持続キャリア）。
//     席は方向性に順次点灯（等速でない spring）。
//   深度レイヤー: 暗背景 / 斜光ベッド / 席の弧 + 質問弾道 / 充填タリー / ラベル
// =====================================================================

const {ink, navy, electric, silver, gold, white} = BRAND.color;

const SEATS = 9;
const QUESTIONS = 24; // 弁論の質問往復の象徴数（CLM-0009 関連・断定しない）
const SEED = 0x0a9c01;

export const OralArgQuestionTally: React.FC<{dur: number}> = ({dur}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // 9 席（上部の弧）
  const seats = React.useMemo(() => {
    const arr: {x: number; y: number}[] = [];
    const cx = 960;
    const cy = 640;
    const rx = 620;
    const ry = 300;
    for (let i = 0; i < SEATS; i++) {
      const a = Math.PI + (i + 0.5) * (Math.PI / SEATS); // 上半弧
      arr.push({x: cx + Math.cos(a) * rx, y: cy + Math.sin(a) * ry});
    }
    return arr;
  }, []);

  // 各質問: どの席から・いつ（決定論）
  const questions = React.useMemo(() => {
    const r = mulberry32(SEED);
    return Array.from({length: QUESTIONS}, (_, i) => ({
      seat: Math.floor(r() * SEATS),
      f: 20 + Math.round((i / QUESTIONS) * (dur - 60)),
    }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dur]);

  const askedCount = questions.filter((q) => frame >= q.f).length;
  const advocate = {x: 960, y: 940};

  return (
    <AbsoluteFill style={{background: `radial-gradient(120% 100% at 50% 40%, ${navy} 0%, ${ink} 86%)`, overflow: 'hidden'}}>
      {/* 斜光ベッド */}
      <AbsoluteFill style={{background: `radial-gradient(60% 50% at 50% 40%, ${electric}16 0%, transparent 72%)`, mixBlendMode: 'screen', transform: `translateY(${Math.sin(frame / 38) * 8}px)`}} />

      <div style={{position: 'absolute', top: 60, width: '100%', textAlign: 'center', fontFamily: BRAND.font.body, fontSize: 26, letterSpacing: 6, textTransform: 'uppercase', color: silver, opacity: interpolate(frame, [4, 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
        At oral argument
      </div>

      {/* 席の弧 */}
      {seats.map((s, i) => {
        const app = spring({frame: frame - i * 5 - 8, fps, config: {damping: 16}});
        // 直近にこの席が質問したら発火グロー
        const lastAsk = questions.filter((q) => q.seat === i && frame >= q.f).slice(-1)[0];
        const fire = lastAsk ? Math.exp(-(frame - lastAsk.f) / 8) : 0;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: s.x,
              top: s.y,
              transform: `translate(-50%, -50%) scale(${app})`,
              width: 60,
              height: 60,
              borderRadius: '50%',
              background: `radial-gradient(circle, ${navy}, ${ink})`,
              border: `3px solid ${fire > 0.05 ? gold : electric}`,
              boxShadow: fire > 0.05 ? `0 0 ${10 + fire * 30}px ${gold}` : `0 0 8px ${electric}55`,
            }}
          />
        );
      })}

      {/* 質問弾道（Trail・席→advocate） */}
      {questions.map((q, i) => {
        const t = interpolate(frame, [q.f, q.f + 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        if (t <= 0 || t >= 1) return null;
        const s = seats[q.seat];
        const te = 1 - Math.pow(1 - t, 2);
        const x = s.x + (advocate.x - s.x) * te;
        const y = s.y + (advocate.y - s.y) * te;
        return (
          <Trail key={i} layers={6} lagInFrames={0.35} trailOpacity={0.5}>
            <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', width: 14, height: 14, borderRadius: '50%', background: gold, boxShadow: `0 0 16px ${gold}`}} />
          </Trail>
        );
      })}

      {/* Advocate ノード */}
      <div style={{position: 'absolute', left: advocate.x, top: advocate.y, transform: 'translate(-50%,-50%)', width: 74, height: 40, borderRadius: 8, background: navy, border: `2px solid ${silver}`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: BRAND.font.body, fontSize: 16, letterSpacing: 2, color: silver}}>
        ADVOCATE
      </div>

      {/* 充填タリー（持続キャリア・方向性に伸びるバー） */}
      <div style={{position: 'absolute', bottom: 44, left: '50%', transform: 'translateX(-50%)', width: 900}}>
        <div style={{display: 'flex', justifyContent: 'space-between', fontFamily: BRAND.font.body, fontSize: 20, letterSpacing: 3, color: silver, textTransform: 'uppercase', marginBottom: 8}}>
          <span>Questions from the bench</span>
          <span style={{fontFamily: BRAND.font.display, fontSize: 30, color: white}}>{askedCount}</span>
        </div>
        <div style={{height: 14, background: `${silver}22`, borderRadius: 7, overflow: 'hidden'}}>
          <div style={{height: '100%', width: `${(askedCount / QUESTIONS) * 100}%`, background: `linear-gradient(90deg, ${electric}, ${gold})`, boxShadow: `0 0 16px ${gold}88`}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};
