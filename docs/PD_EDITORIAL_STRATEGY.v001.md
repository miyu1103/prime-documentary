# PD Editorial Strategy v001 — the owner's standing direction, 2026-08-11

**Binding on every thread.** This sits alongside `PD_ONE_PASS_PRODUCTION_SPEC.v2.md`. That document
governs how a film is made correctly; this one governs *what gets made at all*, and it outranks any
habit of "we have always produced N episodes a month".

The owner's judgement, in one line: **PD already has the hardest thing — a production base that can
make a lot. What it lacks is the ability to choose.** The next thing to add is not throughput. It is
an editor-in-chief function that kills weak premises, weak titles, weak scripts, reads the numbers,
and concentrates on what wins.

---

## 1. The channel's promise

Not "a documentary channel". This:

> **True stories about law, money, power, and the systems ordinary people never see coming.**

Japanese, as the owner phrased it: 普通のアメリカ人が、法律・警察・金・国家・制度によって突然人生を
狂わされる実話。

The subject is never the doctrine. It is **what the doctrine can do to you.**

| weak | strong |
|---|---|
| Civil Asset Forfeiture Explained | Police Took His Life Savings. He Was Never Charged With a Crime. |
| Miranda Rights Explained | Police Don't Have to Tell You This Immediately |
| Banking Regulations in America | She Deposited $9,900. Then Everything Went Wrong. |

The umbrella concept is **Power**, not police. Police are Power; so are the state, the bank, the
court, the insurer, the corporation. The protagonist is always an **ordinary person**. Narrowing to
"police" makes the channel monotonous, politically legible, and ad-risky. "Power vs the ordinary
American" survives five years.

## 2. Slate allocation — 90% narrow, 10% exploration

| pillar | share | content |
|---|---|---|
| Power & Police | 35% | traffic stops, searches, confessions, warrants, police powers |
| Money & Government | 30% | forfeiture, tax, debt, banking, property seizure |
| Justice Gone Wrong | 25% | wrongful conviction, evidence, prosecutors, courts |
| Experimental | 10% | new-genre probes |

The first fifty episodes were market research, and they returned a signal. Episodes 51-100 are
**verification, not exploration.**

## 3. The premise score — nothing under 70 gets made

100 points: relevance to an ordinary person 20 · surprise 20 · emotion 15 · titleability 15 ·
thumbnailability 10 · story 10 · a real primary source 5 · evergreen 5.

**"It is an important subject" is not a reason to make it.** Only an important subject that can be
packaged well gets made.

## 4. What the recommendation system is actually judging

Appeal (will they choose it) → Engagement (will they keep watching) → Satisfaction (were they glad
they did). Clickbait that wins Appeal and loses Engagement is a net negative. So the goal is **not
maximum CTR** — it is raising CTR *without damaging what happens after the click*.

The channel-level metric to run on is **Watch Time per Impression ≈ CTR × AVD**, because CTR alone
is meaningless: 3.2% against three million impressions beats 9% against five hundred.

## 5. The measured baseline (2026-08-11, this repo's own tooling)

| | measured | how |
|---|---|---|
| long-form CTR | **1.61%** impression-weighted over 58,973 impressions; median 1.26% | `yt_studio_video_ctr.py` |
| retention half-life | **45 s**; 30 of 30 long-forms below peer median at 30 s | official retention curves |
| audience | **92.5% male, 77% over 55, 86% US** | analytics probe, `ageGroup,gender` |
| subs per 1,000 views | long-form **3.88** vs shorts **1.22** | `yt_analytics_probe.py` |
| long-form median APV | **18.7%** | same |
| lifetime long-form views | 57 public, **total 1,887, median 11** | `yt_full_audit.py` |

Two corrections to older canon, both measured tonight:

- "**91% aged 55+**" is now **77.0%**.
- "**27-37 min beats 9-15 min**" is **confounded and must not be used as a length rule.** The band's
  advantage is carried by two videos — OceanGate and D.B. Cooper — which are the only two topics with
  a large external feed. **Length is not the variable. A famous, adjacent premise is.**

That last point is the strongest available support for section 1. The RELATED_VIDEO feeders were
resolved through the Data API: watch time arrives from **FRONTLINE's Madoff film** and **LEMMiNO's
D.B. Cooper**. The search terms that find us are named events — `oceangate`, `aaron swartz`,
`ruja ignatova`, `anthony ray hinton`. **No doctrine term appears anywhere in the feeder data.**

## 6. Titles and thumbnails

Twenty title candidates before production, not one from an LLM adopted as written. The shape that
works: **a person · a specific event · something abnormal · something unfinished.**

Thumbnails: brand consistency is worth less than being distinguishable in half a second. Every video
looking like the same DVD spine is a failure mode, not a house style. Reduce to **2-4 words · one
subject · one abnormality · one background.** Measured evidence: the best long-form CTRs on this
channel are 4.40 / 3.95 / 3.76%, and the worst — 0.43-0.86% — are all abstract-threat framings.

Use YouTube's own title/thumbnail test (up to three variants, decided on watch time). One video is
not one thumbnail; it is a small experiment.

## 7. The first thirty seconds are the asset

Do not open with a logo, an intro, a period, or background. Open on the **abnormal moment**, then
cut to black, then say what the film is. Concentrate craft investment here rather than spreading it
evenly across the runtime.

Script shape: **incident → question → clue → obstacle → new information → reversal → outcome →
meaning.** Not explanation → explanation → explanation. AI scripts want to explain; viewers stay for
"what happens next", not for knowledge. A documentary is not a Wikipedia article read aloud.

## 8. Runtime

Do not commit to a house length. A story that ends at eight minutes runs eight minutes. What matters
is **total satisfied time**, not duration. (Where the owner sets a length for a specific episode,
that instruction governs that episode — see EP70, ordered at 45 minutes.)

## 9. After Effects

AE exists to make hard information instantly legible — the opening, maps, evidence, amounts, the
mechanism of a law, timelines, causation. **Zooming and parallaxing a photograph is not a competitive
advantage.** The visual language is motion design *in service of explanation*.

## 10. Shorts

Keep them, but stop making them as separate content. A short is the **entrance to a specific
long-form**, carrying the core of the incident and not the resolution. Subscribers gathered by
stand-alone shorts are not the same asset as subscribers who watch long-form: long-form converts at
3.88 per 1,000 views against shorts' 1.22. **Shorts acquire; long-form is the asset.**

## 11. AI, disclosure and the real moat

Being able to generate a lot is no longer an advantage; the platform is actively suppressing
repetitive low-quality AI output and has reframed "repetitious" as "inauthentic". So: **let the
machine make the volume and let humans make the difference.** 100% automation is not the optimum.

Where the subject is a real event, AI-generated people and scenes must never be presented as
authentic record. Label reconstructions. This *raises* documentary credibility rather than lowering
it.

Fact integrity is the competitive advantage, not a tax on it: AI script → primary source → fact
check → human approval. **Keep the humans on information quality, not on production.**

The durable moat is not the generator. It is the dataset: for every episode, record protagonist
gender, whether an amount appears, police vs court, incident vs explainer, whether the title carries
a number, whether the thumbnail carries a person, title length, negative emotion, curiosity gap, AVD,
CTR, traffic source. After a hundred episodes that is a dataset **only PD has.**

## 12. KPIs — what to be judged on

S: Good/Great premise rate · 48-72h CTR · 30-second retention · AVD · impression growth · returning
viewers. A: subscribers per 1,000 views. B: number of uploads. C: how elaborate the edit is.

"We published every day" is not an achievement. **How many winning formats did we find this month?**

## 13. Goals, separated

**¥1M/month and 2M subscribers are different objectives and must not be planned as one.**

Revenue is reachable first: at a planning RPM of ¥500-1,000, ¥1M/month needs roughly 1-2M long-form
views per month. Two million subscribers needs far more than that, and needs PD to be a brand
Americans return to rather than a channel that earns.

Phase ladder, in order: 1,000 views per video reliably → 100k long-form views/month → 500k → 1M →
3-10M → 1-2M subscribers. **Subscriber count is an output, never a target.**

Revenue should not depend on ads alone. Sponsorship, affiliate and newsletter fit this subject
matter — privacy, legal services, cybersecurity, identity protection, finance, insurance. Never bend
content for a sponsor; credibility is the asset being sold.

## 14. The competitor set

Not other AI documentary channels. On the viewer's home screen PD competes with Netflix, MrBeast,
CNBC, Business Insider, Law&Crime, Vox, bodycam channels and true crime. **"Good for an AI video" is
not a standard. "Better than television" is.**

## 15. The failure mode to fear

Not incapacity. It is **making a large number of averagely-decent videos and being satisfied.**
Channels do not become large by mass-producing 90-point videos; they become large when someone finds
a 120-point premise and commits everything to it.

## 16. The ninety-day plan

Days 1-30 identify the winning themes; days 31-60 iterate winning theme × winning title × winning
thumbnail; days 61-90 concentrate production on the winning pattern. At day 90 the number to read is
not subscribers — it is **how many times the median impressions per video multiplied.**
