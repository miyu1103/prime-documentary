# PD-2026-004-ftx — Narration Script (English, v001)

- Episode: *He Promised to Give It All Away — The Hidden Line of Code Behind the $8 Billion FTX Fraud*
- Series: How the System Really Works, Episode 4 (follows Miranda, Gideon, Mapp).
- Tone: neutral, authoritative explainer. US English, plain and clear. Readability target grade 7–8.
- Target: ~12:00, ~1,850 words @ ~150 wpm. Final video is English only.
- Sourcing: every factual sentence tagged `[CLM-XXXX]` to a graded claim in `01_research/claims.v001.json`. Untagged lines are framing/transition, not new facts (rules/09).
- Structure (decisions/0004): flash-forward hook (5–8s) → cold open → opening (≤1 min) → 4-act body (each ends on a mini-cliffhanger) → ending (payoff + recap + like-ask + comment question + next-episode tease).
- Delivery: each section marked **[calm] / [building] / [intense]**. `[VO:]` = narration only. Bracketed non-`[CLM]` notes are production intent, NOT spoken.
- Growth design baked in (growth_strategy.v001): hard cold-open hook; "one line of code" open loop teased early, paid off in Act II; satisfying verdict payoff in Act IV with the single like-ask right after it; debate question at the end for comments.
- BAN guard active (R2): state ONLY adjudicated facts; he was **convicted**. Attribute trial assertions ("a co-founder testified…", "prosecutors said…"). No real-person likeness — anonymous silhouettes only. Don't imply crimes by people not convicted. "Not financial or legal advice" + AI-visuals disclosure at end.

---

## PRONUNCIATION NOTES

| Name / term | Pronunciation guide |
|---|---|
| Bankman-Fried | BANK-man FREED |
| FTX | "F-T-X" (letters) |
| Alameda | al-uh-MEE-duh |
| Gary Wang | GAIR-ee WAHNG |
| allow_negative | "allow negative" (read as two words) |
| Lewis Kaplan | LOO-iss KAP-lin |
| Bahamas | buh-HAH-muhz |

---

## FLASH-FORWARD HOOK — 0:00–0:08 — ~28 words [intense]

[VO:] One company held billions of dollars for a million people. It told them their money was safe. It wasn't. And the reason was hidden in a single line of code. [CLM-0005]

---

## COLD OPEN — 0:08–0:40 — ~80 words [building]

[VO:] This is the story of how roughly eight billion dollars of ordinary people's money [CLM-0004] disappeared — not in a crash, not in a hack, but through a setting buried in software that almost nobody was allowed to see. [CLM-0005]

[VO:] The man who built it was, for a moment, one of the most trusted people in finance. He said he wanted to give his entire fortune away. A New York jury would later find him guilty of fraud on every single count. [CLM-0001]

---

## OPENING — 0:40–1:35 — ~115 words [calm]

[VO:] When you hand your money to a bank or an exchange, you are trusting one invisible promise: that your money is still *yours* — that they are holding it, not spending it. [CLM-0005]

[VO:] FTX was a cryptocurrency exchange. People sent it their savings to buy and hold digital coins. [CLM-0005] And it made that same promise — your funds are your funds. [CLM-0005]

[VO:] Over the next twelve minutes: who Sam Bankman-Fried was and the image he built, the hidden door in the code that let his own trading firm reach into customer money [CLM-0005], where roughly eight billion dollars went [CLM-0004], the week it all collapsed, and the verdict that followed. [CLM-0001] Keep one thing in the back of your mind — that single line of code. We'll get to it.

---

## ACT I — THE GOLDEN BOY — 1:35–3:50 — ~330 words

**[calm]**

[VO:] To understand the fall, you have to understand the trust. Sam Bankman-Fried did not look like a villain. He looked like the opposite. [framing]

[VO:] He wore shorts and a rumpled T-shirt to meetings with the most powerful people in finance. He talked about giving nearly all of his money away to good causes — a philosophy he tied to a movement called effective altruism. [framing] The image was simple and powerful: a genius who didn't care about money, only about doing good. [framing]

**[building]**

[VO:] He ran two companies. One was FTX, the exchange where ordinary customers bought and stored crypto. [CLM-0005] The other was Alameda Research, a private trading firm — his own firm, betting on the markets for profit. [CLM-0005]

[VO:] On paper, those two were supposed to be strangers. The exchange holding your money is not supposed to be the same thing as a hedge fund gambling with money. The wall between them was the whole promise. [framing]

[VO:] Prosecutors would later call what happened one of the largest financial frauds in American history, comparing it to Bernie Madoff. [CLM-0002]

**[intense]**

[VO:] But in 2021, none of that was visible. FTX was everywhere — its name on a major arena, on television, beside famous athletes and politicians. [framing] Money poured in. A million customers trusted it. [CLM-0005]

[VO:] And behind the friendly image, behind the wall that was supposed to separate the exchange from his trading firm — there was a door. [framing] Someone had built it on purpose. [CLM-0005]

---

## ACT II — THE HIDDEN DOOR — 3:50–6:30 — ~400 words

**[calm]**

[VO:] Here is the line of code we promised you. [framing]

[VO:] At the trial, FTX's co-founder, Gary Wang, told the jury how it worked. [CLM-0005] When an ordinary customer tried to spend more money than they had, FTX did what any exchange does — it stopped them. Your balance can't go below zero. [CLM-0005]

**[building]**

[VO:] But Wang testified that the software had a special exception. [CLM-0005] One account was allowed to go negative — to keep taking money out even when it had nothing left. A setting in the code, which reporting at the trial described with the name **allow_negative**. [CLM-0005]

[VO:] That one account belonged to Alameda — Bankman-Fried's private trading firm. [CLM-0005]

**[intense]**

[VO:] Think about what that means. The firm gambling in the markets had a hidden line of credit running straight into the pile of customer deposits — a line far larger than any normal customer could ever have. [CLM-0005] [CLM-0006] Wang testified it was built on Bankman-Fried's instruction. [CLM-0005]

[VO:] So when Alameda made a bet and lost, it didn't run out of its own money. It could quietly keep reaching through that door — into the savings of people who thought their coins were just sitting there, safe. [CLM-0005]

**[building]**

[VO:] This is the part that makes the FTX story different from a simple "crypto crashed" headline. The money wasn't lost to bad luck in a market. The mechanism to spend customer money was deliberately built into the system — and hidden. [CLM-0005]

[VO:] It's an old crime wearing new technology. Spending the money people deposited with you, as if it were yours, has a name that is centuries older than crypto. [framing]

[VO:] And here's the quiet horror of it: as long as customers didn't all ask for their money back at the same time, no one would ever notice the door was open. [framing]

[VO:] Which raises the only question that was ever going to matter. [framing] What happens the day everyone asks at once? [framing]

---

## ACT III — THE WEEK IT COLLAPSED — 6:30–8:50 — ~360 words

**[calm]**

[VO:] In November 2022, confidence cracked. [CLM-0005] Reports raised doubts about how healthy FTX and Alameda really were, and customers started doing the one thing the hidden door could not survive. [framing]

**[building]**

[VO:] They asked for their money back. All at once. [framing]

[VO:] It's the oldest test of any institution that holds your cash: a run. [framing] In a few days, customers tried to pull billions of dollars off the exchange. [CLM-0005] A healthy exchange just gives it back — it's your money, it's right there. [framing]

[VO:] FTX couldn't. [CLM-0005] Because a huge share of what customers thought was sitting safely on the exchange wasn't there anymore. It had gone out through the door. [CLM-0005]

**[intense]**

[VO:] When the dust settled, the scale came into focus. Roughly eight billion dollars owed to FTX customers. [CLM-0004] About 1.7 billion to the company's investors. [CLM-0004] About 1.3 billion to Alameda's lenders. [CLM-0004]

[VO:] FTX filed for bankruptcy. [CLM-0005] The man who had promised to give his fortune away had, instead, presided over a hole roughly eight billion dollars deep in other people's money. [CLM-0004]

**[building]**

[VO:] One honest note, because accuracy matters: this was not eight billion dollars set on fire. Much of it had been moved, spent, and bet — and in the bankruptcy that followed, a large share was eventually recovered for customers. [CLM-0004] But "you'll probably get most of it back, years later, through a court process" is not the promise FTX made. The promise was: it's safe, it's here, it's yours. [framing] That promise was false. [CLM-0005]

[VO:] The next question was no longer about code or markets. It was about a person. Did he know? [framing]

---

## ACT IV — THE VERDICT — 8:50–10:50 — ~330 words

**[calm]**

[VO:] In the fall of 2023, Sam Bankman-Fried went on trial in a federal court in New York. [CLM-0001]

[VO:] His defense, in essence: mistakes were made, but not crimes — he hadn't meant to steal. [framing]

**[building]**

[VO:] The prosecution's case was built from the inside. His closest colleagues — the people who had run Alameda and built FTX's code with him — took the stand against him. [CLM-0005] The co-founder who described the hidden setting in the software. [CLM-0005] They testified that the use of customer money was no accident. [CLM-0005]

**[intense]**

[VO:] On November 2nd, 2023, the jury reached its verdict. [CLM-0001] It took only a few hours. [CLM-0001]

[VO:] Guilty. On all seven counts — wire fraud, conspiracy, and money laundering. Every single one. [CLM-0001]

[VO:] He had faced the possibility of decades — a statutory maximum reported as high as 115 years. [CLM-0002]

[VO:] On March 28th, 2024, the judge sentenced Sam Bankman-Fried to 25 years in federal prison [CLM-0003], and ordered the forfeiture of more than eleven billion dollars. [CLM-0003]

**[building — like-ask placed right after the payoff]**

[VO:] From the cover of a major magazine to a 25-year sentence — in about two years. [framing]

[VO:] *(If this finally made the FTX story make sense, take a second to hit like — it genuinely helps more people find clear explainers like this.)* [production: single like-prompt, warm tone]

---

## ENDING — RECAP, QUESTION & TEASE — 10:50–12:00 — ~230 words

**[calm]**

[VO:] So strip away the crypto, the shorts, the talk of saving the world, and what's left is very simple. [framing] An institution told people their money was safe. A hidden line of code let that money be spent. When everyone asked for it back, it was gone. And a jury called it what it was. [CLM-0005] [CLM-0001]

[VO:] There's a lesson here older than FTX, and it's free: if someone else holds your money, you are trusting them — not the technology. The promise "your funds are safe" is only ever as honest as the people who can reach the door. [framing]

[VO:] In crypto, people put it bluntly: *not your keys, not your coins.* [framing] But the deeper truth is bigger than crypto. It's the same question this channel keeps asking — what's really happening behind the words you're told to trust? [framing]

**[building — comment driver]**

[VO:] Here's the one we want to leave you on. Twenty-five years for an eight-billion-dollar fraud — is that too much, too little, or exactly right? [CLM-0003] [CLM-0004] Tell us below. And if you had money on FTX, we'd genuinely like to hear what that week was like for you. [framing]

[VO:] Next time, we stay with the question of trust and money — and a fraud from an age long before computers. [framing] Subscribe so you don't miss it.

[VO:] *(One note: this is a documentary explainer, not financial or legal advice. Dramatized scenes are symbolic reconstructions, generated with AI — not real footage of any person or event.)* [production: on-screen disclosure + lower-third]

---

## WORD/TIMING CHECK (production)
- Spoken words ≈ 1,850; at ~150 wpm ≈ 12:20 before pauses/beats. Trim transitions if final timing runs long.
- Every `[CLM]` tag must resolve to `01_research/claims.v001.json`. CLM-0004 and CLM-0006 are `needs_primary_confirm` — re-verify the $8B shortfall framing and the credit-line size against court record BEFORE script lock; keep "roughly/about" hedging.
- BAN/R2 check: no likeness named for depiction; verdict stated as fact; trial claims attributed; recovery nuance included; disclaimer present.
