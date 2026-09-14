import type {ComponentProps} from 'react';
import type {DocHighlight} from '../DocHighlight';

/**
 * Ready-made prop fills for DocHighlight (document-markup overlay).
 * Usage: <DocHighlight {...docHighlightPresets['key']} />
 * `rects` are {x,y,w,h} in 0..1 fractions of the frame; `mode`:
 *   'underline' 下線 / 'box' 枠囲み / 'redact' 黒塗り. Marks stagger per rect.
 */
export const docHighlightPresets = {
  // ── underline: single key clause / key line ──────────────────────
  'clause-key-line': {
    // 契約書の中ほど、重要な1行に下線
    rects: [{x: 0.14, y: 0.46, w: 0.62, h: 0.05}],
    mode: 'underline',
  },
  'statute-headline': {
    // 条文見出しを1本の太い下線で強調
    rects: [{x: 0.12, y: 0.2, w: 0.5, h: 0.06}],
    mode: 'underline',
  },
  'verdict-line': {
    // 判決文のキメの一行
    rects: [{x: 0.18, y: 0.55, w: 0.64, h: 0.045}],
    mode: 'underline',
  },
  'email-subject': {
    // メールの件名行だけ
    rects: [{x: 0.2, y: 0.14, w: 0.55, h: 0.04}],
    mode: 'underline',
  },
  // ── underline: multiple staggered lines (読み上げに追従) ──────────
  'testimony-three-lines': {
    // 証言の3行を上から順に（index ディレイでスタッガー）
    rects: [
      {x: 0.16, y: 0.34, w: 0.66, h: 0.04},
      {x: 0.16, y: 0.42, w: 0.58, h: 0.04},
      {x: 0.16, y: 0.5, w: 0.7, h: 0.04},
    ],
    mode: 'underline',
  },
  'contract-terms-stack': {
    // 契約条項を段階的に下線でなぞる
    rects: [
      {x: 0.15, y: 0.3, w: 0.6, h: 0.035},
      {x: 0.15, y: 0.38, w: 0.68, h: 0.035},
      {x: 0.15, y: 0.46, w: 0.52, h: 0.035},
      {x: 0.15, y: 0.54, w: 0.64, h: 0.035},
    ],
    mode: 'underline',
  },
  'ledger-rows': {
    // 帳簿の数行を順に下線
    rects: [
      {x: 0.1, y: 0.4, w: 0.8, h: 0.03},
      {x: 0.1, y: 0.47, w: 0.8, h: 0.03},
      {x: 0.1, y: 0.54, w: 0.8, h: 0.03},
    ],
    mode: 'underline',
  },
  'signature-line': {
    // 署名欄の下線（右下に短く）
    rects: [{x: 0.55, y: 0.78, w: 0.32, h: 0.035}],
    mode: 'underline',
  },
  'dual-signature-lines': {
    // 双方の署名欄を左右に2本
    rects: [
      {x: 0.12, y: 0.8, w: 0.3, h: 0.03},
      {x: 0.56, y: 0.8, w: 0.3, h: 0.03},
    ],
    mode: 'underline',
  },
  'date-and-amount': {
    // 日付行と金額行の2箇所を強調
    rects: [
      {x: 0.6, y: 0.16, w: 0.26, h: 0.035},
      {x: 0.55, y: 0.62, w: 0.3, h: 0.045},
    ],
    mode: 'underline',
  },

  // ── box: boxed paragraph / callout ───────────────────────────────
  'boxed-paragraph': {
    // 中央の一段落を枠で囲む
    rects: [{x: 0.14, y: 0.34, w: 0.68, h: 0.24}],
    mode: 'box',
  },
  'box-header-block': {
    // 書類上部のヘッダーブロック
    rects: [{x: 0.1, y: 0.08, w: 0.8, h: 0.16}],
    mode: 'box',
  },
  'box-fine-print': {
    // 下部の細字条項を枠で指す
    rects: [{x: 0.14, y: 0.72, w: 0.72, h: 0.14}],
    mode: 'box',
  },
  'box-stamp-seal': {
    // 右上の押印/シールを正方形の枠で
    rects: [{x: 0.68, y: 0.1, w: 0.16, h: 0.16}],
    mode: 'box',
  },
  'box-two-columns': {
    // 左右2列の比較（順に枠が描かれる）
    rects: [
      {x: 0.1, y: 0.32, w: 0.36, h: 0.4},
      {x: 0.54, y: 0.32, w: 0.36, h: 0.4},
    ],
    mode: 'box',
  },
  'box-evidence-tag': {
    // 証拠写真内の小さな注目領域
    rects: [{x: 0.4, y: 0.38, w: 0.2, h: 0.18}],
    mode: 'box',
  },
  'box-form-fields': {
    // 記入フォームの複数フィールドを順に囲む
    rects: [
      {x: 0.16, y: 0.28, w: 0.66, h: 0.06},
      {x: 0.16, y: 0.4, w: 0.66, h: 0.06},
      {x: 0.16, y: 0.52, w: 0.4, h: 0.06},
    ],
    mode: 'box',
  },

  // ── redact: blacked-out records / classified ─────────────────────
  'redact-single-name': {
    // 氏名1箇所を黒塗り
    rects: [{x: 0.3, y: 0.3, w: 0.28, h: 0.05}],
    mode: 'redact',
  },
  'redact-record-stack': {
    // 記録の複数行を上から順に黒塗り（ワイプイン）
    rects: [
      {x: 0.15, y: 0.32, w: 0.6, h: 0.05},
      {x: 0.15, y: 0.42, w: 0.7, h: 0.05},
      {x: 0.15, y: 0.52, w: 0.5, h: 0.05},
      {x: 0.15, y: 0.62, w: 0.66, h: 0.05},
    ],
    mode: 'redact',
  },
  'redact-classified-heavy': {
    // 機密文書の大部分を黒塗り（密なスタック）
    rects: [
      {x: 0.12, y: 0.22, w: 0.76, h: 0.04},
      {x: 0.12, y: 0.29, w: 0.62, h: 0.04},
      {x: 0.12, y: 0.36, w: 0.74, h: 0.04},
      {x: 0.12, y: 0.43, w: 0.5, h: 0.04},
      {x: 0.12, y: 0.5, w: 0.7, h: 0.04},
      {x: 0.12, y: 0.57, w: 0.58, h: 0.04},
    ],
    mode: 'redact',
  },
  'redact-scattered-pii': {
    // 個人情報が散在する各所を黒塗り
    rects: [
      {x: 0.28, y: 0.24, w: 0.24, h: 0.04},
      {x: 0.55, y: 0.38, w: 0.22, h: 0.04},
      {x: 0.18, y: 0.52, w: 0.3, h: 0.04},
      {x: 0.5, y: 0.66, w: 0.2, h: 0.04},
    ],
    mode: 'redact',
  },
  'redact-ssn-account': {
    // 社会保障番号/口座番号の帯
    rects: [
      {x: 0.5, y: 0.34, w: 0.3, h: 0.045},
      {x: 0.5, y: 0.46, w: 0.34, h: 0.045},
    ],
    mode: 'redact',
  },
  'redact-signature-block': {
    // 署名/宛名ブロックを丸ごと黒塗り
    rects: [{x: 0.14, y: 0.74, w: 0.44, h: 0.12}],
    mode: 'redact',
  },

  // ── default fallback (mode omitted → underline) ──────────────────
  'default-underline': {
    // mode 未指定でもコンポーネント既定の下線で描画
    rects: [{x: 0.18, y: 0.48, w: 0.6, h: 0.05}],
  },
} satisfies Record<string, ComponentProps<typeof DocHighlight>>;
