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

/**
 * EP19 "Operation Varsity Blues" — MEANINGFUL motion graphics.
 *
 * Every graphic here explains a specific beat of the story (not decorative
 * "PowerPoint" motion). Each obeys the house quality rules:
 *   - all movement eased (spring / Easing.out(cubic)); no linear creep
 *   - multi-element beats stagger in
 *   - at least one fast element carries motion blur (Trail)
 *   - built in layers, drawn as vector so it stays crisp at 1080p60
 *
 * Each component is mounted inside its shot's <Sequence>, so useCurrentFrame()
 * is local (0 = the moment the beat begins). Graphics are meant to sit OVER a
 * darkened hero still / b-roll, so backgrounds are transparent.
 */

const {ink, electric, gold, white, silver} = BRAND.color;
const RED = '#D84B4B';
const DISPLAY = BRAND.font.display;
const BODY = BRAND.font.body;

/** ease-out cubic 0..1 over [a,b] frames. */
const eio = (frame: number, a: number, b: number): number =>
  interpolate(frame, [a, b], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic),
  });

const Label: React.FC<{
  x: number;
  y: number;
  kicker?: string;
  title: string;
  accent?: string;
  appear: number;
  w?: number;
}> = ({x, y, kicker, title, accent = gold, appear, w = 360}) => (
  <div
    style={{
      position: 'absolute',
      left: x,
      top: y,
      width: w,
      textAlign: 'center',
      transform: `translateY(${interpolate(appear, [0, 1], [26, 0])}px)`,
      opacity: appear,
    }}
  >
    {kicker ? (
      <div style={{fontFamily: BODY, fontSize: 20, fontWeight: 800, letterSpacing: 3, color: accent, textTransform: 'uppercase'}}>
        {kicker}
      </div>
    ) : null}
    <div style={{fontFamily: DISPLAY, fontSize: 40, color: white, textTransform: 'uppercase', lineHeight: 1, marginTop: 6, textShadow: '0 3px 18px #000'}}>
      {title}
    </div>
  </div>
);

/** A single vector "door" that can open. */
const Door: React.FC<{
  cx: number;
  open: number; // 0 closed .. 1 open
  glow: string;
  emphasise?: boolean;
}> = ({cx, open, glow, emphasise}) => {
  const w = 150;
  const h = 300;
  const x = cx - w / 2;
  const y = 300;
  const swing = interpolate(open, [0, 1], [1, 0.16]); // horizontal squash = perspective open
  return (
    <g>
      {/* frame */}
      <rect x={x - 12} y={y - 12} width={w + 24} height={h + 12} rx={6} fill="none" stroke={emphasise ? gold : `${silver}88`} strokeWidth={emphasise ? 5 : 3} />
      {/* dark interior revealed when open */}
      <rect x={x} y={y} width={w} height={h} fill={`${ink}`} />
      <rect x={x} y={y} width={w} height={h} fill={`url(#doorglow-${cx})`} opacity={open} />
      {/* the swinging leaf */}
      <g transform={`translate(${x} ${y}) scale(${swing} 1)`} style={{transformOrigin: `0px ${y}px`}}>
        <rect x={0} y={0} width={w} height={h} rx={3} fill={emphasise ? '#141821' : '#0f1115'} stroke={emphasise ? gold : silver} strokeWidth={2} />
        <circle cx={w - 22} cy={h / 2} r={5} fill={emphasise ? gold : silver} />
      </g>
      <defs>
        <radialGradient id={`doorglow-${cx}`} cx="50%" cy="46%" r="60%">
          <stop offset="0%" stopColor={glow} stopOpacity="0.9" />
          <stop offset="100%" stopColor={glow} stopOpacity="0" />
        </radialGradient>
      </defs>
    </g>
  );
};

/**
 * THE THREE DOORS — the core metaphor. Front (earned, uncertain), Back (legal,
 * a fortune), Side (Singer's secret, a GUARANTEE). The side door opens, a figure
 * walks straight through, and a gold GUARANTEE stamp slams in with motion blur.
 */
export const ThreeDoors: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const d1 = spring({frame: frame - f(0.3), fps, config: {damping: 16, stiffness: 90}});
  const d2 = spring({frame: frame - f(1.1), fps, config: {damping: 16, stiffness: 90}});
  const d3 = spring({frame: frame - f(1.9), fps, config: {damping: 16, stiffness: 90}});

  // side door opens late, then figure walks + stamp slams
  const sideOpen = spring({frame: frame - f(3.0), fps, config: {damping: 18, stiffness: 60}});
  const walk = eio(frame, f(3.6), f(5.0));
  const stamp = spring({frame: frame - f(5.0), fps, config: {damping: 9, stiffness: 130, mass: 0.9}});
  const stampScale = interpolate(stamp, [0, 1], [2.2, 1]);

  const cxs = [width * 0.24, width * 0.5, width * 0.76];
  const figX = interpolate(walk, [0, 1], [cxs[2] - 130, cxs[2]]);
  const figO = interpolate(walk, [0, 0.2], [0, 1], {extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} 1080`}>
        {/* ground line */}
        <line x1={120} y1={604} x2={width - 120} y2={604} stroke={`${silver}44`} strokeWidth={2} />
        <g transform={`scale(${interpolate(d1, [0, 1], [0.9, 1])})`} style={{transformOrigin: 'center'}}>
          <Door cx={cxs[0]} open={interpolate(d1, [0, 1], [0, 0.28])} glow={`${silver}`} />
        </g>
        <Door cx={cxs[1]} open={interpolate(d2, [0, 1], [0, 0.45])} glow={electric} />
        <Door cx={cxs[2]} open={sideOpen} glow={gold} emphasise />

        {/* figure walking through the side door */}
        <g opacity={figO} transform={`translate(${figX} 430)`}>
          <circle cx={0} cy={0} r={20} fill={gold} />
          <rect x={-15} y={24} width={30} height={90} rx={12} fill={gold} />
        </g>
      </svg>

      <Label x={cxs[0] - 180} y={640} kicker="Door 1" title="Front Door" accent={silver} appear={d1} />
      <div style={{position: 'absolute', left: cxs[0] - 180, top: 712, width: 360, textAlign: 'center', opacity: d1, fontFamily: BODY, fontSize: 22, color: silver}}>
        You earn it. No promises.
      </div>

      <Label x={cxs[1] - 180} y={640} kicker="Door 2" title="Back Door" accent={electric} appear={d2} />
      <div style={{position: 'absolute', left: cxs[1] - 180, top: 712, width: 360, textAlign: 'center', opacity: d2, fontFamily: BODY, fontSize: 22, color: silver}}>
        A fortune to the school. Legal — no guarantee.
      </div>

      <Label x={cxs[2] - 180} y={640} kicker="Door 3 · Singer's" title="Side Door" accent={gold} appear={d3} />

      {/* GUARANTEE stamp slamming in with motion blur */}
      <div style={{position: 'absolute', left: '50%', top: 812, transform: 'translateX(-50%)', opacity: Math.min(1, stamp * 1.4), pointerEvents: 'none'}}>
        <Trail layers={6} lagInFrames={1.3} trailOpacity={0.4}>
          <div style={{transform: `scale(${stampScale}) rotate(-7deg)`, border: `5px solid ${gold}`, color: gold, fontFamily: DISPLAY, fontSize: 46, letterSpacing: 4, padding: '8px 26px', textTransform: 'uppercase', background: '#000000cc', boxShadow: `0 0 34px ${gold}88`, whiteSpace: 'nowrap'}}>
            Guarantee
          </div>
        </Trail>
      </div>
    </AbsoluteFill>
  );
};

/**
 * THE LAUNDRY — a bribe dressed as a charitable donation. Parent → writes a
 * check → "Key Worldwide Foundation (charity)" → back out to a coach as a bribe,
 * with a "no goods or services" tax-receipt stamp and a $25M running total.
 */
export const MoneyLaundry: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const parent = spring({frame: frame - f(0.3), fps, config: {damping: 18, stiffness: 90}});
  const charity = spring({frame: frame - f(1.4), fps, config: {damping: 18, stiffness: 90}});
  const coach = spring({frame: frame - f(2.6), fps, config: {damping: 18, stiffness: 90}});
  const flow1 = eio(frame, f(1.0), f(1.8));
  const flow2 = eio(frame, f(2.2), f(3.0));
  const receipt = spring({frame: frame - f(3.4), fps, config: {damping: 10, stiffness: 120}});

  // $25M counter
  const cnt = eio(frame, f(3.8), f(5.4));
  const dollars = Math.round(interpolate(cnt, [0, 1], [0, 25]));

  const yMid = 470;
  const xs = [width * 0.2, width * 0.5, width * 0.8];

  const Node: React.FC<{x: number; appear: number; label: string; sub: string; color: string}> = ({x, appear, label, sub, color}) => (
    <div
      style={{
        position: 'absolute',
        left: x - 150,
        top: yMid - 70,
        width: 300,
        height: 140,
        borderRadius: 14,
        border: `3px solid ${color}`,
        background: '#05070bE8',
        boxShadow: `0 0 30px ${color}44`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        transform: `scale(${interpolate(appear, [0, 1], [0.8, 1])})`,
        opacity: appear,
      }}
    >
      <div style={{fontFamily: DISPLAY, fontSize: 34, color: white, textTransform: 'uppercase'}}>{label}</div>
      <div style={{fontFamily: BODY, fontSize: 20, color, marginTop: 6, textAlign: 'center', padding: '0 14px'}}>{sub}</div>
    </div>
  );

  const Arrow: React.FC<{x0: number; x1: number; p: number; label: string; color: string}> = ({x0, x1, p, label, color}) => {
    const cx = interpolate(p, [0, 1], [x0, x1]);
    return (
      <>
        <svg width="100%" height="100%" viewBox={`0 0 ${width} 1080`} style={{position: 'absolute', inset: 0}}>
          <line x1={x0} y1={yMid} x2={interpolate(p, [0, 1], [x0, x1])} y2={yMid} stroke={color} strokeWidth={5} strokeDasharray="2 10" strokeLinecap="round" />
        </svg>
        <div style={{position: 'absolute', left: cx - 22, top: yMid - 20, opacity: p}}>
          <Trail layers={5} lagInFrames={1.1} trailOpacity={0.38}>
            <div style={{fontFamily: DISPLAY, fontSize: 34, color: gold}}>$</div>
          </Trail>
        </div>
        <div style={{position: 'absolute', left: (x0 + x1) / 2 - 120, top: yMid + 30, width: 240, textAlign: 'center', opacity: p, fontFamily: BODY, fontSize: 18, color: silver}}>{label}</div>
      </>
    );
  };

  return (
    <AbsoluteFill>
      <Arrow x0={xs[0] + 150} x1={xs[1] - 150} p={flow1} label="a generous check" color={gold} />
      <Arrow x0={xs[1] + 150} x1={xs[2] - 150} p={flow2} label="quietly, a bribe" color={RED} />
      <Node x={xs[0]} appear={parent} label="Parent" sub="wants a guarantee" color={silver} />
      <Node x={xs[1]} appear={charity} label="“Charity”" sub="Key Worldwide Foundation" color={gold} />
      <Node x={xs[2]} appear={coach} label="Coach" sub="waves the fake recruit in" color={RED} />

      {/* tax receipt stamp */}
      <div
        style={{
          position: 'absolute',
          left: xs[1] - 190,
          top: yMid + 96,
          width: 380,
          transform: `rotate(-4deg) scale(${interpolate(receipt, [0, 1], [1.6, 1])})`,
          opacity: Math.min(1, receipt * 1.4),
          border: `3px dashed ${gold}`,
          color: gold,
          fontFamily: BODY,
          fontWeight: 800,
          fontSize: 20,
          textAlign: 'center',
          padding: '8px 10px',
          background: '#000000bb',
        }}
      >
        “NO GOODS OR SERVICES EXCHANGED” — tax-deductible
      </div>

      {/* running total */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 210, textAlign: 'center', opacity: cnt}}>
        <div style={{fontFamily: BODY, fontSize: 22, letterSpacing: 3, color: silver, textTransform: 'uppercase'}}>Paid to Singer over ~8 years</div>
        <div style={{fontFamily: DISPLAY, fontSize: 96, color: gold, textShadow: `0 0 40px ${gold}66`}}>${dollars}M</div>
      </div>
    </AbsoluteFill>
  );
};

/**
 * THE TARGET SCORE — Riddell could hit a chosen score on demand. A gauge needle
 * eases precisely onto a target; the number counts up and locks; a caption notes
 * 24 students across 27 exams.
 */
export const TargetScore: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const cx = width / 2;
  const cy = 560;
  const r = 240;
  // needle sweeps from low to a locked "chosen" score
  const sweep = spring({frame: frame - f(0.6), fps, config: {damping: 14, stiffness: 55}});
  const angle = interpolate(sweep, [0, 1], [-90, 46]); // deg, target ~ upper right
  const score = Math.round(interpolate(sweep, [0, 1], [400, 1340]));
  const lock = spring({frame: frame - f(2.6), fps, config: {damping: 8, stiffness: 130}});
  const stats = spring({frame: frame - f(3.2), fps, config: {damping: 18, stiffness: 90}});

  const a = (angle * Math.PI) / 180;
  const nx = cx + Math.cos(a) * (r - 30);
  const ny = cy + Math.sin(a) * (r - 30);

  const ticks = Array.from({length: 11}, (_, i) => {
    const ta = ((-90 + i * 18) * Math.PI) / 180;
    return {x1: cx + Math.cos(ta) * (r - 6), y1: cy + Math.sin(ta) * (r - 6), x2: cx + Math.cos(ta) * r, y2: cy + Math.sin(ta) * r};
  });

  return (
    <AbsoluteFill>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} 1080`}>
        {/* dial arc */}
        <path d={`M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}`} fill="none" stroke={`${silver}55`} strokeWidth={5} />
        {ticks.map((t, i) => (
          <line key={i} x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2} stroke={i >= 8 ? gold : `${silver}99`} strokeWidth={i >= 8 ? 5 : 3} />
        ))}
        {/* target zone */}
        <path d={`M ${cx} ${cy} L ${cx + Math.cos((28 * Math.PI) / 180) * r} ${cy + Math.sin((28 * Math.PI) / 180) * r} A ${r} ${r} 0 0 1 ${cx + Math.cos((64 * Math.PI) / 180) * r} ${cy + Math.sin((64 * Math.PI) / 180) * r} Z`} fill={`${gold}22`} />
        {/* needle */}
        <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={gold} strokeWidth={7} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={16} fill={gold} />
      </svg>

      {/* score readout */}
      <div style={{position: 'absolute', left: 0, right: 0, top: cy - 40, textAlign: 'center'}}>
        <div style={{fontFamily: DISPLAY, fontSize: 120, color: white, textShadow: `0 0 34px ${gold}55`, transform: `scale(${interpolate(lock, [0, 1], [1, 1.06])})`}}>{score}</div>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: 250, textAlign: 'center'}}>
        <div style={{fontFamily: BODY, fontSize: 24, letterSpacing: 3, color: silver, textTransform: 'uppercase'}}>A score, hit on demand</div>
      </div>
      {/* lock flash */}
      <div style={{position: 'absolute', left: '50%', top: 726, transform: 'translateX(-50%)', opacity: lock > 0.05 ? 1 : 0, pointerEvents: 'none'}}>
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.4}>
          <div style={{fontFamily: DISPLAY, fontSize: 30, color: gold, border: `4px solid ${gold}`, padding: '4px 18px', transform: `rotate(-6deg) scale(${interpolate(lock, [0, 1], [1.8, 1])})`, background: '#000000cc', whiteSpace: 'nowrap'}}>LOCKED</div>
        </Trail>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 250, textAlign: 'center', opacity: stats, transform: `translateY(${interpolate(stats, [0, 1], [20, 0])}px)`}}>
        <span style={{fontFamily: DISPLAY, fontSize: 44, color: gold}}>24 students</span>
        <span style={{fontFamily: BODY, fontSize: 30, color: silver}}>{'  ·  '}</span>
        <span style={{fontFamily: DISPLAY, fontSize: 44, color: white}}>27 exams</span>
      </div>
    </AbsoluteFill>
  );
};

/**
 * THE FAKE ATHLETE — a recruit built out of paper. A blank profile fills in,
 * field by field (staggered), with invented facts; a RECRUITED stamp lands, then
 * a large INVENTED overprint reveals the whole thing was fabricated.
 */
export const FakeAthlete: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const card = spring({frame: frame - f(0.2), fps, config: {damping: 18, stiffness: 90}});
  const rows = [
    {k: 'SPORT', v: 'Crew — coxswain'},
    {k: 'CLUB', v: 'elite team (never played)'},
    {k: '2K TIME', v: 'invented'},
    {k: 'RANKING', v: 'fabricated'},
  ];
  const recruit = spring({frame: frame - f(3.4), fps, config: {damping: 9, stiffness: 120}});
  const invented = spring({frame: frame - f(4.4), fps, config: {damping: 11, stiffness: 90}});

  const cardX = width / 2 - 330;
  return (
    <AbsoluteFill>
      <div
        style={{
          position: 'absolute',
          left: cardX,
          top: 300,
          width: 660,
          height: 460,
          borderRadius: 16,
          border: `3px solid ${electric}`,
          background: '#05070bF0',
          boxShadow: `0 0 40px ${electric}33`,
          transform: `translateY(${interpolate(card, [0, 1], [40, 0])}px)`,
          opacity: card,
          overflow: 'hidden',
        }}
      >
        <div style={{display: 'flex', alignItems: 'center', gap: 22, padding: '26px 30px', borderBottom: `1px solid ${silver}33`}}>
          {/* photo placeholder */}
          <div style={{width: 96, height: 96, borderRadius: 8, background: `${silver}22`, border: `2px solid ${silver}66`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: BODY, color: silver, fontSize: 14, textAlign: 'center'}}>staged<br />photo</div>
          <div>
            <div style={{fontFamily: BODY, fontSize: 18, letterSpacing: 3, color: gold, textTransform: 'uppercase'}}>Recruited Athlete Profile</div>
            <div style={{fontFamily: DISPLAY, fontSize: 44, color: white, textTransform: 'uppercase'}}>Applicant #—</div>
          </div>
        </div>
        <div style={{padding: '18px 34px'}}>
          {rows.map((row, i) => {
            const rs = spring({frame: frame - f(1.0 + i * 0.5), fps, config: {damping: 18, stiffness: 120}});
            return (
              <div key={row.k} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', padding: '13px 0', borderBottom: `1px solid ${silver}1f`, opacity: rs, transform: `translateX(${interpolate(rs, [0, 1], [30, 0])}px)`}}>
                <span style={{fontFamily: BODY, fontSize: 20, letterSpacing: 2, color: silver, textTransform: 'uppercase'}}>{row.k}</span>
                <span style={{fontFamily: DISPLAY, fontSize: 30, color: i >= 2 ? RED : white}}>{row.v}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* RECRUITED stamp */}
      <div style={{position: 'absolute', left: '50%', top: 250, transform: 'translateX(-50%)', opacity: recruit > 0.05 ? 1 : 0, pointerEvents: 'none'}}>
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.4}>
          <div style={{fontFamily: DISPLAY, fontSize: 34, color: gold, border: `4px solid ${gold}`, padding: '4px 16px', transform: `rotate(-8deg) scale(${interpolate(recruit, [0, 1], [1.8, 1])})`, background: '#000000cc', whiteSpace: 'nowrap'}}>RECRUITED</div>
        </Trail>
      </div>

      {/* INVENTED overprint */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', pointerEvents: 'none'}}>
        <div style={{transform: `rotate(-8deg) scale(${interpolate(invented, [0, 1], [2.4, 1])})`, opacity: Math.min(1, invented * 1.3)}}>
          <div style={{fontFamily: DISPLAY, fontSize: 128, color: RED, textShadow: '0 0 40px #000', letterSpacing: 6}}>INVENTED</div>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/**
 * SENTENCE COMPARE — the two famous names, exact and careful. Bars grow (eased)
 * to their prison terms; wording locks noted underneath.
 */
export const SentenceCompare: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const rows = [
    {name: 'Felicity Huffman', pay: '$15,000', term: '14 days', units: 14 / 150, note: 'pleaded guilty · fraud conspiracy'},
    {name: 'Lori Loughlin', pay: '$500,000', term: '2 months', units: 60 / 150, note: 'fraud conspiracy only'},
    {name: 'M. Giannulli', pay: '(same scheme)', term: '5 months', units: 150 / 150, note: 'laundering/bribery dismissed'},
  ];
  const title = spring({frame: frame - f(0.2), fps, config: {damping: 18, stiffness: 90}});
  const maxW = width * 0.5;

  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 210, textAlign: 'center', opacity: title}}>
        <div style={{fontFamily: BODY, fontSize: 22, letterSpacing: 3, color: silver, textTransform: 'uppercase'}}>Who buys a guarantee — and what it cost them</div>
      </div>
      {rows.map((r, i) => {
        const rs = spring({frame: frame - f(0.8 + i * 0.6), fps, config: {damping: 18, stiffness: 90}});
        const grow = interpolate(spring({frame: frame - f(1.1 + i * 0.6), fps, config: {damping: 20, stiffness: 60}}), [0, 1], [0, 1]);
        const y = 340 + i * 150;
        return (
          <div key={r.name} style={{position: 'absolute', left: width * 0.16, top: y, opacity: rs}}>
            <div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
              <span style={{fontFamily: DISPLAY, fontSize: 40, color: white, textTransform: 'uppercase', width: 420}}>{r.name}</span>
              <span style={{fontFamily: BODY, fontSize: 24, color: gold}}>{r.pay}</span>
            </div>
            <div style={{marginTop: 10, height: 34, width: maxW * r.units * grow, background: `linear-gradient(90deg, ${electric}, ${gold})`, borderRadius: 6, boxShadow: `0 0 20px ${gold}55`}} />
            <div style={{marginTop: 8, display: 'flex', gap: 16, alignItems: 'baseline'}}>
              <span style={{fontFamily: DISPLAY, fontSize: 30, color: gold}}>{r.term}</span>
              <span style={{fontFamily: BODY, fontSize: 18, color: silver}}>{r.note}</span>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

/**
 * SCARCITY OF SEATS — elite admission is not a faucet; it is a fixed number of
 * chairs. A grid fills; one seat turns gold ("TAKEN"), one empties ("someone
 * else"), and a line of figures waits outside behind it.
 */
export const SeatsScarcity: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const cols = 8;
  const rowsN = 4;
  const total = cols * rowsN;
  const gx = 150;
  const gy = 300;
  const cell = 118;
  const takenIndex = 11;

  const title = spring({frame: frame - f(0.2), fps, config: {damping: 18, stiffness: 90}});
  const grab = spring({frame: frame - f(3.2), fps, config: {damping: 10, stiffness: 120}});

  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 0, right: 0, top: 200, textAlign: 'center', opacity: title}}>
        <div style={{fontFamily: BODY, fontSize: 22, letterSpacing: 3, color: silver, textTransform: 'uppercase'}}>Elite admission is a fixed number of seats</div>
      </div>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} 1080`}>
        {Array.from({length: total}, (_, i) => {
          const c = i % cols;
          const rr = Math.floor(i / cols);
          const x = gx + c * cell;
          const y = gy + rr * cell;
          const appear = spring({frame: frame - f(0.6) - i * 2, fps, config: {damping: 18, stiffness: 120}});
          const isTaken = i === takenIndex;
          const fill = isTaken ? gold : `${electric}`;
          const op = interpolate(appear, [0, 1], [0, isTaken ? 1 : 0.5]);
          const s = interpolate(isTaken ? grab : appear, [0, 1], [isTaken ? 1 : 0.7, isTaken ? 1.18 : 1]);
          // simple chair glyph
          return (
            <g key={i} transform={`translate(${x} ${y}) scale(${s})`} opacity={op} style={{transformOrigin: `${x}px ${y}px`}}>
              <rect x={-30} y={-14} width={60} height={20} rx={4} fill={fill} />
              <rect x={-30} y={-54} width={12} height={44} rx={4} fill={fill} />
              <rect x={-30} y={4} width={10} height={34} fill={fill} />
              <rect x={20} y={4} width={10} height={34} fill={fill} />
            </g>
          );
        })}
      </svg>
      <div style={{position: 'absolute', left: 504, top: 470, transform: 'translateX(-50%)', opacity: grab > 0.05 ? 1 : 0, pointerEvents: 'none'}}>
        <Trail layers={5} lagInFrames={1.1} trailOpacity={0.4}>
          <div style={{fontFamily: DISPLAY, fontSize: 34, color: ink, background: gold, padding: '4px 18px', transform: `rotate(-6deg) scale(${interpolate(grab, [0, 1], [1.8, 1])})`, whiteSpace: 'nowrap'}}>TAKEN</div>
        </Trail>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 250, textAlign: 'center', opacity: grab}}>
        <span style={{fontFamily: BODY, fontSize: 26, color: silver}}>When someone buys a seat — </span>
        <span style={{fontFamily: DISPLAY, fontSize: 40, color: gold}}>someone else pays.</span>
      </div>
    </AbsoluteFill>
  );
};

/**
 * THE COLLAPSE — one morning in 2019. A wiretap waveform runs, a date snaps in,
 * and an arrest counter races to 50 with motion blur.
 */
export const Collapse: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);

  const date = spring({frame: frame - f(0.3), fps, config: {damping: 12, stiffness: 110}});
  const count = eio(frame, f(1.6), f(3.6));
  const arrested = Math.round(interpolate(count, [0, 1], [0, 50]));
  const punch = spring({frame: frame - f(3.6), fps, config: {damping: 9, stiffness: 130}});

  // wiretap waveform
  const bars = 60;
  const cx0 = width * 0.5 - (bars * 14) / 2;

  return (
    <AbsoluteFill>
      <svg width="100%" height="100%" viewBox={`0 0 ${width} 1080`}>
        {Array.from({length: bars}, (_, i) => {
          const t = frame * 0.14 + i * 0.5;
          const amp = 20 + Math.abs(Math.sin(t)) * (40 + (i % 5) * 12);
          const on = interpolate(frame, [i * 0.6, i * 0.6 + 8], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return <rect key={i} x={cx0 + i * 14} y={300 - amp / 2} width={7} height={amp} rx={3} fill={electric} opacity={0.25 + 0.5 * on} />;
        })}
      </svg>

      <div style={{position: 'absolute', left: 0, right: 0, top: 360, textAlign: 'center', opacity: date, transform: `scale(${interpolate(date, [0, 1], [1.4, 1])})`}}>
        <div style={{fontFamily: BODY, fontSize: 24, letterSpacing: 4, color: silver, textTransform: 'uppercase'}}>The morning it collapsed</div>
        <div style={{fontFamily: DISPLAY, fontSize: 84, color: white}}>March 12, 2019</div>
      </div>

      <div style={{position: 'absolute', left: 0, right: 0, top: 560, textAlign: 'center'}}>
        <span style={{fontFamily: DISPLAY, fontSize: 150, color: gold, textShadow: `0 0 40px ${gold}66`, transform: `scale(${interpolate(punch, [0, 1], [1, 1.05])})`, display: 'inline-block'}}>{arrested}</span>
        <div style={{fontFamily: DISPLAY, fontSize: 46, color: white, letterSpacing: 3, textTransform: 'uppercase', marginTop: -10}}>arrested at once</div>
      </div>

      <div style={{position: 'absolute', left: '50%', bottom: 250, transform: 'translateX(-50%)', opacity: punch > 0.05 ? 1 : 0, pointerEvents: 'none'}}>
        <Trail layers={6} lagInFrames={1.3} trailOpacity={0.42}>
          <div style={{fontFamily: DISPLAY, fontSize: 32, color: gold, border: `4px solid ${gold}`, padding: '4px 20px', transform: `rotate(-5deg) scale(${interpolate(punch, [0, 1], [2, 1])})`, background: '#000000cc', whiteSpace: 'nowrap'}}>THE SIDE DOOR SLAMS SHUT</div>
        </Trail>
      </div>
    </AbsoluteFill>
  );
};

/** Registry: which meaningful graphic (if any) plays over a given span. */
export const GRAPHIC_FOR_SPAN: Record<string, React.FC> = {
  'SPN-0004': ThreeDoors,
  'SPN-0005': ThreeDoors,
  'SPN-0016': MoneyLaundry,
  'SPN-0017': MoneyLaundry,
  'SPN-0027': TargetScore,
  'SPN-0028': TargetScore,
  'SPN-0035': FakeAthlete,
  'SPN-0036': FakeAthlete,
  'SPN-0043': SentenceCompare,
  'SPN-0044': SentenceCompare,
  'SPN-0053': SeatsScarcity,
  'SPN-0054': SeatsScarcity,
  'SPN-0064': Collapse,
  'SPN-0065': Collapse,
  'SPN-0074': SeatsScarcity,
};
