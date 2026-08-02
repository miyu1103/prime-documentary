/**
 * WarrantScreen — an ORIGINAL, Florence-only animation (not a reused template).
 * The moment the trooper's computer flags Albert Florence: a records database
 * scans his name; every line clears — fine SATISFIED, PAID 2003 — but one line
 * refuses to die: a bench warrant that should have been deleted lights up red and
 * ACTIVE, and the machine believes the stale line over the truth. No real names /
 * numbers (anonymized record IDs). Self-contained (no image assets). 180f=6s.
 */
import React from 'react';
import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig, Easing} from 'remotion';
import {BRAND} from '../../brand';

const RED = '#C0473E';

type Row = {id: string; label: string; status: string; warrant?: boolean};
const ROWS: Row[] = [
  {id: 'REC·2291-A', label: 'Fine · installment plan', status: 'SATISFIED'},
  {id: 'REC·3308-B', label: 'Balance paid in full', status: 'PAID · 2003'},
  {id: 'REC·4471-C', label: 'Bench warrant · unpaid fine', status: 'ACTIVE', warrant: true},
  {id: 'REC·5120-D', label: 'Court fees', status: 'CLEARED'},
  {id: 'REC·6642-E', label: 'Case disposition', status: 'CLOSED'},
];

export const warrantScreenDuration = 180;

export const WarrantScreen: React.FC = () => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const boot = spring({frame: f, fps, config: {damping: 200}, durationInFrames: 24});
  const scan = interpolate(f, [20, 96], [0.16, 0.86], {easing: Easing.inOut(Easing.cubic), extrapolateRight: 'clamp'});
  const warrantHit = 92; // frame the scan reaches the warrant row
  const flag = spring({frame: f - warrantHit, fps, config: {damping: 12, stiffness: 140}, durationInFrames: 30});
  const pulse = 0.5 + 0.5 * Math.sin((f - warrantHit) / 4);

  const panelW = width * 0.72, panelH = height * 0.62;
  const rowH = panelH * 0.13;
  const top = (height - panelH) / 2;
  const left = (width - panelW) / 2;

  return (
    <AbsoluteFill style={{backgroundColor: BRAND.color.ink, justifyContent: 'center', alignItems: 'center'}}>
      {/* faint grid */}
      <AbsoluteFill style={{opacity: 0.10, backgroundImage: `linear-gradient(${BRAND.color.electric}55 1px, transparent 1px), linear-gradient(90deg, ${BRAND.color.electric}55 1px, transparent 1px)`, backgroundSize: '48px 48px'}} />
      {/* terminal panel */}
      <div style={{position: 'absolute', left, top, width: panelW, height: panelH,
        transform: `translateY(${(1 - boot) * 30}px)`, opacity: boot,
        background: `linear-gradient(180deg, ${BRAND.color.navy}F2, ${BRAND.color.ink}F2)`,
        border: `1px solid ${BRAND.color.electric}66`, borderRadius: 10, boxShadow: `0 20px 80px #000A, 0 0 40px ${BRAND.color.electric}22`, overflow: 'hidden'}}>
        {/* header */}
        <div style={{height: rowH * 0.9, display: 'flex', alignItems: 'center', padding: '0 28px', borderBottom: `1px solid ${BRAND.color.electric}44`, gap: 14}}>
          <div style={{width: 12, height: 12, borderRadius: '50%', background: BRAND.color.electric, boxShadow: `0 0 12px ${BRAND.color.electric}`}} />
          <div style={{fontFamily: BRAND.font.body, fontWeight: 800, letterSpacing: 3, fontSize: 26, color: BRAND.color.silver}}>STATE RECORDS · SEARCH</div>
          <div style={{marginLeft: 'auto', fontFamily: BRAND.font.body, fontSize: 20, color: `${BRAND.color.silver}99`}}>QUERY: OWNER / LICENSE</div>
        </div>
        {/* scan line */}
        <div style={{position: 'absolute', left: 0, right: 0, top: panelH * scan, height: 3, background: `linear-gradient(90deg, transparent, ${BRAND.color.electric}, transparent)`, boxShadow: `0 0 18px ${BRAND.color.electric}`, opacity: f > 96 ? 0 : 1}} />
        {/* rows */}
        {ROWS.map((r, i) => {
          const y = rowH * 0.9 + i * rowH + 10;
          const appear = spring({frame: f - (10 + i * 5), fps, config: {damping: 200}, durationInFrames: 18});
          const isW = r.warrant;
          const lit = isW ? flag : 1;
          const bg = isW ? `rgba(192,71,62,${0.10 + 0.28 * flag * pulse})` : 'transparent';
          const statusColor = isW ? RED : BRAND.color.silver;
          return (
            <div key={r.id} style={{position: 'absolute', left: 20, right: 20, top: y, height: rowH * 0.82,
              display: 'flex', alignItems: 'center', padding: '0 22px', gap: 20, opacity: appear,
              background: bg, border: isW ? `1px solid rgba(192,71,62,${0.4 * flag})` : `1px solid ${BRAND.color.electric}18`, borderRadius: 8}}>
              <div style={{fontFamily: BRAND.font.body, fontSize: 22, color: `${BRAND.color.silver}CC`, width: 200}}>{r.id}</div>
              <div style={{fontFamily: BRAND.font.body, fontSize: 24, color: BRAND.color.white}}>{r.label}</div>
              <div style={{marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 12}}>
                {isW ? <div style={{width: 12, height: 12, borderRadius: '50%', background: RED, boxShadow: `0 0 ${8 + 14 * pulse}px ${RED}`, opacity: flag}} /> : null}
                <div style={{fontFamily: BRAND.font.display, fontSize: isW ? 30 : 24, letterSpacing: 1, color: statusColor,
                  textShadow: isW ? `0 0 ${10 * flag * pulse}px ${RED}` : 'none', transform: `scale(${isW ? 1 + 0.06 * flag : 1})`}}>
                  {isW ? 'BENCH WARRANT · ACTIVE' : r.status}
                </div>
              </div>
            </div>
          );
        })}
        {/* the truth, struck out — appears after the flag */}
        <div style={{position: 'absolute', left: 42, top: panelH * 0.86, opacity: Math.max(0, flag - 0.2), fontFamily: BRAND.font.body, fontSize: 22, color: `${BRAND.color.silver}AA`}}>
          <span style={{textDecoration: 'line-through', textDecorationColor: RED}}>on record: fine PAID · 2003</span>
          <span style={{color: RED, marginLeft: 16, fontWeight: 800}}>— never cleared from the system</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
