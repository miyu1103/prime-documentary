# EP74 · ITAEWON — FACTS LEDGER v001

**Binding. Read before any script, asset or caption work.**
Every narrated factual sentence in the script carries a row id from this file in an HTML comment on
the line beneath it. A sentence with no row id does not enter the script.

**Provenance.** Rows were retrieved **2026-08-21** by live fetch and search. This episode has almost
no English-language primary record: the investigation file, the National Assembly hearing record and
the court judgments are in Korean, and the handover's standing rule applies — *an English secondary
summary is reporting ABOUT the record, and may never be narrated AS the record.* Grades are therefore
stricter than EP72's:

| grade | meaning |
|---|---|
| `VERBATIM` | The words are the source's own, quoted from a page **this production fetched and read** on 2026-08-21 |
| `SECONDARY` | Reported by a named outlet and paraphrased here. **May not carry a load-bearing beat alone** |
| `UNREAD` | Appears **only in a search-result summary**. This production has not read the article. **NOT USABLE.** Must be fetched and re-graded before it enters a script line |
| `OURS` | Our arithmetic or our paraphrase of a sourced figure |
| `ABSENCE` | The record accessible to this production does not contain it. The film either says so or stays silent |

`UNREAD` is new to this ledger and exists because of the 2026-07-26 retrospective: *伝聞は現物で*.
A search engine's summary of an article is not the article.

**v001 covers the spine.** As on EP72, writing the script will expose regions with nothing in them;
those become **v002 by ADDITION**, never by editing a row here.

| id | source |
|---|---|
| SRC-0001 | **The Korea Times**, "Ex-Yongsan police chief gets 3 years in prison over Itaewon crowd crush; Yongsan ward chief acquitted", 30 September 2024 |
| SRC-0002 | **The Korea Herald**, "Court rules Itaewon tragedy was 'foreseeable'", 30 September 2024 |
| SRC-0003 | **Al Jazeera**, "S Korea police stations raided in probe of Halloween crush deaths", 2 November 2022 |
| SRC-0004 | **South China Morning Post**, "'People are falling down': call transcripts reveal fear at Seoul Halloween crush", 2 November 2022 |
| SRC-0005 | **The Korea Times**, "Presidential office relocation blamed for police failures in Itaewon crowd crush", 23 October 2025 — reporting a joint audit by the Office for Government Policy Coordination, the National Police Agency and the Ministry of the Interior and Safety |
| SRC-0006 | **Korea JoongAng Daily**, "Three years later, tragedy still hangs over Itaewon as police strengthen safety procedures for Halloween", 27 October 2025 |
| SRC-0007 | **The Korea Times**, "Itaewon tragedy hearing turns emotional as survivor recounts horror, police trade blame", 12 March 2026 |
| SRC-0008 | **Reuters**, "South Korea's Lee orders new investigation team to look into deadly 2022 crush", 17 July 2025 |
| SRC-0009 | **Seoul Economic Daily (English)**, "Itaewon Commission Seeks Probe of Yongsan District Chief Over Disaster Response", 9 May 2026, Hwang Dong-gun |
| SRC-0010 | **Seoul Economic Daily (English)**, "10% of Itaewon Victims May Not Have Died from Asphyxiation, Panel Says", 22 July 2026 |
| SRC-0011 | **The Korea Times**, "Hotel next to alley of Halloween crush illegally extended terrace", 1 November 2022 |
| SRC-0012 | **The Korea Herald**, "[News Focus] A year after Halloween crowd crush, legislation remains stalled", 25 October 2023 |
| SRC-0013 | **The Korea Times**, "Yoon rejects special act to investigate Itaewon tragedy", January 2024 |
| SRC-0014 | **National Commission for the Investigation of the October 29 Itaewon Disaster and Prevention of Recurrence**, official site, `1029itaewoncommission.go.kr/eng`, read 2026-08-21 |
| SRC-0015 | **Kyunghyang Shinmun (English)**, commission activity-period extension, 25 June 2026 |
| SRC-0016 | Wikipedia, *Seoul Halloween crowd crush* — **corroboration and lead-generation only**, never a citation of record |
| SRC-0017 | **노컷뉴스 (CBS)**, "운명 갈린 '이태원 참사' 이임재 유죄·박희영 무죄…유족 '통탄'", 2024년 10월 1일 |
| SRC-0018 | **법률신문 (Lawtimes)**, "[판결] '이태원참사 부실대응' 이임재 전 용산서장, 금고 3년", 2024년 9월 30일 — 사건번호 2023고합25 |
| SRC-0019 | **MBC 뉴스**, "검찰, 이태원 참사 관련 이임재 전 서장·박희영 구청장 1심 선고에 항소", 2024년 10월 7일 |
| SRC-0020 | **AFP**, via Gulf News, "Seoul court acquits ex-police chief over Halloween crush", 17 October 2024 |

**Re-grading note, 2026-08-21.** Rows IT-36 to IT-39 were first written `UNREAD` because they existed
here only as search-engine summaries of Korean articles. They were then **fetched and read** the same
day, before any script line was written, and re-graded against SRC-0017 to SRC-0020. Nothing in this
file has been consumed by a downstream artifact; from the moment it is committed it is immutable and
corrections are additions.

---

## 1. THE PLACE — a street you could measure

| id | fact | grade | source |
|---|---|---|---|
| IT-01 | The crush happened in an alley beside the **Hamilton Hotel**, running between **Itaewon-ro** and the streets above it, near **Exit 1 of Itaewon Station**, in **Yongsan-gu, Seoul** | SECONDARY | SRC-0011, SRC-0016 |
| IT-02 | The alley is **about 50 metres long**, **about 5 metres wide at the top**, **narrowing to 3.2 metres at the bottom** | VERBATIM | SRC-0011 |
| IT-03 | A second published description gives the street as "**about 45 metres long and 3.2 metres wide at its narrowest point**". The two accounts agree on 3.2 m and differ on length. **The film uses IT-02** and never presents both | SECONDARY | SRC-0016 |
| IT-04 | **The street slopes.** It rises from Itaewon-ro, and the incline meant people were pushed **downward** | SECONDARY | SRC-0016 |
| IT-05 | The Hamilton Hotel had **illegally extended a 17.2-square-metre terrace on the northern side of its main building**, adjacent to the alley, which "**made the narrow path even narrower**" | VERBATIM | SRC-0011 |
| IT-06 | Yongsan district office had **already notified the hotel of the violation and levied fines the previous year** (2021) | VERBATIM | SRC-0011 |

## 2. THE NIGHT — how many people, and how many of the state's

| id | fact | grade | source |
|---|---|---|---|
| IT-07 | **29 October 2022**, the Saturday of Halloween weekend, in Itaewon | VERBATIM | SRC-0001 |
| IT-08 | **137 police officers** were stationed in the area | SECONDARY | SRC-0004 |
| IT-09 | Rallies and demonstrations inside **Yongsan Police Station's jurisdiction rose from 34 in 2021 to 921 between May and October 2022** | VERBATIM | SRC-0005 |
| IT-10 | The joint audit found: "**The relocation of the presidential office to Yongsan increased the demand for police deployment in the area, which was a key factor behind the lack of crowd control officers in Itaewon**" | VERBATIM | SRC-0005 |
| IT-11 | Police resources in the district had been **redirected to the Samgakji area near the presidential office** | VERBATIM | SRC-0005 |
| IT-12 | The audit was carried out **jointly by the Office for Government Policy Coordination, the National Police Agency and the Ministry of the Interior and Safety**, and reported on **23 October 2025 — three years after the disaster** | VERBATIM | SRC-0005 |

## 3. ELEVEN CALLS — the spine of this film

| id | fact | grade | source |
|---|---|---|---|
| IT-13 | "**Between 6:34 p.m. and 10:11 p.m. that night, Itaewon police received 11 distress reports about dangerous levels of overcrowding**" | VERBATIM | SRC-0007 |
| IT-14 | The first call, **18:34**, as rendered by SCMP: "**Looks like you can get crushed to death with people keep coming up here while there's no room for people to go down. I barely managed to leave but there are too many people, looks like you should come and control.**" | VERBATIM | SRC-0004 |
| IT-15 | The **same call** as rendered by Al Jazeera: "**I feel like I would be almost crushed to death here because people continued to come up even though no more can go down.**" Two English translations of one Korean call. The film uses **one**, and attributes it as a translation of a police-released transcript — never as the caller's English | VERBATIM | SRC-0003 |
| IT-16 | A second report, **about ninety minutes later**: "**there are people who fell over and got hurt because there are too many people**" | VERBATIM | SRC-0003 |
| IT-17 | Later calls: "**We are on the verge of a terrible accident due to the massive crowds**" and "**I am almost being crushed to death**" | VERBATIM | SRC-0003 |
| IT-18 | **Officers were deployed to only 4 of the 11 reports.** They dispersed crowds at those locations and took "**no action**" on the remaining **7** | VERBATIM | SRC-0003 |
| IT-19 | National Police Commissioner **Yoon Hee-keun** acknowledged crowd control at the scene had been "**inadequate**" | VERBATIM | SRC-0003 |
| IT-20 | Prime Minister **Han Duck-soo**: "**The police must conduct thorough inspections and provide a clear and transparent explanation to the public.**" | VERBATIM | SRC-0003 |
| IT-21 | 18:34 to 22:11 is **three hours and thirty-seven minutes** | OURS | arithmetic on IT-13 |

## 4. THE TOLL — and the number the film will not say

| id | fact | grade | source |
|---|---|---|---|
| IT-22 | **159 people died** | VERBATIM | SRC-0001, SRC-0002, SRC-0006, SRC-0007 |
| IT-23 | They were "**mostly young people**" | VERBATIM | SRC-0008 |
| IT-24 | The toll rose over time: **157** in the immediate aftermath, **158** by 14 November 2022, **159** by 3 January 2023; the 159th was a high-school student found dead on 12 December 2022 in a suspected suicide, recognised by the Ministry of the Interior and Safety | SECONDARY | SRC-0016 |
| IT-25 | On **22 July 2026** the Special Investigation Commission published a forensic analysis, carried out by the **Department of Forensic Medicine at Pusan National University School of Medicine**, finding that about **10 %** of victims may not have died from asphyxiation — potentially from crush syndrome, rhabdomyolysis and internal organ damage from compression — and that more might have survived had rescue efforts continued immediately. **That report refers to 160 victims.** The official toll remains 159. **The film narrates 159 and never 160** | SECONDARY | SRC-0010 |

## 5. THE GAP IN THE LAW — the reason this is a PD film and not a news story

| id | fact | grade | source |
|---|---|---|---|
| IT-26 | Under South Korea's framework law on disaster and safety management, **voluntary events without organizers did not have to notify police and fire authorities of a safety management plan in advance**, leaving it ambiguous where responsibility for on-site safety lay | SECONDARY | SRC-0012 |
| IT-27 | **Until its revision in December 2023**, the law specified administrative duty and liability **only for official events and local festivals where the organizer was clear** | SECONDARY | SRC-0012 |
| IT-28 | **Seventeen lawmakers** proposed bills making the head of a local government liable where a large crowd is expected | SECONDARY | SRC-0012 |
| IT-29 | As of **October 2023**, a year of parliamentary debate had produced **no legislation** holding a local government legally liable when people are hurt while crowded in a public space | SECONDARY | SRC-0012 |

## 6. THE JUDGMENTS — first instance, and nothing beyond it

| id | fact | grade | source |
|---|---|---|---|
| IT-30 | On **30 September 2024** a Seoul court sentenced **Lee Im-jae, 54**, former chief of **Yongsan Police Station**, to "**three years in prison without labor**" on charges of "**professional negligence resulting in death and injury**" | VERBATIM | SRC-0001 |
| IT-31 | The court: "**It was either foreseen or it could have been anticipated that a large crowd of people gathering at the slanted alleyway in Itaewon for the 2022 Halloween could cause a serious danger to bodies from pedestrians pushing.**" | VERBATIM | SRC-0001, SRC-0002 |
| IT-32 | The court found he had **neglected to establish and implement a safety management plan** to prevent dangerous situations arising from the crowd, although the danger was foreseeable | VERBATIM | SRC-0002 |
| IT-33 | **Yongsan Ward Office chief Park Hee-young and other ward officials were also indicted, and the same court found them not guilty** | VERBATIM | SRC-0001 |
| IT-34 | The reason for the acquittal: "**related law and regulations did not require them to come up with safety measures for events without organizers**", and "**there were no obligatory regulations specifying the need to establish separate safety management plans**" | VERBATIM | SRC-0001 |
| IT-34a | The same finding in the court's own language: 박희영에게 "**재난안전법령상 2022년 핼러윈데이에 대비해 안전관리계획을 추가‧정비‧보완해야 할 구체적이고 직접적인 업무상 주의의무를 부담한다고 보기 어렵다**" — *it is hard to find that she bore a specific and direct professional duty of care, under the disaster and safety laws, to add to, revise or supplement a safety management plan in preparation for Halloween 2022* | VERBATIM | SRC-0017 |
| IT-34b | And on Lee Im-jae: "**사고를 충분히 예견해야 했고, 인적‧물적 자원을 동원해 각종 대책을 마련하고 대응조치를 취해야 했음에도 안일한 인식하에 이태원 핼러윈데이 대비에 소홀했다**" — *he should have sufficiently foreseen the accident and should have mobilised human and material resources to prepare measures and take response actions, but under a complacent understanding he was negligent in preparing for Halloween in Itaewon* | VERBATIM | SRC-0017 |
| IT-35 | **Kim Kwang-ho**, former Seoul police chief and the highest-ranking officer indicted, was **acquitted on 17 October 2024 along with two other police officers**. The court: "**It is hard to establish beyond reasonable doubt, with the evidence put forward by the prosecution, that the defendants committed professional negligence.**" | VERBATIM | SRC-0020 |
| IT-36 | The bench was the **Seoul Western District Court, Criminal Division 11 (presiding judge Bae Seong-jung)**; Lee Im-jae's case number is **2023고합25** | VERBATIM | SRC-0018 |
| IT-37 | Same day, same bench, on professional negligence causing death and injury: **Song Byung-ju**, former head of the Yongsan 112 situation room — **two years' imprisonment without labour (금고 2년)**; a former 112 situation **team leader** — **one year without labour, suspended for two years** | VERBATIM | SRC-0018 |
| IT-38 | On the **other** charges the same bench **acquitted**: Lee Im-jae of **perjury under the National Assembly testimony act** and of **drawing up and using a false official document**; a former head of the women and juveniles division and a **경위** of the community safety division, both of drawing up and using a false official document | VERBATIM | SRC-0018 |
| IT-39 | On **7 October 2024** prosecutors **appealed** against **Lee Im-jae, Park Hee-young, four other police officers and three ward officials**, arguing that "**피고인들의 과실과 그로 인한 결과가 매우 중대함에도 사고의 책임을 떠넘기며 진지하게 반성하지 않는다**" — *although the defendants' negligence and its consequences are very grave, they shift the blame and do not seriously reflect* — that the court had **misapprehended the law** on the ward chief's duty under the disaster and safety act, and that on the false-document acquittal "**사고 현장 도착시간 등이 명백히 거짓으로 기재됐다**" — *the time of arrival at the scene and other matters were plainly recorded falsely* | VERBATIM | SRC-0019 |
| IT-40 | The Seoul High Court appeal was reported in May 2025 as heading for a ruling **around 27 October 2025**; bereaved families asked in June 2025 for it to be suspended pending the commission's work | **UNREAD** | Korean-language reporting seen only in search summaries |

## 7. WHAT THE STATE DID NEXT

| id | fact | grade | source |
|---|---|---|---|
| IT-41 | In **January 2024** President **Yoon Suk Yeol** rejected the special act to investigate the disaster, the government arguing that an opposition-driven investigation committee undermined constitutional principles | SECONDARY | SRC-0013 |
| IT-42 | The bill provided for an **11-member committee**: four recommended by the ruling party, four by the opposition, three by the speaker of parliament in cooperation with victims' families | SECONDARY | SRC-0013 |
| IT-43 | The body that eventually began work is the **National Commission for the Investigation of the October 29 Itaewon Disaster and Prevention of Recurrence**, launched **September 2024** | VERBATIM (name) / SECONDARY (date) | SRC-0014, SRC-0008 |
| IT-44 | On **17 July 2025** President **Lee Jae Myung** ordered "**the setting up of a new investigation team, involving police and prosecutors**", to work alongside the commission | VERBATIM | SRC-0008 |
| IT-45 | President Lee: "**As the head of the state, I would like to formally apologize on behalf of the government for failing to fulfill its responsibility to protect the lives and safety of the people.**" | VERBATIM | SRC-0008 |
| IT-46 | **Song Hae-jin**, representing victims' families, said **police records and information regarding the government's response had been withheld from the special commission** | VERBATIM | SRC-0008 |
| IT-47 | On **12 March 2026** the commission held an investigative hearing at which a survivor testified and police officials traded blame | SECONDARY | SRC-0007 |
| IT-48 | In **May 2026** the commission passed a resolution requesting investigations into **Park Hee-young** and former Itaewon Station chief **Song Eun-young**, and submitted a formal request to the joint police-prosecution investigation team. Song faces an allegation of **perjury at a parliamentary hearing** | VERBATIM | SRC-0009 |
| IT-49 | In **June 2026** the commission judged that a **one year and three month extension** of its activity period was unavoidable — to **December 2027** — and said it would focus on the **upper chain of command including the Office of the President and the Office of National Security** | SECONDARY | SRC-0015 |

## 8. ITAEWON NOW — what the state finally put in the alley

| id | fact | grade | source |
|---|---|---|---|
| IT-50 | Three years later, a **temporary median barrier was installed on World Food Street to encourage one-way pedestrian flow** | VERBATIM | SRC-0006 |
| IT-51 | "**police officers and subway staff actively guided pedestrians through the station to prevent congestion**"; a **mobile patrol unit began operations around Itaewon from 6 p.m.**; officers inspected streets for hazards and verified that **CCTV and emergency bells** worked; "**Traffic police blew whistles to direct vehicles when roads grew crowded**" | VERBATIM | SRC-0006 |
| IT-52 | Warning signs read: "**Crowded areas can be dangerous.**" | VERBATIM | SRC-0006 |
| IT-53 | "**Police lines, safety signs and barricades underscored a lingering unease three years after the crowd crush.**" | VERBATIM | SRC-0006 |
| IT-54 | "**disaster response standards have been revised and preventive systems strengthened**" — reported without specific legislative detail | VERBATIM | SRC-0006 |

## 9. ABSENCE — what the record accessible to this production does not contain

| id | absence | consequence for the film |
|---|---|---|
| AB-01 | **No gradient figure exists** for the alley's slope in any source this production could read | The film says the alley **slopes**, and shows it. It never gives a percentage or an angle |
| AB-02 | **No appellate outcome is verified.** The Seoul High Court ruling in the Lee Im-jae case, reported in May 2025 as expected around 27 October 2025, could not be retrieved on 2026-08-21 in English or Korean search | The film states **only** first-instance outcomes, each with its date and its court, and says plainly that the cases went to appeal and that the appeal is **outside what this film can verify**. **Re-verify before ship** — if the appellate judgment is found, IT-30 to IT-40 must be re-stated in a v002 and every affected script line rewritten |
| AB-03 | **No Supreme Court decision** is verified for any Itaewon defendant | The film asserts no final resolution for anyone |
| AB-04 | **No verified finding identifies a person who started the crush**, and no verified finding supports the pushing, chanting, celebrity-sighting or drug stories that circulated in 2022 | None of it appears, not even to debunk it at length. One clean sentence at most |
| AB-05 | **No verified finding establishes that any single measure would have prevented the deaths** | No counterfactual is narrated. The film states what was asked for and what was done — never what would have worked |
| AB-06 | **No causal finding links the Hamilton Hotel's illegal terrace to the deaths** | The terrace is **geometry**: it made a narrow path narrower, it was known, it was fined. Causation is never asserted |
| AB-07 | **The Korean-language investigation file, hearing record and judgments have not been read by this production** | Every line resting on them is attributed to the outlet that reported it, in the narration itself where it is load-bearing |

---

## ⛔ QUARANTINE — assertions that must never appear

| id | rule |
|---|---|
| ⛔-01 | **No victim or survivor is named, shown or characterised.** 159 people died and the film names none of them. No generated face may resemble an identifiable real person; no archival frame with a recognisable victim, survivor or family member is used |
| ⛔-02 | **The crush is never depicted.** No bodies, no fallen people, no CPR, no stretchers, no blood, no covered figures. The alley appears in exactly three states: **empty**, **ordinarily busy**, **after**. The event is carried by **sound**, by **the width of the walls**, and by **the slope** |
| ⛔-03 | **Never state 160 deaths.** The official toll is 159 (IT-22). The 160 in the July 2026 forensic report (IT-25) is not the official toll and does not enter narration, caption, title, thumbnail or description |
| ⛔-04 | **Never assert a final legal outcome for anyone.** Every named person carries their **verified status, its date and its court, in the same sentence that names them**. Lee Im-jae: sentenced at first instance, 30 September 2024. Park Hee-young: acquitted at first instance, same day. Kim Kwang-ho: acquitted, 17 October 2024. Beyond that, AB-02 and AB-03 govern |
| ⛔-05 | **Never assert that anyone pushed, or that any individual or group started it** (AB-04) |
| ⛔-06 | **Never assert drugs, alcohol or a stampede as a cause.** This was a compressive failure of a crowd in a confined slope |
| ⛔-07 | **Never say the police did nothing.** They received eleven calls and went to four of them (IT-18). The specific, sourced omission is stronger than the blanket accusation, and the blanket accusation is false |
| ⛔-08 | **Never assert that closing the street, one-way flow or more officers would have prevented the deaths** (AB-05) |
| ⛔-09 | **Never assert that the hotel's terrace caused the deaths** (AB-06) |
| ⛔-10 | **No `UNREAD` row enters a script line.** IT-36 to IT-39 were fetched and re-graded on 2026-08-21. **IT-40 is still `UNREAD`** and is fetched and re-graded, or it is cut |
| ⛔-11 | **No English secondary summary is narrated as the Korean record.** Where it is load-bearing, the outlet is named in the narration |
| ⛔-12 | **No figure for deaths, injuries, crowd size, width, length, times or call counts that is not a row above** |
| ⛔-13 | **No identification of any 112 caller**, and no content of any call beyond what named reporting has published |
| ⛔-14 | **Korean signage in any generated plate is unreadable, never wrong.** No Japanese or Chinese shopfronts. This is the EU-number-plate-in-Texas error of EP62 |

---

## The one-sentence contradiction this film is built on

> The state had **137 officers** in Itaewon and, two kilometres away at the presidential office it had
> just moved into Yongsan, **921 rallies' worth of demand** where there had been 34 the year before;
> it took **eleven calls across three hours and thirty-seven minutes** and sent officers to **four** of
> them; and when it was over, the court that **convicted the police chief acquitted the district
> officials** — because **no law required anyone to write a safety plan for a party nobody had
> organised.**

Every act must serve that sentence. ⛔-01, ⛔-02 and ⛔-04 govern how it is said.
