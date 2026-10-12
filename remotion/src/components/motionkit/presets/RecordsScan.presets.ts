import type {ComponentProps} from 'react';
import type {RecordsScan} from '../RecordsScan';

/**
 * Ready-made prop fills for RecordsScan ("searching the records" scene).
 * Usage: <RecordsScan {...recordsScanPresets['key']} />
 *
 * `lines` は各レコードの中央テキスト列（ID・テール・日付・ステータスチップは
 * コンポーネントが決定論的に自動生成）。`highlightIndex` はスキャンビームが
 * ロックオンする「一致行」で、0..lines.length-1 の範囲。省略時はコンポーネント
 * が中央付近を自動選択。個人情報は出さない方針に合わせ、氏名・番号・金額は
 * すべて █ の伏字プレースホルダーにしてある（実在データは入れない）。
 * `lines` を省いた preset は内蔵の既定9行（伏字）を使い、highlightIndex だけ
 * 差し替える（既定行 index 範囲は 0..8）。
 * `dur` は既定（Composition/durationInFrames）に任せる。
 */
export const recordsScanPresets = {
  // ── transaction ledger: one flagged row among clean entries ──────
  'ledger-flagged-wire': {
    // 送金台帳。1件だけ不審なワイヤーを検出（下から2番目をロックオン）
    lines: [
      'WIRE   OUT   $ ██,███   ██-BANK',
      'WIRE   OUT   $ █,███    ██-BANK',
      'ACH    IN    $ ██,███   PAYROLL',
      'WIRE   OUT   $ █,███    ██-BANK',
      'WIRE   OUT   $ ███,███  OFFSHORE',
      'ACH    OUT   $ █,███    VENDOR-██',
    ],
    highlightIndex: 4,
  },
  'ledger-shell-company-payments': {
    // ペーパーカンパニー宛の連続送金。3行目が経路の要
    lines: [
      'PMT   ██-LLC        $ ██,███',
      'PMT   ████ HOLDINGS $ █,███',
      'PMT   ██████ TRADING $ ███,███',
      'PMT   ██-LLC        $ ██,███',
      'PMT   ████ GROUP    $ █,███',
      'PMT   ██-LLC        $ ██,███',
    ],
    highlightIndex: 2,
  },
  'ledger-cash-deposits-structured': {
    // 反復する少額現金入金（分割入金の疑い）。最後の1件が閾値超え
    lines: [
      'CASH  DEP   $ █,███   BR-██',
      'CASH  DEP   $ █,███   BR-██',
      'CASH  DEP   $ █,███   BR-██',
      'CASH  DEP   $ █,███   BR-██',
      'CASH  DEP   $ ██,███  BR-██',
    ],
    highlightIndex: 4,
  },
  'ledger-expense-reimbursements': {
    // 経費精算の一覧。突出した1件を照会
    lines: [
      'EXP   TRAVEL      $ █,███',
      'EXP   MEALS       $   ███',
      'EXP   CONSULTING  $ ██,███',
      'EXP   SUPPLIES    $   ███',
      'EXP   TRAVEL      $ █,███',
      'EXP   MISC        $   ███',
      'EXP   MEALS       $   ███',
    ],
    highlightIndex: 2,
  },

  // ── bank statements ──────────────────────────────────────────────
  'bank-statement-monthly': {
    // 月次明細。中ほどの1取引を追跡
    lines: [
      'DEBIT   ██-STORE      $   ███.██',
      'CREDIT  DEPOSIT       $ █,███.██',
      'DEBIT   ██████        $ ██,███.██',
      'DEBIT   UTILITY-██    $   ███.██',
      'CREDIT  TRANSFER      $ █,███.██',
      'DEBIT   ██-STORE      $   ███.██',
    ],
    highlightIndex: 2,
  },
  'bank-offshore-transfers': {
    // 国外口座への送金列。4行目が着地先
    lines: [
      'XFER  →  ██-████   ACCT ████',
      'XFER  →  ██████    ACCT ████',
      'XFER  →  ██-████   ACCT ████',
      'XFER  →  ██████ IS ACCT ████',
      'XFER  →  ██-████   ACCT ████',
      'XFER  →  ██████    ACCT ████',
      'XFER  →  ██-████   ACCT ████',
    ],
    highlightIndex: 3,
  },
  'bank-account-freeze': {
    // 凍結対象口座の照合。該当口座が先頭
    lines: [
      'ACCT  ████-████-██  STATUS ██████',
      'ACCT  ████-████-██  STATUS ACTIVE',
      'ACCT  ████-████-██  STATUS ACTIVE',
      'ACCT  ████-████-██  STATUS CLOSED',
      'ACCT  ████-████-██  STATUS ACTIVE',
    ],
    highlightIndex: 0,
  },

  // ── call logs / communication records ────────────────────────────
  'call-log-burner-phone': {
    // 通話履歴。プリペイド番号への1件を特定
    lines: [
      'OUT   +█ ███-███-████   ██:██',
      'IN    +█ ███-███-████   ██:██',
      'OUT   +█ ███-███-████   ██:██',
      'OUT   +█ ███-███-████   ██:██',
      'IN    +█ ███-███-████   ██:██',
      'OUT   +█ ███-███-████   ██:██',
    ],
    highlightIndex: 3,
  },
  'call-log-repeated-contact': {
    // 同一相手への反復発信。頻度が突出した番号
    lines: [
      'CALL  ████████   ×██   LAST ██:██',
      'CALL  ████████   × █   LAST ██:██',
      'CALL  ████████   ×██   LAST ██:██',
      'CALL  ████████   × █   LAST ██:██',
      'CALL  ████████   × █   LAST ██:██',
    ],
    highlightIndex: 0,
  },
  'call-log-timeline-night': {
    // 事件当夜のタイムライン。犯行時刻帯の1件
    lines: [
      '██:██   OUT   ██ sec   TOWER-██',
      '██:██   IN    ██ sec   TOWER-██',
      '██:██   OUT   ███ sec  TOWER-██',
      '██:██   OUT   ██ sec   TOWER-██',
      '██:██   IN    ██ sec   TOWER-██',
      '██:██   OUT   ██ sec   TOWER-██',
    ],
    highlightIndex: 2,
  },

  // ── suspect / person lists / watchlists ──────────────────────────
  'suspect-list-priors': {
    // 容疑者リスト。前科ありの1名を照合
    lines: [
      'SUBJ  ██   M/██   PRIORS ██',
      'SUBJ  ██   F/██   PRIORS ██',
      'SUBJ  ██   M/██   PRIORS ██',
      'SUBJ  ██   M/██   PRIORS ██',
      'SUBJ  ██   F/██   PRIORS ██',
    ],
    highlightIndex: 3,
  },
  'watchlist-flagged-alias': {
    // 監視リスト。別名(alias)一致でヒット
    lines: [
      'ALIAS  "████████"   MATCH  --',
      'ALIAS  "██████"     MATCH  --',
      'ALIAS  "████"       MATCH  ██%',
      'ALIAS  "██████"     MATCH  --',
      'ALIAS  "████████"   MATCH  --',
      'ALIAS  "██████"     MATCH  --',
    ],
    highlightIndex: 2,
  },
  'witness-roster': {
    // 証人名簿。証言済みの1名に到達
    lines: [
      'W-██   STATUS  DEPOSED',
      'W-██   STATUS  PENDING',
      'W-██   STATUS  DEPOSED',
      'W-██   STATUS  SEALED',
      'W-██   STATUS  PENDING',
      'W-██   STATUS  DEPOSED',
      'W-██   STATUS  PENDING',
    ],
    highlightIndex: 3,
  },
  'employee-access-badge': {
    // 社員入退室ログ。深夜アクセスの1件
    lines: [
      'BADGE  ████   DOOR-██   ██:██',
      'BADGE  ████   DOOR-██   ██:██',
      'BADGE  ████   DOOR-██   ██:██',
      'BADGE  ████   VAULT-██  ██:██',
      'BADGE  ████   DOOR-██   ██:██',
      'BADGE  ████   DOOR-██   ██:██',
    ],
    highlightIndex: 3,
  },

  // ── court dockets / case records ─────────────────────────────────
  'docket-criminal-calendar': {
    // 刑事事件カレンダー。審理中の事件を抽出
    lines: [
      'CASE  ██-CR-████   ARRAIGN',
      'CASE  ██-CR-████   TRIAL',
      'CASE  ██-CR-████   SENTENCE',
      'CASE  ██-CR-████   PENDING',
      'CASE  ██-CR-████   ARRAIGN',
    ],
    highlightIndex: 1,
  },
  'docket-civil-motions': {
    // 民事の申立て一覧。係属中のモーション
    lines: [
      'MOT  ██-CV-████   DISMISS   DENIED',
      'MOT  ██-CV-████   SUMMARY   PENDING',
      'MOT  ██-CV-████   COMPEL    GRANTED',
      'MOT  ██-CV-████   SEAL      PENDING',
      'MOT  ██-CV-████   STRIKE    DENIED',
      'MOT  ██-CV-████   SUMMARY   PENDING',
    ],
    highlightIndex: 1,
  },
  'docket-sealed-case': {
    // 封印された事件番号を探し当てる（末尾）
    lines: [
      'DKT  ██-████   OPEN',
      'DKT  ██-████   OPEN',
      'DKT  ██-████   CLOSED',
      'DKT  ██-████   OPEN',
      'DKT  ██-████   CLOSED',
      'DKT  ██-████   ██████',
    ],
    highlightIndex: 5,
  },

  // ── property / immigration / evidence records ────────────────────
  'property-deed-transfers': {
    // 不動産の所有権移転履歴。不自然な1件を照合
    lines: [
      'DEED  PARCEL-████   →  ██-LLC',
      'DEED  PARCEL-████   →  ██████',
      'DEED  PARCEL-████   →  ██-TRUST',
      'DEED  PARCEL-████   →  ██-LLC',
      'DEED  PARCEL-████   →  ██████',
    ],
    highlightIndex: 2,
  },
  'immigration-entry-log': {
    // 出入国記録。該当する入国スタンプ
    lines: [
      'ENTRY  PORT-██   VISA ██   ████-██-██',
      'EXIT   PORT-██   ----     ████-██-██',
      'ENTRY  PORT-██   VISA ██   ████-██-██',
      'ENTRY  PORT-██   VISA ██   ████-██-██',
      'EXIT   PORT-██   ----     ████-██-██',
      'ENTRY  PORT-██   VISA ██   ████-██-██',
    ],
    highlightIndex: 2,
  },
  'evidence-inventory': {
    // 証拠品目録。鍵となる1点を特定
    lines: [
      'ITEM  EX-██   BAGGED   LOCKER-██',
      'ITEM  EX-██   BAGGED   LOCKER-██',
      'ITEM  EX-██   MISSING  LOCKER-██',
      'ITEM  EX-██   BAGGED   LOCKER-██',
      'ITEM  EX-██   BAGGED   LOCKER-██',
      'ITEM  EX-██   BAGGED   LOCKER-██',
      'ITEM  EX-██   BAGGED   LOCKER-██',
    ],
    highlightIndex: 2,
  },

  // ── default lines (highlightIndex only; built-in 9 redacted rows) ─
  'default-scan-mid': {
    // 既定の伏字9行で中央の行をロックオン
    highlightIndex: 4,
  },
  'default-scan-first': {
    // 既定行の先頭を一致行に
    highlightIndex: 0,
  },
  'default-scan-early': {
    // 既定行の上寄り（3行目）
    highlightIndex: 2,
  },
  'default-scan-last': {
    // 既定行の末尾（9行目 = index 8）
    highlightIndex: 8,
  },
} satisfies Record<string, ComponentProps<typeof RecordsScan>>;
