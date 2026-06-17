# PD-2026-004-ftx — Narration Script (English, v002 — "like-worthy" punch-up)

- Episode: *He Promised to Give It All Away — The Hidden Line of Code Behind the $8 Billion FTX Fraud*
- Series: How the System Really Works, Episode 4 (follows Miranda, Gideon, Mapp).
- Tone: gripping, cinematic explainer with restraint. US English, plain, vivid. Readability grade 7–8.
- Target: ~12:00, ~1,880 words; final runtime hit by narration `atempo`, captions force-aligned (APR-0002).
- v002 changes (owner: "write it so an American would *definitely* hit Like"): visceral human cold-open;
  concrete shareable details (shorts + video games, Super Bowl ad, arena, $26B→0); a clearly illustrative
  victim beat; quotable hard lines ("It isn't 'crypto.' It's theft."); stronger emotional verdict payoff.
- Sourcing: factual sentences tagged `[CLM-XXXX]` to `01_research/claims.v001.json`. Untagged = framing/transition.
- BAN guard (R2): adjudicated facts only; he was **convicted**. Trial assertions attributed. No real-person
  likeness — anonymous silhouettes only. Endorsers/non-defendants never implied to be part of the fraud.
  Victim beat is explicitly illustrative ("picture one of them"), not a claimed individual. Disclaimer at end.

---

## PRONUNCIATION NOTES

| Name / term | Pronunciation guide |
|---|---|
| Bankman-Fried | BANK-man FREED |
| FTX | "F-T-X" (letters) |
| Alameda | al-uh-MEE-duh |
| Gary Wang | GAIR-ee WAHNG |
| allow_negative | "allow negative" (two words) |
| Lewis Kaplan | LOO-iss KAP-lin |

---

## FLASH-FORWARD HOOK — 0:00–0:10 — ~32 words [intense]

[VO:] It's 3 a.m. Somewhere in America, a man opens an app and stares at a number — his life savings. It's right there on the screen. He taps "withdraw." Nothing happens. It will never happen. [CLM-0005]

---

## COLD OPEN — 0:10–0:45 — ~85 words [building]

[VO:] He wasn't hacked. There was no crash that night. The money he was looking at had already been spent — quietly, for months — and the door that let it happen was a single setting hidden inside the company's own software. [CLM-0005]

[VO:] He was one of about a million people [CLM-0005] who trusted a company called FTX, and a 30-year-old who told the world he wanted to give his entire fortune away. [framing] Roughly eight billion dollars of their money would vanish. [CLM-0004] This is exactly where it went. [CLM-0005]

---

## OPENING — 0:45–1:35 — ~110 words [calm]

[VO:] Here's the only promise that matters when you hand someone your money: that it's still *yours*. That they're holding it — not spending it. [CLM-0005] FTX made that promise to a million customers. [CLM-0005]

[VO:] In about a year, you're going to watch a man go from a twenty-six-billion-dollar fortune [CLM-0007] and a Super Bowl ad [CLM-0008] to a prison sentence of twenty-five years. [CLM-0003]

[VO:] Over the next twelve minutes: the image he built, the hidden line of code that let his own hedge fund reach into customer money [CLM-0005], where the billions actually went, the week it all collapsed, and the verdict. [CLM-0001] Keep one thing in mind — that line of code. We'll get to it.

---

## ACT I — THE MOST TRUSTED MAN IN CRYPTO — 1:35–3:55 — ~340 words

**[calm]**

[VO:] To understand how eight billion dollars walks out the door, you have to understand why nobody was watching it. [framing]

[VO:] Sam Bankman-Fried did not look like a man stealing from anyone. That was the genius of it. [framing] He wore the same rumpled T-shirt and shorts to meet senators and billionaires. He slept on a beanbag chair at the office. He reportedly played a video game in the middle of an investor pitch — and they wired the money anyway. [CLM-0009]

**[building]**

[VO:] Because the story around him was irresistible: a math whiz who didn't care about money, who said he was only getting rich to give it all away to save the world. [framing] The scruffy genius you could trust precisely because he didn't seem to want anything. [framing]

[VO:] And the trust was everywhere. FTX bought a Super Bowl commercial. [CLM-0008] It put its name on the arena where an NBA team played. [CLM-0008] Famous athletes vouched for it. [CLM-0008] Money poured in from a million ordinary customers. [CLM-0005]

**[intense]**

[VO:] But there were really two companies. One was FTX — the exchange, where your money was supposed to just sit there, safe. [CLM-0005] The other was Alameda Research: his private hedge fund, making huge, risky bets to win. [CLM-0005]

[VO:] Those two were never supposed to touch. The wall between "money we're holding for customers" and "money we're gambling with" — that wall *was* the promise. [framing]

[VO:] Someone had cut a door through it. And it was built on purpose. [CLM-0005]

---

## ACT II — THE LINE OF CODE — 3:55–6:35 — ~400 words

**[calm]**

[VO:] Here's the line of code I promised you. It's almost insultingly simple. [framing]

[VO:] When a normal FTX customer tries to spend more money than they have, the software stops them cold. Your balance cannot go below zero. [CLM-0005] Same rule for everyone. [framing]

**[building]**

[VO:] Except it wasn't the same for everyone. At the trial, FTX's own co-founder, Gary Wang, told the jury the software had a secret exception. [CLM-0005] One account — and only one — was allowed to go negative. To keep pulling money out after it hit zero. Reporting at the trial described the setting by its name in the code: **allow_negative**. [CLM-0005]

[VO:] That one account belonged to Alameda. His hedge fund. [CLM-0005]

**[intense]**

[VO:] Sit with what that means. The firm placing the giant, risky bets had a secret tap running straight into the customers' deposits — a line of credit bigger than any real customer could ever have. [CLM-0005] [CLM-0006] Wang testified it was built on Bankman-Fried's instruction. [CLM-0005]

[VO:] So when Alameda bet and lost, it didn't run out of *its* money. It reached through the door — into the savings of people who thought their coins were just sitting there, untouched. [CLM-0005]

**[building]**

[VO:] And this is the part I want you to remember, because it cuts through all the jargon: there is an old, plain word for taking money people trusted you to hold, and spending it as your own. [framing]

[VO:] It isn't "crypto." It isn't "a liquidity issue." It's theft. [framing]

[VO:] Picture just one of those million customers. Not a trader — a nurse, a teenager, someone who put in the down payment for a house because an ad on the Super Bowl said it was safe. [CLM-0008] To them, the balance on the screen was real. [framing] On the night it mattered, it was a ghost. [CLM-0005]

[VO:] As long as everyone didn't ask for their money back at the same time, no one would ever see the door. [framing] Which leaves one question the whole thing was always going to come down to. [framing] What happens the day everyone asks at once? [framing]

---

## ACT III — THE WEEK IT ALL CAME DUE — 6:35–8:55 — ~360 words

**[calm]**

[VO:] November 2022. Confidence cracks. [CLM-0007] A report raises doubts about how solid FTX and Alameda really are, a rival pulls its support, and customers start doing the one thing the hidden door cannot survive. [framing]

**[building]**

[VO:] They ask for their money back. All of them. At once. [framing]

[VO:] It's the oldest test there is — a run. [framing] In days, customers try to yank billions off the exchange. [CLM-0005] A healthy company just hands it over. It's your money. It's right there. [framing]

[VO:] FTX couldn't. Because most of what customers thought was sitting safely on the exchange wasn't there anymore. [CLM-0005] It had gone out through the door, into bets, and deals, and spending. [CLM-0005]

**[intense]**

[VO:] Watch how fast a fortune built on trust evaporates when the trust is gone. By some estimates, Bankman-Fried's wealth fell from around sixteen billion dollars to under one billion — in a single day. [CLM-0007] Within days, effectively zero. [CLM-0007]

[VO:] And the hole he left behind: roughly eight billion dollars owed to customers. [CLM-0004] About 1.7 billion to investors. [CLM-0004] Another 1.3 billion to Alameda's lenders. [CLM-0004] FTX filed for bankruptcy. [CLM-0005] The man who said he'd give his fortune away had presided over a crater eight billion dollars deep — in other people's money. [CLM-0004]

**[building]**

[VO:] One honest note, because the truth should be exact: this was not eight billion dollars set on fire. The money was moved, bet, and spent — and through years of bankruptcy proceedings, much of it was eventually clawed back for customers. [CLM-0004] But "you'll get most of it back, years later, if you fight through a court" is not what the ad promised. [CLM-0008] The promise was: it's safe, it's here, it's yours. [framing] That was a lie. [CLM-0005]

[VO:] Which left one question that code and spreadsheets can't answer. Did he know? [framing]

---

## ACT IV — THE VERDICT — 8:55–10:55 — ~330 words

**[calm]**

[VO:] In the fall of 2023, Sam Bankman-Fried went on trial in a federal courtroom in New York. [CLM-0001] His defense, boiled down: mistakes were made — but not crimes. He didn't *mean* to. [framing]

**[building]**

[VO:] The problem was who sat in the witness chair. Not outside investigators — his own inner circle. [CLM-0005] The people who ran Alameda with him. The co-founder who built the code with him and described, out loud, the secret setting that let the money move. [CLM-0005] They testified the use of customer money was no accident. [CLM-0005]

**[intense]**

[VO:] On November 2nd, 2023, the jury went out. It was back in a few hours. [CLM-0001]

[VO:] Guilty. [CLM-0001]

[VO:] Not on some of it. On all seven counts — wire fraud, conspiracy, money laundering. Every. Single. One. [CLM-0001] Prosecutors called it one of the biggest financial frauds in American history. [CLM-0002]

[VO:] On March 28th, 2024, the judge sentenced him to twenty-five years in federal prison [CLM-0003] and ordered him to forfeit more than eleven billion dollars. [CLM-0003]

[VO:] From the cover of the magazines and a Super Bowl ad [CLM-0008] to a number on a prison door — in about two years. [CLM-0003] The arena that carried his company's name? They scrubbed it off the building. [CLM-0008]

**[like-ask — placed right after the payoff, warm]**

[VO:] *(If this finally made the FTX mess actually make sense — do me one favor and hit that like button. It genuinely helps these explainers reach the next person who got burned.)* [production: single like-prompt only]

---

## ENDING — THE LESSON, THE QUESTION, THE TEASE — 10:55–12:00 — ~225 words

**[calm]**

[VO:] Strip away the shorts, the beanbag, the talk of saving the world, and what's left is brutally simple. [framing] A company told a million people their money was safe. A hidden line of code let that money be spent. When everyone asked for it back, it was gone. And twelve strangers in a jury box called it exactly what it was. [CLM-0005] [CLM-0001]

[VO:] Here's the part that's free, and worth more than anything FTX ever sold: if somebody else holds your money, you are trusting *them* — not the technology, not the ad, not the genius in the T-shirt. "Your funds are safe" is only ever as honest as the person who can reach the door. [framing]

**[building — comment driver]**

[VO:] So I'll leave you with the argument everyone's still having. Twenty-five years, for an eight-billion-dollar fraud. [CLM-0003] [CLM-0004] Too much? Too little? Exactly right? Tell me below — and if you had money on FTX that week, I genuinely want to hear what it was like. [framing]

[VO:] Next time, same question — money, trust, and the people who break it — but a fraud from an age long before computers. [framing] Subscribe so you don't miss it.

[VO:] *(This is a documentary explainer — not financial or legal advice. The dramatized scenes are symbolic reconstructions generated with AI; they are not real footage of any person or event.)* [production: on-screen disclosure + lower-third]

---

## WORD/TIMING CHECK (production)
- Spoken words ≈ 1,880; ~150 wpm ≈ 12:30 raw → fit to 12:00 via narration `atempo` (APR-0002), captions force-aligned to the final master.
- Every `[CLM]` resolves to `01_research/claims.v001.json`. Re-verify CLM-0004 ($8B shortfall framing) and CLM-0006 (credit-line size, NOT amount stolen) against court record before narration record.
- R2 / BAN check: verdict + sentence stated as fact; trial claims attributed to testimony; endorsers never implied complicit (CLM-0008 notes); victim beat explicitly illustrative ("picture one of them"); recovery nuance kept; AI-visual + no-advice disclaimer present; no real-person likeness anywhere.
