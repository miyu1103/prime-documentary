import type {ComponentProps} from 'react';
import type {EvidenceCard} from '../EvidenceCard';

// =====================================================================
// EvidenceCard preset catalog — MOTIONKIT
//   証拠／展示カードのシネマティックSCENE用プリセット。Prime Documentary の
//   スレート（金融詐欺・実録犯罪・法廷/憲法・科学捜査・調査報道・企業不正）
//   向けにチューニング。
//
//   RULES:
//   - tag は展示ラベルの総称（'EXHIBIT A'..'EXHIBIT F' / "STATE'S EVIDENCE" /
//     'DEFENSE EXHIBIT 12' など）。実在の事件番号・機関ロゴは不使用。
//   - caption は一般的・匿名の展示説明（実在人物の肖像・氏名・企業名なし）。
//   - dur は EvidenceCard 側で durationInFrames にフォールバックするため未指定。
// =====================================================================

export const evidenceCardPresets = {
  // -------------------------------------------------------------------
  // Financial fraud / 金融詐欺・不正会計（書類・送金）
  // -------------------------------------------------------------------
  'fraud-forged-wire': {
    tag: 'EXHIBIT A',
    caption: 'The forged wire transfer',
  },
  'fraud-doctored-ledger': {
    tag: 'EXHIBIT B',
    caption: 'The doctored accounting ledger',
  },
  'fraud-shell-company': {
    tag: 'EXHIBIT C',
    caption: 'The paperwork for a shell company that never existed',
  },
  'fraud-offshore-account': {
    tag: 'EXHIBIT D',
    caption: 'A statement from the hidden offshore account',
  },
  'fraud-falsified-audit': {
    tag: "STATE'S EVIDENCE",
    caption: 'The falsified audit report',
  },

  // -------------------------------------------------------------------
  // Digital / communications / デジタル証拠・通信
  // -------------------------------------------------------------------
  'digital-deleted-email': {
    tag: 'EXHIBIT E',
    caption: 'The deleted email, recovered from the server',
  },
  'digital-encrypted-message': {
    tag: 'EXHIBIT F',
    caption: 'The encrypted message that gave the plan away',
  },
  'digital-hidden-drive': {
    tag: 'EXHIBIT G',
    caption: 'The hard drive found hidden behind the wall',
  },
  'digital-phone-log': {
    tag: "STATE'S EVIDENCE",
    caption: 'The phone log placing the call at midnight',
  },
  'digital-security-footage': {
    tag: 'EXHIBIT H',
    caption: 'A single frame from the security footage',
  },

  // -------------------------------------------------------------------
  // True crime / physical evidence / 実録犯罪・物証
  // -------------------------------------------------------------------
  'crime-murder-weapon': {
    tag: 'EXHIBIT 1',
    caption: 'The murder weapon',
  },
  'crime-bloodstained-note': {
    tag: "STATE'S EVIDENCE",
    caption: 'The bloodstained note left at the scene',
  },
  'crime-anonymous-letter': {
    tag: 'EXHIBIT 2',
    caption: 'The anonymous letter that reopened the case',
  },
  'crime-torn-photograph': {
    tag: 'EXHIBIT 3',
    caption: 'The torn photograph found in the ashes',
  },
  'crime-getaway-map': {
    tag: 'DEFENSE EXHIBIT 12',
    caption: 'A hand-drawn map of the getaway route',
  },

  // -------------------------------------------------------------------
  // Forensic / lab / 科学捜査・鑑定
  // -------------------------------------------------------------------
  'forensic-falsified-lab': {
    tag: "STATE'S EVIDENCE",
    caption: 'The falsified lab report',
  },
  'forensic-dna-mismatch': {
    tag: 'EXHIBIT 4',
    caption: 'The DNA result that never matched',
  },
  'forensic-fingerprint-card': {
    tag: 'EXHIBIT 5',
    caption: 'The fingerprint lifted from the doorframe',
  },
  'forensic-autopsy-chart': {
    tag: 'DEFENSE EXHIBIT 12',
    caption: 'The autopsy chart the jury never saw',
  },

  // -------------------------------------------------------------------
  // Legal / constitutional / 法廷・憲法（判例もの）
  // -------------------------------------------------------------------
  'legal-signed-confession': {
    tag: "STATE'S EVIDENCE",
    caption: 'The signed confession taken without a lawyer',
  },
  'legal-sealed-warrant': {
    tag: 'EXHIBIT 6',
    caption: 'The search warrant that was never signed',
  },
  'legal-suppressed-memo': {
    tag: 'DEFENSE EXHIBIT 12',
    caption: 'The internal memo the defense fought to unseal',
  },

  // -------------------------------------------------------------------
  // Corporate / investigation / 企業不正・調査報道
  // -------------------------------------------------------------------
  'corp-shredded-contract': {
    tag: 'EXHIBIT 7',
    caption: 'The contract that was shredded, then reassembled',
  },
  'corp-whistleblower-file': {
    tag: 'EXHIBIT 8',
    caption: "The whistleblower's file, smuggled out on a drive",
  },
  'corp-leaked-blueprint': {
    tag: 'EXHIBIT 9',
    caption: 'The leaked blueprint of a product that never worked',
  },
} satisfies Record<string, ComponentProps<typeof EvidenceCard>>;
