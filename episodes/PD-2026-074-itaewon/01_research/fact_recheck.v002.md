# PD-2026-074-itaewon — Pre-Publish Fact Re-Verification Packet (v002)

**Supersedes v001.** v001's §2 listed four items that had to be resolved before a frame was rendered.
**Three of them are now resolved** and the fourth is unchanged. This file is the whole packet, not a
diff, because a pre-publish gate has to be readable on its own.

- **Episode:** PD-2026-074-itaewon — the Itaewon crowd crush, Seoul, 29 October 2022 (30:51)
- **Risk class:** **R3** — **159 real deaths**, most of them people in their twenties; 26 of them
  foreign nationals from 14 countries whose families were in Seoul in October 2025; bereaved
  families alive and politically active in 2026; **and a criminal record that is not merely
  unfinished but formally suspended** — both appeals stopped by the Seoul High Court to wait for a
  fact-finding commission that has extended itself to December 2027.
- **Produced by:** Claude (Opus 5, Claude Code), 2026-08-21, by live retrieval
- **Binds to:** `EP74_itaewon_script.en.v005.md`, `EP74_itaewon_FACTS_LEDGER.v001`–`.v004.md`,
  `episodes/PD-2026-074-itaewon/episode_spec.v001.json`
- **Status:** **CLEARED TO RENDER once §2 R4 is done. NOT CLEARED FOR PUBLISH** — §3 has six items
  and §5 is the day-of check.

---

## 1. What was read, and what was not

**Read in full, by live fetch, 2026-08-21.** The **statute itself** — Framework Act on the Management
of Disasters and Safety **Article 66-11** and **Enforcement Decree Article 73-9** on `law.go.kr`. The
**PLOS ONE** study (peer-reviewed, 12 July 2024). The **Seoul Metropolitan Government's** own page on
the intelligent disaster safety system. Korea Times (first-instance judgment, illegal terrace,
October 2025 joint audit, March 2026 hearing, foreign victims' families, Constitutional Court
ruling). Korea Herald (foreseeability, stalled legislation). Al Jazeera (calls, deployment). SCMP
(call transcripts). Reuters (2025 re-investigation and apology). Korea JoongAng Daily (Itaewon three
years on). 노컷뉴스 and 법률신문 (per-defendant outcomes). MBC (the prosecution appeal; and the
Seoul Transportation Corporation passenger counts). AFP via Gulf News (Kim Kwang-ho acquittal).
Seoul Economic Daily (2026 commission activity). **뉴시스 and 경향신문 (the suspension of both
appeals).** **이데일리 (the 12 March 2026 hearing testimony).**

**NOT read, and the film says so (AB-07):**

| not read | consequence |
|---|---|
| **Any court judgment text**, Korean or English | Every judgment row is the *reporting* of a judgment. Where a court is quoted, the outlet is named in the narration, out loud |
| **The Korean investigation file and the National Assembly hearing record** | The film describes what the commission *did* — resolutions, referrals, an extension, a hearing — and never characterises what the record *contains* |
| **The Washington Post's November 2022 investigation** | HTTP 403. Its 350-video analysis and rescue-delay findings are **not in the ledger and may not be narrated** (AB-09). The thirteen minutes come from the PLOS ONE timeline alone |
| **Any survivor or bereaved-family account** | The film contains none, deliberately (⛔-01) |
| **The forensic study behind the July 2026 "160"** | Only its English summary was read — which is exactly why the film does not use that number (⛔-03) |

---

## 2. Before the render

| # | item | status |
|---|---|---|
| **R1** | **The appellate outcome** | ✅ **RESOLVED.** There is none, because there is no proceeding running. **Criminal Division 13 suspended the police defendants' appeal on 14 July 2025; Criminal Division 9-1 suspended the district office chief's on 28 August 2025**, both to wait for the commission (IT-84, IT-86). This is now the film's ending rather than its hole |
| **R2** | **`IT-58` and `IT-74`** | ✅ **HALF RESOLVED, HALF CUT.** IT-58 is superseded by **IT-93/IT-94**, read in the MBC article, from Seoul Transportation Corporation's own count — 81,573 against 31,878, with the hourly curve. It is now in ACT_1. **IT-74 is cut**: the Constitutional Court's "many factors" line was never read in the article, and IT-73 from the same ruling is read and says enough |
| **R3** | **The official toll on the day of the render** | ⏳ **Unchanged. 159.** Cheap to check, catastrophic to miss |
| **R4** | **`check_packaging_claims.py` on the chosen title and thumbnail** | ⏳ **Outstanding, and it is the only thing between here and a render.** Note the script now speaks **81,573**, **31,878** and **2.6** as words, so the numeral/word mismatch risk in title A is unchanged |

## 3. Before the upload

| # | item | current position |
|---|---|---|
| U1 | Legal status of every named person, as at the upload date | Lee Im-jae — sentenced at first instance 30 Sep 2024; **appeal suspended 14 Jul 2025**; testified to the commission 12 Mar 2026. Park Hee-young — acquitted at first instance 30 Sep 2024; **appeal suspended 28 Aug 2025**; referred by the commission for fresh investigation May 2026. Kim Kwang-ho — acquitted 17 Oct 2024; **refused the witness oath 12 Mar 2026**. Song Byung-ju and a 112 team leader — sentenced at first instance 30 Sep 2024, appeals suspended. Lee Sang-min — impeachment rejected unanimously 25 Jul 2023, reinstated |
| U2 | **`AB-11` — has either appeal restarted?** | The commission's June 2026 deliberation date passed and it extended itself to December 2027. **A resumed hearing rewrites the last act.** This is the single most likely thing to change between render and publish |
| U3 | The commission's mandate | Extended June 2026 to December 2027. Confirm not extended again, curtailed or superseded |
| U4 | The penalty bill (`IT-82`) | Proposed 29 April 2026. **Confirm it is still a bill.** If it passed, ACT_5's last legal beat changes |
| U5 | Article 66-11 and Decree 73-9 | Confirm no amendment after 26 Dec 2023 / 26 Mar 2024 |
| U6 | Description, on-screen text, plate verdicts | Re-run `check_packaging_claims.py` on final text; `runs/qc/itaewon_plate_verdicts.v001.json` complete with **no rejected or unresolved plate in a cut** |

## 4. The numbers, and where each is allowed to come from

| figure | value | source | changeable? |
|---|---|---|---|
| deaths | **159** | official toll, named reporting through Mar 2026 | Only by a ministry revision. **Never 160** |
| injuries | 196 | SECONDARY | Weakest number in the film; cut it before defending it |
| calls | **11**, 18:34 → 22:11 | Korea Times, Mar 2026 | No |
| attended | **4**; no action on **7** | Al Jazeera, Nov 2022 | No |
| officers | **137** | two named sources | No |
| rallies | **34** → **921** | joint government audit, Oct 2025 | No |
| **station** | **81,573** vs **31,878**, ×2.6; 10,747 / 11,873 / 11,666 / 9,285 by hour | **Seoul Transportation Corporation**, via MBC | No |
| alley | **~50 m, ~5 m → 3.2 m** | Korea Times, building records | A second account says 45 m; the film uses 50 and never both |
| gradient | — | **does not exist** (AB-01) | No figure, ever |
| density | 7.57 ped/m², max 9.95 | PLOS ONE | No |
| pressure | 1,063 N/m, max 1,961 | PLOS ONE | No |
| crowd | ~100,000 | Al Jazeera | Always characterised as an estimate |
| foreign dead | **26 from 14 countries** | Korea Times, Oct 2025 | No |
| cameras | **909** across **71** areas | Seoul Metropolitan Government (PRIMARY) | No |
| **appeals suspended** | **14 Jul 2025**, **28 Aug 2025** | 뉴시스, 경향신문 | **Re-check at publish (U2)** |

## 5. What the publish-day check has to cover

1. **U2.** Has either appeal restarted? This film's last act is built on the fact that they stopped.
2. **U1, name by name.** A status that changes between render and publish turns a true sentence false
   while the file sits on disk.
3. **The toll. 159.**
4. **Title, thumbnail text and description through `check_packaging_claims.py`**, against the final
   script.
5. **The contact sheet, opened by a person**, looking for a body, a real face, a generated glyph, or
   Japanese/Chinese/Western signage.
6. **The four blocking classes in `config/ship_policy.v001.json`**, read against the finished file.
   `real_person_likeness` is the live one here and it is live in every frame containing a crowd.

## 6. Two things this packet says about itself

**⛔-16 is the most fragile rule in the episode.** Lee Im-jae's testimony — that the disaster was
less likely without the presidential office move — is a counterfactual spoken by a man convicted at
first instance with a suspended appeal. It is reported, attributed, dated, and **never adopted**. The
scene plan carries the same rule as a cutting instruction. If any reviewer feels the film *argues*
that point rather than *reports* it, that is a defect and it is the one to look for first.

**Nothing here lowers a threshold and nothing here is self-certification.** The packet's function is
to name, in advance, the things that would make a finished film wrong — so they are checked against
the world rather than against the film's own confidence.
