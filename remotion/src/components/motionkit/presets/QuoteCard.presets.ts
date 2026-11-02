import type {ComponentProps} from 'react';
import type {QuoteCard} from '../QuoteCard';

// =====================================================================
// QuoteCard preset catalog — MOTIONKIT
//   逐語引用のシネマティックSCENE用プリセット。Prime Documentary のスレート
//   （最高裁の法廷もの・金融詐欺・実録犯罪・一般解説）向けにチューニング。
//
//   RULES:
//   - すべて架空だが本物らしい／パブリックドメイン調の引用文。
//   - attribution は「役割」の総称のみ（実在人物の発言・肖像は不使用）。
//   - dur は QuoteCard 側で durationInFrames にフォールバックするため未指定。
// =====================================================================

export const quoteCardPresets = {
  // -------------------------------------------------------------------
  // Supreme Court / 法廷・憲法（判例もの）
  // -------------------------------------------------------------------
  'court-majority-liberty': {
    quote: 'The liberty of the individual does not end where the convenience of the state begins.',
    attribution: "The court's majority opinion",
  },
  'court-dissent-warning': {
    quote: 'Today the door is opened wide, and those who come after us will not easily close it.',
    attribution: 'The dissenting opinion',
  },
  'constitution-plain-text': {
    quote: 'The words of the Constitution mean what they say, and they say the people are protected.',
    attribution: 'The concurring justice',
  },
  'fourth-amendment-search': {
    quote: 'A search is no less a search because it is conducted with a screen instead of a key.',
    attribution: "The court's holding",
  },
  'due-process-core': {
    quote: 'No conviction can stand upon a right that the accused was never told he possessed.',
    attribution: 'The written judgment',
  },
  'defense-closing': {
    quote: 'The state must prove its case; the citizen is never required to prove his innocence.',
    attribution: 'Counsel for the defense',
  },
  'prosecution-rule-of-law': {
    quote: 'The law is not a weapon of the powerful; it is the shield of every ordinary person.',
    attribution: 'A federal prosecutor',
  },

  // -------------------------------------------------------------------
  // Financial fraud / 金融詐欺・不正会計
  // -------------------------------------------------------------------
  'fraud-too-good': {
    quote: 'When the returns never fall and never falter, you are not looking at genius but at a lie.',
    attribution: 'A forensic accountant',
  },
  'fraud-house-of-cards': {
    quote: 'Every empire built on borrowed trust collapses the moment someone asks to be repaid.',
    attribution: 'The investigative report',
  },
  'fraud-whistleblower': {
    quote: 'I raised my hand a dozen times, and a dozen times I was told to lower it and be quiet.',
    attribution: 'A former employee',
  },
  'fraud-regulator-warning': {
    quote: 'The numbers were flawless, which was precisely the reason no one should have believed them.',
    attribution: 'A securities regulator',
  },
  'fraud-investor-loss': {
    quote: 'We were not investing in a company; we were paying the earlier victims with our own savings.',
    attribution: 'A defrauded investor',
  },
  'fraud-audit-trail': {
    quote: 'Follow the money far enough and it always leads back to a room where the truth was rewritten.',
    attribution: 'The audit findings',
  },

  // -------------------------------------------------------------------
  // True crime / 実録犯罪・捜査
  // -------------------------------------------------------------------
  'crime-cold-case': {
    quote: 'A case is never truly closed while a single question is still left without an answer.',
    attribution: 'The lead investigator',
  },
  'crime-detective-detail': {
    quote: 'The smallest detail, the one everyone overlooked, was the thread that unraveled everything.',
    attribution: 'A homicide detective',
  },
  'crime-witness-testimony': {
    quote: 'I saw what I saw, and no amount of time has softened the edges of that night.',
    attribution: 'A key witness',
  },
  'crime-verdict-read': {
    quote: 'When the verdict was read, the room did not erupt; it fell into a silence that lasted for years.',
    attribution: 'A courtroom observer',
  },
  'crime-wrongful-conviction': {
    quote: 'It took one afternoon to convict an innocent man and three decades to admit the mistake.',
    attribution: 'The appeals court',
  },

  // -------------------------------------------------------------------
  // Investigation / ジャーナリズム・調査報道
  // -------------------------------------------------------------------
  'invest-follow-record': {
    quote: 'Records do not lie the way people do; they simply wait to be read by someone patient enough.',
    attribution: 'An investigative journalist',
  },
  'invest-power-accountable': {
    quote: 'The purpose of the question is not to embarrass the powerful, but to make them answerable.',
    attribution: 'The editorial board',
  },
  'invest-document-leak': {
    quote: 'A single document, handed over in the dark, can outweigh a thousand official denials.',
    attribution: 'An anonymous source',
  },

  // -------------------------------------------------------------------
  // General explainer / 一般解説・思想的クローズ
  // -------------------------------------------------------------------
  'explainer-history-repeats': {
    quote: 'History rarely repeats its words, but it is remarkably faithful in repeating its warnings.',
    attribution: 'The historical record',
  },
  'explainer-truth-inconvenient': {
    quote: 'The truth is patient; it can wait as long as it takes for the convenient story to fail.',
    attribution: 'A closing narration',
  },
  'explainer-systems-not-villains': {
    quote: 'It was not one villain that failed us, but a system that quietly rewarded looking away.',
    attribution: 'The final analysis',
  },
  'explainer-question-everything': {
    quote: 'Ask who benefits, ask who was silenced, and the shape of the whole story begins to appear.',
    attribution: 'A guiding principle',
  },
} satisfies Record<string, ComponentProps<typeof QuoteCard>>;
