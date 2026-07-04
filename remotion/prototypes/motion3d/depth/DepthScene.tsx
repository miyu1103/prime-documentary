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

// カメラを緩い楕円で動かす（深度に沿ってパララックス）。frame駆動＝決定論。
const DepthCam: React.FC<{progress: number}> = ({progress}) => {
  const camera = useThree((s) => s.camera);
  const a = progress * Math.PI * 2;
  camera.position.set(
    Math.sin(a) * 0.36,
    Math.cos(a * 0.8) * 0.2,
    5.2 - progress * 0.5, // わずかに寄る
  );
  camera.lookAt(0, 0, 0.4);
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

  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    easing: Easing.inOut(Easing.sin),
  });

  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <ThreeCanvas
        width={width}
        height={height}
        camera={{fov: 42, position: [0, 0, 5.2], near: 0.1, far: 100}}
        gl={{antialias: true}}
        style={{position: 'absolute'}}
      >
        <ambientLight intensity={2.4} />
        <DepthCam progress={progress} />
        <DepthPlane image={image} depth={depth} displace={displace} />
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
