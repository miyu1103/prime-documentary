import type {ComponentProps} from 'react';
import type {TerminalType} from '../TerminalType';

// =====================================================================
// TerminalType preset catalog — MOTIONKIT
//   ハッカー/記録端末シーン用プリセット。Prime Documentary のスレート
//   （最高裁の令状もの・実録犯罪・金融詐欺・DNA/科学捜査・暗号通貨）向け。
//
//   RULES:
//   - lines は string[]、prompt はシェル種別で変える（'> ' / '$ ' / 'SQL> '）。
//   - すべて架空／総称データのみ。実在人物名・実在住所・本物のPII・実IP・
//     実ハッシュ・実ウォレットは一切使わない（invariant 3 / 11）。
//   - dur は TerminalType 側で durationInFrames にフォールバックするため未指定。
// =====================================================================

export const terminalTypePresets = {
  // -------------------------------------------------------------------
  // Records access / 記録アクセス・データベース照会（判例・実録犯罪）
  // -------------------------------------------------------------------
  'records-open-case-db': {
    prompt: '> ',
    lines: [
      'ssh archivist@records.gov -p 443',
      'authenticating credential... OK',
      'mount /vol/case-archive',
      'open CASE-1972-0447',
      'STATUS: SEALED — access granted',
    ],
  },
  'records-query-warrant': {
    prompt: 'SQL> ',
    lines: [
      'SELECT * FROM warrants',
      "WHERE subject_id = 'SUBJ-0091'",
      "AND status = 'EXECUTED';",
      '-- 1 row returned',
      'warrant_no: W-4471   issued: 03/14',
    ],
  },
  'records-pull-transcript': {
    prompt: '$ ',
    lines: [
      'fetch --archive court-transcripts',
      'query "docket=DKT-8830"',
      'downloading transcript... 100%',
      'pages: 214   redactions: 37',
      'saved to ./evidence/transcript.txt',
    ],
  },
  'records-cross-reference': {
    prompt: 'SQL> ',
    lines: [
      'SELECT name, file_no FROM subjects s',
      'JOIN filings f ON s.id = f.subject_id',
      "WHERE f.year BETWEEN 1969 AND 1974;",
      '-- 3 rows returned',
      'cross-reference complete',
    ],
  },
  'records-access-denied': {
    prompt: '> ',
    lines: [
      'open FILE-CLASSIFIED-0007',
      'verifying clearance level...',
      'ERROR: insufficient authorization',
      'retry with override token? [y/N]',
      'ACCESS DENIED — event logged',
    ],
  },

  // -------------------------------------------------------------------
  // Ledger decrypt / 台帳の復号（金融詐欺・帳簿改ざん）
  // -------------------------------------------------------------------
  'ledger-decrypt-start': {
    prompt: '$ ',
    lines: [
      'openvault ./ledger.enc',
      'algorithm: AES-256-GCM',
      'deriving key from passphrase...',
      'decrypting blocks [########--] 82%',
      'ledger unlocked — 4,118 entries',
    ],
  },
  'ledger-find-discrepancy': {
    prompt: 'SQL> ',
    lines: [
      'SELECT quarter, reported, actual',
      'FROM ledger WHERE reported <> actual;',
      '-- 6 rows returned',
      'Q3: reported 8.4M / actual 2.1M',
      'variance flagged: -6.3M',
    ],
  },
  'ledger-shell-accounts': {
    prompt: 'SQL> ',
    lines: [
      'SELECT account, owner FROM entities',
      "WHERE type = 'SHELL';",
      '-- 9 rows returned',
      'HOLDINGS-A ... HOLDINGS-I',
      'all registered same P.O. box',
    ],
  },
  'ledger-second-set-books': {
    prompt: '> ',
    lines: [
      'diff ledger_public.db ledger_hidden.db',
      'comparing 4,118 records...',
      '312 entries mismatch',
      'hidden book totals: +14.7M',
      'CONCLUSION: two sets of books',
    ],
  },

  // -------------------------------------------------------------------
  // IP / network trace / IPトレース・接続追跡（サイバー・監視もの）
  // -------------------------------------------------------------------
  'trace-ip-hops': {
    prompt: '$ ',
    lines: [
      'traceroute target.host',
      '1  gateway        2 ms',
      '2  10.0.0.1       14 ms',
      '3  edge-node-77   41 ms',
      '4  origin *masked* — 3 hops via VPN',
    ],
  },
  'trace-geolocate': {
    prompt: '> ',
    lines: [
      'geoip 203.0.113.42',
      'resolving origin...',
      'region: [REDACTED]  ISP: Node7 Telecom',
      'last seen: 02:14 local time',
      'confidence: 71%',
    ],
  },
  'trace-proxy-chain': {
    prompt: '$ ',
    lines: [
      'unmask --follow-proxies',
      'hop 1: exit-node-alpha',
      'hop 2: exit-node-bravo',
      'hop 3: residential relay',
      'true origin isolated',
    ],
  },
  'trace-packet-capture': {
    prompt: '$ ',
    lines: [
      'tcpdump -i eth0 host suspect.node',
      'capturing packets...',
      '1,204 packets  /  38 flagged',
      'payload signature match: EXFIL',
      'capture saved: ./pcap/session.dump',
    ],
  },

  // -------------------------------------------------------------------
  // Database match / 生体・DNA照合ヒット（科学捜査・冤罪もの）
  // -------------------------------------------------------------------
  'match-dna-hit': {
    prompt: '> ',
    lines: [
      'run codis --sample SMP-0042',
      'comparing against 1.4M profiles...',
      'loci compared: 20 / 20',
      'MATCH FOUND: PROFILE-88301',
      'probability: 1 in 2.7 billion',
    ],
  },
  'match-fingerprint': {
    prompt: '$ ',
    lines: [
      'afis scan latent_print.tif',
      'extracting minutiae... 74 points',
      'searching database...',
      'candidate: REC-5590  score 0.94',
      'analyst review required',
    ],
  },
  'match-facial-review': {
    prompt: '> ',
    lines: [
      'load frame_0417.jpg',
      'detecting faces... 1 subject',
      'querying watchlist...',
      'top candidate score: 0.61',
      'BELOW THRESHOLD — no positive ID',
    ],
  },
  'match-no-result': {
    prompt: '> ',
    lines: [
      'run codis --sample SMP-0043',
      'comparing against 1.4M profiles...',
      'loci compared: 18 / 20',
      'NO MATCH in database',
      'sample queued for re-test',
    ],
  },

  // -------------------------------------------------------------------
  // Crypto wallet trace / 暗号ウォレット追跡（OneCoin風・資金洗浄）
  // -------------------------------------------------------------------
  'wallet-trace-flow': {
    prompt: '$ ',
    lines: [
      'chaintrace --wallet WLT-3f9a',
      'reading on-chain history...',
      'inflow: 1,240 BTC across 88 tx',
      'hop to WLT-c71e ... WLT-be04',
      'trail ends at mixer service',
    ],
  },
  'wallet-cluster': {
    prompt: 'SQL> ',
    lines: [
      'SELECT wallet, balance FROM cluster',
      "WHERE tag = 'SUSPECT';",
      '-- 5 rows returned',
      'combined balance: 3,902 BTC',
      'linked by common change-address',
    ],
  },
  'wallet-mixer-exit': {
    prompt: '> ',
    lines: [
      'demix --session MIX-0099',
      'analyzing timing correlations...',
      'inputs: 140   outputs: 138',
      'probable exit: WLT-a204',
      'confidence: 68% — flagged',
    ],
  },
  'wallet-cashout': {
    prompt: '$ ',
    lines: [
      'monitor exchange-gateway',
      'watching for cash-out event...',
      'ALERT: 512 BTC -> fiat request',
      'destination: acct *masked*',
      'freeze order dispatched',
    ],
  },

  // -------------------------------------------------------------------
  // Wiretap / surveillance log / 傍受・監視ログ（令状・監視vsプライバシー）
  // -------------------------------------------------------------------
  'wiretap-live-log': {
    prompt: '> ',
    lines: [
      'tap --line LN-0077 --warrant W-4471',
      'session opened 22:41',
      'call intercepted: 03:12 duration',
      'keyword hit: "the shipment"',
      'log appended — chain of custody OK',
    ],
  },
  'wiretap-metadata': {
    prompt: 'SQL> ',
    lines: [
      'SELECT caller, callee, ts FROM cdr',
      "WHERE line = 'LN-0077'",
      'ORDER BY ts DESC LIMIT 3;',
      '02:14  SUBJ-0091 -> NODE-B',
      '01:58  NODE-B    -> SUBJ-0091',
    ],
  },
  'wiretap-pen-register': {
    prompt: '$ ',
    lines: [
      'pentrace --device DEV-2210',
      'logging dialed numbers only...',
      '17 outbound in last hour',
      'pattern: nightly 02:00 contact',
      'no content captured — metadata only',
    ],
  },
  'wiretap-warrant-expired': {
    prompt: '> ',
    lines: [
      'tap --line LN-0077 --extend',
      'checking warrant validity...',
      'WARNING: warrant W-4471 EXPIRED',
      'interception suspended',
      'evidence after 00:00 inadmissible',
    ],
  },
} satisfies Record<string, ComponentProps<typeof TerminalType>>;
