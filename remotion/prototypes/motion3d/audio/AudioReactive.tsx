import React from 'react';
import {
  AbsoluteFill,
  Audio,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {useAudioData, visualizeAudio} from '@remotion/media-utils';

// =====================================================================
// AudioReactive — 「音に反応する映像」: 完成ミックス(音楽＋声)の周波数を毎フレーム
//   解析し、中央コアの脈動・円形スペクトラム・波形・タイトルが音に同期して動く。
//   Remotion標準の @remotion/media-utils (useAudioData / visualizeAudio) で完結。
//   ドキュメンタリー用途: 声の抑揚に画面が呼吸する＝退屈な区間の離脱を防ぐ。
// =====================================================================

export type AudioReactiveProps = {
  src: string;
  accent: string;
  title: string;
  startInSeconds: number; // 曲の何秒目から使うか
};

export const audioReactiveDurationInFrames = (fps: number) => Math.round(fps * 12);

const BG = '#06080f';

export const AudioReactive: React.FC<AudioReactiveProps> = ({
  src,
  accent,
  title,
  startInSeconds,
}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const audioData = useAudioData(staticFile(src));

  if (!audioData) return null;

  // startInSeconds ぶんずらして解析（音のある区間を使う）
  const analyzeFrame = frame + Math.round(startInSeconds * fps);
  const bins = visualizeAudio({
    fps,
    frame: analyzeFrame,
    audioData,
    numberOfSamples: 128,
    optimizeFor: 'accuracy',
  });

  const bass = Math.min(1, (bins[0] + bins[1] + bins[2]) / 3 * 2.2);
  const energy = Math.min(1, (bins.reduce((a, b) => a + b, 0) / bins.length) * 6);

  const cx = width / 2;
  const cy = height / 2;
  const N = 56; // 円周のバー数
  const innerR = 190;

  // 円形スペクトラム（低〜中域を円周にマップ、上下対称）
  const bars = Array.from({length: N}).map((_, i) => {
    const idx = Math.floor((i < N / 2 ? i : N - 1 - i) / (N / 2) * 42); // 対称
    const v = Math.min(1, bins[idx] * 5.5);
    const ang = (i / N) * Math.PI * 2 - Math.PI / 2;
    const len = 14 + v * 260;
    const x1 = cx + Math.cos(ang) * innerR;
    const y1 = cy + Math.sin(ang) * innerR;
    const x2 = cx + Math.cos(ang) * (innerR + len);
    const y2 = cy + Math.sin(ang) * (innerR + len);
    return {x1, y1, x2, y2, v};
  });

  // 下部の波形（binsを折れ線に）
  const wf = bins.slice(0, 96);
  const wfPath = wf
    .map((v, i) => {
      const x = (i / (wf.length - 1)) * width;
      const y = height - 120 - Math.min(1, v * 6) * 150;
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');

  const coreScale = 1 + bass * 0.5;
  const titleScale = 1 + bass * 0.06;

  return (
    <AbsoluteFill style={{backgroundColor: BG}}>
      {/* 音を実際に鳴らす（該当区間から） */}
      <Audio src={staticFile(src)} startFrom={Math.round(startInSeconds * fps)} />

      {/* 背景グロー（総エネルギーで明滅・opacity単独でなくscaleも） */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(40% 40% at 50% 50%, ${accent}${Math.round(
            20 + energy * 60,
          ).toString(16).padStart(2, '0')} 0%, transparent 70%)`,
          transform: `scale(${1 + energy * 0.2})`,
        }}
      />

      <svg width={width} height={height} style={{position: 'absolute', inset: 0}}>
        {/* コア裏グロー */}
        <circle cx={cx} cy={cy} r={innerR * coreScale * 0.9} fill={accent} opacity={0.12 + bass * 0.2} />
        {/* 円形スペクトラム */}
        {bars.map((b, i) => (
          <line
            key={i}
            x1={b.x1} y1={b.y1} x2={b.x2} y2={b.y2}
            stroke={accent}
            strokeWidth={5}
            strokeLinecap="round"
            opacity={0.5 + b.v * 0.5}
          />
        ))}
        {/* コアリング（ビートで脈動） */}
        <circle
          cx={cx} cy={cy} r={innerR * coreScale}
          fill="none" stroke={accent} strokeWidth={3} opacity={0.85}
        />
        <circle cx={cx} cy={cy} r={innerR * coreScale * 0.62} fill="#0b1020" stroke={accent} strokeWidth={2} opacity={0.9} />

        {/* 下部波形 */}
        <path d={wfPath} fill="none" stroke={accent} strokeWidth={2.5} opacity={0.55} strokeLinejoin="round" />
      </svg>

      {/* 中央タイトル（声で微妙にスケール） */}
      <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
        <div
          style={{
            fontFamily: 'Inter, system-ui, sans-serif',
            fontWeight: 800,
            fontSize: 76,
            letterSpacing: -1,
            color: '#fff',
            transform: `scale(${titleScale})`,
            textShadow: `0 0 ${20 + bass * 50}px ${accent}`,
          }}
        >
          {title}
        </div>
      </AbsoluteFill>

      {/* うっすらビネット */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(120% 100% at 50% 50%, transparent 45%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
