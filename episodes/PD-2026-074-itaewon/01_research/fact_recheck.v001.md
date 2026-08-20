# PD-2026-074-itaewon — Pre-Publish Fact Re-Verification Packet (v001)

- **Episode:** PD-2026-074-itaewon — the Itaewon crowd crush, Seoul, 29 October 2022 (30 min)
- **Risk class:** **R3** — **159 real deaths**, most of them people in their twenties; 26 of them
  foreign nationals from 14 countries whose families were in Seoul as recently as October 2025;
  bereaved families who are alive and politically active in 2026; **a criminal record that is still
  moving**, with one first-instance conviction, several first-instance acquittals, a prosecution
  appeal, a joint police-prosecution re-investigation ordered in July 2025 and a statutory commission
  extended to December 2027.
- **Produced by:** Claude (Opus 5, Claude Code), 2026-08-21, by live retrieval
- **Binds to:** `episodes/_planning/EP74_itaewon_script.en.v004.md`,
  `EP74_itaewon_FACTS_LEDGER.v001/.v002/.v003.md`,
  `episodes/PD-2026-074-itaewon/episode_spec.v001.json`
- **Status:** **NOT CLEARED FOR PUBLISH, AND NOT CLEARED TO RENDER.** Four items in §2 must be
  resolved before a frame is rendered; six more before upload.

> This packet is the *preparation* for the R3 pre-publish gate, not the gate. A final re-check on the
> day of publish is still required, and §5 is what that day's check has to cover.

---

## 1. What was actually read, and what was not

**Read in full, this session, by live fetch:** the Framework Act on the Management of Disasters and
Safety **Article 66-11** and its **Enforcement Decree Article 73-9** on `law.go.kr` (the statute
itself); the PLOS ONE study *Unraveling the causes of the Seoul Halloween crowd-crush disaster*
(peer-reviewed, 12 July 2024); the Seoul Metropolitan Government's own page on the intelligent
disaster safety system; Korea Times reporting of the first-instance judgment, the illegal terrace,
the October 2025 joint audit, the March 2026 hearing and the foreign victims' families; the Korea
Herald on foreseeability and on the stalled legislation; Al Jazeera on the emergency calls and the
deployment; SCMP on the call transcripts; Reuters on the 2025 re-investigation and apology;
Korea JoongAng Daily on Itaewon three years later; 노컷뉴스 and 법률신문 on the per-defendant
outcomes; MBC on the prosecution appeal; AFP via Gulf News on the Kim Kwang-ho acquittal;
Seoul Economic Daily on the 2026 commission activity; the Constitutional Court impeachment ruling as
reported by the Korea Times.

**NOT read, and the film says so (AB-07):**

| not read | consequence |
|---|---|
| **Any court judgment text**, in Korean or English | Every judgment row is the *reporting* of a judgment. Where a court is quoted, the outlet that printed the quotation is named in the narration, out loud |
| **The Korean special-investigation file and the National Assembly hearing record** | The film describes what the commission *did* — resolutions, referrals, an extension — and never characterises what the record *contains* |
| **The Washington Post's November 2022 investigation** | HTTP 403. Its analysis of 350+ videos and its findings on rescue delay are **not in the ledger and may not be narrated** (AB-09). The thirteen minutes are carried by the PLOS ONE timeline alone |
| **Any survivor or bereaved-family account** | The film contains none. Deliberate, and it is why ⛔-01 is stated as a production rule rather than left implicit |
| **The forensic study behind the July 2026 "160" figure** | Only its English summary was read, which is exactly why the film does not use that number (⛔-03) |

---

## 2. Items that must be resolved BEFORE the render

| # | item | why it cannot wait |
|---|---|---|
| **R1** | **`AB-02` — the appellate outcome.** The Seoul High Court judgment for Lee Im-jae and co-defendants was reported in May 2025 as expected around **27 October 2025**. It could not be retrieved on 2026-08-21 in English or Korean. | ACT_5 is built on first-instance outcomes and says out loud that the appeal is outside what the film can verify. **If the judgment exists, that passage is false by omission and ACT_5 is rewritten** — which means the narration master, the captions and the scene plan are all thrown away. Resolve first, render second |
| **R2** | **`IT-58` and `IT-74` are still `UNREAD`.** The Seoul Metro passenger figures (81,573 that day against ~23,800 a week earlier) and the Constitutional Court's reported "many factors, not a specific one" line. | Both are strong and **both are deliberately absent from the script**. If either is fetched and confirmed it earns a place; if not, the script is already correct. Either way this must be decided before the words are spoken, not after |
| **R3** | **The official toll on the day of the render.** The film says **159** everywhere and refuses **160** (⛔-03). | If the Ministry of the Interior and Safety revises the official figure, every occurrence changes — narration, captions, title, thumbnail, description. Cheap to check, catastrophic to miss |
| **R4** | **`check_packaging_claims.py` on the chosen title and thumbnail.** | The script speaks every figure in words and the leading title candidate uses numerals — the documented `UNVERIFIED` false-positive mode. The fix is a title change or a narration line, **never a weakened check** |

## 3. Items to re-check before upload

| # | item | current position |
|---|---|---|
| U1 | Legal status of every named person, re-stated as at the upload date | Lee Im-jae — sentenced at first instance 30 Sep 2024, appealed. Park Hee-young — acquitted at first instance the same day, appealed, and referred by the commission for fresh investigation in May 2026. Kim Kwang-ho — acquitted 17 Oct 2024. Song Byung-ju and a 112 team leader — sentenced at first instance the same day. Lee Sang-min — impeachment rejected unanimously 25 Jul 2023, reinstated. **Every one of these is in the same sentence as the person's name in the script; verify each is still true** |
| U2 | The commission's mandate | Extended in June 2026 to December 2027. Confirm it was not extended again, curtailed, or superseded |
| U3 | The penalty bill (`IT-82`) | Proposed 29 April 2026. **Confirm it is still a bill.** If it passed, the film's last beat changes from "was still a bill" to something else |
| U4 | Article 66-11 and Decree 73-9 | Confirm no further amendment since 26 Dec 2023 / 26 Mar 2024 |
| U5 | Description and on-screen text | Every claim in the description is a claim. Re-run `check_packaging_claims.py` against the final text |
| U6 | Plate verdicts | `runs/qc/itaewon_plate_verdicts.v001.json` complete, and **no rejected or unresolved plate in a cut** |

## 4. The numbers, and where each one is allowed to come from

| figure | value | source | may it be changed by a later edit? |
|---|---|---|---|
| deaths | **159** | official toll, carried by named reporting through March 2026 | Only by a ministry revision. **Never to 160** |
| injuries | 196 | SECONDARY (SRC-0016) | Weakest number in the film; cut it before defending it |
| emergency calls | **11**, 18:34 → 22:11 | Korea Times, March 2026 | No |
| calls attended | **4**; no action on **7** | Al Jazeera, Nov 2022 | No |
| officers | **137** | two named sources | No |
| rallies | **34** in 2021 → **921** May–Oct 2022 | joint government audit, Oct 2025 | No |
| alley | **~50 m long, ~5 m → 3.2 m wide** | Korea Times, building records | A second published account says 45 m; the film uses 50 and **never presents both** |
| gradient | — | **does not exist** (AB-01) | The film gives no figure, ever |
| density | 7.57 ped/m², max 9.95 | PLOS ONE, peer-reviewed | No |
| pressure | 1,063 N/m, max 1,961 | PLOS ONE | No |
| crowd | ~100,000 | Al Jazeera | Characterised as an estimate, always |
| foreign dead | **26 from 14 countries** | Korea Times, Oct 2025 | No |
| cameras | **909** across **71** areas | Seoul Metropolitan Government (PRIMARY) | No |

## 5. What the publish-day check has to cover

1. **R1 again.** An appellate judgment can appear at any time and this film's ACT_5 is the part that
   breaks when it does.
2. **U1 again, name by name.** A person acquitted at first instance who is convicted on appeal
   between render and publish turns a true sentence into a false one while the file sits on disk.
3. **The toll.** 159.
4. **Title, thumbnail text and description through `check_packaging_claims.py`**, against the final
   script, not against this packet.
5. **The contact sheet, opened by a person**, looking for a body, a real face, a generated glyph, or
   Japanese/Chinese/Western signage.
6. **`config/ship_policy.v001.json`'s four blocking classes**, read against the finished file:
   `real_person_likeness` is the live one here, and it is live in every frame that contains a crowd.

---

**Nothing in this packet lowers a threshold, and nothing in it is a self-certification.** Its whole
function is to name, in advance, the eleven things that would make a finished film wrong — so that
they are checked against the world rather than against the film's own confidence.
