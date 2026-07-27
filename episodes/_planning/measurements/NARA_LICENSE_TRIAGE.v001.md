# NARA license triage — quarantine sweep 001

**Date:** 2026-07-28 · **Rules version:** `nara-license-triage-v001`
**Scope:** every `license_decision: review_required` row in
`H:\pd-media\assets\archive\_ledger\nara.jsonl` whose file sits in
`H:\pd-media\assets\archive\_quarantine\<theme>\`.
**Question answered per item:** is this safe for commercial use on a monetised
YouTube channel — on EVIDENCE from the NARA catalog record, not on the filename.

Evidence source: full item records from
`https://catalog.archives.gov/proxy/records/search?naId=<naId>` (fresh TCP
connection, JSON body guard, ≥1 req/s — the gov lane's proven pattern), plus the
**series- and record-group-level** records, which turned out to be the deciding
evidence (see §2).

---

## 1. Rule set

Every verdict below is produced by one of these rules, in this order. The rule id
is written into the ledger row (`triage_rule`) together with the exact
`useRestriction` text (`license_evidence`), so no row was changed without evidence.

| id | rule | verdict |
|---|---|---|
| **R0/explicit-claim** | `useRestriction.note` / `specificUseRestrictions` / record text contains an affirmative claim or commercial bar (`is copyrighted`, `copyright is retained`, `may not be used for commercial`, `written permission of the donor`, …) | **reject** — delete + tombstone |
| **R0/status-restricted** | `useRestriction.status == "Restricted"` (hard, not "Restricted - Possibly") | **reject** |
| **R3/donated-collection** | ancestor chain contains a `collection` (donated third-party material: Ford, CBS, March of Time, MCA/Universal…) | **review_required_keep** |
| **R3/no-record-group** | no federal `recordGroup` ancestor → provenance unclear | **review_required_keep** |
| **R3/creator-not-federal** | record group present but the creating organisation is not on the US-federal-agency list | **review_required_keep** |
| **R3/third-party-content-language** | federal record group, but the record itself describes third-party material (`newsreel`, `courtesy of`, `Paramount`, `Pathé`, `March of Time`, `obtained from other sources`, `captured …`, …) — the agency **collected** it, it did not **make** it | **review_required_keep** |
| **R3/undated-multiyear-compilation** | federal record group, but NARA records **no** `productionDates` **and** a coverage span ≥ 1 year → an accessioned compilation, not a dated agency shoot (see §4, the eyeball catch) | **review_required_keep** |
| **R3/restriction-flagged** | `useRestriction.status` is anything other than `Unrestricted` / `Undetermined` (in practice: `Restricted - Possibly`, usually with `specificUseRestrictions: ["Copyright"]`) | **review_required_keep** |
| **R3/specific-use-restriction**, **R3/restriction-note** | any `specificUseRestrictions` or item-level note survives the above | **review_required_keep** |
| **R1/us-federal-record** | *everything else*: federal `recordGroup` ancestor **AND** creating org on the US-federal-agency list **AND** no `collection`/donor ancestor **AND** `status ∈ {Unrestricted, Undetermined}` **AND** no note / specificUseRestrictions **AND** no third-party-content language **AND** not an undated multi-year compilation | **pd_us_gov** — US Government work, 17 U.S.C. §105 → promote to shelf |
| **R2/pd-expired** | US **publication** before 1930, evidenced | pd_expired — *0 items qualified; see §5* |
| **R4/no-catalog-record** | catalog record unreachable | **review_required_keep** (fail closed) |

---

## 2. The finding that drives everything: `useRestriction` is *series* boilerplate, not an item verdict

Measured over **460 live NARA moving-image search hits (445 unique naIds)**:

| status × specificUseRestrictions × has-note | n |
|---|---:|
| `Restricted - Possibly` / `Copyright` / no note | 219 |
| `Restricted - Possibly` / `Copyright` / **note** | 194 |
| `Undetermined` / — / no note | 25 |
| `Restricted - Possibly` / — / note | 12 |
| `Unrestricted` / — / no note | 10 |

Per series:

| series | RG / collection | status mix |
|---|---|---|
| 13807 "Moving Images Relating to Military Activities" | RG **111** (Army Signal Corps) | `Restricted - Possibly` **223 / 223 — 100 %** |
| 97797 "Outtakes from 'March Of Time' Newsreels" | MT collection | `Restricted - Possibly` 93 / 93 |
| 75284 "Moving Images Relating to Military Activities" | RG **428** (Navy) | `Undetermined` 17, `Unrestricted` 4, `Restricted - Possibly` 1 |
| 24608 "Historical Films" | RG 111 | `Restricted - Possibly` 14, `Unrestricted` 1 |
| 25061 "Army Library Copy Collection" | RG 111 | `Restricted - Possibly` 4, `Unrestricted` 2 |

Two conclusions, both load-bearing:

1. **The generic note is boilerplate.** *"Some or all of this material may be
   restricted by copyright or other intellectual property rights restrictions"*
   appears verbatim on the **series** record of RG 111, RG 428, RG 65 (FBI), Ford,
   CBS and March of Time alike. It is inherited by items and carries **zero**
   item-level information. Never treat its presence as an item's rights status.
2. **The status field is informative in some series and blanket in others.**
   Series 75284 (RG 428) carries three different statuses → NARA made per-item
   determinations there. Series 13807 (RG 111) is 223/223 identical → NARA made
   **no** determination there; the flag is a series-wide caution.

So the discriminator that actually carries provenance is **`ancestors[]`**:
a `recordGroup` ancestor = records of a US federal agency; a `collection`
ancestor = donated third-party material with a named non-federal creator/donor.

### Why the RG 111 (Signal Corps) trial footage still stays in quarantine

**26 of the 41 kept items (4.01 GB)** are RG 111 Army Signal Corps material, 24 of
them war-crimes-trial coverage (Nuremberg / Yokohama / Yamashita / Quisling /
Pétain) — the single most valuable block in the quarantine, and almost certainly
US Government work. They are **kept** because:

* NARA has affirmatively flagged `specificUseRestrictions: ["Copyright"]` on them
  and, in series 13807, has never made a per-item determination to lift it; and
* the series demonstrably **mixes** agency-shot and commercially-produced film.
  naId **23674 "QUISLING TRIAL"** (RG 111, 111-ADC-9909) carries
  `Contributor: Producer, Paramount, March of Time & Pathe News` in its general
  notes. One reel in the same series, same shelf number range, is commercial
  newsreel. 25 of the other 26 RG-111 items carry **no** general notes at all, so
  the same cannot be ruled out for any of them from metadata.

That is an owner decision, not an automation decision — see §6 "Owner unlock".

---

## 3. Per-item table

Verdicts, the raw `useRestriction` NARA returned, and the action taken.
`+note` means the (boilerplate) note was present.

| naId | title | provenance | useRestriction (raw) | verdict | rule | MB | evidence + action taken |
|---|---|---|---|---|---|---:|---|
| 80631 | USS TIRANTE (SS-420) COMBAT FILM | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 198 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-17259; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\war_history\` |
| 80630 | USS TIRANTE COMBAT FILM | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 196 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-17258; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\war_history\` |
| 77646 | RESCUE OF AUSTRALIAN PRISONERS OF WAR FROM Japanese PR | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 153 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-5743; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 79797 | POWS RELEASED FROM PRISON CAMPS NEAR TOKYO | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 128 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-14557; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 77693 | RESCUE OF AUSTRALIAN PRISONERS OF WAR AFTER SINKING OF | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 97 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-5865; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 79746 | TREASON TRIAL ON GUAM | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 87 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-14429; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\courtroom_justice\` |
| 79817 | PRISON CAMP AT SHINAGAWA TOKYO | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 77 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-14615; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 77994 | SHOTS OF PRISONERS OF WAR & BILIBID PRISON AT MANILA,  | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 53 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-7241; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 76954 | LST PRISON SHIP FOUNDERS OFF ITALIAN COAST | RG 428 | `Undetermined` | **pd_us_gov** | us-federal-record | 47 | RG 428 (Navy); creator Navy Naval Photographic Center; localId 428-NPC-4047; no donor/collection ancestor, no 3rd-party language — US Government work, 17 U.S.C. 105 — MOVED to `E:\pd-archive\prison_jail\` |
| 89353 | [STOCK NEWSREEL EXCERPTS] | COLL CBS | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 282 | donated third-party collection ancestor [CBS: Columbia Broadcasting System, Inc., Collection] — creator Columbia Broadcasting System, inc. is not a federal agency acting in official duty — kept in quarantine |
| 90805 | [SCENES IN SOUTH WEST UNITED STATES] | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 174 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 124450448 | Fiorello LaGuardia | COLL MT | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 142 | donated third-party collection ancestor [MT: "March of Time" Collection] — creator Time, Inc. is not a federal agency acting in official duty — kept in quarantine |
| 149270194 | British Courtroom | COLL MT | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 142 | donated third-party collection ancestor [MT: "March of Time" Collection] — creator Time, Inc. is not a federal agency acting in official duty — kept in quarantine |
| 92280 | LOS ANGELES | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 141 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 7422244 | Greenfield Village / 41st Annual Convention of the Int | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 134 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 93093 | Crown Prince Olaf and Princess Martha of Norway at Riv | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 111 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 91009 | AT THE CROSS ROADS [LEAVENWORTH PRISON] | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 110 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 89353 | [STOCK NEWSREEL EXCERPTS] | COLL CBS | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 84 | donated third-party collection ancestor [CBS: Columbia Broadcasting System, Inc., Collection] — creator Columbia Broadcasting System, inc. is not a federal agency acting in official duty — kept in quarantine |
| 7403239 | Indianapolis, Indiana / President Woodrow Wilson in In | COLL FC | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 81 | donated third-party collection ancestor [FC: Ford Motor Company Collection] — creator Ford Motor Company. is not a federal agency acting in official duty — kept in quarantine |
| 503127714 | Prison Ship is Wrecked / Laying Lighthouse Cornerstone | COLL UN | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 42 | donated third-party collection ancestor [UN: MCA/Universal Pictures Collection] — creator MCA/Universal Pictures. is not a federal agency acting in official duty — kept in quarantine |
| 503129318 | Rioting Felons Damage Prison in 8-Hour Row | COLL UN | `Restricted - Possibly / Copyright +note` | review_required_keep | donated-collection | 25 | donated third-party collection ancestor [UN: MCA/Universal Pictures Collection] — creator MCA/Universal Pictures. is not a federal agency acting in official duty — kept in quarantine |
| 19400 | PARIS. [No.] 460, WAR CRIMES TRIALS, NUREMBERG, GERMAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 266 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 23816 | THE VERDICT, NUREMBERG TRIAL | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 219 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19879 | MUNICH. [Nos.] 211-222, WAR CRIMES TRIALS, NUREMBERG,  | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 216 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 20223 | MUNICH. [No.] 522, WAR CRIMES TRIALS CASE NO. 1 (MEDIC | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 200 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19878 | MUNICH. [Nos.] 211-222, WAR CRIMES TRIALS, NUREMBERG,  | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 197 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 15131 | TRIAL OF NAZI SPIES, CHERBOURG, FRANCE ; TRIAL OF NAZI | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 194 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19613 | MUNICH. [No.] 15, WAR CIRMES TRIALS, NUREMBERG, GERMAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 187 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19463 | PARIS. [No.] 457, WAR CRIMES TRIAL, NUREMBERG, GERMANY | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 184 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 20795 | WAR CRIMES ATROCITY TRIALS, YOKOHAMA, JAPAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 179 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 21261 | ESPIONAGE TRIAL, MUNICH ; KOREAN CONSTABULARY, SEOUL,  | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 168 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19611 | MUNICH. [No.] 84, WAR CRIMES TRIALS, NUREMBERG, GERMAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 165 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 21254 | DECISION BOARD TRIAL - FRITZ KUHN, MUNICH, GERMANY | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 159 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19383 | YAMASHITA TRIAL, 31ST DAY, MANILA, PHILIPPINE ISLANDS  | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 149 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 23628 | TRIAL OF MARSHAL HENRI PETAIN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 146 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19251 | YAMASHITA TRIAL, FOURTH DAY, MANILA, PHILIPPINE ISLAND | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 144 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 16664 | FIRST SHOT INTO GERMANY, THEDING (?), FRANCE ; ARTILLE | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 140 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19661 | MUNICH. [No.] 004, WAR CRIMES TRIALS, NUREMBERG, GERMA | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 139 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19941 | WAR CRIMES TRIALS, TOKYO, JAPAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 137 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 20262 | MUNICH. [No.] 544, SENTENCING OF GEN. ERHARD MILCH, NU | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 120 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 17647 | PRISON CAMP, BAD ORB, GERMANY | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 107 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 20264 | THE MARCH OF DIMES DRIVE IN THE 88TH INFANTRY DIVISION | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 107 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19382 | YAMASHITA TRIAL, 32ND DAY, MANILA, PHILIPPINE ISLANDS | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 101 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 19413 | WAR CRIMES TRIAL, TATSUO TSUCHIYA, YOKOHAMA, JAPAN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 99 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 23559 | QUISLING TRIAL | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 97 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 23629 | TRIAL OF MARSHAL HENRI PETAIN | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | restriction-flagged | 74 | NARA flags status "Restricted - Possibly" specificUseRestrictions=['Copyright'] (no item-level note) — kept in quarantine |
| 12101 | Black Panther | RG 65 | `Restricted - Possibly / Copyright +note` | review_required_keep | third-party-content-language | 244 | federal RG 65 but the record describes third-party material (matched ['newsreel']) — agency-collected, not agency-created — kept in quarantine |
| 23674 | QUISLING TRIAL | RG 111 | `Restricted - Possibly / Copyright` | review_required_keep | third-party-content-language | 111 | federal RG 111 but the record describes third-party material (matched ['pathe', 'march of time']) — agency-collected, not agency-created — kept in quarantine |
| 87665 | JAPANESE PRISON CAMPS (273-X) | RG 428 | `Undetermined` | review_required_keep | undated-multiyear-compilation | 300 | RG 428 but NARA records NO productionDate and a 4-year coverage span (1941-1945) — an accessioned compilation the agency COLLECTED, not a dated agency shoot; shot list places foreign personnel ['japanese', 'british'] in custodial  — kept in quarantine |
| 87666 | JAPANESE PRISON CAMPS (273-X) | RG 428 | `Undetermined` | review_required_keep | undated-multiyear-compilation | 162 | RG 428 but NARA records NO productionDate and a 4-year coverage span (1941-1945) — an accessioned compilation the agency COLLECTED, not a dated agency shoot; shot list places foreign personnel ['japanese', 'british'] in custodial  — kept in quarantine |

---

## 4. Eyeball QC — 3 frames per promoted item at 10 % / 50 % / 90 %

Frames and contact sheets: `H:\pd-media\assets\archive\_qc\quarantine_triage\`
(`<file>__p10/p50/p90.jpg`, plus `sheet_1..3.jpg`). All 11 promotion **candidates**
were eyeballed before the move.

**No third-party logo, watermark or modern rights-holder bug was found on any item.**

Findings:

* **naId 87665 / 87666 "JAPANESE PRISON CAMPS (273-X)" — CAUGHT BY THE EYEBALL, DEMOTED.**
  Metadata alone would have promoted them: RG 428, creator Naval Photographic
  Center, `useRestriction: Undetermined`, no note, no donor. The frames show POWs
  under guard, camp assemblies and forced labour **inside Japanese-run camps**, and
  the shot lists confirm it — *"prisoners eating food with Japanese officers …
  Japanese bugler … Japanese officer placing wreath on monument and saluting"*,
  coverage `ca.1941 – ca.1945`, **no production date**. A US Navy cameraman was not
  inside those camps during captivity; this is captured / foreign-government film
  the Navy accessioned. Demoted to `review_required_keep`
  (`R3/undated-multiyear-compilation`, 462 MB), and the rule was added to the rule
  set so the gov lane catches the class automatically.
* **naId 76954 "LST PRISON SHIP FOUNDERS OFF ITALIAN COAST"** — a burned-in archival
  timecode window (`00:32:36.27 RTC`) is visible bottom-left for the whole reel.
  Not a rights bug (it is NARA's transfer timecode) but it **must be cropped or the
  clip must be framed to exclude the lower-left** before use. The 90 % frame is
  black (tail leader). Theme fit is loose: it is a shipwreck rescue of German POWs,
  not prison interior — usable as "prison ship", not as jail B-roll.
* **naId 80630 / 80631 "USS TIRANTE COMBAT FILM"** — colour stock, severely faded to
  magenta/blue. Content is correct (submarine deck, Pearl Harbor, captured
  material). Needs colour correction before use; do not cut it against clean
  black-and-white without grading.
* **Bundled reels (per the gov lane's finding — these are shot-selection notes, not
  rejections):** naId 79817 "PRISON CAMP AT SHINAGAWA" runs camp footage into
  unrelated street scenes of Haikimo village; naId 77646 opens on ~2 minutes of
  featureless open sea before the rescue material. Both are legitimate items that
  need **shot selection**, not the whole reel.
* **Strong, clean, on-theme:** naId 79746 "TREASON TRIAL ON GUAM" (military
  tribunal in a quonset hut — genuine courtroom footage), naId 77994 "BILIBID
  PRISON" (emaciated POWs, prison walls, liberation), naId 79797 "POWS RELEASED".
* Faces are prominent throughout (POWs, defendants, tribunal members). Historically
  appropriate, but note the channel's person-focus policy before using as
  decorative B-roll.

---

## 5. Counts

| verdict | rule | items | GB |
|---|---|---:|---:|
| **pd_us_gov** | R1/us-federal-record | **9** | **1.04** |
| pd_expired | — | 0 | 0.00 |
| review_required_keep | R3/restriction-flagged | 25 | 3.89 |
| review_required_keep | R3/donated-collection | 12 | 1.47 |
| review_required_keep | R3/undated-multiyear-compilation | 2 | 0.46 |
| review_required_keep | R3/third-party-content-language | 2 | 0.36 |
| **review_required_keep total** | | **41** | **6.18** |
| **reject** | | **0** | **0.00** |
| **TOTAL triaged** | | **50** | **7.21** |

* **Moved to the shelf:** 9 items / **1.04 GB** → `E:\pd-archive\{prison_jail,
  war_history, courtroom_justice}\` (filenames unchanged; sha256 re-verified after
  the move on a sample; ledger `file_path` updated).
* **Kept in quarantine:** 41 items / **6.18 GB**.
* **Deleted:** 0 items / 0.00 GB. No item carried an affirmative copyright claim or
  a commercial-use bar — every restriction encountered was either NARA's
  undetermined-status boilerplate or a donor's "rights may exist" caution, neither
  of which is a claim. `gov_dedup_removed.jsonl` was not appended to.
* **pd_expired scored 0.** The five pre-1930 candidates (Ford Motor Company
  Collection: naId 7403239 [1916], 92280 [1917], 91009 [1919], 90805 [1920]) are
  pre-1930 *production* dates, but PD-by-date requires evidenced US **publication**
  before 1930, and NARA documents neither publication nor date of publication for
  them — and all five carry Ford's explicit "proprietary rights … may exist" note.
  Production date alone is not a date-based clearance. See §6.

---

## 6. DECISION PROCEDURE — for the gov lane to apply automatically

Deterministic, needs only fields already in the search response (no extra API
call: `ancestors`, `useRestriction`, `productionDates`, `coverage*Date`,
`generalNotes`, `contributors`, `scopeAndContentNote`, `shotList` all ship inside
`hits[]._source.record`).

```python
# ---------------------------------------------------------------- NARA rights
# Adopt as `nara_license_decision(rec)` in ingest_gov_archives.py::src_nara,
# replacing:  decision = "pd" if "unrestricted" in use_s.lower() else "review_required"
# Returns (decision, rule_id, evidence).  decision in {"pd", "review_required",
# "reject"}.  Rules version: nara-license-triage-v001
#
# WHY this is not just the useRestriction field: measured over 445 unique NARA
# moving-image records, the "Restricted - Possibly / Copyright" flag is applied to
# 223/223 items of RG-111 series 13807 — it is a series-wide caution, not an
# item determination, and its note is boilerplate present on federal and donated
# series alike.  The field that actually carries provenance is ancestors[].

US_FEDERAL_CREATOR = (
    "department of defense", "department of the navy", "department of the army",
    "department of the air force", "office of the chief signal officer",
    "naval photographic center", "army pictorial", "signal corps",
    "united states marine corps", "marine corps", "coast guard",
    "department of justice", "federal bureau of investigation",
    "office of war information", "united states information agency",
    "department of state", "department of the interior", "department of agriculture",
    "national aeronautics and space administration", "works progress administration",
    "office of strategic services", "war department", "atomic energy commission",
    "environmental protection agency", "bureau of ",
)
THIRD_PARTY_LANG = (            # scanned over title+scope+generalNotes+contributors+donors
    "newsreel", "courtesy of", "obtained from other sources", "proprietary rights",
    "copyright", "universal", "pathe", "path\u00e9", "movietone", "hearst",
    "march of time", "paramount news", "cbs", "nbc", "abc news",
    "gift of", "donated by", "captured german", "captured enemy", "captured japanese",
    "licensed", "stock footage from",
)
SHOTLIST_LANG = (               # narrow set — shot lists name real objects, so the
    "newsreel", "captured enemy", "captured german", "captured japanese",
    "courtesy of", "stock shot from", "copyright",   # broad list would false-positive
)
HARD_CLAIM = (
    "is copyrighted", "copyright is retained", "copyright retained by",
    "may not be used for commercial", "not for commercial use",
    "commercial use is prohibited", "permission of the copyright owner is required",
    "written permission of the donor",
)
OK_STATUS = {"unrestricted", "undetermined", ""}


def nara_license_decision(rec: dict) -> tuple[str, str, str]:
    use    = rec.get("useRestriction") or {}
    status = str(use.get("status", "")).strip()
    note   = str(use.get("note", "") or "")
    spec   = [str(s) for s in (use.get("specificUseRestrictions") or [])]
    anc    = rec.get("ancestors") or []
    rgs    = [a for a in anc if a.get("levelOfDescription") == "recordGroup"]
    colls  = [a for a in anc if a.get("levelOfDescription") == "collection"]
    creators = [str(c.get("heading", "")) for a in anc for c in (a.get("creators") or [])]
    creators += [str(c.get("heading", "")) for c in (rec.get("creators") or [])]
    creator_s = " | ".join(creators)
    ev = "useRestriction=" + json.dumps(use, ensure_ascii=False)

    blob = " ".join([str(rec.get("title", "")), str(rec.get("scopeAndContentNote", "")),
                     " ".join(str(x) for x in (rec.get("generalNotes") or [])),
                     json.dumps(rec.get("contributors") or [], ensure_ascii=False),
                     json.dumps(rec.get("donors") or [], ensure_ascii=False),
                     str(rec.get("productionSeriesTitle", ""))]).lower()

    # R0 — affirmative claim or commercial bar anywhere in the rights fields.
    hay = (note + " " + " ".join(spec) + " " + blob).lower()
    for p in HARD_CLAIM:
        if p in hay:
            return "reject", "R0/explicit-claim", f'{ev}; hard-claim phrase "{p}"'
    if status.lower() == "restricted":              # hard, not "Restricted - Possibly"
        return "reject", "R0/status-restricted", ev

    # R3 — provenance gates (a collection ancestor means DONATED third-party film).
    if colls:
        why = ", ".join(f'{c.get("collectionIdentifier")}: {c.get("title")}' for c in colls)
        return ("review_required", "R3/donated-collection",
                f"{ev}; donated collection ancestor [{why}]; creator {creator_s or '?'}")
    if not rgs:
        return "review_required", "R3/no-record-group", f"{ev}; no federal recordGroup ancestor"
    if not any(k in creator_s.lower() for k in US_FEDERAL_CREATOR):
        return ("review_required", "R3/creator-not-federal",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')} but creator {creator_s or '?'}")

    # R3 — federal record group, but the record describes third-party material.
    tp  = [k for k in THIRD_PARTY_LANG if k in blob]
    tp += [k for k in SHOTLIST_LANG if k in str(rec.get("shotList", "")).lower()]
    if tp:
        return ("review_required", "R3/third-party-content-language",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')} but record describes "
                f"third-party material {tp} — agency-collected, not agency-created")

    # R3 — OFFICIAL-DUTY / CUSTODY GUARD.  17 U.S.C. 105 clears a work only if a US
    # federal employee MADE it.  No production date + multi-year coverage span = an
    # accessioned compilation the agency collected.  (Caught naId 87665/87666,
    # captured Japanese POW-camp film sitting in RG 428 with status "Undetermined".)
    cs, ce = rec.get("coverageStartDate") or {}, rec.get("coverageEndDate") or {}
    span = (int(ce.get("year", 0)) - int(cs.get("year", 0))) if (cs and ce) else 0
    if not (rec.get("productionDates") or []) and span >= 1:
        return ("review_required", "R3/undated-multiyear-compilation",
                f"{ev}; RG {rgs[0].get('recordGroupNumber')}, no productionDate, "
                f"{span}-year coverage span {cs.get('year')}-{ce.get('year')}")

    # R3 — any surviving restriction flag (the RG-111 blanket case lands here).
    if status.lower() not in OK_STATUS:
        return ("review_required", "R3/restriction-flagged",
                f'{ev}; NARA flags status "{status}" spec={spec}')
    if spec:
        return "review_required", "R3/specific-use-restriction", f"{ev}; spec={spec}"
    if note:
        return "review_required", "R3/restriction-note", ev

    # R1 — US Government work.
    return ("pd", "R1/us-federal-record",
            f'{ev}; RG {rgs[0].get("recordGroupNumber")} "{rgs[0].get("title")}"; '
            f'creator {creator_s}; localId {rec.get("localIdentifier","")}; no donor or '
            f"collection ancestor; no third-party-content language — 17 U.S.C. 105")
```

Wiring notes for the gov lane:

* Write **all three** return values into the ledger row:
  `license_decision`, `triage_rule`, and `license_evidence` (the `ev` string plus
  the rule id and `nara-license-triage-v001`). A row must never carry a decision
  without its evidence.
* `"reject"` → do not download; log to `rejects.jsonl` with
  `reason: "license:R0/explicit-claim"`.
* Keep `license_field_raw` exactly as it is today (verbatim `useRestriction`) —
  §2 of the contract still requires the raw field.
* **Expected effect on the current corpus:** of the 50 items that piled up in
  quarantine, this rule block auto-clears 9 to the shelf and files the other 41
  under a *named, evidenced* reason instead of the undifferentiated
  `review_required`. It does not turn the quarantine off — it makes it small and
  legible.

### Owner unlock (deliberate policy call — do NOT automate)

Two blocks are almost certainly public domain but are held on the conservative
side of the line above. Each needs one owner decision, and each is a one-line
rule change once decided:

1. **RG 111 Signal Corps trial footage** — 25 items / 3.89 GB, incl. the complete
   Nuremberg / Yokohama / Yamashita / Pétain / Quisling trial coverage. Evidence
   for unlocking: creator is the Army Chief Signal Officer, the flag is applied to
   223/223 items of the series (no per-item determination), and access status is
   `Unrestricted`. Evidence against: naId 23674 in the very same series is credited
   to *Paramount, March of Time & Pathé News*. If the owner accepts the class,
   promote **only** items whose record has no `generalNotes` and no contributors —
   which is what `R3/third-party-content-language` already tests — by adding
   `RG 111` to an allowlist that bypasses `R3/restriction-flagged`.
2. **Ford Motor Company Collection pre-1930 items** — 4 items / 0.51 GB
   (naId 7403239, 92280, 91009, 90805; produced 1916–1920). PD-by-date needs
   evidenced US publication before 1930; NARA documents production only. A single
   copyright-office / catalogue check per title would settle all four.

---

## 7. Side observations (not acted on — outside this task's write scope)

* **Tombstone does not block re-ingest.** naId 16664 was deleted and tombstoned to
  `gov_dedup_removed.jsonl` at 16:24:48 as off-theme, then **re-downloaded** at
  16:29:59 and is back in quarantine with a fresh ledger row. Resume/dedup reads
  `<source>.jsonl` but not `<source>_dedup_removed.jsonl`, so every tombstoned item
  will be re-fetched on the next pass. Worth a one-line fix in the lane's resume
  index.
* **`coverr__coverr-premium-couple-observes-ocean-waves`** sits in
  `_quarantine\ocean_nature\` with `license_field_raw: "Coverr slug marked
  'premium' — tier/license uncertain"`. Not NARA; belongs to the stock lane.
* `_quarantine\government_buildings\` is empty.

---

## 8. Reproducing / re-running this triage

The triage engine is re-runnable and state-free apart from the ledger itself:
a row that already carries `triage_rule` is settled and is never re-decided, so a
later pass only touches rows the gov lane has appended since. Catalog fetches are
cached by naId. The ledger rewrite re-reads the file immediately before
`os.replace` and retries if the gov lane appended meanwhile, so rows appended
during the sweep are never lost.

```
scripts (scratchpad, this session):
  fetch_nara.py <naId>...   # cache full catalog records (fresh conn, JSON guard, 1 req/s)
  triage.py                 # plan only — prints the decision table
  triage.py --apply         # move / delete / rewrite ledger
  frames.py <video>...      # 10/50/90 % QC frames -> _qc\quarantine_triage\
```

Order of operations for the next sweep: `triage.py` (it prints the naIds it still
needs) → `fetch_nara.py <those naIds>` → `triage.py` → eyeball the promotion
candidates → `triage.py --apply`.

---
---

# 9. OWNER UNLOCK — executed 2026-07-28 (rules version `nara-license-triage-v002`)

Everything above (§1–§8) is the v001 sweep and is unchanged. This section records
the owner decision on the two blocks §6 "Owner unlock" left open, the per-item
verification that preceded promotion, and the new counts.

## 9.1 The decision

> **Owner, 2026-07-28, verbatim: 「両方使う」** — approve **both** flagged classes for use.
>
> * **Class A — RG 111 Signal Corps trial footage** (25 items / 3.89 GB, incl. the
>   Nuremberg / Yokohama / Yamashita coverage). Rationale accepted: the
>   "Restricted - Possibly" flag is series boilerplate (measured 223/223 in series
>   13807, §2), the creator is a US federal agency, so 17 U.S.C. §105 PD applies.
> * **Class B — the 4 pre-1930 Ford items** (production dates 1916–1920).

The approval is recorded on every affected ledger row as
`owner_approval: "2026-07-28 owner approved both flagged classes (両方使う)"`.

## 9.2 What the owner decision does *not* cover — the one disqualifier tested per item

The decision clears *federal creator* (class A) and *pre-1930 production* (class B).
It does **not** clear an item that is a **commercial newsreel or carries a
third-party commercial production credit** — the failure mode §2 named, evidenced by
naId 23674 "QUISLING TRIAL", which sits in the very same RG 111 series and carries
`Contributor: Producer, Paramount, March of Time & Pathe News`.

So no row was flipped in bulk. Each of the 29 items was checked individually, on
two independent channels:

1. **Catalog record re-read** (cached full records, `nara_records.json`): `title`,
   `scopeAndContentNote`, `generalNotes`, `contributors`, `donors`, `creators`,
   `productionSeriesTitle`, `shotList`, `variantControlNumbers`, `ancestors`
   scanned for `paramount`, `pathe/pathé`, `march of time`, `universal`,
   `movietone`, `hearst`, `mgm`, `warner`, `rko`, `gaumont`, `telenews`,
   `castle films`, `news of the day`, `cbs`, `nbc`, plus `newsreel`,
   `produced by`, `released by`, `courtesy of`, `stock footage from`.
   **Result: 0 hits across all 29.** (The same scan flags naId 23674 correctly, so
   it is not a silent no-op.) All 25 class-A records are `editStatus: Unedited`
   with `accessRestriction: Unrestricted` and no `generalNotes`/`contributors`.
2. **Eyeball** — QC frames at 10 / 50 / 90 % per the §4 convention, **plus a 2 %
   frame and head frames at 4–55 s**, because a newsreel credit lives in the head
   leader where a 10 % sample lands well past it. 116 new frames + 10 labelled
   contact sheets in `H:\pd-media\assets\archive\_qc\quarantine_triage\`
   (`unlock_sheet_1..6.jpg`, `unlock_headA_1..3.jpg`, `unlock_headstrip.jpg`).
   **This is what caught the one disqualified item** — see §9.4.

## 9.3 Per-item outcome

| naId | title | class | localId | MB | outcome | `license_decision` | rule |
|---|---|:--:|---|---:|---|---|---|
| 15131 | TRIAL OF NAZI SPIES, CHERBOURG, FRANCE ; … | A | 111-ADC-1324 | 194 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 16664 | FIRST SHOT INTO GERMANY, THEDING (?), FRANCE ; … | A | 111-ADC-2861 | 140 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 17647 | PRISON CAMP, BAD ORB, GERMANY | A | 111-ADC-3844 | 107 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19251 | YAMASHITA TRIAL, FOURTH DAY, MANILA | A | 111-ADC-5452 | 144 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19382 | YAMASHITA TRIAL, 32ND DAY, MANILA | A | 111-ADC-5583 | 101 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19383 | YAMASHITA TRIAL, 31ST DAY, MANILA | A | 111-ADC-5584 | 149 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19400 | PARIS. [No.] 460, WAR CRIMES TRIALS, NUREMBERG | A | 111-ADC-5601 | 266 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19413 | WAR CRIMES TRIAL, TATSUO TSUCHIYA, YOKOHAMA | A | 111-ADC-5614 | 99 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19463 | PARIS. [No.] 457, WAR CRIMES TRIAL, NUREMBERG | A | 111-ADC-5665 | 184 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19611 | MUNICH. [No.] 84, WAR CRIMES TRIALS, NUREMBERG | A | 111-ADC-5813 | 165 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19613 | MUNICH. [No.] 15, WAR CIRMES TRIALS, NUREMBERG | A | 111-ADC-5815 | 187 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19661 | MUNICH. [No.] 004, WAR CRIMES TRIALS, NUREMBERG | A | 111-ADC-5863 | 139 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19878 | MUNICH. [Nos.] 211-222, WAR CRIMES TRIALS | A | 111-ADC-6080 | 197 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19879 | MUNICH. [Nos.] 211-222, WAR CRIMES TRIALS | A | 111-ADC-6081 | 216 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 19941 | WAR CRIMES TRIALS, TOKYO, JAPAN | A | 111-ADC-6143 | 137 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 20223 | MUNICH. [No.] 522, WAR CRIMES TRIALS CASE NO. 1 | A | 111-ADC-6449 | 200 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 20262 | MUNICH. [No.] 544, SENTENCING OF GEN. MILCH | A | 111-ADC-6488 | 120 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 20264 | THE MARCH OF DIMES DRIVE … ; BUCHENWALD TRIAL | A | 111-ADC-6490 | 107 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 20795 | WAR CRIMES ATROCITY TRIALS, YOKOHAMA, JAPAN | A | 111-ADC-7023 | 179 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 21254 | DECISION BOARD TRIAL - FRITZ KUHN, MUNICH | A | 111-ADC-7482 | 159 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 21261 | ESPIONAGE TRIAL, MUNICH ; KOREAN CONSTABULARY | A | 111-ADC-7489 | 168 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 23559 | QUISLING TRIAL | A | 111-ADC-9794 | 97 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 23628 | TRIAL OF MARSHAL HENRI PETAIN | A | 111-ADC-9863 | 146 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| 23629 | TRIAL OF MARSHAL HENRI PETAIN | A | 111-ADC-9864 | 74 | **promoted** | `pd_us_gov` | R5/owner-unlock-rg111-federal |
| **23816** | **THE VERDICT, NUREMBERG TRIAL** | A | 111-ADC-10054 | **219** | **HELD** | `review_required` | **R3/non-us-coproduction-credit** |
| 7403239 | Indianapolis, Indiana / President Woodrow Wilson … | B | FC-FC-1 | 81 | **promoted** | `pd_expired_owner_approved` | R5/owner-unlock-pre1930-ford |
| 90805 | [SCENES IN SOUTH WEST UNITED STATES] | B | FC-FC-204 | 174 | **promoted** | `pd_expired_owner_approved` | R5/owner-unlock-pre1930-ford |
| 91009 | AT THE CROSS ROADS [LEAVENWORTH PRISON] | B | FC-FC-332 | 110 | **promoted** | `pd_expired_owner_approved` | R5/owner-unlock-pre1930-ford |
| 92280 | LOS ANGELES | B | FC-FC-2434 | 141 | **promoted** | `pd_expired_owner_approved` | R5/owner-unlock-pre1930-ford |

Every promoted row now carries: `license_decision`, new `file_path`,
`owner_approval`, a per-item `license_evidence` (creator / record group / ancestors
/ localId / production dates **plus** the series-boilerplate measurement for class A,
or the 1916–1920 production dates for class B, **plus** the frames actually looked at),
`use_check_required: true`, `use_check_note`, `qc_note`, `triage_rule`, and
`prior_triage_rule` (what quarantined it in v001, kept for audit).

## 9.4 The eyeball contradiction — naId 23816 stays in quarantine

The metadata said promote. The pixels said no. **This is the second time in this
corpus that the frames overruled a clean record** (the first was 87665/87666 in §4).

naId 23816 "THE VERDICT, NUREMBERG TRIAL" — RG 111, `editStatus: Unedited`,
`accessRestriction: Unrestricted`, no generalNotes, no contributors, and it passed
the commercial-producer text scan clean. Its head frames:

| t | frame |
|---|---|
| 4 s | NARA transfer card `111.ADC.10054 / Source: Digital Betacam (I Copy)` |
| 10–18 s | `FILMVORFÜHRUNGSSCHEIN — Es wird hiermit bescheinigt dass **Welt im Film Nr 71** zur öffentlichen Vorführung zugelassen ist. Bescheinigung ausgestellt im Auftrag der **Alliierten Behörden**` |
| 28 s | **WELT IM FILM** main title (animated globe logo) |
| 40 s | `NÜRNBERGER PROZESS: DAS URTEIL` / *WELT IM FILM* |
| 55 s | German narration card describing the Nuremberg judgment |

This is a **finished, released issue of *Welt im Film*** — the occupation newsreel
produced **jointly by the US and British military governments** in occupied Germany
— not raw Signal Corps camera coverage. The catalog corroborates it and was
half-read in v001: `productionSeriesTitle: "World in film"`,
`productionSeriesNumber: "71"`. It also **mislabels** the reel `editStatus: Unedited`,
which is plainly false against the picture.

A British co-author is outside 17 U.S.C. §105, so the owner's federal-creator
rationale does not reach this item. Held, **not rejected**, at 219 MB, with
`hold_reason: non-us-coproduction-credit`.

*Naming note:* it is filed as `non-us-coproduction-credit`, **not**
`commercial-producer-credit`, because the release credit names the *Allied
Authorities* — a governmental body, not a commercial producer. Writing
"commercial" into the ledger would have been factually wrong. It needs its own
one-line owner decision: *is a US/UK jointly produced occupation newsreel
acceptable?*

**Commercial-producer credits found: none.** No item among the 29 named Paramount,
Pathé, March of Time, Universal, Fox Movietone or any other commercial producer,
in metadata or on screen. naId 23674 — the item that proved the risk is real — was
already held in v001 under `R3/third-party-content-language` and was not part of
this promotion set.

## 9.5 Evidence the eyeball found *for* the promotions

Not just an absence of bad news. Several reels carry on-screen proof of the very
authorship the owner's rationale asserts:

* **naId 20262** — Army Pictorial Division slate: `ARMY PICTORIAL DIVISION / WAR
  CRIMES TRIALS / NURNBERG / SENTENCE MILCH / CASE: NO.2 / CAM: 342 MAG: 2 /
  CAMERAMAN: VILIM / SOUNDMAN: VILIM`.
* **naId 20223** — same APD slate form, `ROLL 100 / CAM 342 MAG 3 / CAMERAMAN: TACEY`.
* **naId 19383** — `SIG PHOTO / Tec 3 Al Bettcher / 31ST DAY / YAMASHITA TRIAL /
  MANILA / 5 DEC / ROLL 1`.
* **naId 19251** — `YAMASHITA 4TH DAY … SGT. McCLURE / LT. DETMERS`.
* **naId 19941** — `WAR CRIMES TRIAL - TOKYO / ROLL 1 / CREW 3 / DATE 8/15/46`.
* **naId 20264** — `A.P.S. PHOTOLAB 3 / CAMERA-TAYLOR / 6-2-47` (Army Pictorial Service).
* **naId 17647** — Army film-library stencil `LIB 5064`.

Class B gained the element §5 said was missing — **evidence of publication**:

* **naId 92280** — main title `LOS ANGELES / A visit to American Cities with the
  **Ford Educational Weekly** / Produced by the Ford Motor Company` + lettered
  intertitles: a released theatrical series issue, published 1917.
* **naId 91009** — `Produced & Distributed by **Ford MOTION PICTURE LABORATORIES** /
  Copyrighted by Ford Motor Company` + narrative intertitles: a finished, released
  1919 theatrical short. The 1919 copyright notice does **not** defeat the
  clearance — it evidences publication, and a US work published in 1919 left
  copyright at the 95-year maximum (2014). Do not put that card on screen.
* **naId 7403239 and 90805 remain weaker**: NARA transfer cards (`FC.FC.1`,
  `FC.FC.204`) straight to picture, **no release title card** — unedited Ford
  outtakes. Their clearance rests on the owner's production-date approval alone,
  with no independent on-screen publication evidence. Recorded as such in
  `license_evidence`.

## 9.6 Standing use-time check (now on every promoted row)

`use_check_required: true` and:

> `use_check_note`: "Before using in a published video, confirm this item's
> on-screen and catalog credits name no commercial producer (Paramount/Pathé/March
> of Time/Universal/Fox Movietone); crop burned-in timecode if present."

This is not ceremony. Series 13807 demonstrably mixes agency-shot and
third-party-produced film (naId 23674), and 23816 above proves the mix reaches
items whose metadata looks clean. The check is cheap at edit time — the head
leader and the first title card answer it.

### QC notes carried forward so the build stage cannot be surprised

Written into `qc_note` on every promoted row. The v001-promoted rows were
back-filled with §4's findings in the same pass:

| naId | qc_note (summary) |
|---|---|
| 76954 | Burned-in archival timecode `00:32:36.27 RTC` bottom-left for the whole reel — **crop** or frame out the lower left. 90 % frame is black tail leader. |
| 80630 / 80631 | Colour stock **severely faded to magenta/blue** — grade before use; do not cut ungraded against clean B&W. |
| 79817 | **Bundled** — camp footage runs into unrelated street scenes of Haikimo village; needs shot selection. |
| 77646 | **Bundled** — opens on ~2 min of featureless open sea before the rescue material. |
| 16664 | Heavy sepia/amber transfer cast — grade. Largely **off-theme** (artillery; only a short civil-court segment). |
| 19613 / 19661 | Markedly **underexposed** Nuremberg interiors — lift before use. |
| 20264 | **Bundled** — first part is a March-of-Dimes fundraising drive; Buchenwald/Dachau trial material comes later. Title says *March of **Dimes***, not *March of Time* — not a newsreel. |
| 21261 | **Bundled** — Munich espionage tribunal + unrelated Korean Constabulary material. |
| 23559 | **Bundled** — Quisling courtroom, then unrelated U-boat surrender / naval footage. |
| 15131 / 19400 / 19878 / 19879 / 20795 | Head is SMPTE colour bars (picture starts late); several have black tail leader at 90 %. Trim heads/tails. |
| 20262 | One sampled frame out of focus — check focus when selecting shots. |
| 19463 | The 90 % frame is a large *"Position of Kaltenbrunner and the Gestapo and SD in the German Police System"* evidence chart — usable as a graphic. |
| 90805 | Low-contrast/dark scenery — grade. No release title (see §9.5). |
| 91009 | Do **not** show the "Copyrighted by Ford Motor Company" card on screen. |
| 92280 | Avoid the Ford Educational Weekly credit card on screen. |

## 9.7 New counts by verdict

Promotion, measured after the move (sha256 of every shelf copy re-verified against
the ledger hash **before** the quarantine source was removed):

| | items | GB |
|---|---:|---:|
| **Promoted this pass** | **28** | **4.181** |
| — class A → `pd_us_gov` | 24 | 3.675 |
| — class B → `pd_expired_owner_approved` | 4 | 0.506 |
| **Held this pass** | **1** | **0.219** |
| **Rejected / deleted** | **0** | **0.00** |

Whole-archive state after the pass:

| location / verdict | items | GB |
|---|---:|---:|
| **Shelf `E:\pd-archive\` total** | **72** | **5.974** |
| — `pd` (gov lane + v001 sweep) | 44 | 1.793 |
| — `pd_us_gov` (this pass) | 24 | 3.675 |
| — `pd_expired_owner_approved` (this pass) | 4 | 0.506 |
| **Quarantine total** | **24** | **3.257** |
| — `R3/donated-collection` | 8 | 0.961 |
| — `R3/undated-multiyear-compilation` (87665/87666) | 2 | 0.461 |
| — `R3/third-party-content-language` (12101, 23674) | 2 | 0.355 |
| — `R3/non-us-coproduction-credit` (23816, new) | 1 | 0.219 |
| — untriaged: ingested by the gov lane after the v001 sweep | 11 | 1.260 |

The quarantine fell from 41 items / 6.18 GB to 13 triaged items / 2.00 GB
(24 / 3.26 GB counting the 11 rows the gov lane has appended since — those need
the next sweep, they were not in scope here).

**naId 87665 / 87666 stay quarantined regardless** — captured foreign POW-camp film
per §4, not touched by this decision.

## 9.8 Verification actually performed

* 29/29 ledger rows located, 0 missing source files, 0 destination collisions.
* Copy → **sha256 re-verified against the ledger hash** → ledger rewritten → only
  then the quarantine source removed. A mismatch would have aborted with nothing
  deleted.
* The gov lane held `ingest_gov.lock` and was appending during the pass, so the
  ledger rewrite re-read the file immediately before `os.replace` and would have
  retried on any change (§8 pattern).
* Post-check: 96 ledger rows, **0 rows whose `file_path` does not exist**,
  28 rows with `use_check_required`, 33 rows with a `qc_note`,
  24 `pd_us_gov` / 4 `pd_expired_owner_approved`, 23816 still on disk in
  `_quarantine\courtroom_justice\`, no `.part` leftovers on the shelf.

---

## 9.9 FOR THE GOV LANE — paste-ready rule change for FUTURE ingests

`ingest_gov_archives.py` is owned by the gov-lane sibling and was **not** edited
here. The block below is what this owner decision implies for new NARA items, ready
to drop into `nara_license_decision()`. It changes the outcome only for federal
records whose sole blocker was a series-boilerplate restriction flag.

```python
# ---------------------------------------------------------------------------
# nara-license-triage-v002 — OWNER DECISION 2026-07-28 ("両方使う"):
# RG 111 / federal-creator items whose only blocker is a SERIES-BOILERPLATE
# restriction flag auto-classify as pd_us_gov WITH use_check_required=True,
# EXCEPT when a commercial producer credit is present.
#
# Evidence: series 13807 carries "Restricted - Possibly / Copyright" on 223/223
# items — a series-wide caution, not a per-item determination (v001 §2). The
# creator is the Army Chief Signal Officer, a US federal agency, so 17 U.S.C. 105
# applies. The residual risk is that the series MIXES agency-shot and
# commercially-produced film (naId 23674 = Paramount / March of Time / Pathé News),
# so the commercial-producer test stays hard and a use-time check is attached to
# every row this rule clears.
#
# INSERT INTO nara_license_decision() immediately BEFORE the
# "R3 — any surviving restriction flag" block, i.e. after the third-party-content
# and undated-multiyear-compilation guards have already had their say.
# Those guards MUST keep running first — they are what catches 23674 and 87665/6.

BOILERPLATE_RG = {"111", "428"}          # series-wide flag measured, no per-item call
BOILERPLATE_STATUS = {"restricted - possibly"}

    rg_no = str(rgs[0].get("recordGroupNumber") or "")
    if (status.lower() in BOILERPLATE_STATUS
            and rg_no in BOILERPLATE_RG
            and not tp                        # no third-party-content language (above)
            and not (rec.get("generalNotes") or [])
            and not (rec.get("contributors") or [])
            and not (rec.get("donors") or [])
            and str(use.get("note", "") or "") .strip().lower().startswith(
                "some or all of this material may be restricted")):
        return ("pd", "R5/owner-unlock-rg111-federal",
                f'{ev}; RG {rg_no}; creator {creator_s}; localId '
                f'{rec.get("localIdentifier","")}; status "{status}" is SERIES BOILERPLATE '
                f'(223/223 in series 13807, nara-license-triage-v001 §2), no item-level '
                f'determination, no generalNotes/contributors/donors, no third-party-content '
                f'language — 17 U.S.C. 105. OWNER-APPROVED 2026-07-28 ("両方使う"). '
                f'USE-CHECK REQUIRED.')
# ---------------------------------------------------------------------------
```

Three wiring requirements that come with it — the rule is **not** safe without them:

1. **Every row this rule clears must be written with**
   `use_check_required = True` and
   `use_check_note = "Before using in a published video, confirm this item's
   on-screen and catalog credits name no commercial producer (Paramount/Pathé/March
   of Time/Universal/Fox Movietone); crop burned-in timecode if present."`
   plus `owner_approval = "2026-07-28 owner approved both flagged classes (両方使う)"`.
   A `pd_us_gov` row from this rule without `use_check_required` is a defect.
2. **Order is load-bearing.** `R3/third-party-content-language` and
   `R3/undated-multiyear-compilation` must still be evaluated *before* this rule.
   The `not tp` / `not generalNotes` / `not contributors` conditions are exactly
   what keeps naId 23674 (Paramount / March of Time / Pathé) out.
3. **Metadata alone is not sufficient — keep the eyeball gate.** naId 23816 passed
   *every* condition above (RG 111, Unedited, Unrestricted, no notes, no
   contributors, clean text scan) and is a released Anglo-American *Welt im Film*
   newsreel. Recommended cheap machine guard, since the give-away was in the
   catalog all along:

   ```python
   # A record that names a released production series is not raw agency coverage.
   pst = str(rec.get("productionSeriesTitle", "")).strip().lower()
   if pst and pst not in {"munich", "paris"}:      # ADC lab dailies, not releases
       return ("review_required", "R3/released-production-series",
               f'{ev}; productionSeriesTitle "{rec.get("productionSeriesTitle")}" '
               f'no. {rec.get("productionSeriesNumber","?")} — a released series issue, '
               f'not raw agency camera coverage; check the head title card')
   ```

   And keep sampling a **2 % / head frame**, not only 10/50/90 %: the release
   credit is in the head leader, which a 10 % sample lands past.

**Pre-1930 (class B) is deliberately NOT automated.** The four Ford items were
cleared by owner decision on production date. Two of them (92280, 91009) turned out
to carry on-screen publication evidence and two (7403239, 90805) did not. Date-based
PD still needs evidenced US publication, so the gov lane should keep returning
`R3/donated-collection` for donated-collection items and let a human decide.
