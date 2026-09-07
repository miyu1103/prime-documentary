# Per-video CTR baseline (28-day window, pulled 2026-07-25 22:43) — RECONSTRUCTED 2026-07-28

**Why this file exists (honest incident record).** On 2026-07-28 01:2x I ran `yt_studio_video_ctr.py` on a fresh cookie; the cookie rotated mid-run, every row came back `imp=None ctr=None`, and the script **overwrote `scripts/_yt_studio_video_ctr.json`** — which held the only copy of the 7/25 baseline (it had never been committed to git). The numbers below are reconstructed verbatim from the analysis output produced from that file earlier in the same session, so the baseline survives for the 8/8 comparison.

**Mechanism fix required (do before the next pull):** `yt_studio_video_ctr.py` must (a) refuse to overwrite when every row lacks impressions (401/rotation), (b) write to a dated filename `_yt_studio_video_ctr.<YYYYMMDD>.json` and update a `latest` pointer, and (c) the measurement runbook must snapshot+commit the JSON before any new pull.

## Channel level
| date | impressions | CTR | shorts feed VTR | avg watch from impressions |
|---|---|---|---|---|
| 2026-07-25 | 27,015 | **1.58%** | 32.9% | 269 s |
| 2026-07-28 (tonight, valid HTTP 200) | 30,265 | **1.57%** | 34.35% | 284 s |

Note: the 7/25 packaging refresh (19 thumbnails + 17 titles) went live ON 7/25, so the 28-day window on 7/28 still contains ~25 days of pre-refresh impressions. **No verdict is possible yet** — this is expected, not a failure of the refresh. The real read is the 8/8 pull (2-4 weeks post-apply, per the plan).

## Per-video baseline (long-forms + shorts with ≥50 impressions, 28d ending 2026-07-25)
| CTR % | impressions | avg watch (s) | length (s) | title |
|---|---|---|---|---|
| 4.48 | 736 | 103 | 554 | He Drove Home Honking. The Police Followed Him Inside. |
| 3.85 | 779 | 136 | 697 | Police Can Search Your Car Without a Warrant — Except One Place |
| 3.32 | 241 | 175 | 1336 | The Day $1 Trillion Vanished in 36 Minutes |
| 3.27 | 520 | 175 | 1210 | There Was No Coin: $4 Billion in Empty Promises |
| 3.14 | 4,070 | 108 | 682 | Police Can Stop and Frisk You Without Arresting You |
| 2.99 | 67 | 33 | 564 | A Judge Took $2.8 Million to Send Kids to Prison |
| 2.91 | 103 | 132 | 715 | Police Can Force Your Thumb — But Maybe Not Your Mind |
| 2.69 | 632 | 127 | 720 | Police Took His $42,000 Car. The Supreme Court Drew a Line. |
| 2.63 | 114 | 42 | 721 | The Hidden Code Door Behind the $8 Billion FTX Fraud |
| 2.59 | 116 | 142 | 721 | The Fine Print That Quietly Took Your Right to Sue |
| 2.42 | 4,292 | 525 | 2174 | They Were Warned — The Last Dive of the Titan |
| 2.35 | 425 | 275 | 648 | The Traffic Stop Was Over. Then the Dog Arrived. |
| 2.24 | 626 | 147 | 679 | Your Phone Is Tracking You — and the Police Wanted the Map |
| 1.85 | 1,459 | 219 | 721 | Madoff's Perfect Chart: The $65B Lie Wall Street Believed |
| 1.74 | 460 | 146 | 632 | The FBI Recorded His Calls — and Never Touched the Booth |
| 1.64 | 61 | 208 | 621 | Can the Police Scan Your Home From the Street? |
| 1.54 | 455 | 634 | 1107 | Can the Government Take Your Home Over a Small Tax Debt? |
| 1.39 | 1,367 | 355 | 1782 | D.B. Cooper: The Only Hijacking America Never Solved |
| 1.36 | 369 | 279 | 1717 | The Wiretap That Cracked Wall Street |
| 1.35 | 2,880 | 186 | 698 | He Spent 30 Years on Death Row for a Murder He Didn't Commit |
| 1.28 | 390 | 100 | 714 | Police Arrested Him Because Software Said His Face Matched. It Was Wrong. |
| 1.24 | 1,855 | 56 | 1156 | The IRS Seized Her Entire Bank Account — For Following the Bank's Own Rule |
| 1.21 | 828 | 409 | 1659 | Michael Milken: Genius, or the Face of Greed? |
| 1.18 | 595 | 543 | 1644 | $500M Gone: The Gardner Heist |
| 1.17 | 513 | 309 | 1661 | The Side Door: Operation Varsity Blues |
| 1.02 | 684 | 130 | 647 | Police Took His Phone. Then They Opened It. |
| 0.82 | 1,468 | 95 | 1743 | The Internet's Own Boy: Aaron Swartz |
| 0.81 | 124 | 11 | 641 | Your Home for a Developer? The Kelo Supreme Court Case |
| 0.74 | 1,760 | 115 | 711 | She Studied His Face to Be Certain. She Convicted the Wrong Man. |
| 0.71 | 2,260 | 117 | 552 | He Paid the Fine — and Was Strip-Searched Twice… |
| 0.70 | 143 | 56 | 696 | Read Rights or It's Out \| Miranda v. Arizona |
| 0.52 | 191 | 5 | 721 | Can Your School Punish You for a Post You Made Off Campus? |
| 0.50 | 201 | 462 | 707 | Their Son Was Charged. The City Came for His Parents' House. |
| 0.00 | 92 / 201 / 481 / 132 / 79 / 56 | — | — | frazier / hinders-airport / theranos / king-DNA / young / gideon (six videos at 0.00%) |

**Use at the 8/8 re-measure:** compare each row's CTR against the new pull, weighted by impressions; the refresh targets are the 19 replaced thumbnails + 17 rewritten titles (see `thumbnail_refresh_mapping.v001.json` / `title_refresh_receipt.v001.json`). Videos left untouched on purpose: terry (3.14% proven), riley, timbs.
