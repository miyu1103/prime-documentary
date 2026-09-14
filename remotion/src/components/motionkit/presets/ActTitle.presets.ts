import type {ComponentProps} from 'react';
import type {ActTitle} from '../ActTitle';

// =====================================================================
// ActTitle preset catalog — 章/幕タイトルカードの量産プリセット。
//   PD スレート（連邦最高裁の判例／金融詐欺／実録犯罪／一般解説）に合わせた
//   kicker + title + index の組み合わせ。実在ロゴ・肖像・商標は使わない。
//   使い方: <ActTitle {...actTitlePresets['the-verdict']} />
//   dur は各シーンの尺で決まるため既定では設定しない（必要時のみ上書き）。
// =====================================================================

export const actTitlePresets = {
  // -----------------------------------------------------------------
  // 汎用ドラマ構成ビート（どのジャンルにも効く三幕〜五幕の背骨）
  // -----------------------------------------------------------------
  'the-setup': {kicker: 'Chapter One', title: 'The Setup', index: 1},
  'the-turn': {kicker: 'Chapter Two', title: 'The Turn', index: 2},
  'the-unraveling': {kicker: 'Chapter Three', title: 'The Unraveling', index: 3},
  'the-reckoning': {kicker: 'Chapter Four', title: 'The Reckoning', index: 4},
  'the-aftermath': {kicker: 'Chapter Five', title: 'The Aftermath', index: 5},

  // -----------------------------------------------------------------
  // 連邦最高裁・法廷（判例エピソードの主軸ジャンル）
  // -----------------------------------------------------------------
  'part-one-the-traffic-stop': {
    kicker: 'Part One',
    title: 'The Traffic Stop',
    index: 1,
  },
  'the-arrest': {kicker: 'The Record', title: 'The Arrest', index: 2},
  'the-question-of-law': {
    kicker: 'The Question',
    title: 'A Question of Law',
    index: 3,
  },
  'oral-argument': {kicker: 'Before The Court', title: 'Oral Argument', index: 4},
  'the-dissent': {kicker: 'Nine Justices', title: 'The Dissent', index: 5},
  'the-verdict': {kicker: 'The Ruling', title: 'The Verdict', index: 6},
  'the-precedent': {kicker: 'What It Meant', title: 'The Precedent'},

  // -----------------------------------------------------------------
  // 金融詐欺・企業スキャンダル（Theranos / OneCoin 系）
  // -----------------------------------------------------------------
  'the-pitch': {kicker: 'Act I', title: 'The Pitch', index: 1},
  'the-money': {kicker: 'Act II', title: 'Follow The Money', index: 2},
  'the-red-flags': {kicker: 'Warning Signs', title: 'The Red Flags', index: 3},
  'the-collapse': {kicker: 'Act III', title: 'The Collapse', index: 4},
  'the-indictment': {kicker: 'The Charges', title: 'The Indictment', index: 5},

  // -----------------------------------------------------------------
  // 実録犯罪・捜査（未解決事件 / 強盗 / 誤認 系）
  // -----------------------------------------------------------------
  'the-crime': {kicker: 'The Case', title: 'The Crime', index: 1},
  'the-investigation': {
    kicker: 'The Case',
    title: 'The Investigation',
    index: 2,
  },
  'the-evidence': {kicker: 'The Case', title: 'The Evidence', index: 3},
  'the-suspect': {kicker: 'The Case', title: 'The Suspect', index: 4},
  'the-cold-case': {kicker: 'Unsolved', title: 'The Cold Case'},
  'the-confession': {kicker: 'The Break', title: 'The Confession', index: 5},

  // -----------------------------------------------------------------
  // 一般解説（仕組み・背景・結論を説くドキュメンタリー）
  // -----------------------------------------------------------------
  'how-it-works': {kicker: 'The Mechanism', title: 'How It Works'},
  'the-big-picture': {kicker: 'Context', title: 'The Big Picture'},
  'what-it-means': {kicker: 'In The End', title: 'What It Means'},
  'the-takeaway': {kicker: 'Conclusion', title: 'The Takeaway'},
} satisfies Record<string, ComponentProps<typeof ActTitle>>;
