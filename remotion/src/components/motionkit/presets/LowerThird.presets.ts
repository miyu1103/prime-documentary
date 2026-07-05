import type {ComponentProps} from 'react';
import type {LowerThird} from '../LowerThird';

// =====================================================================
// MOTIONKIT — LowerThird presets（放送用ロワーサード名札カタログ）
//   Prime Documentary のスレートに合わせた汎用ロール名札。
//   実在人物名・実在ロゴは一切使わない（invariant 11）。すべて総称の
//   役職／所属で構成。accent は BRAND 既定ゴールドを上書きしたい時だけ指定。
//   使い方: <LowerThird {...lowerThirdPresets['former-prosecutor']} />
// =====================================================================

// アクセント色（accent 上書き用の定数。BRAND.color 由来だが依存を持たない）
const ACCENT_ELECTRIC = '#1F6BFF'; // 電気ブルー（捜査・テック系）
const ACCENT_GOLD = '#E5B53A'; // ゴールド（既定・法曹系）
const ACCENT_CRIMSON = '#C7402F'; // クリムゾン（内部告発・警告系）
const ACCENT_TEAL = '#2FA8A0'; // ティール（医療・科学系）
const ACCENT_SILVER = '#C8CDD6'; // シルバー（匿名・中立系）

export const lowerThirdPresets = {
  // --- 法曹・司法（Legal / Judiciary）--------------------------------
  'former-prosecutor': {
    primary: 'Former Prosecutor',
    secondary: "U.S. Attorney's Office",
  },
  'defense-attorney': {
    primary: 'Defense Attorney',
    secondary: 'Counsel for the Defense',
  },
  'constitutional-scholar': {
    primary: 'Constitutional Law Scholar',
    secondary: 'School of Law',
  },
  'retired-judge': {
    primary: 'Retired Trial Judge',
    secondary: 'State Superior Court',
  },
  'appellate-clerk': {
    primary: 'Former Appellate Clerk',
    secondary: 'Court of Appeals',
  },
  'district-attorney': {
    primary: 'District Attorney',
    secondary: "County Prosecutor's Office",
  },

  // --- 捜査・法執行（Investigation / Law Enforcement）----------------
  'lead-investigator': {
    primary: 'Lead Investigator',
    secondary: 'Major Case Unit',
    accent: ACCENT_ELECTRIC,
  },
  'fbi-special-agent': {
    primary: 'Former Special Agent',
    secondary: 'Federal Bureau of Investigation',
    accent: ACCENT_ELECTRIC,
  },
  'forensic-examiner': {
    primary: 'Forensic Examiner',
    secondary: 'Crime Laboratory',
    accent: ACCENT_ELECTRIC,
  },
  'homicide-detective': {
    primary: 'Retired Homicide Detective',
    secondary: 'Metropolitan Police Department',
    accent: ACCENT_ELECTRIC,
  },
  'evidence-analyst': {
    primary: 'Digital Evidence Analyst',
    secondary: 'Cyber Forensics Division',
    accent: ACCENT_ELECTRIC,
  },

  // --- 金融・企業（Finance / Corporate）-----------------------------
  'securities-analyst': {
    primary: 'Securities Analyst',
    secondary: 'Independent Research Firm',
    accent: ACCENT_GOLD,
  },
  'forensic-accountant': {
    primary: 'Forensic Accountant',
    secondary: 'Fraud Examination Practice',
    accent: ACCENT_GOLD,
  },
  'sec-enforcement': {
    primary: 'Former Enforcement Attorney',
    secondary: 'Securities & Exchange Commission',
    accent: ACCENT_GOLD,
  },
  'venture-investor': {
    primary: 'Early-Stage Investor',
    secondary: 'Venture Capital Partner',
    accent: ACCENT_GOLD,
  },
  'market-regulator': {
    primary: 'Market Regulator',
    secondary: 'Commodity Futures Oversight',
    accent: ACCENT_GOLD,
  },

  // --- 内部告発・当事者（Whistleblower / Subjects）-----------------
  'the-whistleblower': {
    primary: 'The Whistleblower',
    secondary: 'Identity Protected',
    accent: ACCENT_CRIMSON,
  },
  'former-employee': {
    primary: 'Former Employee',
    secondary: 'Spoke on Condition of Anonymity',
    accent: ACCENT_CRIMSON,
  },
  'company-insider': {
    primary: 'Company Insider',
    secondary: 'Former Executive Team',
    accent: ACCENT_CRIMSON,
  },
  'anonymous-witness': {
    primary: 'Anonymous Witness',
    secondary: 'Voice & Likeness Altered',
    accent: ACCENT_SILVER,
  },

  // --- 科学・医療（Science / Medical）-------------------------------
  'medical-examiner': {
    primary: 'Chief Medical Examiner',
    secondary: 'Office of the Coroner',
    accent: ACCENT_TEAL,
  },
  'research-scientist': {
    primary: 'Research Scientist',
    secondary: 'Institute of Molecular Biology',
    accent: ACCENT_TEAL,
  },
  'bioethics-expert': {
    primary: 'Bioethics Expert',
    secondary: 'Center for Medical Ethics',
    accent: ACCENT_TEAL,
  },

  // --- 報道・学術（Press / Academia）-------------------------------
  'investigative-journalist': {
    primary: 'Investigative Journalist',
    secondary: 'Award-Winning Reporter',
  },
  'documentary-historian': {
    primary: 'Documentary Historian',
    secondary: 'Department of History',
  },
  'true-crime-author': {
    primary: 'Best-Selling Author',
    secondary: 'True Crime Correspondent',
  },

  // --- 汎用・単行（Generic single-line）----------------------------
  'expert-witness': {
    primary: 'Expert Witness',
  },
  'case-narration': {
    primary: 'The Case',
    secondary: 'A Prime Documentary Investigation',
    accent: ACCENT_GOLD,
  },
} satisfies Record<string, ComponentProps<typeof LowerThird>>;
