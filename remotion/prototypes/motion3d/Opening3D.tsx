import React, {useMemo} from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {Trail} from '@remotion/motion-blur';
import * as THREE from 'three';
import {useThree, useLoader} from '@react-three/fiber';

// =====================================================================
// Opening3D — 「本物の3D空間 × Remotion」で奥行き・パララックス・質感を出す
// 実装の2バリエーション（同じ props 型）:
//   A) OpeningDoc3D    … ドキュメンタリー映画調（暗い/落ち着き/グレイン/ボケ玉/ゆっくり寄り）
//   B) OpeningMotion3D … モーショングラフィックス（光る幾何形/軌道運動/ダイナミック）
// 平面Opening.tsxとの差:
//   - 背景が「板の合成」ではなく three.js の3Dシーン。カメラが空間を移動する
//     → 奥行き違いの要素が自動でパララックス（近い物は速く、遠い物は遅く動く）
//   - フィルムグレイン(feTurbulenceを毎フレーム再生成)・ビネットで実写質感
//   - 文字はDOMで最前面に重ねてシャープに（3Dテキストのボケ回避）
// 品質ルール順守: 全モーションにイージング/spring・opacity単独なし・スタッガー・
//   Trailモーションブラー・最低3レイヤー・overflow:hiddenのマスク切れ上がり・尺はfps算出。
// =====================================================================

export type Opening3DProps = {
  title: string;
  subtitle: string;
  accent: string; // アクセントカラー（HEX）
  hasLogo: boolean;
};

// 尺は fps から算出（4.0秒）。フレーム直書き禁止。
export const opening3DDurationInFrames = (fps: number) => Math.round(fps * 4.0);
const sec = (fps: number, s: number) => Math.round(fps * s);

// 決定論的な擬似乱数（レンダー間で完全再現。Math.random禁止）
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

// 毎フレーム seed を変えたフィルムグレイン（動く粒子＝実写っぽさ）
const grainLayer = (frame: number, opacity: number): React.CSSProperties => {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>` +
    `<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 137}'/>` +
    `<feColorMatrix type='saturate' values='0'/></filter>` +
    `<rect width='100%' height='100%' filter='url(#n)'/></svg>`;
  return {
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svg)}")`,
    backgroundSize: '200px 200px',
    mixBlendMode: 'overlay',
    opacity,
    pointerEvents: 'none',
  };
};

// DOMで最前面に置くタイトル（マスク切れ上がり＋1文字スタッガー＋Trailブラー）
const TitleOverlay: React.FC<{
  title: string;
  subtitle: string;
  accent: string;
  startSec: number;
  serif?: boolean;
  fontSize?: number;
  offsetY?: number;
}> = ({title, subtitle, accent, startSec, serif, fontSize = 128, offsetY = -60}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const chars = Array.from(title);
  const stagger = Math.max(1, sec(fps, 0.045));

  const accentSpring = spring({
    frame: frame - sec(fps, startSec + 0.75),
    fps,
    config: {damping: 16, mass: 0.8},
  });
  const accentScaleX = interpolate(accentSpring, [0, 1], [0, 1]);

  const subSpring = spring({
    frame: frame - sec(fps, startSec + 0.9),
    fps,
    config: {damping: 20, mass: 1},
  });
  const subY = interpolate(subSpring, [0, 1], [22, 0]);
  const subOpacity = interpolate(subSpring, [0, 1], [0, 1]);

  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <Trail layers={5} lagInFrames={1.1} trailOpacity={0.4}>
        <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
          <div
            style={{
              display: 'flex',
              transform: `translateY(${offsetY}px)`,
              fontFamily: serif
                ? "'Times New Roman', Georgia, serif"
                : 'Inter, system-ui, sans-serif',
              fontWeight: serif ? 500 : 800,
              fontSize,
              letterSpacing: serif ? 4 : -2,
              color: '#ffffff',
              lineHeight: 1.05,
              textShadow: '0 6px 40px rgba(0,0,0,0.55)',
            }}
          >
            {chars.map((ch, i) => {
              const cs = spring({
                frame: frame - sec(fps, startSec) - i * stagger,
                fps,
                config: {damping: 16, mass: 1},
              });
              const y = interpolate(cs, [0, 1], [115, 0]);
              const o = interpolate(cs, [0, 0.25], [0, 1], {
                extrapolateRight: 'clamp',
              });
              return (
                <span
                  key={i}
                  style={{display: 'inline-block', overflow: 'hidden', paddingBottom: '0.12em'}}
                >
                  <span
                    style={{
                      display: 'inline-block',
                      transform: `translateY(${y}%)`,
                      opacity: o,
                      whiteSpace: 'pre',
                    }}
                  >
                    {ch}
                  </span>
                </span>
              );
            })}
          </div>
        </AbsoluteFill>
      </Trail>

      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          flexDirection: 'column',
          gap: 16,
          transform: `translateY(${offsetY + 120}px)`,
        }}
      >
        <div
          style={{
            width: 220,
            height: 4,
            borderRadius: 3,
            backgroundColor: accent,
            transform: `scaleX(${accentScaleX})`,
            transformOrigin: 'center',
            boxShadow: `0 0 24px ${accent}aa`,
          }}
        />
        <div
          style={{
            marginTop: 6,
            fontFamily: serif
              ? "'Times New Roman', Georgia, serif"
              : 'Inter, system-ui, sans-serif',
            fontWeight: serif ? 400 : 500,
            fontSize: 34,
            letterSpacing: 8,
            textTransform: 'uppercase',
            color: '#d6deec',
            transform: `translateY(${subY}px)`,
            opacity: subOpacity,
          }}
        >
          {subtitle}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------
// カメラリグ: Remotionの frame でカメラ位置を駆動（useFrameは使わない＝決定論）
// ---------------------------------------------------------------------
const CameraRig: React.FC<{
  posFn: (t: number) => [number, number, number];
  lookAt?: [number, number, number];
  progress: number;
}> = ({posFn, lookAt = [0, 0, 0], progress}) => {
  const camera = useThree((s) => s.camera);
  const [x, y, z] = posFn(progress);
  camera.position.set(x, y, z);
  camera.lookAt(lookAt[0], lookAt[1], lookAt[2]);
  camera.updateProjectionMatrix();
  return null;
};

// ソフトなボケ玉テクスチャ（放射グラデ）を1枚だけ生成して共有
const useBokehTexture = () =>
  useMemo(() => {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const g = c.getContext('2d')!;
    const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.35, 'rgba(255,255,255,0.55)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  }, []);

// =====================================================================
// A) ドキュメンタリー映画調
// =====================================================================
export const OpeningDoc3D: React.FC<Opening3DProps> = ({
  title,
  subtitle,
  accent,
  hasLogo,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const bokeh = useBokehTexture();

  // カメラ: z=6.5 → 3.6 へゆっくり寄る＋わずかに横ドリフト（イージング）
  const dolly = interpolate(frame, [0, durationInFrames], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // 奥行き違いのボケ玉（近い/遠いが混在 → カメラ移動でパララックス）
  const orbs = useMemo(() => {
    const rnd = mulberry32(7);
    return Array.from({length: 26}).map(() => ({
      x: (rnd() - 0.5) * 10,
      y: (rnd() - 0.5) * 6,
      z: -1 - rnd() * 7,
      s: 0.4 + rnd() * 1.6,
      o: 0.12 + rnd() * 0.35,
      drift: (rnd() - 0.5) * 0.6,
    }));
  }, []);

  const accentColor = new THREE.Color(accent);
  const tSec = frame / fps;

  return (
    <AbsoluteFill style={{backgroundColor: '#04070c'}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 42, position: [0, 0, 6.5], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <color attach="background" args={['#04070c']} />
        <fog attach="fog" args={['#04070c', 4, 12]} />
        <ambientLight intensity={0.25} />
        <pointLight position={[3, 2, 4]} intensity={18} color={accentColor} />
        <pointLight position={[-4, -1, 2]} intensity={8} color={'#0a2c40'} />

        <CameraRig
          progress={dolly}
          posFn={(t) => [Math.sin(t * Math.PI) * 0.5, t * 0.25, 6.5 - t * 2.9]}
          lookAt={[0, 0.15, 0]}
        />

        {/* レイヤー1: 遠景の霞んだ地平グラデ板（奥に固定） */}
        <mesh position={[0, 0, -9]}>
          <planeGeometry args={[40, 22]} />
          <meshBasicMaterial color={'#0a1622'} />
        </mesh>

        {/* レイヤー2: 奥行き差のあるボケ玉群（加算合成／パララックスの主役） */}
        {orbs.map((o, i) => {
          const rise = interpolate(dolly, [0, 1], [0, o.drift]);
          const tw =
            0.6 + 0.4 * Math.sin(tSec * (0.6 + i * 0.05) + i); // 明滅（等速でなく sin）
          return (
            <sprite
              key={i}
              position={[o.x, o.y + rise, o.z]}
              scale={[o.s, o.s, o.s]}
            >
              <spriteMaterial
                map={bokeh}
                color={i % 3 === 0 ? accentColor : new THREE.Color('#8fb6d8')}
                transparent
                opacity={o.o * tw}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </sprite>
          );
        })}

        {/* レイヤー3: タイトル裏のソフトグロー（大玉のボケ） */}
        <sprite position={[0, 0.1, -0.5]} scale={[7, 4, 1]}>
          <spriteMaterial
            map={bokeh}
            color={accentColor}
            transparent
            opacity={interpolate(dolly, [0, 0.4, 1], [0, 0.22, 0.16])}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </sprite>
      </ThreeCanvas>

      {/* ビネット（周辺減光＝映画の額縁） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 42%, transparent 45%, rgba(0,0,0,0.72) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* タイトル（セリフ体・上品・最前面） */}
      <TitleOverlay
        title={title}
        subtitle={subtitle}
        accent={accent}
        startSec={0.5}
        serif
        fontSize={120}
        offsetY={-40}
      />

      {/* フィルムグレイン（毎フレーム更新） */}
      <AbsoluteFill style={grainLayer(frame, 0.08)} />

      {hasLogo ? (
        <div
          style={{
            position: 'absolute',
            top: 60,
            left: 68,
            fontFamily: "'Times New Roman', Georgia, serif",
            fontSize: 22,
            letterSpacing: 6,
            color: '#9fb2c8',
            opacity: interpolate(
              spring({frame: frame - sec(fps, 0.2), fps, config: {damping: 20}}),
              [0, 1],
              [0, 0.9],
            ),
          }}
        >
          EST. DOCUMENTARY
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// =====================================================================
// B) モーショングラフィックス（光る幾何形／軌道運動／ダイナミック）
// =====================================================================
export const OpeningMotion3D: React.FC<Opening3DProps> = ({
  title,
  subtitle,
  accent,
  hasLogo,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const accentColor = new THREE.Color(accent);
  const tSec = frame / fps;

  // カメラ: 遠くから punch-in（spring）＋ゆるやかに周回
  const intro = spring({frame, fps, config: {damping: 18, mass: 1.1}});
  const camZ = interpolate(intro, [0, 1], [11, 6]);
  const orbit = interpolate(frame, [0, durationInFrames], [0, 0.5], {
    easing: Easing.inOut(Easing.sin),
  });

  // 中央コアの登場（scale spring）と自転
  const coreIn = spring({
    frame: frame - sec(fps, 0.1),
    fps,
    config: {damping: 12, mass: 1},
  });
  const coreScale = interpolate(coreIn, [0, 1], [0, 1.4]);
  const coreRot = tSec * 0.6;

  // 軌道リング上の小球（スタッガー登場）
  const satellites = useMemo(() => {
    const rnd = mulberry32(21);
    return Array.from({length: 9}).map((_, i) => ({
      a: (i / 9) * Math.PI * 2,
      r: 2.6 + rnd() * 0.6,
      y: (rnd() - 0.5) * 1.6,
      s: 0.12 + rnd() * 0.12,
      delay: i * 0.05,
    }));
  }, []);

  return (
    <AbsoluteFill style={{backgroundColor: '#05060f'}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 45, position: [0, 0, 11], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <color attach="background" args={['#05060f']} />
        <fog attach="fog" args={['#05060f', 9, 22]} />
        {/* コントラストの効いた三点照明。面ごとに光を変えて“宝石”の陰影を出す */}
        <ambientLight intensity={0.12} />
        <pointLight position={[5, 4, 6]} intensity={40} color={'#ffffff'} />
        <pointLight position={[-6, -1, 2]} intensity={22} color={accentColor} />
        <pointLight position={[0, -4, -3]} intensity={16} color={'#6a2ecf'} />

        <CameraRig
          progress={0}
          posFn={() => [Math.sin(orbit) * 2.2, 0.6 + Math.sin(orbit * 0.7) * 0.5, camZ]}
          lookAt={[0, -1.1, 0]}
        />

        {/* レイヤー1: 背面の巨大ワイヤーフレーム球（ゆっくり逆回転） */}
        <mesh
          position={[0, -1.1, 0]}
          rotation={[coreRot * -0.3, coreRot * -0.5, 0]}
          scale={[3.6, 3.6, 3.6]}
        >
          <icosahedronGeometry args={[1, 1]} />
          <meshBasicMaterial color={accentColor} wireframe transparent opacity={0.1} />
        </mesh>

        {/* レイヤー2: 主役コア＝面カットの宝石（低emissive＋金属質＋flatShadingで面が光を拾う） */}
        <group
          position={[0, -1.2, 0]}
          scale={[coreScale, coreScale, coreScale]}
          rotation={[coreRot, coreRot * 0.8, 0]}
        >
          <mesh>
            <icosahedronGeometry args={[1, 1]} />
            <meshStandardMaterial
              color={'#0a1436'}
              emissive={accentColor}
              emissiveIntensity={0.18}
              metalness={0.95}
              roughness={0.14}
              flatShading
            />
          </mesh>
          <mesh scale={[1.015, 1.015, 1.015]}>
            <icosahedronGeometry args={[1, 1]} />
            <meshBasicMaterial color={accentColor} wireframe transparent opacity={0.55} />
          </mesh>
        </group>

        {/* レイヤー3: 軌道リング（トーラス／別軸回転） */}
        <mesh position={[0, -1.1, 0]} rotation={[Math.PI / 2.3, coreRot * 0.5, orbit * 2]}>
          <torusGeometry args={[2.7, 0.015, 12, 140]} />
          <meshBasicMaterial color={accentColor} transparent opacity={0.45} />
        </mesh>

        {/* レイヤー4: 軌道上のサテライト小球（スタッガー登場＋発光。コア下側を周回） */}
        {satellites.map((s, i) => {
          const inn = spring({
            frame: frame - sec(fps, 0.4 + s.delay),
            fps,
            config: {damping: 14, mass: 0.7},
          });
          const ang = s.a + orbit * 2;
          const pop = interpolate(inn, [0, 1], [0, s.s]);
          return (
            <mesh
              key={i}
              position={[Math.cos(ang) * s.r, -1.1 + s.y * 0.5, Math.sin(ang) * s.r]}
              scale={[pop, pop, pop]}
            >
              <sphereGeometry args={[1, 16, 16]} />
              <meshStandardMaterial
                color={'#ffffff'}
                emissive={accentColor}
                emissiveIntensity={2}
              />
            </mesh>
          );
        })}
      </ThreeCanvas>

      {/* 立体（画面下寄り）のグロー。宝石の位置に合わせて下側を持ち上げる */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 38% at 50% 66%, ${accent}3a 0%, transparent 70%)`,
          pointerEvents: 'none',
          opacity: interpolate(intro, [0, 1], [0, 1]),
        }}
      />

      {/* タイトル（サンセリフ・極太・上寄せ＝立体と分離してダイナミックに） */}
      <TitleOverlay
        title={title}
        subtitle={subtitle}
        accent={accent}
        startSec={0.55}
        fontSize={128}
        offsetY={-230}
      />

      {/* 軽いグレイン（モーショングラフィックスは控えめに） */}
      <AbsoluteFill style={grainLayer(frame, 0.05)} />

      {hasLogo ? (
        <div
          style={{
            position: 'absolute',
            top: 58,
            left: 70,
            width: 78,
            height: 78,
            borderRadius: 18,
            background: `linear-gradient(135deg, ${accent}, #ffffff22)`,
            border: `2px solid ${accent}`,
            boxShadow: `0 0 30px ${accent}66`,
            transform: `scale(${interpolate(
              spring({frame: frame - sec(fps, 0.15), fps, config: {damping: 14}}),
              [0, 1],
              [0.3, 1],
            )})`,
          }}
        />
      ) : null}
    </AbsoluteFill>
  );
};

// =====================================================================
// C) 実写フォトパララックス（2.5D）… 「今までと明確に違う」本命
//   - 実写1枚を3D空間の板に貼り、カメラをゆっくり寄せる（周辺パララックス）
//   - 手前を大きなボケ玉が横切る（写真より速く動く＝被写界深度＝奥行きが一目で分かる）
//   - シネマ調グレード（accentで色被せ）＋光漏れ＋ビネット＋フィルムグレイン
//   - タイトルは下三分割の“タイトルカード”配置（センター置きの旧OPと差別化）
//   props に image（public配下のファイル名）を追加。差し替えで各話に量産可能。
// =====================================================================
export type OpeningPhoto3DProps = Opening3DProps & {image: string};

const PhotoPlane: React.FC<{image: string; dolly: number}> = ({image, dolly}) => {
  const tex = useLoader(THREE.TextureLoader, staticFile(image));
  // 3:2写真を16:9ビューにカバーさせる大きめの板（stretchさせない）
  return (
    <mesh position={[0, 0, 0]} scale={[1 + dolly * 0.04, 1 + dolly * 0.04, 1]}>
      <planeGeometry args={[6, 4]} />
      <meshBasicMaterial map={tex} toneMapped={false} />
    </mesh>
  );
};

export const OpeningPhoto3D: React.FC<OpeningPhoto3DProps> = ({
  title,
  subtitle,
  accent,
  hasLogo,
  image,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  const bokeh = useBokehTexture();
  const accentColor = new THREE.Color(accent);
  const tSec = frame / fps;

  // カメラ: d=4.0 → 3.15 へゆっくり寄る＋横ドリフト（周辺パララックス）。イージング必須
  const dolly = interpolate(frame, [0, durationInFrames], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });

  // 手前を横切るボケ玉（写真より手前・大きい・速い＝被写界深度の演出）
  const fgOrbs = useMemo(() => {
    const rnd = mulberry32(101);
    return Array.from({length: 7}).map(() => ({
      x0: -4 + rnd() * 8,
      y: (rnd() - 0.5) * 3.4,
      z: 1.6 + rnd() * 0.9,
      s: 0.8 + rnd() * 1.4,
      o: 0.1 + rnd() * 0.22,
      speed: 0.6 + rnd() * 1.1,
    }));
  }, []);

  // タイトルカード（下三分割・左寄せ）の登場
  const cardSpring = spring({
    frame: frame - sec(fps, 0.55),
    fps,
    config: {damping: 18, mass: 1},
  });
  const chars = Array.from(title);
  const stagger = Math.max(1, sec(fps, 0.045));
  const subSpring = spring({
    frame: frame - sec(fps, 1.15),
    fps,
    config: {damping: 20, mass: 1},
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 40, position: [0, 0, 4], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <CameraRig
          progress={dolly}
          posFn={(t) => [
            interpolate(t, [0, 1], [-0.18, 0.14]),
            interpolate(t, [0, 1], [0.05, -0.06]),
            interpolate(t, [0, 1], [4.0, 3.15]),
          ]}
          lookAt={[0, 0, 0]}
        />

        {/* レイヤー1: 実写の板（3D空間・カメラ移動で周辺パララックス） */}
        <PhotoPlane image={image} dolly={dolly} />

        {/* レイヤー2: 光漏れ（写真の窓＝右上から差す暖色。加算） */}
        <sprite position={[2.1, 1.0, 0.8]} scale={[3.2, 3.2, 1]}>
          <spriteMaterial
            map={bokeh}
            color={'#ffd9a0'}
            transparent
            opacity={interpolate(dolly, [0, 0.5, 1], [0.12, 0.26, 0.2])}
            blending={THREE.AdditiveBlending}
            depthWrite={false}
          />
        </sprite>

        {/* レイヤー3: 手前を横切るボケ玉（写真より速い＝被写界深度／奥行き） */}
        {fgOrbs.map((o, i) => {
          const x = o.x0 + Math.sin(tSec * o.speed + i) * 1.2;
          const y = o.y + interpolate(dolly, [0, 1], [0, o.speed * 0.5]);
          return (
            <sprite key={i} position={[x, y, o.z]} scale={[o.s, o.s, 1]}>
              <spriteMaterial
                map={bokeh}
                color={i % 2 === 0 ? accentColor : new THREE.Color('#ffffff')}
                transparent
                opacity={o.o}
                blending={THREE.AdditiveBlending}
                depthWrite={false}
              />
            </sprite>
          );
        })}
      </ThreeCanvas>

      {/* グレード1: accentを影に被せるシネマ調ダクト（乗算＋加算の2枚） */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, ${accent}22 0%, transparent 35%, transparent 60%, #04070c 100%)`,
          mixBlendMode: 'multiply',
          pointerEvents: 'none',
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(80% 60% at 70% 30%, ${accent}18 0%, transparent 60%)`,
          mixBlendMode: 'screen',
          pointerEvents: 'none',
        }}
      />

      {/* ビネット（額縁） */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 40%, rgba(0,0,0,0.7) 100%)',
          pointerEvents: 'none',
        }}
      />

      {/* タイトルカード（下三分割・左寄せ＝ドキュメンタリーの題字） */}
      <div
        style={{
          position: 'absolute',
          left: 96,
          bottom: 120,
          display: 'flex',
          flexDirection: 'column',
          gap: 18,
        }}
      >
        {/* アクセント縦バー＋タイトル */}
        <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
          <div
            style={{
              width: 5,
              height: interpolate(cardSpring, [0, 1], [0, 96]),
              backgroundColor: accent,
              boxShadow: `0 0 20px ${accent}`,
            }}
          />
          <div
            style={{
              display: 'flex',
              fontFamily: "'Times New Roman', Georgia, serif",
              fontWeight: 600,
              fontSize: 92,
              letterSpacing: 2,
              color: '#fff',
              lineHeight: 1.0,
              textShadow: '0 6px 40px rgba(0,0,0,0.6)',
            }}
          >
            {chars.map((ch, i) => {
              const cs = spring({
                frame: frame - sec(fps, 0.6) - i * stagger,
                fps,
                config: {damping: 16, mass: 1},
              });
              const y = interpolate(cs, [0, 1], [115, 0]);
              const o = interpolate(cs, [0, 0.25], [0, 1], {
                extrapolateRight: 'clamp',
              });
              return (
                <span
                  key={i}
                  style={{
                    display: 'inline-block',
                    overflow: 'hidden',
                    paddingBottom: '0.12em',
                  }}
                >
                  <span
                    style={{
                      display: 'inline-block',
                      transform: `translateY(${y}%)`,
                      opacity: o,
                      whiteSpace: 'pre',
                    }}
                  >
                    {ch}
                  </span>
                </span>
              );
            })}
          </div>
        </div>

        {/* サブタイトル（左寄せ・トラッキング広め） */}
        <div
          style={{
            marginLeft: 27,
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 500,
            fontSize: 26,
            letterSpacing: 8,
            textTransform: 'uppercase',
            color: '#d6deec',
            transform: `translateY(${interpolate(subSpring, [0, 1], [18, 0])}px)`,
            opacity: interpolate(subSpring, [0, 1], [0, 0.95]),
          }}
        >
          {subtitle}
        </div>
      </div>

      {/* フィルムグレイン（毎フレーム更新） */}
      <AbsoluteFill style={grainLayer(frame, 0.09)} />

      {hasLogo ? (
        <div
          style={{
            position: 'absolute',
            top: 60,
            right: 72,
            fontFamily: "'Times New Roman', Georgia, serif",
            fontSize: 22,
            letterSpacing: 6,
            color: '#c8d2e6',
            opacity: interpolate(
              spring({frame: frame - sec(fps, 0.3), fps, config: {damping: 20}}),
              [0, 1],
              [0, 0.85],
            ),
          }}
        >
          PRIME · DOCUMENTARY
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
