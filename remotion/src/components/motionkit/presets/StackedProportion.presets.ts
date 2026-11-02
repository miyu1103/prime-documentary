import type {ComponentProps} from 'react';
import type {StackedProportion} from '../StackedProportion';

// =====================================================================
// PRESET CATALOG — StackedProportion
//   100% breakdown scenarios tuned to Prime Documentary storytelling:
//   where the money went, how time was spent, verdict outcomes, budget
//   allocation, and population splits. `value`s are normalized to their
//   sum inside the component, so raw magnitudes stand in for real figures.
//   Labels are GENERIC (reusable across episodes). Brand accents only:
//     electric #1F6BFF · gold #E5B53A · silver #C8CDD6 · white #F5F7FA
//   `dur` is intentionally omitted (inherits composition duration).
// =====================================================================

export const stackedProportionPresets = {
  // ---------------------------------------------------------------
  // Where the money went (fraud / scheme dissection)
  // ---------------------------------------------------------------
  'money-lifestyle-vs-victims': {
    title: 'WHERE THE MONEY WENT',
    parts: [
      {label: 'Personal Lifestyle', value: 58, accent: '#E5B53A'},
      {label: 'New Investors Paid Out', value: 31, accent: '#1F6BFF'},
      {label: 'Actually Recovered', value: 11, accent: '#C8CDD6'},
    ],
  },
  'money-scheme-flow': {
    title: 'FOLLOW THE MONEY',
    parts: [
      {label: 'Founders & Insiders', value: 44},
      {label: 'Marketing & Recruiting', value: 27},
      {label: 'Operating Costs', value: 18},
      {label: 'Refunds to Victims', value: 11},
    ],
  },
  'money-stolen-funds': {
    parts: [
      {label: 'Untraceable / Spent', value: 62, accent: '#E5B53A'},
      {label: 'Frozen by Court', value: 25, accent: '#1F6BFF'},
      {label: 'Returned to Victims', value: 13, accent: '#C8CDD6'},
    ],
  },
  'money-shell-companies': {
    title: 'THE PAPER TRAIL',
    parts: [
      {label: 'Offshore Accounts', value: 47},
      {label: 'Real Estate', value: 33},
      {label: 'Luxury Assets', value: 20},
    ],
  },

  // ---------------------------------------------------------------
  // Budget allocation (production / campaign / institutional spend)
  // ---------------------------------------------------------------
  'budget-allocation-four': {
    title: 'HOW THE BUDGET WAS SPENT',
    parts: [
      {label: 'Payroll', value: 41, accent: '#1F6BFF'},
      {label: 'Facilities', value: 24, accent: '#C8CDD6'},
      {label: 'Equipment', value: 21, accent: '#E5B53A'},
      {label: 'Overhead', value: 14, accent: '#F5F7FA'},
    ],
  },
  'budget-legal-defense': {
    title: 'COST OF THE DEFENSE',
    parts: [
      {label: 'Attorney Fees', value: 54},
      {label: 'Expert Witnesses', value: 26},
      {label: 'Investigation', value: 20},
    ],
  },
  'budget-campaign-spend': {
    parts: [
      {label: 'Advertising', value: 48, accent: '#E5B53A'},
      {label: 'Staff & Field', value: 29, accent: '#1F6BFF'},
      {label: 'Events', value: 14, accent: '#C8CDD6'},
      {label: 'Compliance', value: 9, accent: '#F5F7FA'},
    ],
  },
  'budget-relief-fund': {
    title: 'WHERE THE AID WENT',
    parts: [
      {label: 'Direct Payments', value: 63},
      {label: 'Administration', value: 22},
      {label: 'Lost to Fraud', value: 15, accent: '#E5B53A'},
    ],
  },

  // ---------------------------------------------------------------
  // Verdict & case outcomes (charges, sentencing, appeals)
  // ---------------------------------------------------------------
  'verdict-guilty-vs-acquitted': {
    title: 'THE VERDICT',
    parts: [
      {label: 'Guilty', value: 71, accent: '#E5B53A'},
      {label: 'Acquitted', value: 18, accent: '#1F6BFF'},
      {label: 'Mistrial', value: 11, accent: '#C8CDD6'},
    ],
  },
  'verdict-charges-disposition': {
    title: 'HOW THE CHARGES RESOLVED',
    parts: [
      {label: 'Convicted', value: 52},
      {label: 'Plea Deal', value: 28},
      {label: 'Dismissed', value: 20},
    ],
  },
  'verdict-case-load': {
    parts: [
      {label: 'Settled', value: 64, accent: '#1F6BFF'},
      {label: 'Went to Trial', value: 24, accent: '#E5B53A'},
      {label: 'Dropped', value: 12, accent: '#C8CDD6'},
    ],
  },
  'verdict-appeal-outcomes': {
    title: 'ON APPEAL',
    parts: [
      {label: 'Upheld', value: 68},
      {label: 'Reduced', value: 21},
      {label: 'Overturned', value: 11, accent: '#E5B53A'},
    ],
  },
  'verdict-sentence-served': {
    title: 'THE SENTENCE',
    parts: [
      {label: 'Time Served', value: 34, accent: '#C8CDD6'},
      {label: 'Suspended', value: 41, accent: '#1F6BFF'},
      {label: 'Parole', value: 25, accent: '#E5B53A'},
    ],
  },

  // ---------------------------------------------------------------
  // How time was spent (timelines, effort, workday splits)
  // ---------------------------------------------------------------
  'time-investigation-phases': {
    title: 'HOW THE TIME WAS SPENT',
    parts: [
      {label: 'Surveillance', value: 38, accent: '#1F6BFF'},
      {label: 'Interviews', value: 27, accent: '#C8CDD6'},
      {label: 'Forensics', value: 22, accent: '#E5B53A'},
      {label: 'Paperwork', value: 13, accent: '#F5F7FA'},
    ],
  },
  'time-trial-days': {
    parts: [
      {label: 'Prosecution', value: 44},
      {label: 'Defense', value: 39},
      {label: 'Deliberation', value: 17},
    ],
  },
  'time-project-schedule': {
    title: 'THREE YEARS, DIVIDED',
    parts: [
      {label: 'Planning', value: 19},
      {label: 'Construction', value: 55},
      {label: 'Delays', value: 26, accent: '#E5B53A'},
    ],
  },
  'time-daily-routine': {
    parts: [
      {label: 'Work', value: 33, accent: '#1F6BFF'},
      {label: 'Sleep', value: 33, accent: '#C8CDD6'},
      {label: 'Everything Else', value: 34, accent: '#E5B53A'},
    ],
  },

  // ---------------------------------------------------------------
  // Population & demographic splits
  // ---------------------------------------------------------------
  'population-affected-split': {
    title: 'WHO WAS AFFECTED',
    parts: [
      {label: 'Directly Harmed', value: 46, accent: '#E5B53A'},
      {label: 'Indirectly Impacted', value: 37, accent: '#1F6BFF'},
      {label: 'Unaffected', value: 17, accent: '#C8CDD6'},
    ],
  },
  'population-age-brackets': {
    parts: [
      {label: 'Under 30', value: 28},
      {label: '30 to 50', value: 41},
      {label: 'Over 50', value: 31},
    ],
  },
  'population-region-share': {
    title: 'BY REGION',
    parts: [
      {label: 'Urban', value: 57},
      {label: 'Suburban', value: 29},
      {label: 'Rural', value: 14},
    ],
  },
  'population-victims-known': {
    title: 'THE VICTIMS',
    parts: [
      {label: 'Identified', value: 61, accent: '#1F6BFF'},
      {label: 'Presumed', value: 24, accent: '#C8CDD6'},
      {label: 'Never Found', value: 15, accent: '#E5B53A'},
    ],
  },

  // ---------------------------------------------------------------
  // Public opinion & response splits
  // ---------------------------------------------------------------
  'opinion-support-oppose': {
    title: 'PUBLIC OPINION',
    parts: [
      {label: 'Supported', value: 42, accent: '#1F6BFF'},
      {label: 'Opposed', value: 45, accent: '#E5B53A'},
      {label: 'Undecided', value: 13, accent: '#C8CDD6'},
    ],
  },
  'opinion-poll-three-way': {
    parts: [
      {label: 'Approve', value: 39},
      {label: 'Disapprove', value: 48},
      {label: 'No Opinion', value: 13},
    ],
  },
  'opinion-jury-lean': {
    title: 'THE JURY ROOM',
    parts: [
      {label: 'Convict', value: 75, accent: '#E5B53A'},
      {label: 'Acquit', value: 25, accent: '#1F6BFF'},
    ],
  },

  // ---------------------------------------------------------------
  // Two-part dramatic splits (odds, margins, before/after)
  // ---------------------------------------------------------------
  'split-recovered-vs-lost': {
    title: 'WHAT WAS RECOVERED',
    parts: [
      {label: 'Recovered', value: 9, accent: '#1F6BFF'},
      {label: 'Gone Forever', value: 91, accent: '#E5B53A'},
    ],
  },
  'split-narrow-margin': {
    parts: [
      {label: 'For', value: 51},
      {label: 'Against', value: 49},
    ],
  },
} satisfies Record<string, ComponentProps<typeof StackedProportion>>;
