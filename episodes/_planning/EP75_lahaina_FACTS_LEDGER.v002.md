# EP75 · LAHAINA — FACTS LEDGER v002

**Binding, together with `EP75_lahaina_FACTS_LEDGER.v001.md`.** v001 is not withdrawn: every row in
it stands except section 9, which this file supersedes. v002 adds what v001 could not carry, because
v001 was written before two things happened:

1. **`SRC-0009` (Phase One) has now been read.** v001 marked it `NOT YET READ` and AB-05 named it as
   the largest open hole in the record. It was retrieved and read on **2026-08-21** (how, below).
   Everything in section 11 of this file is from it, and it is the reason this film has an afternoon
   with a shape instead of a list of findings.
2. **Section 9 was re-verified on the day of writing, as ⛔-11 requires — and it had gone stale.**
   v001 said the first of four annual payments "was expected to begin flowing in July or August 2026."
   As of **2026-08-21 that has not happened and cannot happen**, because an appeal over attorneys'
   fees is pending before the Hawaiʻi Supreme Court. Section 10 below carries the corrected rows.
   **The v001 rows LH-101…LH-103 may not be narrated.**

**Grades are unchanged from v001** (`VERBATIM` / `OURS` / `SECONDARY` / `ABSENCE`), and the rule is
unchanged: a `SECONDARY` row may not carry a load-bearing beat. **The ⛔ quarantine in v001 governs
this file in full**, plus the four additions at the end of this one.

---

## How Phase One was read, so the next person can repeat it

`ag.hawaii.gov` returns 403 to WebFetch. The report is also deposited by UL Research Institutes on
figshare, which does not:

```
curl -sSL "https://api.figshare.com/v2/articles/28062371" -o fig.json     # -> download_url
curl -sSL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0" \
     "https://ndownloader.figshare.com/files/51306806" -o phase1.pdf      # 132 MB, 199 pages
py -3.11 p1_extract.py phase1.pdf phase1.txt      # pypdf 6.14.2, page-tagged
py -3.11 p1_decode.py  phase1.txt phase1_dec.txt  # see below
```

**The trap, and it is a real one.** Most of the body text is set in a font whose embedded encoding
makes pypdf return every character **shifted down by 29 code points**: `ACKNOWLEDGMENTS` comes out as
`$&.12:/('*0(176`, a space comes out as `\x03`, and — the dangerous part — **every digit comes out as
a control character**, so a naive extraction reads `"leading to  fatalities"` and `"at  p.m."`. A
reader who does not notice this concludes the report has no numbers in it. `p1_decode.py` shifts each
line back by 29 where the line is encoded, leaving the ~2,500 already-plain lines alone. Both scripts
are in this session's scratchpad; if they are gone, they are eight lines each and the shift is +29.

Quotations below were read in `phase1_dec.txt` and are cited by **PDF page number** (not the report's
printed page number, which runs about 8 ahead).

---

## 11. PHASE ONE — the day, as the state's own timeline records it

`SRC-0009` = *Lahaina Fire Comprehensive Timeline Report* (Phase One), FSRI for the Hawaiʻi Attorney
General, 17 April 2024, **read in full-text 2026-08-21**. Its own scope: "beginning at 14:55 (2:55
p.m. HST) on August 8, 2023, and concluding at 08:30 (8:30 a.m.) on August 9, 2023" (p. 9).
It states of itself: **"this report does not analyze causation"** (p. 9).

### 11.1 The week the forecast was right

| id | fact | grade | source |
|---|---|---|---|
| LH-200 | Hurricane Dora passed "approximately 500 miles offshore" and "created a pressure gradient that meteorologists warned would bring damaging winds, low humidity, and an elevated risk of wildfires to the island" | VERBATIM | SRC-0009 p.9 |
| LH-201 | On 1 August 2023 NWS predicted the arrival of increased trade wind speeds and dry air with Dora's passage, and mentioned "the possibility of Red Flag conditions by early the next week" | VERBATIM | SRC-0009 p.27 |
| LH-202 | On 3 August 2023 an NWS Area Forecast Discussion "specifically mentioned the possibility of severe fire weather development early in the coming week" | VERBATIM | SRC-0009 p.27 |
| LH-203 | A forecaster contacted fire contacts predicting strong dry winds the following Monday and Tuesday and warning that a Fire Weather Watch would be issued over the weekend. **"The forecaster recognized that this much notice of such a warning was rare."** | VERBATIM | SRC-0009 p.27 |
| LH-204 | Red Flag Warnings were issued for the leeward portions of the Hawaiian Islands at **03:33 on 6 August 2023**, and **"Lahaina and Kāʻanapali were specifically mentioned"** | VERBATIM | SRC-0009 p.27 |
| LH-205 | Early on 8 August 2023, between 03:00 and 09:30, NWS "reiterated its wind and Red Flag Warnings and predicted the development of wind gusts up to 60 mph" | VERBATIM | SRC-0009 p.28 |
| LH-206 | On 4 August 2023 the NWS Honolulu Field Office issued a weather warning notifying agencies including HI-EMA "about high winds and impending 'critical fire weather' conditions" | VERBATIM | SRC-0009 p.29 |

> **LH-205 retires half of AB-06.** The film may now say *"forecast gusts of up to sixty miles an
> hour,"* attributed to the National Weather Service and dated, because that is a primary row. It may
> still **not** say what the wind actually did — no measured wind speed is a row in this ledger.

### 11.2 What was staffed, and what was not

| id | fact | grade | source |
|---|---|---|---|
| LH-210 | MEMA **partially activated** the Maui EOC on **7 August 2023 at 21:00** "for the wind warning and to monitor any associated incidents" (WebEOC entry, 21:33, MEMA Director). Two people staffed it | VERBATIM | SRC-0009 pp.29,131 |
| LH-211 | "The partial activation extended to August 8, 2023, at 16:30 when it was fully activated." As per the EOC Communications Test Log, **the EOC was fully activated at 16:30 on 8 August 2023** | VERBATIM | SRC-0009 pp.29,131 |
| LH-212 | On and before 8 August 2023, MEMA full-strength staffing "consisted of an Administrator and eight full time direct reports." On 7 August two of them were unavailable for EOC staffing | VERBATIM | SRC-0009 p.29 |
| LH-213 | MPD "had staffing levels that were consistent with normal day-to-day operations. No additional personnel were added to the patrol shifts on August 7, 2023." Holding the graveyard shift over on the morning of 8 August "increased the staffing level in Lahaina Town to a total of **13 officers**" | VERBATIM | SRC-0009 p.109 |
| LH-214 | HI-EMA's State Warning Point in Honolulu is staffed 24/7/365 "with a minimum of two (2) personnel." The State EOC "is typically unstaffed unless an impending or ongoing disaster situation creates a need"; it went to partial activation only in the overnight hours between 8 and 9 August, and to full activation "during the early morning hours of August 9, 2023" | VERBATIM | SRC-0009 pp.28,29 |

### 11.3 The morning fire, and the thirty-eight minutes

| id | fact | grade | source |
|---|---|---|---|
| LH-220 | Phase One's points of reference: **"Lahaina AM fire: Fire occurring August 8, 2023, between 06:34 and 14:17"** and **"Lahaina PM fire (Kuʻialua fire): Fire occurring August 8-9, 2023, between 14:55 and 06:00 HST"** | VERBATIM | SRC-0009 p.26 |
| LH-221 | Of the morning fire: firefighters "responded to the scene, employing private bulldozers and water tankers to construct perimeter lines and soak the fire area with water. **They later reported that the fire was extinguished and returned to quarters at 14:17 (2:17 p.m.)**" | VERBATIM | SRC-0009 p.9 |
| LH-222 | The afternoon fire, "later named the 'Kuʻialua fire,' was reported **at the same location as the earlier fire**" | VERBATIM | SRC-0009 p.9 |
| LH-223 | Four fires burned on Maui across 8–9 August 2023: **Olinda, started 00:22**; **Lahaina AM, 06:35**; **Kula, 11:27**; and the Pūlehu-Kīhei fire, which "eventually burned over 3,000 acres and required many days to contain." "During the Lahaina PM fire, emergency responders were engaged with multiple fires and continued to respond to new incidents across the island" | VERBATIM | SRC-0009 pp.26,27 |
| LH-224 | At 07:51 on the morning fire, the relieving engine officer "walked the burned area and saw where fire had come through," and "noted that power lines had already come down along the gulch … and the standing lines were swaying in the wind" | VERBATIM | SRC-0009 p.56 |

> **LH-220 + LH-221 + LH-222 are the film's hinge and must always travel together with LH-12, LH-13
> and LH-15 from v001.** The permitted form is: the crews reported it out and left at 14:17; it was
> reported again at 14:55, at the same place; the County has said its firefighters "went above and
> beyond their due diligence" (LH-15); and Phase Two Finding 67 says the mopup they performed was the
> mopup "proven successful under typical weather conditions" and "appears to have been insufficient"
> under the conditions of that day (LH-85). **The film never says they failed to put it out. It says
> what the record says, in that order, and stops.**

### 11.4 The afternoon, minute by minute

All from `SRC-0009` §4.3.1, pp.35–36, and read there.

| id | fact | grade | source |
|---|---|---|---|
| LH-230 | **14:55** — the fire is dispatched near Kuʻialua Street "after numerous callers to 911 identified that there was a fast-[moving fire]" | VERBATIM | SRC-0009 p.35 |
| LH-231 | **14:57** — Engine 11 advised they could see smoke | VERBATIM | SRC-0009 p.35 |
| LH-232 | **15:00** — Engine 11 arrived on scene and reported the fire "was approximately **20 x 100 feet**, moving rapidly makai (toward the ocean)" | VERBATIM | SRC-0009 p.35 |
| LH-233 | **15:05** — the first structure fire, a shed, confirmed by police officers arriving at it | VERBATIM | SRC-0009 p.35 |
| LH-234 | **15:21** — "Embers carried by the wind caused the fire to spot toward the bypass and over the bypass westward into the culvert" | VERBATIM | SRC-0009 p.35 |
| LH-235 | **15:23** — MFD command advised the fire "had been spotted over Lahainaluna Road and was in the Kelawea Mauka Makai Park and noted that there was very poor visibility due to the amount of smoke" | VERBATIM | SRC-0009 p.35 |
| LH-236 | **15:28** — Ladder 3 advised there was a structure on fire south of Lahainaluna Road | VERBATIM | SRC-0009 p.35 |
| LH-237 | **15:30** — "numerous vehicles caught on fire in the area of the Lahaina Bypass, and embers were exposing all of the homes west (makai) and south of Kelawea Park" | VERBATIM | SRC-0009 p.35 |
| LH-238 | **15:37** — MFD Command, on the radio, verbatim: **"There is one house on Lahainaluna that is fully going now. We need to stop it where you are. That has to be the cutoff there, that road back there."** Engine 3 replies that it might be multiple houses; Command: "Yeah, there are multiple structures going." | VERBATIM QUOTE | SRC-0009 p.35 |
| LH-239 | **15:43** — an MPD officer advised the smoke was getting "pretty bad" at Lahainaluna and Hwy-30 | VERBATIM QUOTE | SRC-0009 p.36 |
| LH-240 | **16:11** — Command: "We need to shut power down." Central: "MECO confirming power is shut off." The request was made "due to multiple downed utility poles and wires down" | VERBATIM QUOTE | SRC-0009 p.105 |
| LH-241 | The mechanisms of spread, in the report's own words: "direct flame contact, radiant heat, and embers," with embers "generated by burning fuels and transported by wind, causing ignitions beyond the fire perimeter" and able to "enter the building through vents, windows, and/or openings caused by wind damage that may ignite the structure and cause it to burn from the inside out" | VERBATIM | SRC-0009 p.33 |
| LH-242 | "The fire quickly spread across Honoapiʻilani Highway (Hwy-30) and all the way to the ocean's edge" | VERBATIM | SRC-0009 p.10 |

### 11.5 The warning that was sent, and the network it was sent over

**This is the film's spine and every row here is primary.**

| id | fact | grade | source |
|---|---|---|---|
| LH-250 | **"High winds crippled the communications infrastructure, destroying cellular phone communication within the Lahaina region in the late morning of August 8, 2023."** | VERBATIM | SRC-0009 p.109 |
| LH-251 | **"With no cellular communication, residents and tourists were not able to receive emergency alerts, communicate with loved ones, and/or to receive incoming or outgoing calls/texts."** | VERBATIM | SRC-0009 p.109 |
| LH-252 | "The MPD no longer had cellular communication capabilities and had to rely solely on their portable and car radio systems while working in the Lahaina area" | VERBATIM | SRC-0009 p.109 |
| LH-253 | Most households "no longer utilize traditional landline telephones," and the report states it is "unknown if landlines were operable when Lahaina suffered power outages" | VERBATIM | SRC-0009 p.109 |
| LH-254 | MEMA's Wireless Emergency Alert log for 8 August 2023 records evacuation orders at **04:09** (Kula 200 subdivision), **05:00** (Hoʻopalua Drive, Kula), **05:21** (Hanamu Road and Kealaloa Avenue near Makawao) and **16:04** (Kulalani Subdivision, Kula) | VERBATIM | SRC-0009 pp.132–133 |
| LH-255 | **The first Wireless Emergency Alert in that log naming a Lahaina subdivision was sent at 16:16 on 8 August 2023**, for Kelawea Mauka: "Maui Emergency Management Agency has issued an evacuation order on Maui Island for Kelawea Mauka Subdivision due to a brushfire… Evacuate your family and pets now, do not delay. Shelter is open at Lahaina Civic Center." | VERBATIM | SRC-0009 p.133 |
| LH-256 | The next Lahaina entry in the same log is **20:46**, for Wahikuli — "Evacuate North out of town toward Kapalua" — and then **01:26 on 9 August**, for Kualapa Loop | VERBATIM | SRC-0009 p.133 |
| LH-257 | At 13:13 on 8 August the Red Cross shelter manager reported the Lahaina Recreation Center shelter had no clients: "Shelter population now zero." At 14:00, "Lahaina Civic Center shelter closed." | VERBATIM | SRC-0009 p.132 |
| LH-258 | At 12:50 on 8 August a Maui County command-centre entry records "Network issues Lahaina Locations: Senior Center, Fire Station" | VERBATIM | SRC-0009 p.132 |

> **How LH-255 may be used, and how it may not.** It is a fact about a **log**: the first WEA in
> MEMA's own public-alert table naming a Lahaina subdivision carries the timestamp 16:16. It is **not**
> a finding that nothing else was sent, and the County's own position (LH-37) is that it sent at least
> 14 alert messages. The permitted form is: *the first evacuation order in MEMA's alert log that names
> a Lahaina neighbourhood is timestamped 16:16 — an hour and twenty-one minutes after the fire was
> reported, and hours after cellular communication in the Lahaina region had been destroyed.* Attribute
> the log. Do not convert it into "no one was warned until 16:16."

### 11.6 The roads

| id | fact | grade | source |
|---|---|---|---|
| LH-260 | "Trees toppled, utility poles fell, and power lines were downed, **blocking critical roadways and making evacuation challenging**" — in the early morning of 8 August, before the fire | VERBATIM | SRC-0009 p.9 |
| LH-261 | MPD's traffic-control table records, at **05:40 on 8 August**, downed utility poles and power lines at Keawe Street and the northbound lanes of Hwy-30: "Impeded northbound traffic… Limited access to the Bypass. Caused major traffic congestion. Limited evacuation from south to north" | VERBATIM | SRC-0009 p.112 |
| LH-262 | The conflagration "overwhelmed the town's limited evacuation routes, some of which were blocked by downed utility poles and electrical lines" | VERBATIM | SRC-0009 p.9 |
| LH-263 | **~16:45** — an officer found an access dirt road blocked by a locked metal gate in the Kelawea residential community. "The officer stated there were about **30–50 cars trapped by the gate and unable to flee the area**. The officer got help from a resident who responded with a reciprocating saw to cut the lock." A nearby chain-link gate was pulled open with a tow strap. One side opened; a motorist stopped, unsure of the clearance; "The officer noticed the structures next to the line of cars were now fully engulfed, so **he ran toward the gate and rammed his body into the cyclone gate to open the other side**." "The officer indicated 30–50 fully loaded cars passed through the gate to safety" | VERBATIM | SRC-0009 p.117 |
| LH-264 | At approximately **19:04**, Shaw Street became impassable due to fire. "With Papalaua Street already blocked off from the fire and now Shaw Street being blocked off from the fire, **the potential evacuation exit routes from Front Street in Lahaina Town were reduced from eight (8) to six (6)**" | VERBATIM | SRC-0009 p.118 |
| LH-265 | At approximately 16:38 a sergeant directed egress traffic to the Bypass via Kai Hele Kū Street, "the southernmost street of Lahaina," which "allowed officers to evacuate residents to the south and safely out of Lahaina Town" | VERBATIM | SRC-0009 p.117 |
| LH-266 | Fire apparatus were trapped or unable to move "due to obstructions — and had to be abandoned, further hampering efforts to combat the growing blaze." "**One (1) firefighter rescued seven (7) colleagues, including an unconscious officer who required urgent medical attention.** Numerous firefighters administered emergency care to the officer" | VERBATIM | SRC-0009 p.10 |
| LH-267 | A wildland unit "became trapped by a downed utility pole and was tangled in wires"; a tanker's windows "would not roll up, which exposed the driver to heavy smoke and flying embers during the course of the day" | VERBATIM | SRC-0009 p.54 |
| LH-268 | A ladder-company crew, driving out, "were surprised to encounter numerous structures that had burned to the ground on both sides of the street." The operator "lived on Komo Mai Street, and he saw that his home was completely destroyed." At the bottom of the street the road was blocked, and the crew "had to use a rotary saw (K12) to cut a street sign and a tree in order to egress out of the neighborhood" | VERBATIM | SRC-0009 p.63 |
| LH-269 | An engine officer, driving out through blocked streets, went "around the traffic by driving over a concrete barrier, over downed power lines, over a short rock wall, through debris, and through the yard of the HECO substation to make it to Hwy-30," and "made several attempts to call a mayday via radio but was unsure if transmissions were being received" | VERBATIM | SRC-0009 p.80 |
| LH-270 | At 23:24 an engine crew "recalled driving through the neighborhood with sirens and knocking on doors" — vehicle sirens, in Wahikuli, eight and a half hours after the fire was reported | VERBATIM | SRC-0009 p.81 |

### 11.7 The water, as the timeline saw it

| id | fact | grade | source |
|---|---|---|---|
| LH-280 | "As homes and other buildings burned, the water pipes failed and water flowed unrestricted. **Pressure in the water mains dropped to the point that there was no water coming from fire hydrants in some parts of Lahaina**" | VERBATIM | SRC-0009 p.10 |
| LH-281 | A relief engine "tried to refill their tank while there but the hydrant was only producing 'a trickle'" | VERBATIM QUOTE | SRC-0009 p.72 |
| LH-282 | At 05:02 on 9 August a utility unit "advised that hydrants around the Civic Center and fire station were dry" | VERBATIM | SRC-0009 p.103 |
| LH-283 | An engine crew "was able to refill tanks at Canoe Beach, since it still had good water pressure" | VERBATIM | SRC-0009 p.81 |

> LH-280…LH-283 are the picture of Finding 24 and Finding 26 (LH-41, LH-42). They do **not** modify
> Finding 21 (LH-40): both water systems had uninterrupted power and produced at capacity throughout.
> ⛔-08 is unchanged and absolute.

### 11.8 The record of the day is itself incomplete

**This is a finding about the record, and it is the strongest thing in Phase One that nobody quotes.**

| id | fact | grade | source |
|---|---|---|---|
| LH-290 | **"There is no data showing which MEMA personnel responded on August 8, 2023. The only missing EOC sign-in sheet is the one for MEMA personnel for August 8, 2023. Maui County has not produced this document after multiple requests."** | VERBATIM | SRC-0009 p.131 |
| LH-291 | MEMA Activity Logs (ICS 214 forms) "create an understanding of the event response minute-by-minute and hour-by-hour… **There were no ICS 214 Forms received from MEMA personnel for these dates**" | VERBATIM | SRC-0009 p.131 |
| LH-292 | **"Because of missing data, it is difficult to make a complete and accurate accounting of activities within the EOC from August 7, 2023, through August 9, 2023."** | VERBATIM | SRC-0009 p.131 |
| LH-293 | "Even though MEMA encourages strict compliance, it is apparent that people entered the EOC without following the sign-in/out process" | VERBATIM | SRC-0009 p.131 |
| LH-294 | The investigation issued subpoenas. One of them, served on the Maui Emergency Management Agency, asked for "**All maintenance and testing logs for the statewide alert and warning siren system in Maui County**" — served 20 October 2023, answered 13 December 2023 | VERBATIM | SRC-0009 p.147 |
| LH-295 | Another subpoena sought records of "how the storage and distribution system was brought back online assuming a loss of pressure during the fire event." The response: "As of December 13, 2023, Maui Dept. of Corp Counsel confirmed **no further responsive record exists**" | VERBATIM | SRC-0009 p.147 |

> **⛔-14 (new).** LH-290…LH-292 are a fact about **documents**, not about people. The permitted form is
> that the sign-in sheet for that agency for that day was not produced, that no activity logs were
> received from its personnel, and that the report says the consequence in its own words. **No motive,
> no implication of concealment, no rhetorical question.** The film states it and moves on. Reaching
> for a reason here is exactly the move ⛔-04 forbids.

---

## 10 (revised). AFTER — re-verified 2026-08-21, the day of writing

**These rows replace v001's LH-100…LH-104.** Retrieved 2026-08-21 by live fetch.

| id | fact | grade | source |
|---|---|---|---|
| LH-110 | The death toll was first reported as high as 115, revised down to 97 on 15 September 2023 after DNA analysis, and the Honolulu Medical Examiner confirmed the 102nd death in June 2024. **The figure the film uses is the County's own, from its 3 October 2024 release: "at least 102 lives" (LH-19)** | SECONDARY | SRC-0008 |
| LH-111 | The $4.037 billion global settlement was announced in August 2024 and resolves roughly 450 lawsuits arising from the Lahaina and Upcountry fires | SECONDARY | SRC-0012 |
| LH-112 | On **13 February 2026** the Hawaiʻi Supreme Court ruled unanimously that insurers may not intervene in the settlement, holding that "economic interests alone do not confer intervention rights." At the time, counsel noted that some carriers had "continued to file two other appeals currently pending before state appellate courts" | SECONDARY | SRC-0012 |
| LH-113 | As of mid-April 2026, **nearly 22,000 claimants had filed more than 94,000 claims**; the Star-Advertiser reported the figures on 16 August 2026 as **94,816 claims by 21,750 claimants** | SECONDARY | SRC-0013 |
| LH-114 | Settlement administrators sent the first round of award determination notices on 17 June 2026. A notice is an offer, not a payment | SECONDARY | SRC-0008 |
| LH-115 | **As of 16 August 2026 no settlement payment has been made.** Three attorneys and one fire survivor are challenging a state judge's ruling on attorneys' fees; the case was filed on 2 July 2026 with Hawaiʻi's Intermediate Court of Appeals and elevated to the Hawaiʻi Supreme Court on 5 August 2026. **"While the appeal is pending, no settlement payments can be made."** About **$1.1 billion** is held for the first of four annual instalments | SECONDARY | SRC-0013 |
| LH-116 | Counsel for claimants said she anticipated a Supreme Court ruling as soon as September 2026, which could allow payments to begin by October 2026 | SECONDARY | SRC-0013 |
| LH-117 | As of the publication date of the Phase Two report, MEMA "has implemented a process for activating sirens for wildfires" (LH-31) | VERBATIM | SRC-0001 |

**New sources for this section**

| id | source | how it was read |
|---|---|---|
| SRC-0012 | *Maui Now*, "High court clears path for $4 billion wildfire settlement payments," 13 February 2026 | fetched and read 2026-08-21 |
| SRC-0013 | *Honolulu Star-Advertiser*, "Maui wildfire settlement payments delayed again," 16 August 2026 | fetched and read 2026-08-21 |

> **⛔-11 is not discharged by this file.** It is discharged for **2026-08-21 only**. The Hawaiʻi
> Supreme Court may rule between now and the publish date, and LH-115/LH-116 will be wrong the day it
> does. **Re-verify section 10 again before the packaging is written and again before the video is
> scheduled**, and if the film has already stated a status, state it with its date attached — "as of
> August 2026" — so that it ages into a true sentence instead of a false one.
>
> **⛔-15 (new).** Never say victims "have not been paid" as an accusation, and never name or
> characterise the appellants. The permitted form is the procedural one: notices went out in June, an
> appeal over fees is pending, and while it is pending no payment can be made. That is the whole of it.

---

## AB — absences, revised

| id | absence |
|---|---|
| AB-05 **(revised)** | **Phase One has now been read** (this file). Still **NOT READ**: Phase Three, the Forward-Looking Report of 14 January 2025 (`SRC-0010`), and the full MFD/ATF Origin and Cause Report (`SRC-0011`) — only the County's release of it. Also not read: the online 12,000-line composite timeline dataset, which Phase One points to and which this ledger does not need |
| AB-06 **(revised)** | The film still has **no** primary-source figure for acreage or for structures destroyed, and **no measured wind speed** — LH-205 is a *forecast* of gusts up to 60 mph, attributed to NWS and dated, and it may be spoken only in that form. Evacuation timing is now partly sourced (LH-254…LH-256, LH-263…LH-265) and those rows may be used exactly as written |
| AB-08 **(new)** | Phase One says of itself, "this report does not analyze causation" (SRC-0009 p.9). Nothing in section 11 may be used to assert a cause. Causation in this film comes only from the MFD/ATF release (LH-11, LH-14, LH-16) and from Phase Two's findings |
| AB-09 **(new)** | **Why no siren appears in Phase One's narrative.** Searching the full text for "siren" returns three hits, and none of them is the outdoor warning network: two are fire-apparatus sirens (LH-267, LH-270) and one is the subpoena for the network's maintenance logs (LH-294). **This is an absence, not a finding**, and the film may not present it as one. What the film says about the sirens comes from Phase Two's Findings 37 and 38 (LH-30, LH-31) and from HI-EMA's own page (LH-01…LH-04) |

---

## ⛔ ADDITIONS TO THE QUARANTINE

v001's ⛔-01 … ⛔-13 are unchanged and binding. These are added:

| id | rule |
|---|---|
| ⛔-14 | **The missing EOC records (LH-290…LH-292) are stated as a fact about documents and nothing else.** No motive, no concealment, no rhetorical question, no pause for the viewer to fill in. State it, source it, move on |
| ⛔-15 | **The settlement is described procedurally and with its date.** Never "victims still have not been paid" as an accusation; never name or characterise the appellants; never predict when payment will come |
| ⛔-16 | **The 38 minutes between 14:17 and 14:55 (LH-220, LH-221) is never spoken as an accusation.** It travels with LH-15 (the County's statement about its firefighters' diligence) and LH-85 (Finding 67 on mopup) in the same passage, and the film never states or implies that the crews left too early |
| ⛔-17 | **No person in section 11 is named in the film.** Phase One names dispatchers, duty officers, EOC staff, an operator whose house burned, an officer who broke a gate open. **They appear in the film as roles, never as names**, and never with fault attached. The one exception the record already makes for itself — an officer's act at the gate (LH-263) — is narrated as an action, not as a biography |

---

## The one-sentence contradiction, restated with what Phase One added

> Hawaiʻi built the largest outdoor warning siren network in the world and tested it on the first
> business day of every month. On the day a town burned from the mountain side down, one siren inside
> the burn perimeter was operable, the network had never once been used to warn of a wildfire, and the
> first evacuation order in the county's alert log that names a Lahaina neighbourhood is timestamped
> 16:16 — sent to cellphones in a region whose cellular communication had been destroyed that morning.
