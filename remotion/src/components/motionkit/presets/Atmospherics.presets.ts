import type {ComponentProps} from 'react';
import type {
  DustMotes,
  SoftGlow,
  FilmGrain,
  VignetteBreath,
} from '../Atmospherics';
import {BRAND} from '../../../brand';

// =====================================================================
// Atmospherics — プリセットカタログ（空気感オーバーレイ4種）。
//   色はブランドトークンのみ（brand.ts）。dur はフレーム単位（fps=30 基準、
//   30f=1秒）。省略時は Composition の durationInFrames を継承。
//   ムード語彙: somber(沈痛) / tense(緊張) / hopeful(希望) / cold(冷) /
//   warm(温) / neutral(標準)。各コンポーネントの EXACT props を満たす。
// =====================================================================

// ---------------------------------------------------------------------
// DustMotes — count? / color? / dur?（漂う塵）。
//   count で密度、color でムード、dur でカット尺に合わせる。
// ---------------------------------------------------------------------
export const dustMotesPresets = {
  // somber — 疎らな銀塵。沈黙の法廷・追想カット向け
  'dust-somber-sparse': {count: 22, color: BRAND.color.silver},
  // neutral — 標準密度の銀塵。汎用オーバーレイの既定
  'dust-neutral': {count: 40, color: BRAND.color.silver},
  // tense — 密で細かい塵、白寄りで張り詰めた空気
  'dust-tense-dense': {count: 70, color: BRAND.color.white},
  // cold — 電光ブルーの塵。取調室・夜間・監視カット
  'dust-cold-electric': {count: 48, color: BRAND.color.electric},
  // warm — 金の微塵。回想・希望・和解の場面
  'dust-warm-gold': {count: 30, color: BRAND.color.gold},
  // hopeful — 明るい白塵をやや多めに。開放・救済のトーン
  'dust-hopeful-white': {count: 55, color: BRAND.color.white},
  // deep-navy — 沈んだネイビー塵。重い導入・背景に溶ける
  'dust-deep-navy': {count: 34, color: BRAND.color.navy},
  // ultra-fine — 高密度の微粒。ヒーローショット上の質感付け
  'dust-ultra-fine': {count: 90, color: BRAND.color.silver},
  // whisper — ごく僅かな塵。字幕/インタビューを邪魔しない最小演出
  'dust-whisper': {count: 14, color: BRAND.color.silver},
} satisfies Record<string, ComponentProps<typeof DustMotes>>;

// ---------------------------------------------------------------------
// SoftGlow — color? / dur?（緩やかに周回する放射グロー）。
//   1つ目の色を指定（2つ目は常にブランド navy 固定・実装側）。
// ---------------------------------------------------------------------
export const softGlowPresets = {
  // neutral — 電光ブルーの既定グロー。汎用の空気奥行き
  'glow-neutral-electric': {color: BRAND.color.electric},
  // cold — ネイビー同士の低体温グロー。夜/監視/尋問
  'glow-cold-navy': {color: BRAND.color.navy},
  // warm — 金のグロー。希望・和解・エピローグ
  'glow-warm-gold': {color: BRAND.color.gold},
  // somber — 沈んだインクのグロー。重い導入・喪失
  'glow-somber-ink': {color: BRAND.color.ink},
  // hopeful — 白いソフトライト。朝・救済・解放
  'glow-hopeful-white': {color: BRAND.color.white},
  // silver — 銀の中立グロー。証拠提示・アーカイブ
  'glow-silver-archive': {color: BRAND.color.silver},
  // tense — 電光ブルーで張り詰めた奥行き（既定と同色・意味付け違い）
  'glow-tense-electric': {color: BRAND.color.electric},
} satisfies Record<string, ComponentProps<typeof SoftGlow>>;

// ---------------------------------------------------------------------
// FilmGrain — dur? のみ（フィルムグレイン、overlay）。
//   強度は実装固定（0.05–0.09 呼吸）。dur はカット尺への同期のみ。
// ---------------------------------------------------------------------
export const filmGrainPresets = {
  // default — Composition 尺を継承（最も汎用）
  'grain-default': {},
  // beat-1s — 1秒ビート（フック内カット刻み）
  'grain-beat-1s': {dur: 30},
  // short-2s — 2秒の短カット
  'grain-short-2s': {dur: 60},
  // cut-3s — 標準カット尺
  'grain-cut-3s': {dur: 90},
  // scene-5s — シーン尺
  'grain-scene-5s': {dur: 150},
  // long-8s — 長回しカット
  'grain-long-8s': {dur: 240},
  // hold-10s — 10秒ホールド（ヒーロー/引き）
  'grain-hold-10s': {dur: 300},
} satisfies Record<string, ComponentProps<typeof FilmGrain>>;

// ---------------------------------------------------------------------
// VignetteBreath — dur? のみ（周辺減光の息づき、overlay）。
//   強度は実装固定（0.28–0.5 のイーズド正弦）。dur は尺同期のみ。
// ---------------------------------------------------------------------
export const vignetteBreathPresets = {
  // default — Composition 尺を継承（最も汎用）
  'vignette-default': {},
  // beat-1s — 1秒ビート（フックの緊張カット）
  'vignette-beat-1s': {dur: 30},
  // short-2s — 2秒の短カット
  'vignette-short-2s': {dur: 60},
  // cut-3s — 標準カット尺
  'vignette-cut-3s': {dur: 90},
  // scene-5s — シーン尺（一呼吸の沈静）
  'vignette-scene-5s': {dur: 150},
  // long-8s — 長回しの緩い呼吸
  'vignette-long-8s': {dur: 240},
  // hold-15s — 長尺ホールド（導入/エピローグ）
  'vignette-hold-15s': {dur: 450},
} satisfies Record<string, ComponentProps<typeof VignetteBreath>>;
