# END SCREENS - Studio work order v001

## Can this be scripted? No - verified, not assumed

- `videos.list?part=endScreens` -> HTTP **400** (`unknownPart`): END SCREENS ARE NOT READABLE OR WRITABLE VIA THE DATA API
- `videos.list?part=cards` -> HTTP **400** (`unknownPart`): CARDS ARE NOT READABLE OR WRITABLE VIA THE DATA API
- There is no `endScreens` or `cards` resource in the YouTube Data API v3 at any part name, and no write endpoint exists. End screens are settable only through YouTube Studio (web) or the YouTube Studio mobile app.
- Consequence: this is the one item on the distribution list that stays owner-manual no matter how much tooling is built.

## What to click, per video

1. Open the Studio link in the table.
2. **Editor -> End screen -> Apply to video** (or *+ Element* if one already exists).
3. Element 1 = **Video -> Specific video** -> paste the slot-1 id.
4. Element 2 = **Playlist** -> pick the slot-2 playlist.
5. Drag both elements so they start at the endcard and run to the end - the last 9s (YouTube requires each element to run at least 5s and to sit inside the final 20s; 9s satisfies both).
6. **Position**: the PD endcard fills only the middle third (logo, wordmark, subscribe line). Put element 1 in the LEFT third and element 2 in the RIGHT third - both areas are empty dark sky, so nothing gets covered.
7. **Save**.

Do the first video, then use **Apply template from video** on the rest and only swap element 1 - it turns a ~3-minute job into ~45 seconds per video.

- videos: **42**
- rough effort: **126 minutes** at 3 min each, less with the template shortcut
- ordering: highest views first. An end screen converts impressions the video already gets; putting the same 2 minutes into a video with 1 view returns roughly nothing.

## Priority order

| # | views | APV | video | slot 1 (specific video) | slot 2 (playlist) | window | Studio |
|---|---|---|---|---|---|---|---|
| 1 | 172 | 10.9% | Following the deposit rule is what mad (`Xc_PxdC_75c`) | They Took His Life Savings at th (`6ozsIfwqrP0`) | The Forfeiture Files: When t | 1147s - 1156s | [edit](https://studio.youtube.com/video/Xc_PxdC_75c/editor) |
| 2 | 159 | 15.0% | Police Can Stop and Frisk You Without  (`bYcqabvvxak`) | Police Took His Phone. Then They (`XWYWAgkExH4`) | Police Power: What They Can  | 673s - 682s | [edit](https://studio.youtube.com/video/bYcqabvvxak/editor) |
| 3 | 158 | 30.9% | He called safety pure waste and dove a (`marQjsCagh0`) | Alabama kept a date to kill him  (`Qyad4FejCIc`) | The System Got It Wrong | 2165s - 2174s | [edit](https://studio.youtube.com/video/marQjsCagh0/editor) |
| 4 | 57 | 20.5% | He warned regulators about Madoff for  (`sphERPA4gAc`) | There Was No Coin: $4 Billion in (`vikfOBHullI`) | Fraud, Finance & Power | 712s - 721s | [edit](https://studio.youtube.com/video/sphERPA4gAc/editor) |
| 5 | 56 | 27.9% | Fifty years later the FBI still cannot (`tt7U1XgjCU4`) | Two men dressed as police emptie (`1h267U6PY0I`) | The System Got It Wrong | 1773s - 1782s | [edit](https://studio.youtube.com/video/tt7U1XgjCU4/editor) |
| 6 | 51 | 25.1% | Alabama kept a date to kill him for 30 (`Qyad4FejCIc`) | She memorized her attacker's fac (`5L_HCGJxX_U`) | The System Got It Wrong | 689s - 698s | [edit](https://studio.youtube.com/video/Qyad4FejCIc/editor) |
| 7 | 46 | 21.8% | He showed the officer the receipt and  (`SOu4Y1NkGGY`) | Police Are Allowed to Lie to You (`X40EbUw5kzQ`) | Police Power: What They Can  | 543s - 552s | [edit](https://studio.youtube.com/video/SOu4Y1NkGGY/editor) |
| 8 | 46 | 32.6% | Police Can Search Your Car Without a W (`bXATF9ZnKLE`) | He Drove Home Honking. The Polic (`Sz8zPUoBANM`) | Police Power: What They Can  | 688s - 697s | [edit](https://studio.youtube.com/video/bXATF9ZnKLE/editor) |
| 9 | 43 | 18.7% | He Drove Home Honking. The Police Foll (`Sz8zPUoBANM`) | Police Can Stop and Frisk You Wi (`bYcqabvvxak`) | Police Power: What They Can  | 545s - 554s | [edit](https://studio.youtube.com/video/Sz8zPUoBANM/editor) |
| 10 | 26 | 15.3% | There Was No Coin: $4 Billion in Empty (`vikfOBHullI`) | Behind the $9 billion promise wa (`LXFjJqE6vKU`) | Fraud, Finance & Power | 1201s - 1210s | [edit](https://studio.youtube.com/video/vikfOBHullI/editor) |
| 11 | 23 | 21.4% | She memorized her attacker's face to b (`5L_HCGJxX_U`) | They Hid the Evidence That Prove (`tYZuE76Hwdc`) | The System Got It Wrong | 702s - 711s | [edit](https://studio.youtube.com/video/5L_HCGJxX_U/editor) |
| 12 | 23 | 4.0% | The website he took from never wanted  (`FTm1icKgycU`) | He called safety pure waste and  (`marQjsCagh0`) | The System Got It Wrong | 1734s - 1743s | [edit](https://studio.youtube.com/video/FTm1icKgycU/editor) |
| 13 | 19 | 16.8% | Police Took His $42,000 Car. The Supre (`m-uWzgWHGPg`) | Police Destroyed His Home Chasin (`4uuY6G0LmHo`) | The Forfeiture Files: When t | 711s - 720s | [edit](https://studio.youtube.com/video/m-uWzgWHGPg/editor) |
| 14 | 18 | 17.9% | One banker was paid $550 million in a  (`mj9qEKPRatE`) | He sold a side door into America (`j8U8c4BB_GQ`) | Fraud, Finance & Power | 1650s - 1659s | [edit](https://studio.youtube.com/video/mj9qEKPRatE/editor) |
| 15 | 18 | 23.9% | The phone in his pocket testified agai (`zE3nCUlUmLY`) | Can the Police Scan Your Home Fr (`rrftLmSVivk`) | Police Power: What They Can  | 670s - 679s | [edit](https://studio.youtube.com/video/zE3nCUlUmLY/editor) |
| 16 | 14 | 34.8% | The county sold her condo and kept the (`rU2vk9XL4vY`) | Their Son Was Charged. The City  (`YhEJHK279f8`) | The Forfeiture Files: When t | 1098s - 1107s | [edit](https://studio.youtube.com/video/rU2vk9XL4vY/editor) |
| 17 | 12 | 28.7% | They Hid the Evidence That Proved Him  (`tYZuE76Hwdc`) | A Judge Took $2.8 Million to Sen (`Pmh6h5SfWw4`) | The System Got It Wrong | 728s - 737s | [edit](https://studio.youtube.com/video/tYZuE76Hwdc/editor) |
| 18 | 12 | 20.3% | Two men dressed as police emptied a Bo (`1h267U6PY0I`) | The website he took from never w (`FTm1icKgycU`) | The System Got It Wrong | 1635s - 1644s | [edit](https://studio.youtube.com/video/1h267U6PY0I/editor) |
| 19 | 11 | 13.1% | The Day $1 Trillion Vanished in 36 Min (`5Jap-0h43A4`) | The Fine Print That Quietly Took (`1pox44KsaV8`) | Fraud, Finance & Power | 1327s - 1336s | [edit](https://studio.youtube.com/video/5Jap-0h43A4/editor) |
| 20 | 11 | 20.3% | The FBI taped a microphone to a phone  (`68oWZRiOnB8`) | The Police Broke In — So the Cou (`An0to4U0hJQ`) | Police Power: What They Can  | 623s - 632s | [edit](https://studio.youtube.com/video/68oWZRiOnB8/editor) |
| 21 | 11 | 39.0% | The Traffic Stop Was Over. Then the Do (`tpAKfHKuwqY`) | Police Can Search Your Car Witho (`bXATF9ZnKLE`) | Police Power: What They Can  | 639s - 648s | [edit](https://studio.youtube.com/video/tpAKfHKuwqY/editor) |
| 22 | 10 | - | A billionaire heard his own voice on a (`rYV4rxtQCV0`) | He warned regulators about Madof (`sphERPA4gAc`) | Fraud, Finance & Power | 1708s - 1717s | [edit](https://studio.youtube.com/video/rYV4rxtQCV0/editor) |
| 23 | 9 | - | Thirty hours in jail because an algori (`gR_nzXIyIlk`) | He showed the officer the receip (`SOu4Y1NkGGY`) | Police Power: What They Can  | 705s - 714s | [edit](https://studio.youtube.com/video/gR_nzXIyIlk/editor) |
| 24 | 8 | - | Police Took His Phone. Then They Opene (`XWYWAgkExH4`) | Police Can Force Your Thumb — Bu (`YQIhk2dKZHU`) | Police Power: What They Can  | 638s - 647s | [edit](https://studio.youtube.com/video/XWYWAgkExH4/editor) |
| 25 | 7 | - | He sold a side door into America's bes (`j8U8c4BB_GQ`) | The Day $1 Trillion Vanished in  (`5Jap-0h43A4`) | Fraud, Finance & Power | 1652s - 1661s | [edit](https://studio.youtube.com/video/j8U8c4BB_GQ/editor) |
| 26 | 7 | 11.0% | They Took His Life Savings at the Airp (`6ozsIfwqrP0`) | The county sold her condo and ke (`rU2vk9XL4vY`) | The Forfeiture Files: When t | 1141s - 1150s | [edit](https://studio.youtube.com/video/6ozsIfwqrP0/editor) |
| 27 | 6 | - | A Judge Took $2.8 Million to Send Kids (`Pmh6h5SfWw4`) | Fifty years later the FBI still  (`tt7U1XgjCU4`) | The System Got It Wrong | 555s - 564s | [edit](https://studio.youtube.com/video/Pmh6h5SfWw4/editor) |
| 28 | 5 | - | He Had No Lawyer. So He Wrote the Supr (`ch2hQ5jhDmQ`) | Can Your School Punish You for a (`cSfe3iGnBBM`) | Police Power: What They Can  | 692s - 701s | [edit](https://studio.youtube.com/video/ch2hQ5jhDmQ/editor) |
| 29 | 5 | - | Police Can Force Your Thumb — But Mayb (`YQIhk2dKZHU`) | The phone in his pocket testifie (`zE3nCUlUmLY`) | Police Power: What They Can  | 706s - 715s | [edit](https://studio.youtube.com/video/YQIhk2dKZHU/editor) |
| 30 | 5 | 9.6% | Police Raided the Wrong House and Hand (`Enok7A7wGBA`) | The Supreme Court Let Police Tak (`g5yFmDt48oU`) | Police Power: What They Can  | 724s - 733s | [edit](https://studio.youtube.com/video/Enok7A7wGBA/editor) |
| 31 | 5 | - | The Fine Print That Quietly Took Your  (`1pox44KsaV8`) | The Hidden Code Door Behind the  (`waA4XJ9bYcE`) | Fraud, Finance & Power | 712s - 721s | [edit](https://studio.youtube.com/video/1pox44KsaV8/editor) |
| 32 | 5 | - | The Hidden Code Door Behind the $8 Bil (`waA4XJ9bYcE`) | A billionaire heard his own voic (`rYV4rxtQCV0`) | Fraud, Finance & Power | 712s - 721s | [edit](https://studio.youtube.com/video/waA4XJ9bYcE/editor) |
| 33 | 5 | - | Their Son Was Charged. The City Came f (`YhEJHK279f8`) | Police Took His $42,000 Car. The (`m-uWzgWHGPg`) | The Forfeiture Files: When t | 698s - 707s | [edit](https://studio.youtube.com/video/YhEJHK279f8/editor) |
| 34 | 2 | - | Can Your School Punish You for a Post  (`cSfe3iGnBBM`) | The Traffic Stop Was Over. Then  (`tpAKfHKuwqY`) | Police Power: What They Can  | 712s - 721s | [edit](https://studio.youtube.com/video/cSfe3iGnBBM/editor) |
| 35 | 2 | - | Police Are Allowed to Lie to You Until (`X40EbUw5kzQ`) | Read Rights or It's Out / Mirand (`cQFql7tT1fE`) | Police Power: What They Can  | 728s - 737s | [edit](https://studio.youtube.com/video/X40EbUw5kzQ/editor) |
| 36 | 2 | - | Police Destroyed His Home Chasing a St (`4uuY6G0LmHo`) | Your Home for a Developer? The K (`89SQoRgAD7U`) | The Forfeiture Files: When t | 751s - 760s | [edit](https://studio.youtube.com/video/4uuY6G0LmHo/editor) |
| 37 | 2 | - | Read Rights or It's Out / Miranda v. A (`cQFql7tT1fE`) | He Had No Lawyer. So He Wrote th (`ch2hQ5jhDmQ`) | Police Power: What They Can  | 687s - 696s | [edit](https://studio.youtube.com/video/cQFql7tT1fE/editor) |
| 38 | 2 | - | The Police Broke In — So the Court Let (`An0to4U0hJQ`) | Police Raided the Wrong House an (`Enok7A7wGBA`) | Police Power: What They Can  | 711s - 720s | [edit](https://studio.youtube.com/video/An0to4U0hJQ/editor) |
| 39 | 2 | - | Your Home for a Developer? The Kelo Su (`89SQoRgAD7U`) | Following the deposit rule is wh (`Xc_PxdC_75c`) | The Forfeiture Files: When t | 632s - 641s | [edit](https://studio.youtube.com/video/89SQoRgAD7U/editor) |
| 40 | 1 | - | Can the Police Scan Your Home From the (`rrftLmSVivk`) | The FBI taped a microphone to a  (`68oWZRiOnB8`) | Police Power: What They Can  | 612s - 621s | [edit](https://studio.youtube.com/video/rrftLmSVivk/editor) |
| 41 | 1 | - | The Supreme Court Let Police Take Your (`g5yFmDt48oU`) | Thirty hours in jail because an  (`gR_nzXIyIlk`) | Police Power: What They Can  | 683s - 692s | [edit](https://studio.youtube.com/video/g5yFmDt48oU/editor) |
| 42 | 0 | - | Behind the $9 billion promise was a ma (`LXFjJqE6vKU`) | One banker was paid $550 million (`mj9qEKPRatE`) | Fraud, Finance & Power | 727s - 736s | [edit](https://studio.youtube.com/video/LXFjJqE6vKU/editor) |

## Why these targets

Slot 1 is always the next video in the same series playlist, and the last video in each playlist points back at position 1. That closes each cluster into a loop, which is the point: DEEP_RESEARCH_FINDINGS v001 section 5 found that 100% of measured suggested traffic arrives from other channels' videos, so the channel has no co-watch edges of its own. End screens and playlists are the only two mechanisms that create them.

## Rollback

End screens are removable in Studio (Editor -> End screen -> delete element) and removing one restores the previous state exactly. There is no viewer-facing record and no effect on the video file, its id, or its watch history.

## Prerequisite

Slot 2 needs the playlists to exist. Run the playlist plan first, or slot 2 can only offer the two playlists that exist today.
