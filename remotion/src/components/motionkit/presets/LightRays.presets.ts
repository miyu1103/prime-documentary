import type {ComponentProps} from 'react';
import type {LightRays} from '../LightRays';

// =====================================================================
// LightRays プリセット集
//   透明のボリューメトリック god-ray オーバーレイ。実映像/カットの上に screen 合成。
//   使えるのは以下2つのみ（LightRays.tsx の props と厳密一致）:
//     - color?: string  … シャフト/グロー/塵の色。BRANDパレットの hex のみ使う。
//     - dur?:   number  … 出入りエンベロープの尺（フレーム）。省略時は composition
//                          の durationInFrames を採用。fps60 前提（60=1.0秒）。
//   ブランドパレット:
//     electric #1F6BFF / gold #E5B53A / silver #C8CDD6 / white #F5F7FA
// =====================================================================
export const lightRaysPresets = {
  // --- 既定（bare）: props なし。electric/white の標準ゴッドレイ ---------
  'default': {},

  // --- Cold / 冷たい・厳格（青〜銀）: 尋問前夜・監視・法の冷たさ ---------
  'cold-shafts': {color: '#1F6BFF'}, // electric: 冷たい青い光条
  'surveillance-blue': {color: '#1F6BFF'}, // 監視・青の緊張
  'steel-morning': {color: '#C8CDD6'}, // silver: 硬い鋼色の朝

  // --- Hope / 希望・救済（金）: 無実の証明・恩赦・夜明け ------------------
  'hope-rays': {color: '#E5B53A'}, // gold: 希望の光条
  'dawn-verdict': {color: '#E5B53A'}, // 夜明けの評決・救済
  'holy-descent': {color: '#E5B53A', dur: 150}, // 神々しく差し込む・ゆっくり(2.5s)

  // --- Interrogation / 尋問・追及（白）: 眩しい詰問・供述室 --------------
  'interrogation-glare': {color: '#F5F7FA'}, // white: 眩しい尋問のグレア
  'confession-room': {color: '#F5F7FA', dur: 90}, // 供述室・引き締めた尺(1.5s)

  // --- Neutral / 中立・上品（銀白）: タイトル/引用のさりげない後光 ------
  'silver-veil': {color: '#C8CDD6'}, // silver: 上品な銀のベール
  'quiet-archive': {color: '#F5F7FA', dur: 120}, // 静かな記録・2.0s

  // --- Duration variants / 尺バリエーション（fps60・色は既定electric） ---
  'quick-flare': {dur: 45}, // 短い一閃・0.75s
  'lingering-glow': {dur: 240}, // 長く残る後光・4.0s
} satisfies Record<string, ComponentProps<typeof LightRays>>;
