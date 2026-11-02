# PLAYLIST PLAN v001 - DRY RUN, NOTHING EXECUTED

- generated: `2026-08-01T21:52:49.179488+00:00`
- design: `config/distribution/series_clusters.v001.json` (status: `approved`)
- measured against: `episodes/_planning/measurements/DISTRIBUTION_STATE.v001.json`
- total API calls if approved: **46** (2300 quota units of a 10,000/day allowance)

**No write has been performed.** Running this script again without `--execute` will never change the channel.

## Validation: PASS - every public long-form is in exactly one playlist

## The four playlists

### Police Power: What They Can Actually Do to You

- action: **reuse_existing** (id `PLKcrM3x4g1h9uB4_PDJQNUEX2oNUmAZZ9`, currently titled "Landmark Rights Cases")
- items: 18
- entry point: **The Traffic Stop Was Over. Then the Dog Arrived.** (`tpAKfHKuwqY`)
  - why: 38.98% average view percentage - the highest measured on the channel - on the most universally relatable scenario (a traffic stop).
- CLEANUP: position 0 currently holds PjGEqW6F9WM, a DELETED video. It is the slot the playlist link lands on. Remove it first.
- CLEANUP: Retitling changes the anchor text in 4 live descriptions that say 'Landmark Rights Cases playlist'. Those descriptions are rewritten in the same batch, so schedule the retitle and the description batch together.

```
A traffic stop. A phone in your pocket. A knock at the wrong door. Every film here is one real case that decided how far the police can go before they need a warrant - and what happens to the person who found out the hard way. Watch in order: the cases build from the roadside to your front door to the interrogation room.

New case every week.
```

| pos | video id | title | views | why here | end-screen slot 1 |
|---|---|---|---|---|---|
| 1 | `tpAKfHKuwqY` | The Traffic Stop Was Over. Then the Dog Arrive | 11 | APV 38.98% - best on channel; everyday scenario | `bXATF9ZnKLE` |
| 2 | `bXATF9ZnKLE` | Police Can Search Your Car Without a Warrant — | 46 | same lane, 2nd highest views in cluster | `Sz8zPUoBANM` |
| 3 | `Sz8zPUoBANM` | He Drove Home Honking. The Police Followed Him | 43 | escalates from roadside to the doorway | `bYcqabvvxak` |
| 4 | `bYcqabvvxak` | Police Can Stop and Frisk You Without Arrestin | 159 | stop and frisk - the doctrine under 1-3 | `XWYWAgkExH4` |
| 5 | `XWYWAgkExH4` | Police Took His Phone. Then They Opened It. | 8 | pivot to the phone | `YQIhk2dKZHU` |
| 6 | `YQIhk2dKZHU` | Police Can Force Your Thumb — But Maybe Not Yo | 5 | thumb vs passcode - direct sequel to Riley | `zE3nCUlUmLY` |
| 7 | `zE3nCUlUmLY` | The phone in his pocket testified against him  | 18 | APV 23.88%; location history | `rrftLmSVivk` |
| 8 | `rrftLmSVivk` | Can the Police Scan Your Home From the Street? | 1 | sensors pointed at the home | `68oWZRiOnB8` |
| 9 | `68oWZRiOnB8` | The FBI taped a microphone to a phone booth ro | 11 | APV 21.58%; the doctrine Kyllo rests on | `An0to4U0hJQ` |
| 10 | `An0to4U0hJQ` | The Police Broke In — So the Court Let Her Go | 2 | what happens when they break in | `Enok7A7wGBA` |
| 11 | `Enok7A7wGBA` | Police Raided the Wrong House and Handcuffed a | 5 | wrong house - the sharpest stakes gap in the cluster | `g5yFmDt48oU` |
| 12 | `g5yFmDt48oU` | The Supreme Court Let Police Take Your DNA at  | 1 | pivot from the home to the body | `gR_nzXIyIlk` |
| 13 | `gR_nzXIyIlk` | Thirty hours in jail because an algorithm chos | 9 | facial recognition; 30 hours in jail | `SOu4Y1NkGGY` |
| 14 | `SOu4Y1NkGGY` | He showed the officer the receipt and was arre | 46 | strip search over a paid fine | `X40EbUw5kzQ` |
| 15 | `X40EbUw5kzQ` | Police Are Allowed to Lie to You Until You Con | 2 | pivot to the interrogation room | `cQFql7tT1fE` |
| 16 | `cQFql7tT1fE` | Read Rights or It's Out / Miranda v. Arizona | 2 | the warning itself | `ch2hQ5jhDmQ` |
| 17 | `ch2hQ5jhDmQ` | He Had No Lawyer. So He Wrote the Supreme Cour | 5 | APV 7.51% - weak, placed late | `cSfe3iGnBBM` |
| 18 | `cSfe3iGnBBM` | Can Your School Punish You for a Post You Made | 2 | weakest thematic fit (student speech, not police) - last | `tpAKfHKuwqY` |

### The Forfeiture Files: When the Government Takes What's Yours

- action: **create_new**
- items: 7
- entry point: **Following the deposit rule is what made her a suspect** (`Xc_PxdC_75c`)
  - why: 172 views - the highest of any long-form on the channel - and the premise (following the rule is what made her a target) is the cluster's cleanest stakes gap.

```
Nobody was convicted of anything. The house, the car, the savings, the surplus from the sale - taken anyway, legally. These are the real cases behind civil forfeiture, tax-sale windfalls and eminent domain, and the ordinary people who spent years getting their own property back.

Watch in order - the amounts get smaller and the injustice gets sharper.
```

| pos | video id | title | views | why here | end-screen slot 1 |
|---|---|---|---|---|---|
| 1 | `Xc_PxdC_75c` | Following the deposit rule is what made her a  | 172 | top-viewed long-form on the channel | `6ozsIfwqrP0` |
| 2 | `6ozsIfwqrP0` | They Took His Life Savings at the Airport — No | 7 | airport cash seizure - direct sibling | `rU2vk9XL4vY` |
| 3 | `rU2vk9XL4vY` | The county sold her condo and kept the extra $ | 14 | completes the announced property trilogy | `YhEJHK279f8` |
| 4 | `YhEJHK279f8` | Their Son Was Charged. The City Came for His P | 5 | APV 24.37% - strongest watch-through in cluster | `m-uWzgWHGPg` |
| 5 | `m-uWzgWHGPg` | Police Took His $42,000 Car. The Supreme Court | 19 | the Supreme Court answer to 1-4 | `4uuY6G0LmHo` |
| 6 | `4uuY6G0LmHo` | Police Destroyed His Home Chasing a Stranger — | 2 | destroyed home, no compensation | `89SQoRgAD7U` |
| 7 | `89SQoRgAD7U` | Your Home for a Developer? The Kelo Supreme Co | 2 | eminent domain - the widest frame, closes the arc | `Xc_PxdC_75c` |

### Fraud, Finance & Power

- action: **reuse_existing** (id `PLKcrM3x4g1h8f4A4PNJLnr8Zy8Uc3as3P`, currently titled "Fraud, Finance & Power")
- items: 9
- entry point: **He warned regulators about Madoff for nearly ten years** (`sphERPA4gAc`)
  - why: 57 views at 19.13% APV - the best combination in this cluster, and the whistleblower framing is the cluster's strongest present-tense injustice.
- CLEANUP: Currently ordered waA4XJ9bYcE (APV 4.24%) at position 0. That is the weakest-retention video in the cluster sitting in the entry-point slot. Reorder before anything else.

```
Nine real collapses: the money that was never there, the warnings nobody acted on, and the people who were paid enormously to look away. Ponzi schemes, fake technology, a trillion dollars that vanished in 36 minutes, and the fine print that quietly took your right to sue.

Watch in order - each film explains the machinery the next one runs on.
```

| pos | video id | title | views | why here | end-screen slot 1 |
|---|---|---|---|---|---|
| 1 | `sphERPA4gAc` | He warned regulators about Madoff for nearly t | 57 | APV 19.13% at 57 views | `vikfOBHullI` |
| 2 | `vikfOBHullI` | There Was No Coin: $4 Billion in Empty Promise | 26 | 26 views; same 'money was never there' premise | `LXFjJqE6vKU` |
| 3 | `LXFjJqE6vKU` | Behind the $9 billion promise was a machine th | 0 | 0 views - strongest premise in the cluster, needs the playlist's traffic | `mj9qEKPRatE` |
| 4 | `mj9qEKPRatE` | One banker was paid $550 million in a single y | 18 | APV 21.14%, 350s AVD - pivot from fraud to legal power | `j8U8c4BB_GQ` |
| 5 | `j8U8c4BB_GQ` | He sold a side door into America's best univer | 7 | buying access | `5Jap-0h43A4` |
| 6 | `5Jap-0h43A4` | The Day $1 Trillion Vanished in 36 Minutes | 11 | machinery, not people | `1pox44KsaV8` |
| 7 | `1pox44KsaV8` | The Fine Print That Quietly Took Your Right to | 5 | the power that reaches the viewer directly | `waA4XJ9bYcE` |
| 8 | `waA4XJ9bYcE` | The Hidden Code Door Behind the $8 Billion FTX | 5 | APV 4.24% - placed late | `rYV4rxtQCV0` |
| 9 | `rYV4rxtQCV0` | A billionaire heard his own voice on an FBI ta | 10 | APV 3.64% - weakest on channel, last | `sphERPA4gAc` |

### The System Got It Wrong

- action: **create_new**
- items: 8
- entry point: **He called safety pure waste and dove anyway** (`marQjsCagh0`)
  - why: 158 views at 22.77% APV with 495s average view duration - the deepest-watched film on the channel.

```
Eight cases the system never answered for: men who spent decades in prison for crimes they did not commit, a judge who was paid by the jail he sent children to, evidence that stayed buried, and disappearances still open after fifty years.

Watch in order - the wrongful convictions first, then the cases nobody ever closed.
```

| pos | video id | title | views | why here | end-screen slot 1 |
|---|---|---|---|---|---|
| 1 | `marQjsCagh0` | He called safety pure waste and dove anyway | 158 | 158 views, 495s AVD - deepest watch on the channel | `Qyad4FejCIc` |
| 2 | `Qyad4FejCIc` | Alabama kept a date to kill him for 30 years | 51 | 30 years on death row - strongest injustice premise | `5L_HCGJxX_U` |
| 3 | `5L_HCGJxX_U` | She memorized her attacker's face to be certai | 23 | APV 23.08%; eyewitness certainty | `tYZuE76Hwdc` |
| 4 | `tYZuE76Hwdc` | They Hid the Evidence That Proved Him Innocent | 12 | buried evidence - direct sequel to Cotton | `Pmh6h5SfWw4` |
| 5 | `Pmh6h5SfWw4` | A Judge Took $2.8 Million to Send Kids to Pris | 6 | pivot from error to corruption | `tt7U1XgjCU4` |
| 6 | `tt7U1XgjCU4` | Fifty years later the FBI still cannot name hi | 56 | 56 views, APV 19.41% - pivot to unclosed cases | `1h267U6PY0I` |
| 7 | `1h267U6PY0I` | Two men dressed as police emptied a Boston mus | 12 | APV 24.09%, 396s AVD | `FTm1icKgycU` |
| 8 | `FTm1icKgycU` | The website he took from never wanted him char | 23 | APV 3.97% - weakest, last | `marQjsCagh0` |

## Exact API call sequence (not executed)

| # | playlist | operation | method | quota | reversible |
|---|---|---|---|---|---|
| 1 | police_power | `playlists.update` | PUT | 50 | yes - re-PUT the previous title/description, capture |
| 2 | police_power | `playlistItems.delete` | DELETE | 50 | no - the item cannot be restored, but it points at a |
| 3 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 4 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 5 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 6 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 7 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 8 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 9 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 10 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 11 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 12 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 13 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 14 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 15 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 16 | police_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 17 | police_power | `playlistItems.update` | PUT | 50 | yes - re-PUT position 2 |
| 18 | police_power | `playlistItems.update` | PUT | 50 | yes - re-PUT position 4 |
| 19 | police_power | `playlistItems.update` | PUT | 50 | yes - re-PUT position 1 |
| 20 | forfeiture_files | `playlists.insert` | POST | 50 | yes - playlists.delete removes it; no viewer-visible |
| 21 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 22 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 23 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 24 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 25 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 26 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 27 | forfeiture_files | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 28 | fraud_finance_power | `playlists.update` | PUT | 50 | yes - re-PUT the previous title/description, capture |
| 29 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 30 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 31 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 32 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 33 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 34 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 35 | fraud_finance_power | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 36 | fraud_finance_power | `playlistItems.update` | PUT | 50 | yes - re-PUT position 1 |
| 37 | fraud_finance_power | `playlistItems.update` | PUT | 50 | yes - re-PUT position 0 |
| 38 | system_got_it_wrong | `playlists.insert` | POST | 50 | yes - playlists.delete removes it; no viewer-visible |
| 39 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 40 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 41 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 42 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 43 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 44 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 45 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |
| 46 | system_got_it_wrong | `playlistItems.insert` | POST | 50 | yes - playlistItems.delete |

Full request bodies are in `episodes/_planning/measurements/PLAYLIST_PLAN.v001.json`.

## Rollback

- `playlists.insert` -> `playlists.delete` on the returned id. A playlist that never appeared in a description has no inbound links to strand.
- `playlists.update` -> re-PUT the `was_title` / `was_description` captured in the plan JSON for every update call.
- `playlistItems.insert` -> `playlistItems.delete`.
- `playlistItems.update` -> re-PUT the `was_position` captured in the plan JSON.
- `playlistItems.delete` of the dead item is not reversible, and does not need to be: it points at a video that no longer exists.

## To execute (owner only)

```
python scripts/plan_series_playlists.py \
    --execute \
    --owner-approval APR-XXXX \
    --confirm "I APPROVE THE PLAYLIST WRITES"
```

All three flags are required. Without them the script re-prints this plan and exits 0.
