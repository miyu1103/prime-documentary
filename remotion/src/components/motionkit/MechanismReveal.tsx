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
// MechanismReveal — フルスクリーンの「概念メカニズム」演出（3種）。
//   kind='closingdoor' : ベクター製の扉が spring/eased の rotateY で閉まり、
//                        最後にボルト錠がカチッと差し込まれる（ロッククリック）。
//   kind='gears'       : 噛み合う歯車が順番にスピンアップ（eased 回転＝「機構」）。
//   kind='faultsplit'  : 地盤/枠が断層線に沿って spring で割れ、破片が決定論的に散る。
//   共通: シーン背景 radial-gradient・奥行き3層以上・単一アクセント(electric)・
//         速い部分に @remotion/motion-blur の Trail。全モーション eased（線形禁止）・
//         opacity 単独禁止・乱数は remotion random(seed) で決定論・常時わずかに動く。
//   dur=有効フレーム数（既定 durationInFrames）。
// =====================================================================

const sec = (fps: number, s: number) => Math.round(fps * s);

// 単一アクセント（このコンポーネント全体で electric のみ）
const ACCENT = BRAND.color.electric;

// 指定のフルスクリーン・シーン背景
const SCENE_BG = `radial-gradient(125% 105% at 50% 42%, ${BRAND.color.navy} 0%, #06080f 82%)`;

// 速い部分に掛ける共通モーションブラー設定
const FAST_TRAIL = {layers: 6, lagInFrames: 1.1, trailOpacity: 0.5} as const;

// ---------------------------------------------------------------------
// 奥行きレイヤー（背景グラデ / パースグリッド / アクセントグロー）＝3層
// ---------------------------------------------------------------------
const DepthLayers: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  // グリッドは緩やかにドリフト（静止しない・sin は本質的に eased）
  const drift = interpolate(frame, [0, durationInFrames], [-22, 22], {
    easing: Easing.inOut(Easing.sin),
  });
  // グローは常時わずかに呼吸
  const pulse = 0.5 + 0.5 * Math.sin((frame / fps) * 1.3);

  return (
    <>
      {/* L1: シーン背景グラデ */}
      <AbsoluteFill style={{background: SCENE_BG}} />

      {/* L2: パースの効いた薄いグリッド（奥行き） */}
      <AbsoluteFill
        style={{
          opacity: 0.15,
          transform: `translateY(${drift}px)`,
          backgroundImage: `
            repeating-linear-gradient(0deg, ${ACCENT}26 0px, ${ACCENT}26 1px, transparent 1px, transparent 86px),
            repeating-linear-gradient(90deg, ${ACCENT}26 0px, ${ACCENT}26 1px, transparent 1px, transparent 86px)`,
          maskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
          WebkitMaskImage:
            'radial-gradient(120% 92% at 50% 46%, black 26%, transparent 84%)',
        }}
      />

      {/* L3: アクセントグロー（呼吸で常時可変） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(46% 42% at 50% 47%, ${ACCENT}55 0%, transparent 62%)`,
          opacity: 0.34 + 0.2 * pulse,
          mixBlendMode: 'screen',
        }}
      />

      {/* ビネット（縁を締める・奥行き補助） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 46%, transparent 44%, rgba(0,0,0,0.72) 100%)',
        }}
      />
    </>
  );
};

// =====================================================================
// kind='closingdoor'
// =====================================================================

// 扉パネル本体（Trail の内側で useCurrentFrame を読む＝ラグ複製がアニメする）
const DoorPanel: React.FC<{total: number}> = ({total}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  // 扉が閉まる：spring の rotateY（-84° 開 → 0° 閉、わずかにスラム）
  const swing = spring({
    frame: frame - sec(fps, 0.12),
    fps,
    config: {damping: 14, mass: 1.2, stiffness: 72},
  });
  const rotY = interpolate(swing, [0, 1], [-84, 0]);
  // 閉じ切りで手前へわずかに寄る（opacity 単独回避の scale/translate 併用）
  const settle = interpolate(swing, [0.82, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // ロッククリック：終端でボルトが差し込まれる（spring pop）
  const lockStart = total - sec(fps, 0.55);
  const lock = spring({
    frame: frame - lockStart,
    fps,
    config: {damping: 12, mass: 0.6, stiffness: 200},
  });
  const boltX = interpolate(lock, [0, 1], [24, 0]);
  const flash = interpolate(lock, [0, 0.35, 1], [0, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const flashScale = interpolate(lock, [0, 1], [0.5, 1.9]);

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div style={{perspective: 1700, perspectiveOrigin: '52% 50%'}}>
        <div
          style={{
            position: 'relative',
            width: 460,
            height: 780,
            transformStyle: 'preserve-3d',
            transformOrigin: '0% 50%',
            transform: `translateX(-4px) rotateY(${rotY}deg) translateZ(${settle * 8}px)`,
            borderRadius: 10,
            background: `linear-gradient(120deg, #0e2033 0%, ${BRAND.color.navy} 46%, #081321 100%)`,
            border: `2px solid ${BRAND.color.silver}55`,
            boxShadow: `0 40px 120px rgba(0,0,0,0.6), inset 0 0 60px rgba(0,0,0,0.55)`,
          }}
        >
          {/* 上下の彫り込みパネル（面取りで扉らしさ） */}
          {[0, 1].map((i) => (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: 42,
                right: 96,
                top: i === 0 ? 52 : 402,
                height: 326,
                borderRadius: 8,
                background:
                  'linear-gradient(160deg, rgba(255,255,255,0.05), rgba(0,0,0,0.35))',
                boxShadow:
                  'inset 0 2px 6px rgba(255,255,255,0.06), inset 0 -3px 10px rgba(0,0,0,0.5)',
                border: `1px solid ${BRAND.color.silver}22`,
              }}
            />
          ))}

          {/* 縦のヘアライン（アクセント・閉じ切りで発光） */}
          <div
            style={{
              position: 'absolute',
              top: 30,
              bottom: 30,
              right: 74,
              width: 2,
              background: ACCENT,
              opacity: 0.25 + 0.55 * settle,
              boxShadow: `0 0 ${8 + 18 * settle}px ${ACCENT}`,
            }}
          />

          {/* ハンドル */}
          <div
            style={{
              position: 'absolute',
              right: 30,
              top: 372,
              width: 20,
              height: 84,
              borderRadius: 10,
              background: `linear-gradient(180deg, ${BRAND.color.white}, ${BRAND.color.silver})`,
              boxShadow: '0 4px 12px rgba(0,0,0,0.6)',
            }}
          />

          {/* 錠プレート＋ボルト（終端でカチッと差し込み） */}
          <div
            style={{
              position: 'absolute',
              right: 18,
              top: 470,
              width: 44,
              height: 44,
              borderRadius: 8,
              background: '#0a1420',
              border: `1px solid ${BRAND.color.silver}44`,
              overflow: 'visible',
            }}
          >
            <div
              style={{
                position: 'absolute',
                right: -18,
                top: 16,
                width: 30,
                height: 12,
                borderRadius: 3,
                transform: `translateX(${boltX}px)`,
                background: `linear-gradient(180deg, ${BRAND.color.white}, ${BRAND.color.silver})`,
                boxShadow: `0 0 ${6 + 14 * flash}px ${ACCENT}${flash > 0.05 ? 'cc' : '00'}`,
              }}
            />
            {/* クリック時のフラッシュリング（scale 併用＝opacity 単独でない） */}
            <div
              style={{
                position: 'absolute',
                right: -6,
                top: 22,
                width: 10,
                height: 10,
                marginLeft: -5,
                marginTop: -5,
                borderRadius: '50%',
                border: `2px solid ${ACCENT}`,
                transform: `scale(${flashScale})`,
                opacity: flash * 0.85,
              }}
            />
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const ClosingDoorScene: React.FC<{total: number}> = ({total}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // 奥のドア枠（静止レイヤー＝奥行きの一部・わずかに発光呼吸）
  const jambGlow = 0.4 + 0.25 * Math.sin((frame / fps) * 1.1);

  return (
    <>
      {/* ドア枠（ジャム）＋敷居の影 */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            width: 512,
            height: 828,
            borderRadius: 12,
            border: `10px solid #060b12`,
            boxShadow: `inset 0 0 0 2px ${ACCENT}${jambGlow > 0.5 ? '55' : '33'}, 0 0 80px rgba(0,0,0,0.6)`,
            background:
              'radial-gradient(120% 90% at 50% 30%, rgba(0,0,0,0.4), rgba(0,0,0,0.85))',
          }}
        />
      </AbsoluteFill>

      {/* 敷居の光（扉が閉じる先の縦スリット・電光。※黄ではなく electric） */}
      <div
        style={{
          position: 'absolute',
          left: width / 2 - 6,
          top: height / 2 - 400,
          width: 12,
          height: 800,
          background: ACCENT,
          opacity: 0.5,
          filter: 'blur(9px)',
        }}
      />

      {/* 扉本体（速い swing → Trail でモーションブラー） */}
      <Trail
        layers={FAST_TRAIL.layers}
        lagInFrames={FAST_TRAIL.lagInFrames}
        trailOpacity={FAST_TRAIL.trailOpacity}
      >
        <DoorPanel total={total} />
      </Trail>
    </>
  );
};

// =====================================================================
// kind='gears'
// =====================================================================

type GearCfg = {
  cx: number;
  cy: number;
  r: number;
  teeth: number;
  dir: 1 | -1;
  spin: number; // 総回転角(deg)
  startS: number; // 開始秒（スタッガー）
};

// 純表示の歯車（回転角は親から受け取る）
const Gear: React.FC<{cfg: GearCfg; angle: number}> = ({cfg, angle}) => {
  const {cx, cy, r, teeth} = cfg;
  const toothH = r * 0.2;
  const toothW = (2 * Math.PI * r) / teeth / 2.2;
  const hub = r * 0.3;

  return (
    <g transform={`rotate(${angle} ${cx} ${cy})`}>
      {/* リムグロー */}
      <circle cx={cx} cy={cy} r={r + toothH * 0.4} fill="none" stroke={ACCENT} strokeOpacity={0.35} strokeWidth={4} />
      {/* 歯 */}
      {Array.from({length: teeth}).map((_, i) => {
        const a = (360 / teeth) * i;
        return (
          <g key={i} transform={`rotate(${a} ${cx} ${cy})`}>
            <rect
              x={cx - toothW / 2}
              y={cy - r - toothH}
              width={toothW}
              height={toothH + 4}
              rx={3}
              fill={BRAND.color.silver}
            />
          </g>
        );
      })}
      {/* 本体ディスク */}
      <circle
        cx={cx}
        cy={cy}
        r={r}
        fill={BRAND.color.navy}
        stroke={BRAND.color.silver}
        strokeOpacity={0.5}
        strokeWidth={3}
      />
      {/* スポーク */}
      {Array.from({length: 5}).map((_, i) => (
        <rect
          key={i}
          x={cx - r * 0.05}
          y={cy - r * 0.82}
          width={r * 0.1}
          height={r * 0.6}
          rx={r * 0.05}
          fill={BRAND.color.silver}
          fillOpacity={0.28}
          transform={`rotate(${(360 / 5) * i} ${cx} ${cy})`}
        />
      ))}
      {/* ハブ（アクセント発光） */}
      <circle cx={cx} cy={cy} r={hub} fill="#0a1420" stroke={ACCENT} strokeWidth={4} />
      <circle cx={cx} cy={cy} r={hub * 0.42} fill={ACCENT} />
    </g>
  );
};

const GearsGroup: React.FC<{gears: GearCfg[]}> = ({gears}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{position: 'absolute', inset: 0}}
    >
      {gears.map((g, i) => {
        // スピンアップ：eased で加速→減速（線形禁止）。順番はスタッガー開始。
        const p = interpolate(
          frame,
          [sec(fps, g.startS), sec(fps, g.startS) + sec(fps, 2.4)],
          [0, 1],
          {
            easing: Easing.out(Easing.cubic),
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          },
        );
        // 常時わずかに動く微揺れ（完全静止の回避・sin は eased）
        const idle = Math.sin((frame / fps) * 0.9 + i) * 1.4;
        const angle = g.dir * (p * g.spin) + idle;
        return <Gear key={i} cfg={g} angle={angle} />;
      })}
    </svg>
  );
};

const GearsScene: React.FC = () => {
  const {width, height} = useVideoConfig();
  const cx = width / 2;
  const cy = height / 2;

  // 噛み合う3枚（隣接は逆回転）。半径の和≒中心間距離で噛み合いを示唆。
  const gears: GearCfg[] = [
    {cx: cx - 40, cy: cy + 30, r: 230, teeth: 22, dir: 1, spin: 250, startS: 0.15},
    {cx: cx + 300, cy: cy - 150, r: 150, teeth: 15, dir: -1, spin: 330, startS: 0.5},
    {cx: cx - 330, cy: cy - 120, r: 128, teeth: 13, dir: -1, spin: 360, startS: 0.85},
  ];

  return (
    <Trail
      layers={FAST_TRAIL.layers}
      lagInFrames={FAST_TRAIL.lagInFrames}
      trailOpacity={FAST_TRAIL.trailOpacity}
    >
      <GearsGroup gears={gears} />
    </Trail>
  );
};

// =====================================================================
// kind='faultsplit'
// =====================================================================

type Shard = {
  x: number;
  y: number;
  size: number;
  side: 1 | -1;
  vx: number;
  vy: number;
  rot: number;
  startS: number;
};

const Debris: React.FC<{shards: Shard[]; total: number}> = ({shards, total}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      style={{position: 'absolute', inset: 0}}
    >
      {shards.map((s, i) => {
        const st = sec(fps, s.startS);
        // 放出は eased（out.cubic）。落下は重力＝二次（非線形）。
        const life = total - st;
        const p = interpolate(frame, [st, st + life], [0, 1], {
          easing: Easing.out(Easing.cubic),
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const t = Math.max(0, (frame - st) / fps); // 秒
        const dx = s.side * s.vx * p;
        const dy = -s.vy * p + 340 * t * t * 0.06; // 上昇→重力落下
        const o = interpolate(p, [0, 0.08, 0.82, 1], [0, 1, 1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const rot = s.rot * p;
        const half = s.size / 2;
        return (
          <g
            key={i}
            transform={`translate(${s.x + dx} ${s.y + dy}) rotate(${rot})`}
            opacity={o}
          >
            <polygon
              points={`${-half},${-half * 0.7} ${half * 0.8},${-half} ${half},${half * 0.6} ${-half * 0.6},${half}`}
              fill={BRAND.color.navy}
              stroke={ACCENT}
              strokeOpacity={0.7}
              strokeWidth={2}
            />
          </g>
        );
      })}
    </svg>
  );
};

const FaultSplitScene: React.FC<{total: number}> = ({total}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();

  // ---- 断層線（決定論的にギザギザを一度だけ生成） ----
  const N = 14;
  const centerX = width / 2;
  const faultPts = React.useMemo(() => {
    const pts: {x: number; y: number}[] = [];
    for (let k = 0; k <= N; k++) {
      const y = (height * k) / N;
      // 端点は中央寄り、中間ほど揺れる
      const edge = Math.sin((k / N) * Math.PI);
      const jag = (random(`fault-${k}`) * 2 - 1) * 120 * edge;
      pts.push({x: centerX + jag, y});
    }
    return pts;
  }, [height, width]);

  // ---- 破片（決定論的） ----
  const shards = React.useMemo<Shard[]>(() => {
    const arr: Shard[] = [];
    for (let i = 0; i < 22; i++) {
      const k = 1 + Math.floor(random(`sh-y-${i}`) * (N - 1));
      const base = faultPts[k];
      const side: 1 | -1 = random(`sh-side-${i}`) > 0.5 ? 1 : -1;
      arr.push({
        x: base.x,
        y: base.y,
        size: 22 + random(`sh-sz-${i}`) * 46,
        side,
        vx: 140 + random(`sh-vx-${i}`) * 260,
        vy: 90 + random(`sh-vy-${i}`) * 200,
        rot: (random(`sh-rot-${i}`) * 2 - 1) * 220,
        startS: 0.42 + random(`sh-t-${i}`) * 0.22,
      });
    }
    return arr;
  }, [faultPts]);

  // ---- 割れる：spring（オーバーシュートで裂ける） ----
  const split = spring({
    frame: frame - sec(fps, 0.35),
    fps,
    config: {damping: 11, mass: 1, stiffness: 90},
  });
  const gap = interpolate(split, [0, 1], [0, 96]);
  const tilt = interpolate(split, [0, 1], [0, 1.6]);

  // 断層グローの描き上げ＋幅の脈動（常時可変）
  const crackDraw = spring({
    frame: frame - sec(fps, 0.2),
    fps,
    config: {damping: 24, stiffness: 120},
  });
  const faultLen = height * 1.35;
  const crackPulse = 0.6 + 0.4 * Math.sin((frame / fps) * 4.0);

  // 左右スラブのポリゴン（断層辺を共有）
  const faultPath = faultPts.map((p) => `${p.x},${p.y}`).join(' ');
  const leftPts = `0,0 ${faultPath} 0,${height}`;
  const rightPts = `${width},0 ${faultPath} ${width},${height}`;
  const faultLine = faultPts.map((p) => `${p.x},${p.y}`).join(' ');

  return (
    <>
      <svg
        width={width}
        height={height}
        viewBox={`0 0 ${width} ${height}`}
        style={{position: 'absolute', inset: 0}}
      >
        <defs>
          <linearGradient id="mr-slab" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#0e2033" />
            <stop offset="100%" stopColor="#070f18" />
          </linearGradient>
        </defs>

        {/* 左スラブ（外へずれ＋わずかに傾く） */}
        <g transform={`translate(${-gap} 0) rotate(${-tilt} 0 ${height})`}>
          <polygon
            points={leftPts}
            fill="url(#mr-slab)"
            stroke={BRAND.color.silver}
            strokeOpacity={0.28}
            strokeWidth={2}
          />
        </g>
        {/* 右スラブ */}
        <g transform={`translate(${gap} 0) rotate(${tilt} ${width} ${height})`}>
          <polygon
            points={rightPts}
            fill="url(#mr-slab)"
            stroke={BRAND.color.silver}
            strokeOpacity={0.28}
            strokeWidth={2}
          />
        </g>

        {/* 断層のアクセント発光（描き上げ＋脈動） */}
        <polyline
          points={faultLine}
          fill="none"
          stroke={ACCENT}
          strokeWidth={3 + crackPulse * 3}
          strokeLinejoin="round"
          strokeOpacity={0.85}
          strokeDasharray={faultLen}
          strokeDashoffset={faultLen * (1 - crackDraw)}
          style={{filter: `drop-shadow(0 0 ${10 + crackPulse * 10}px ${ACCENT})`}}
        />
      </svg>

      {/* 破片（速い散り → Trail でモーションブラー） */}
      <Trail
        layers={FAST_TRAIL.layers}
        lagInFrames={FAST_TRAIL.lagInFrames}
        trailOpacity={FAST_TRAIL.trailOpacity}
      >
        <Debris shards={shards} total={total} />
      </Trail>
    </>
  );
};

// =====================================================================
// 親：フルスクリーン・シーン
// =====================================================================
export const MechanismReveal: React.FC<{
  kind: 'closingdoor' | 'gears' | 'faultsplit';
  dur?: number;
}> = ({kind, dur}) => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();
  const total = dur ?? durationInFrames;

  // シーンの出入り（scale 併用＝opacity 単独でない）
  const outStart = total - sec(fps, 0.5);
  const o = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [0, 1, 1, 0],
    {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
  );
  const s = interpolate(
    frame,
    [0, sec(fps, 0.3), outStart, total],
    [1.03, 1, 1, 1.02],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    },
  );

  return (
    <AbsoluteFill style={{backgroundColor: '#06080f', overflow: 'hidden'}}>
      <DepthLayers />
      <AbsoluteFill style={{opacity: o, transform: `scale(${s})`}}>
        {kind === 'closingdoor' ? <ClosingDoorScene total={total} /> : null}
        {kind === 'gears' ? <GearsScene /> : null}
        {kind === 'faultsplit' ? <FaultSplitScene total={total} /> : null}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
