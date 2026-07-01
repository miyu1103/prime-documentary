import {Config} from '@remotion/cli/config';
import os from 'os';

// =====================================================================
// クオリティ最優先・ローカルCPUレンダ（libx264）。NVENCには切り替えない。
// 正典値（docs オープニング設計ルール / pino-channel と一致 / one-pass spec row 6）。
// 2026-06-28: 旧設定(jpeg＋上書きのみ)から正典値へ昇格。published mp4 は再レンダしない(invariant6)。
// =====================================================================

// 中間フレームはロスレスPNG（jpegの圧縮劣化＝画面の"くすみ/ブロック"を排除）
Config.setVideoImageFormat('png');

// 配信用コーデックはH.264（libx264 / CPU）
Config.setCodec('h264');

// CRF=16：数値が小さいほど高品質。16はほぼ視覚的ロスレス（one-pass spec row6と一致）
Config.setCrf(16);

// 全プレーヤー互換のyuv420p
Config.setPixelFormat('yuv420p');

// 色域を明示して色ズレ（くすみ/転び）を防止
Config.setColorSpace('bt709');

// 音声は最高ビットレートのAAC
Config.setAudioCodec('aac');
Config.setAudioBitrate('320k');

// 全CPUコアを使う（最大並列）
Config.setConcurrency(os.cpus().length);

// GPU合成をANGLEで安定化（モーションブラー/グロー/グラデの破綻防止）
Config.setChromiumOpenGlRenderer('angle');

Config.setOverwriteOutput(true);
