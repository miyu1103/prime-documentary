import React, {useMemo} from 'react';
import {
  AbsoluteFill,
  Easing,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {useThree, useLoader} from '@react-three/fiber';

// =====================================================================
// DepthScene — 「どんな画像も3D化」: 深度マップ(AI推定)で写真をメッシュ変位させ、
//   カメラを動かして本物のパララックスを出す 2.5D 部品。
//   入力: image(カラー) + depth(深度PNG, 近=白/遠=黒)。両方 public 配下。
//   depth.py (ComfyUI venv + Intel/dpt-large) で depth を生成 → ここで displacementMap。
//   平面Ken Burnsと違い、深度に沿って近景と遠景が別々の速さで動く（本物の奥行き）。
// =====================================================================

export type DepthSceneProps = {
  image: string;
  depth: string;
  displace: number; // 変位量（奥行きの強さ）
  accent: string;
};

export const depthSceneDurationInFrames = (fps: number) => Math.round(fps * 6.0);

// ソフトなボケ玉テクスチャ（浮遊塵用）
const useBokeh = () =>
  useMemo(() => {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const g = c.getContext('2d')!;
    const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.4, 'rgba(255,255,255,0.5)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
  }, []);

// 決定論乱数
const mulberry32 = (seed: number) => {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

// 手前〜奥に散る浮遊塵（深度メッシュより手前/奥で別々にパララックス＝奥行きが本物に見える）
const DustField: React.FC<{accent: string; tSec: number}> = ({accent, tSec}) => {
  const bokeh = useBokeh();
  const motes = useMemo(() => {
    const rnd = mulberry32(42);
    return Array.from({length: 30}).map(() => ({
      x: (rnd() - 0.5) * 8,
      y: (rnd() - 0.5) * 5,
      z: -0.5 + rnd() * 3.2, // 一部はカメラ側（手前）で大きくボケる
      s: 0.05 + rnd() * 0.22,
      o: 0.15 + rnd() * 0.4,
      sp: 0.2 + rnd() * 0.5,
      ph: rnd() * 6.28,
    }));
  }, []);
  const col = new THREE.Color(accent);
  return (
    <>
      {motes.map((m, i) => {
        const x = m.x + Math.sin(tSec * m.sp + m.ph) * 0.25;
        const y = m.y + Math.cos(tSec * m.sp * 0.8 + m.ph) * 0.18;
        const tw = 0.6 + 0.4 * Math.sin(tSec * (0.8 + i * 0.03) + m.ph);
        return (
          <sprite key={i} position={[x, y, m.z]} scale={[m.s, m.s, 1]}>
            <spriteMaterial
              map={bokeh}
              color={i % 4 === 0 ? col : new THREE.Color('#cfe0f5')}
              transparent
              opacity={m.o * tw}
              blending={THREE.AdditiveBlending}
              depthWrite={false}
            />
          </sprite>
        );
      })}
    </>
  );
};

const DepthPlane: React.FC<{image: string; depth: string; displace: number}> = ({
  image,
  depth,
  displace,
}) => {
  const color = useLoader(THREE.TextureLoader, staticFile(image));
  const disp = useLoader(THREE.TextureLoader, staticFile(depth));
  color.colorSpace = THREE.SRGBColorSpace;
  // 3:2 写真をカバーする板。高分割で変位が滑らかに。
  // 板をやや大きく（オーバースキャン）＝カメラが動いても端がフレーム外に残る
  return (
    <mesh scale={[1.16, 1.16, 1]}>
      <planeGeometry args={[6, 4, 360, 240]} />
      <meshStandardMaterial
        map={color}
        displacementMap={disp}
        displacementScale={displace}
        roughness={1}
        metalness={0}
        toneMapped={false}
      />
    </mesh>
  );
};

// 「写真の中へ入っていく」dolly-in（横移動を抑える＝溶けない／寄りで迫力）。frame駆動＝決定論。
const DepthCam: React.FC<{dolly: number}> = ({dolly}) => {
  const camera = useThree((s) => s.camera);
  camera.position.set(
    Math.sin(dolly * Math.PI) * 0.22, // ごく僅かな横スウェイ
    0.05 - dolly * 0.12,
    5.6 - dolly * 2.3, // 5.6 → 3.3 へしっかり寄る
  );
  camera.lookAt(0, 0, 0.5);
  camera.updateProjectionMatrix();
  return null;
};

// 毎フレーム更新フィルムグレイン
const grain = (frame: number, opacity: number): React.CSSProperties => {
  const svg =
    `<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'>` +
    `<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${frame % 137}'/>` +
    `<feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>`;
  return {
    backgroundImage: `url("data:image/svg+xml,${encodeURIComponent(svg)}")`,
    backgroundSize: '200px 200px',
    mixBlendMode: 'overlay',
    opacity,
    pointerEvents: 'none',
  };
};

export const DepthScene: React.FC<DepthSceneProps> = ({
  image,
  depth,
  displace,
  accent,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();

  // 寄り（dolly-in）はイージング付き（等速禁止）
  const dolly = interpolate(frame, [0, durationInFrames], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: 'clamp',
  });
  const tSec = frame / fps;

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 42, position: [0, 0, 5.6], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <ambientLight intensity={2.4} />
        <DepthCam dolly={dolly} />
        <DepthPlane image={image} depth={depth} displace={displace} />
        <DustField accent={accent} tSec={tSec} />
      </ThreeCanvas>

      {/* シネマグレード：accentを影に、ビネット */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, ${accent}18 0%, transparent 40%, transparent 62%, #04070c 100%)`,
          mixBlendMode: 'multiply',
          pointerEvents: 'none',
        }}
      />
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 45%, transparent 42%, rgba(0,0,0,0.66) 100%)',
          pointerEvents: 'none',
        }}
      />
      <AbsoluteFill style={grain(frame, 0.07)} />

      {/* ラベル（この技法の説明用。実運用では外す/差し替え） */}
      <div
        style={{
          position: 'absolute',
          left: 90,
          bottom: 84,
          fontFamily: 'Inter, system-ui, sans-serif',
          fontWeight: 600,
          fontSize: 24,
          letterSpacing: 6,
          textTransform: 'uppercase',
          color: '#d6deec',
          opacity: interpolate(frame, [10, 40], [0, 0.9], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        2.5D Depth Parallax · from a single still
      </div>
    </AbsoluteFill>
  );
};
