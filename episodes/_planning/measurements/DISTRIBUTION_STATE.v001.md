# DISTRIBUTION STATE v001 - measured, read-only

- measured_at: `2026-08-12T17:38:22.358297+00:00`
- channel: `UCuQPtAz1rca9eJ4xhvX0yKA` (Prime Documentary)
- videos total: 150 (long-form 69, shorts 81)
- long-forms **public** 51 / private-or-scheduled 18

> All tables below count **public long-forms only** - a private/scheduled video has
> no distribution surface yet, and its description is still editable pre-publish.

## Headline counts (public long-forms)

| metric | value |
|---|---|
| public long-forms | 51 |
| chapters render correctly (`OK`) | 29 |
| **no chapter block written at all** (`MISSING`) | **22** |
| block written but YouTube will NOT render it (`RENDER_BROKEN`, a <10s chapter) | 0 |
| published with placeholder chapter text (`PLACEHOLDER`) | 0 |
| stray timestamps only (`FRAGMENT`) | 0 |
| **total not showing chapters to viewers** | **22** |
| description links another video | 37 |
| description links a playlist | 37 |
| member of >=1 playlist | 48 |
| has a channel-authored comment thread | 49 |
| has any external comment thread | 2 |

- playlists on channel: **4** covering 55 distinct videos (48 public long-forms)

## Chapter regression timeline (public long-forms, `has_chapter_block`)

| publish month | long-forms | with chapter block | without | actually rendering |
|---|---|---|---|---|
| 2026-06 | 15 | 8 | 7 | 8 |
| 2026-07 | 26 | 21 | 5 | 21 |
| 2026-08 | 10 | 0 | 10 | 0 |

- last long-form WITH a chapter block: `2026-07-27` (`Enok7A7wGBA`)
- first long-form WITHOUT one after it: `2026-07-28`
- **unbroken chapterless run at the tail: 14 videos**

## Playlists on the channel

| id | title | privacy | items | dead items | private items |
|---|---|---|---|---|---|
| `PLfPI0t-nSRxw` | The System Got It Wrong | public | 12 | 3 | 0 |
| `PLd04glUie5rg` | The Forfeiture Files: When the Government Takes What's Yours | public | 8 | 1 | 0 |
| `PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P` | Fraud, Finance & Power | public | 11 | 0 | 0 |
| `PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9` | Police Power: What They Can Actually Do to You | public | 24 | 3 | 0 |

**The System Got It Wrong** has unviewable entries:
- position 4: `Pmh6h5SfWw4` "A Judge Took $2.8 Million to Fill a Private Jail With Children. Hearings Ran 90 Seconds." - unresolved (deleted / not owned)
- position 9: `PfdEpNQyaQQ` "6 Trials. 4 Death Sentences. 23 Years. The Same Prosecutor Every Time." - unresolved (deleted / not owned)
- position 10: `4FlCaOVpln0` "A Computer Invents a £2,000 Debt. Her Own Employer Prosecutes Her. 236 Go to Prison." - unresolved (deleted / not owned)

**The Forfeiture Files: When the Government Takes What's Yours** has unviewable entries:
- position 5: `4uuY6G0LmHo` "Police Destroyed His Home Chasing a Stranger — Then Paid Him Nothing" - unresolved (deleted / not owned)

**Police Power: What They Can Actually Do to You** has unviewable entries:
- position 13: `gR_nzXIyIlk` "A Computer Picked His Face Out of a Blurry Still. He Spent 30 Hours in a Cell." - unresolved (deleted / not owned)
- position 14: `SOu4Y1NkGGY` "He Showed the Officer the Paid Receipt. He Was Jailed and Strip-Searched Twice." - unresolved (deleted / not owned)
- position 15: `X40EbUw5kzQ` "Detectives Told Him His Cousin Had Confessed. It Was a Lie, and the Court Allowed It." - unresolved (deleted / not owned)

## Enumeration cross-check

- uploads playlist: 150
- `search.list(forMine=true)`: 0
- union used by this audit: **150**
- channel `statistics.videoCount`: 125
- videos search omits (150): `Y_U9FuHhtt8`, `EOJ0UZpez2c`, `ks3bD1y8jME`, `7FtjlGfFoLk`, `-pCnBZIXvXY`, `XKqMNTfECbE`, `urLPe23TPWg`, `lI5O-q-OeQY`, `dlCX2deks60`, `jVxPEiWhFH0`, `rm1EA-6iYJ8`, `ssvpqiFPM7k`, `ENEMRpoJsMM`, `r68gt0ApNAM`, `8OlcLmZcr7I` ...

> Any audit that enumerates from the uploads playlist alone under-counts this channel.

## Per long-form state (oldest first)

| # | published | video id | title | dur | views | chapters | links vid | links pl | in playlist | owner comment |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-16 | `ch2hQ5jhDmQ` | He Had No Lawyer and Lost. Then He Wrote the Supreme Court | 11m | 5 | MISSING | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 2 | 2026-06-17 | `An0to4U0hJQ` | Police Forced Her Door With a Warrant No One Ever Produced | 12m | 2 | MISSING | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 3 | 2026-06-19 | `waA4XJ9bYcE` | The App Still Showed Their Balances. $8 Billion Had Alread | 12m | 5 | MISSING | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 4 | 2026-06-20 | `sphERPA4gAc` | He Handed the SEC the Arithmetic in 2000. Madoff Kept Runn | 12m | 61 | MISSING | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 5 | 2026-06-21 | `bYcqabvvxak` | A Detective Watched Two Men Pace a Store Window. The Frisk | 11m | 160 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 6 | 2026-06-22 | `XWYWAgkExH4` | Police Took His Phone at Arrest and Opened It. The Supreme | 10m | 8 | MISSING | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 7 | 2026-06-23 | `zE3nCUlUmLY` | Police Never Followed Him. His Carrier Handed Over 127 Day | 11m | 18 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 8 | 2026-06-23 | `cQFql7tT1fE` | He Confessed in Two Hours. Nobody Had Told Him He Was Allo | 11m | 3 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 9 | 2026-06-24 | `m-uWzgWHGPg` | Police Took His $42,000 Car. The Supreme Court Drew a Line | 12m | 19 | MISSING | yes | yes | PLd04glUie5rg | yes |
| 10 | 2026-06-25 | `89SQoRgAD7U` | The City Took Her Pink House for a Development. The Land I | 10m | 2 | OK | yes | yes | PLd04glUie5rg | yes |
| 11 | 2026-06-26 | `cSfe3iGnBBM` | A Cheerleader Swore on Snapchat on a Saturday. Her School  | 12m | 3 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 12 | 2026-06-27 | `1pox44KsaV8` | A Clause Nobody Reads Removed the Right to Sue. The Suprem | 12m | 5 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 13 | 2026-06-28 | `g5yFmDt48oU` | A Swab Taken at Booking Solved a 2003 Rape. The Court Call | 11m | 1 | MISSING | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 14 | 2026-06-29 | `Sz8zPUoBANM` | He Honked His Horn and Drove Home. An Officer Followed Him | 9m | 43 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 15 | 2026-06-30 | `LXFjJqE6vKU` | The Machine Never Worked. The Company Was Valued at $9 Bil | 12m | 0 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 16 | 2026-07-01 | `marQjsCagh0` | OceanGate Fired the Man Who Wrote the Safety Report in 201 | 36m | 201 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 17 | 2026-07-02 | `vikfOBHullI` | She Raised $4 Billion for a Cryptocurrency. There Was No B | 20m | 29 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 18 | 2026-07-03 | `5Jap-0h43A4` | $1 Trillion Vanished in 36 Minutes. The US Extradited One  | 22m | 11 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 19 | 2026-07-04 | `j8U8c4BB_GQ` | He Sold a Side Door Into America's Best Universities. 33 P | 27m | 8 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 20 | 2026-07-05 | `1h267U6PY0I` | Two Men in Police Uniforms Emptied a Boston Museum. The Fr | 27m | 16 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 21 | 2026-07-06 | `tt7U1XgjCU4` | He Jumped Into a Storm With $200,000. Fifty Years On the F | 29m | 121 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 22 | 2026-07-07 | `mj9qEKPRatE` | One Banker Was Paid $550 Million in a Year. Then the Gover | 27m | 22 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 23 | 2026-07-08 | `FTm1icKgycU` | The Site He Downloaded From Dropped It. Prosecutors Filed  | 29m | 23 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 24 | 2026-07-09 | `rYV4rxtQCV0` | A Billionaire Heard His Own Voice on an FBI Tape Built for | 28m | 11 | OK | yes | yes | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 25 | 2026-07-10 | `rrftLmSVivk` | Agents Never Stepped on His Property. They Read the Heat C | 10m | 2 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 26 | 2026-07-11 | `68oWZRiOnB8` | Agents Taped a Microphone to the Outside of a Phone Booth. | 10m | 12 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 27 | 2026-07-12 | `tpAKfHKuwqY` | The Ticket Was Already Written and Handed Back. The Dog Ar | 10m | 14 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 28 | 2026-07-13 | `YhEJHK279f8` | Their Son Was Charged. The City Came for His Parents' Hous | 11m | 5 | OK | yes | yes | PLd04glUie5rg | yes |
| 29 | 2026-07-14 | `Qyad4FejCIc` | Alabama Held an Execution Date on Him for 30 Years. The Ba | 11m | 53 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 30 | 2026-07-15 | `5L_HCGJxX_U` | She Memorised His Face on Purpose So She Would Be Certain. | 11m | 25 | OK | yes | yes | PLfPI0t-nSRxw | yes |
| 31 | 2026-07-16 | `YQIhk2dKZHU` | A Thumb Can Be Compelled. A Passcode Held Only in Memory I | 11m | 5 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 32 | 2026-07-17 | `bXATF9ZnKLE` | Police Searched the Motorcycle in His Driveway. The Court  | 11m | 71 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 33 | 2026-07-18 | `rU2vk9XL4vY` | She Owed the County $15,000. It Sold Her Home for $40,000  | 18m | 224 | OK | yes | yes | PLd04glUie5rg | yes |
| 34 | 2026-07-19 | `6ozsIfwqrP0` | They Took His Life Savings at the Airport — No Charges, No | 19m | 32 | OK | yes | yes | PLd04glUie5rg | yes |
| 35 | 2026-07-20 | `Xc_PxdC_75c` | She Banked Under $10,000 Because That Is What the Till Hel | 19m | 255 | OK | yes | yes | PLd04glUie5rg | yes |
| 36 | 2026-07-26 | `tYZuE76Hwdc` | They Hid the Evidence That Proved Him Innocent — He Spent  | 12m | 41 | MISSING | yes | yes | PLfPI0t-nSRxw | yes |
| 37 | 2026-07-27 | `Enok7A7wGBA` | Police Raided the Wrong House and Handcuffed an Innocent W | 12m | 34 | OK | yes | yes | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 38 | 2026-07-28 | `yRwxBfrOY5o` | Police Came for a Welfare Check and Left With His Guns — N | 12m | 42 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 39 | 2026-07-29 | `GGW1SIAAgkY` | Police Skipped His Rights — Then He Learned He Couldn't Ev | 12m | 18 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 40 | 2026-07-30 | `AxOlQ2NIaBU` | She Owed $1,554 in Traffic Fines. Alabama Jailed Her Until | 11m | 14 | MISSING | no | no | PLd04glUie5rg | yes |
| 41 | 2026-07-31 | `bSnyfsulna8` | Police Never Saw the Driver — the Supreme Court Let Them S | 11m | 134 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 42 | 2026-08-01 | `2pLWw_vhfI8` | The Stop Was Illegal — the Supreme Court Kept the Evidence | 11m | 6 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 43 | 2026-08-02 | `hC5KE6IqmhM` | A Vice Principal Opened a 14-Year-Old's Purse. The Supreme | 11m | 8 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 44 | 2026-08-03 | `i95peRcdtz4` | A Seatbelt Ticket Carried No Jail Time. She Was Handcuffed | 11m | 8 | MISSING | no | no | PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9 | yes |
| 45 | 2026-08-04 | `_8DaMu8_yFw` | Five Children Confessed to a Crime They Didn't Commit. The | 61m | 2 | MISSING | no | no | PLfPI0t-nSRxw | yes |
| 46 | 2026-08-07 | `Wo-SvvGsv8g` | He Paid $139,000 Cash. There Was No Mortgage. The Bank Pad | 27m | 3 | MISSING | no | no | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 47 | 2026-08-08 | `dNhu-IJUc5k` | The Repair Money Was Due July 1. The Building Fell June 24 | 35m | 2 | MISSING | no | no | PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P | yes |
| 48 | 2026-08-09 | `Iw-EPUD2nHg` | A Doctor Reports Police Torture in 1982. The Letter Is Bur | 29m | 5 | MISSING | no | no | PLfPI0t-nSRxw | yes |
| 49 | 2026-08-10 | `H8j_K1x9Dog` | 4 Sailors Confess to One Murder. The DNA Clears Each One.  | 28m | 8 | MISSING | no | no | NONE | yes |
| 50 | 2026-08-11 | `KPYLtYYODLE` | A $2 Test Turned Blue. She Served 21 Days. Police Still Ca | 27m | 6 | MISSING | no | no | NONE | no |
| 51 | 2026-08-12 | `J97Rh1qOTPA` | He Buried His Daughter at Nine. 408,000 Have Filed. One Cl | 29m | 0 | MISSING | no | no | NONE | no |

## Long-forms not showing chapters (restoration targets, highest views first)

| views | published | video id | state | title | fix needed |
|---|---|---|---|---|---|
| 134 | 2026-07-31 | `bSnyfsulna8` | MISSING | Police Never Saw the Driver — the Supreme Court Let  | author a full chapter block |
| 61 | 2026-06-20 | `sphERPA4gAc` | MISSING | He Handed the SEC the Arithmetic in 2000. Madoff Kep | author a full chapter block |
| 42 | 2026-07-28 | `yRwxBfrOY5o` | MISSING | Police Came for a Welfare Check and Left With His Gu | author a full chapter block |
| 41 | 2026-07-26 | `tYZuE76Hwdc` | MISSING | They Hid the Evidence That Proved Him Innocent — He  | author a full chapter block |
| 19 | 2026-06-24 | `m-uWzgWHGPg` | MISSING | Police Took His $42,000 Car. The Supreme Court Drew  | author a full chapter block |
| 18 | 2026-07-29 | `GGW1SIAAgkY` | MISSING | Police Skipped His Rights — Then He Learned He Could | author a full chapter block |
| 14 | 2026-07-30 | `AxOlQ2NIaBU` | MISSING | She Owed $1,554 in Traffic Fines. Alabama Jailed Her | author a full chapter block |
| 8 | 2026-06-22 | `XWYWAgkExH4` | MISSING | Police Took His Phone at Arrest and Opened It. The S | author a full chapter block |
| 8 | 2026-08-02 | `hC5KE6IqmhM` | MISSING | A Vice Principal Opened a 14-Year-Old's Purse. The S | author a full chapter block |
| 8 | 2026-08-03 | `i95peRcdtz4` | MISSING | A Seatbelt Ticket Carried No Jail Time. She Was Hand | author a full chapter block |
| 8 | 2026-08-10 | `H8j_K1x9Dog` | MISSING | 4 Sailors Confess to One Murder. The DNA Clears Each | author a full chapter block |
| 6 | 2026-08-01 | `2pLWw_vhfI8` | MISSING | The Stop Was Illegal — the Supreme Court Kept the Ev | author a full chapter block |
| 6 | 2026-08-11 | `KPYLtYYODLE` | MISSING | A $2 Test Turned Blue. She Served 21 Days. Police St | author a full chapter block |
| 5 | 2026-06-16 | `ch2hQ5jhDmQ` | MISSING | He Had No Lawyer and Lost. Then He Wrote the Supreme | author a full chapter block |
| 5 | 2026-06-19 | `waA4XJ9bYcE` | MISSING | The App Still Showed Their Balances. $8 Billion Had  | author a full chapter block |
| 5 | 2026-08-09 | `Iw-EPUD2nHg` | MISSING | A Doctor Reports Police Torture in 1982. The Letter  | author a full chapter block |
| 3 | 2026-08-07 | `Wo-SvvGsv8g` | MISSING | He Paid $139,000 Cash. There Was No Mortgage. The Ba | author a full chapter block |
| 2 | 2026-06-17 | `An0to4U0hJQ` | MISSING | Police Forced Her Door With a Warrant No One Ever Pr | author a full chapter block |
| 2 | 2026-08-04 | `_8DaMu8_yFw` | MISSING | Five Children Confessed to a Crime They Didn't Commi | author a full chapter block |
| 2 | 2026-08-08 | `dNhu-IJUc5k` | MISSING | The Repair Money Was Due July 1. The Building Fell J | author a full chapter block |
| 1 | 2026-06-28 | `g5yFmDt48oU` | MISSING | A Swab Taken at Booking Solved a 2003 Rape. The Cour | author a full chapter block |
| 0 | 2026-08-12 | `J97Rh1qOTPA` | MISSING | He Buried His Daughter at Nine. 408,000 Have Filed.  | author a full chapter block |

## API capability probes (read-only evidence)

- **videos.list?part=endScreens** -> HTTP `400` (unknownPart)
  - END SCREENS ARE NOT READABLE OR WRITABLE VIA THE DATA API
- **videos.list?part=cards** -> HTTP `400` (unknownPart)
  - CARDS ARE NOT READABLE OR WRITABLE VIA THE DATA API
- **comments.setModerationStatus / pin** -> HTTP `None` 
  - NO PIN ENDPOINT EXISTS. `comments.insert` can post as the channel (a write - not performed here); pinning is Studio/app-manual only, and the pinned flag is not returned by commentThreads.list.
- **playlists.insert / playlistItems.insert** -> HTTP `None` 
  - WRITABLE via Data API (owner GO required). Quota 50 units per insert.
- **videos.update?part=snippet (description/chapters)** -> HTTP `None` 
  - WRITABLE via Data API (owner GO required). Quota 50 units per update. Full snippet must be sent or fields are cleared.

_This file is generated by `scripts/yt_distribution_state.py`. The script performs GET requests only; it has no write path._
