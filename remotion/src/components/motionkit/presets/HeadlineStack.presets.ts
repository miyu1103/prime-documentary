import type {ComponentProps} from 'react';
import type {HeadlineStack} from '../HeadlineStack';

// =====================================================================
// MOTIONKIT — HeadlineStack PRESETS (Prime Documentary)
//   報道モンタージュSCENE（新聞クリッピング風カードの飛び込み積層）の
//   使い回しカタログ。すべて HeadlineStack の props 型に厳密適合。
//   props: headlines(必須: string[]) / dur?(任意・未指定推奨)
//   ・見出しは一流全国紙のトーン（総称・架空。実在の媒体名/ロゴ/実在人名は不使用）。
//   ・1セットあたり 3〜6 本。カードは飛び込み順に前面へ積層するので、
//     配列は「時系列に事態が動いていく」並びにしてある（速報→続報→帰結）。
//   ・dur は意図的に未指定（Composition の durationInFrames をそのまま使う）。
//   使い方: <HeadlineStack {...headlineStackPresets['scandal-breaking']} />
// =====================================================================

export const headlineStackPresets = {
  // --- スキャンダル速報（A scandal breaking：疑惑が一気に表面化） -------
  'scandal-breaking': {
    headlines: [
      'Documents Reveal Years of Hidden Payments',
      'Executives Named in Widening Inquiry',
      'Board Calls Emergency Session at Dawn',
      'Pressure Mounts for Full Disclosure',
    ],
  },
  'scandal-political': {
    headlines: [
      'Leaked Memos Point to the Highest Office',
      'Aides Ordered to Preserve Every File',
      'Opposition Demands an Independent Probe',
      'Capital Braces for a Long Reckoning',
    ],
  },
  'scandal-corporate-ethics': {
    headlines: [
      'Firm Accused of Silencing Internal Alarms',
      'Auditors Flagged Concerns Two Years Ago',
      'Shares Slide as Questions Multiply',
      'Regulators Signal a Formal Review',
    ],
  },
  'scandal-doping-sport': {
    headlines: [
      'Champion Under Investigation Over Samples',
      'Federation Suspends Program Pending Review',
      'Sponsors Distance Themselves Overnight',
      'Records Now Cast in Doubt',
    ],
  },

  // --- 市場暴落（A market crash：パニックから連鎖へ） ------------------
  'market-crash': {
    headlines: [
      'Markets Plunge in Steepest Fall on Record',
      'Panic Selling Grips Trading Floors',
      'Billions Erased Before the Closing Bell',
      'Central Banks Weigh Emergency Action',
      'Investors Told to Brace for More',
    ],
  },
  'market-flash-crash': {
    headlines: [
      'Indexes Collapse in a Matter of Minutes',
      'Trades Frozen as Systems Buckle',
      'Regulators Scramble to Explain the Void',
      'Order Restored, but Confidence Is Not',
    ],
  },
  'market-bank-run': {
    headlines: [
      'Depositors Line the Streets at First Light',
      'Lender Halts Withdrawals to Stem the Tide',
      'Contagion Fears Spread Across the Sector',
      'Officials Pledge to Guarantee Accounts',
    ],
  },
  'market-housing-bust': {
    headlines: [
      'Home Prices Post Sharpest Drop in Decades',
      'Foreclosure Notices Pile Up Nationwide',
      'Lenders Tighten as Defaults Surge',
      'A Generation Left Holding the Losses',
    ],
  },

  // --- 逮捕（An arrest：捜査が身柄確保に至る） ------------------------
  'arrest-dramatic': {
    headlines: [
      'Suspect Taken Into Custody Before Dawn',
      'Agents Seize Records in Coordinated Raids',
      'Charges Span Fraud and Conspiracy',
      'Bail Denied as Flight Risk Cited',
    ],
  },
  'arrest-white-collar': {
    headlines: [
      'Financier Detained on Fraud Charges',
      'Assets Frozen Across Three Jurisdictions',
      'Investors Left Counting the Losses',
      'Prosecutors Vow to Follow the Money',
    ],
  },
  'arrest-fugitive-caught': {
    headlines: [
      'Fugitive Captured After Years on the Run',
      'Trail Led Across Borders and Aliases',
      'Extradition Proceedings Begin at Once',
      'Victims Await a Day in Court',
    ],
  },
  'arrest-raid-dawn': {
    headlines: [
      'Predawn Raid Ends a Long Manhunt',
      'Evidence Hauled Out in Sealed Crates',
      'Neighbors Describe a Quiet Facade',
      'Investigators Say the Case Is Only Beginning',
    ],
  },

  // --- 裁判の評決（A trial verdict：審理から判決へ） -------------------
  'trial-verdict-guilty': {
    headlines: [
      'Jury Returns a Verdict of Guilty',
      'Courtroom Falls Silent as It Is Read',
      'Sentencing Set for Later This Month',
      'Victims Say Justice Has Been Served',
    ],
  },
  'trial-verdict-acquittal': {
    headlines: [
      'Defendant Acquitted on All Counts',
      'Prosecution Case Falters Under Scrutiny',
      'Reaction Splits the Courthouse Steps',
      'Questions Linger Over What Went Wrong',
    ],
  },
  'trial-landmark-ruling': {
    headlines: [
      'High Court Issues a Landmark Ruling',
      'Decision Set to Reshape the Law',
      'Dissent Warns of Sweeping Consequences',
      'Both Sides Claim a Kind of Victory',
    ],
  },
  'trial-opening-day': {
    headlines: [
      'Long-Awaited Trial Opens to a Packed Gallery',
      'Prosecutors Promise a Mountain of Evidence',
      'Defense Insists the Case Is Circumstantial',
      'A Nation Watches the First Witness',
    ],
  },
  'trial-appeal-overturned': {
    headlines: [
      'Appeals Court Overturns the Conviction',
      'Judges Cite Grave Errors at Trial',
      'A New Hearing Is Ordered',
      'Families Left to Relive the Ordeal',
    ],
  },

  // --- 隠蔽の暴露（A cover-up exposed：内部告発から追及へ） -------------
  'coverup-exposed': {
    headlines: [
      'Whistleblower Alleges a Years-Long Cover-Up',
      'Internal Files Contradict Public Denials',
      'Officials Insisted There Was Nothing to Hide',
      'Calls Grow for Those Responsible to Answer',
      'The Paper Trail Tells Another Story',
    ],
  },
  'coverup-safety-hidden': {
    headlines: [
      'Company Knew of the Danger for Years',
      'Warnings Buried, Memos Show',
      'Families Demand to Know Who Signed Off',
      'Regulators Failed to Act on Early Signs',
    ],
  },
  'coverup-documents-shredded': {
    headlines: [
      'Investigators Find Records Deliberately Destroyed',
      'Missing Files Point to a Wider Scheme',
      'Testimony Unravels the Official Account',
      'The Truth Kept Just Out of View',
    ],
  },
  'coverup-institutional': {
    headlines: [
      'Institution Accused of Protecting Its Own',
      'Complaints Were Quietly Set Aside',
      'Leadership Faces a Reckoning at Last',
      'Survivors Speak After Years of Silence',
    ],
  },

  // --- 破綻・崩壊（A collapse：企業/計画の瓦解） ----------------------
  'empire-collapse': {
    headlines: [
      'A Sprawling Empire Falls in a Single Week',
      'Creditors Move In as Cash Runs Dry',
      'Thousands of Jobs Hang in the Balance',
      'From Golden Child to Cautionary Tale',
    ],
  },
  'scheme-unravels': {
    headlines: [
      'Investors Discover the Returns Were Never Real',
      'A House of Cards Finally Gives Way',
      'Losses Are Counted in the Billions',
      'How Did So Many Miss the Signs',
      'The Reckoning Reaches the Top',
    ],
  },
  'startup-implosion': {
    headlines: [
      'Once-Celebrated Startup Collapses Overnight',
      'Promised Breakthrough Was Never Real',
      'Backers and Patients Left in the Dark',
      'A Founder\'s Vision Meets Hard Questions',
    ],
  },

  // --- 未解決・追跡（Unsolved & manhunt：長期報道の帯） --------------
  'heist-unsolved': {
    headlines: [
      'Priceless Works Vanish in an Overnight Heist',
      'Investigators Chase a Cold and Winding Trail',
      'A Reward Grows as Leads Run Dry',
      'Decades On, the Case Remains Open',
    ],
  },
  'missing-money-hunt': {
    headlines: [
      'Where Did the Missing Millions Go',
      'Accounts Traced Through a Maze of Shells',
      'Trail Cools Behind Sealed Borders',
      'Victims Wait for Answers That Never Come',
    ],
  },
} satisfies Record<string, ComponentProps<typeof HeadlineStack>>;
