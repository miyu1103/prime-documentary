# EP67 · TRANSUNION v. RAMIREZ — SCRIPT v001

**Design `EP67_ramirez_FILM_BIBLE.v001.md` · facts `EP67_ramirez_FACTS_LEDGER.v001.md` (the only
source) · front `EP67_ramirez_PACKAGING.v001.md` (§3 is fixed) · contract
`episodes/PD-2026-067-ramirez/episode_spec.v001.json` (`script_words` **[4400, 5000]**).**

**v002 · 2026-08-11 · +446 narration words over v001, pure insertion — not one word of v001 was
deleted or reworded.** v001's delivered ElevenLabs master measured **1448.020 s**, which with
`ENDCARD_SEC` 9.0 makes a **1457.0 s** film against `episode_spec.runtime_seconds` **[1560, 1895]** —
**103 s under its own declared floor.** The cause was a measuring-instrument error, not a short
script: the band was derived from `check_script_craft.narration_lines()` returning 4,682, a figure
that counted this front matter, the wrapped production notes and the closing appendix. The narration
index measured the spoken text at **4,044**. The instrument was fixed the same day; the words below
are the shortfall, written where the film was thin rather than where they were cheapest to add.

**Citation convention.** Every factual line is followed on the next line by an HTML comment carrying
its ledger row id. `check_script_craft.narration_lines()` now delegates to
`gen_narration_case.extract_events`, so what it counts is exactly what is sent to the provider:
comment lines, front matter, wrapped `【…】` notes and post-ENDING appendices are all excluded, and a
bold narration line is no longer skipped.

**Register.** Declarative. No adjective the record does not carry. Nothing tells the audience what to
feel. Three rules bind every page:

1. **Dissents are always attributed out loud.** "Justice Thomas wrote", "in dissent, Justice Kagan".
   Never in the film's own voice (⛔-06).
2. **The three money figures never touch.** The jury's $984.22 and $6,353.08 (MN-04); the Ninth
   Circuit's reduced $3,936.88 (MN-06); and the Supreme Court, which set no figure at all (MN-11).
3. **Nothing after 25 June 2021 is spoken** (⛔-12, ○-04). The ENDING says so out loud.

**Two sentences that will tempt a rewriter, and must not come back.** The Ninth Circuit's file opens
with ✓ *"TransUnion, aware that its practice was unlawful"* — that is the **court staff summary**,
which states of itself ✓ *"This summary constitutes no part of the opinion of the court."* It is not
in this script and must never be added (⛔-14). And it was **5–4**, never 6–3 (⛔-01).

---

## HOOK (voice from frame 0)

【0:00.0–0:21.2 · PACKAGING §3, approved shape, 56 words. Pictures: archive forecourt with a 6%
push-in → car lot row → car door and window (R007) → three backs at a sales desk (R073) → hand on
keyboard (R075) / monitor back (R005) / keys on the desk (R004), 1.9 s each with 0.35 s
motion-blurred pushes → 4 frames at black-level 12% → wide of the empty forecourt through showroom
glass (R009) → the envelope on the kitchen table (R018). Nothing on any screen is legible. Re-time
against the delivered ElevenLabs master before captions are locked.】

Dublin, California. February 27th, 2011.
<!-- SR-01 ✓ VERBATIM ("On February 27, 2011, Ramirez visited a Nissan dealership in Dublin, California") -->

Sergio Ramirez has come to buy a Nissan Maxima.
<!-- SR-01 ✓ VERBATIM ("seeking to buy a Nissan Maxima") -->

His wife is with him, and his father-in-law.
<!-- SR-01 ✓ VERBATIM ("Ramirez was accompanied by his wife and his father-in-law") -->

The salesman runs a credit check, and says Nissan will not sell him the car.
<!-- SR-02 (the report TransUnion produced carried the alert) · SR-03 ✓ VERBATIM ("A Nissan salesman told Ramirez that Nissan would not sell the car to him"). The salesman is not named, described or given a second line, here or anywhere — ⛔-08. -->

His name is on a terrorist list.
<!-- SR-03 ✓ VERBATIM ("because his name was on a ' \"terrorist list.\" ' "). Spoken as the salesman's sentence; an attributed quotation card carries it on screen at 0:13.9. -->

The letter that follows will not say how to argue with it.
<!-- SR-10 ✓ VERBATIM ("the OFAC Letter did not include instructions for initiating a dispute") -->

---

## OP

【The brand band rises at 0:21.6 over the envelope and falls at 0:25.1 — PACKAGING §4,
`openingVariant: 'overlay'`, `leadSeconds: 0`. Picture and voice do not stop under it.】

His wife buys the car in her own name.
<!-- SR-04 ✓ VERBATIM ("Ramirez's wife had to purchase the car in her own name") -->

Everything that happens after that — a jury, an appeal, and the Supreme Court of the United States — turns on one question. Not whether the list was wrong about him. Whether the piece of paper it was written on ever left the building.
<!-- HD-06 (the standing inquiry distinguishes internal credit files from disseminated consumer reports). States the shape of the question and withholds the answer; no outcome, no vote, no figure. -->

---

## ACT_1 — ONE MAN AT A COUNTER

【R001–R017 and R073–R082. 2011 era: bright daylight, glass, chrome. Motif state 1 at 3:40 — the
drawer closed, one envelope on the desk above it (R032).】

The dealership ran his credit, the way a dealership does.
<!-- SR-02 -->

What came back was a report produced by TransUnion, and it carried an alert across the top of it. The alert said that the name that had been entered matched a name on something called the OFAC database.
<!-- SR-02 ✓ VERBATIM ("Ramirez's credit report, produced by TransUnion, contained the following alert: '***OFAC ADVISOR ALERT - INPUT NAME MATCHES NAME ON THE OFAC DATABASE.'"). On screen as attributed typography, never as an image of a document — ⛔-13. -->

A salesman told him Nissan would not sell him the car, because his name was on a terrorist list.
<!-- SR-03 ✓ VERBATIM -->

That is the entire record of what was said at that counter. Nobody in this film knows what the salesman was looking at, or what he had been told, because no court ever asked him. He was not a party. He is not named anywhere in either opinion.
<!-- ⛔-08 · ND-08 (neither opinion evaluates the dealership's or the salesman's conduct) -->

His wife bought the car in her own name.
<!-- SR-04 ✓ VERBATIM -->

The next day, Ramirez asked TransUnion for his own credit file.
<!-- SR-05 -->

They sent it the same day. It came with the standard federal summary of a consumer's rights, and it did not mention the alert at all.
<!-- SR-05 (TU @16473 — the credit-file mailing omits the OFAC alert and encloses the CFPB summary of rights) -->

The day after that, a second envelope arrived. This one was about the alert. It told him that the name on his TransUnion credit file was considered a potential match to information on a United States Treasury database — and it did not enclose another copy of his rights.
<!-- SR-05 (TU @16687) · SR-06 ✓ VERBATIM ("the name that appears on your TransUnion credit file 'SERGIO L RAMIREZ' is considered a potential match to information listed on the United States Department of Treasury's Office of Foreign Asset Control ('OFAC') Database") -->

Then the letter explained how this sort of thing is supposed to be checked.
<!-- SR-07 -->

Financial institutions, it said, are required to check customers' names against the OFAC database, and if a potential name match is found, to verify whether their potential customer is the person on the database. For that reason, it said, some institutions may ask for your date of birth, or ask to see a government-issued form of identification.
<!-- SR-07 ✓ VERBATIM (CA9 @13387; the source's run-together "governmentissued" is a line-break artefact of the PDF) -->

That is TransUnion's own letter, describing the check a bank should make. A date of birth. A piece of identification. Something other than a name.
<!-- SR-07. The comparison is the film's, and it is a comparison of the letter with itself — no claim about intent, ⛔-05. -->

And enclosed with it were the OFAC records for the two people he had supposedly matched. The Ninth Circuit describes what those records contained. First, middle and last names. Dates of birth. Passport information.
<!-- SR-08 ✓ VERBATIM, as the court's bracketed description of the enclosure — NOT as words of the letter. The two individuals are never named or characterised: ⛔-09. -->

He had two mailings in front of him now. One said nothing about any alert. The other said he was a potential match to a Treasury list. Ramirez testified that he was confused by them. The absence of any OFAC information in the credit-report mailing suggested the alert had been removed. The other mailing suggested otherwise.
<!-- SR-09 ✓ VERBATIM (both sentences: "Ramirez testified that he was confused by the two mailings." / "The lack of any OFAC information in the creditreport mailing suggested the alert had been removed, but the OFAC Letter mailing suggested otherwise.") -->

Neither one told him how to dispute anything.
<!-- SR-10 ✓ VERBATIM -->

He cancelled a trip he had planned. The Ninth Circuit calls it an international vacation he had planned with his family. The Supreme Court says he consulted a lawyer and ultimately cancelled a planned trip to Mexico.
<!-- SR-10 ✓ VERBATIM ("Concerned about possible consequences of the OFAC match, Ramirez canceled an international vacation he had planned with his family") · SR-11 ✓ VERBATIM ("Ramirez consulted a lawyer and ultimately canceled a planned trip to Mexico"). Both descriptions are read out and attributed to their courts rather than merged — ⛔-15 forbids synthesising a third version. -->

TransUnion eventually removed the alert from his file.
<!-- SR-11 ✓ VERBATIM ("TransUnion eventually removed the OFAC alert from Ramirez's file.") -->

So that is one man, over about a week, in one town. A car he did not buy. Two letters that disagreed with each other. A lawyer. A trip he did not take.
<!-- SR-01, SR-04, SR-05, SR-09, SR-10, SR-11 — a recapitulation, no new fact. -->

Everything past that point is about a question he could not have asked at the counter, because nobody at the counter could have answered it. How did a machine decide that his name was on that list?
<!-- Transition. States a question, asserts nothing about anyone's knowledge. -->

---

## ACT_2 — TWO WORDS

【R054–R072 and R083–R084. The identifier stack builds through this act. AE beat
`ep67_kin_two_words` lands at ≈9:55 on the line marked below. Motif state 2 at 9:50 — the drawer
opens on rows of identical cards (R034).】

The list is real, and it belongs to the Treasury.
<!-- LS-01 -->

The Office of Foreign Assets Control publishes a list of individuals and companies owned or controlled by, or acting for or on behalf of, targeted countries. It also lists individuals, groups and entities — such as terrorists and narcotics traffickers — designated under programs that are not country-specific. Collectively, they are called Specially Designated Nationals.
<!-- LS-01 ✓ VERBATIM (ofac.treasury.gov FAQ topic 1631) -->

Their assets are blocked, and United States persons are generally prohibited from dealing with them.
<!-- LS-02 ✓ VERBATIM -->

Treasury puts it more exactly than that. United States persons are prohibited from engaging in any transactions with Specially Designated Nationals, and must block any property in their possession or under their control in which one of them has an interest.
<!-- LS-03 ✓ VERBATIM. The source writes "SDNs"; the abbreviation is read out in full because the term was defined two lines earlier. -->

The Supreme Court's own summary is shorter. Individuals on the OFAC list are terrorists, drug traffickers, or other serious criminals. It is generally unlawful to transact business with any person on the list.
<!-- LS-04 ✓ VERBATIM (TU @14119) -->

How long is the list? On the eight Treasury pages retrieved for this film, there is no current count of any kind. There is one official figure, from a 2021 sanctions review, which speaks of over twelve thousand OFAC designations — but that is a cumulative count of designations, not the size of the list today.
<!-- LS-05 ✓ VERBATIM ("the over 12,000 OFAC designations") · ⛔-11 -->

We counted the file ourselves. Treasury publishes the list as a data file, and the copy dated the seventh of August, 2026 holds nineteen thousand, one hundred and ninety-nine records. That is our count of their file. It is not a Treasury statement, and we are not going to present it as one.
<!-- LS-05 (own arithmetic, labelled) · ⛔-11 — the figure is attributed to our own count on air, exactly as the ledger requires. -->

Which brings us to the part of this story that decides it. OFAC does not simply publish names. It publishes, alongside them, the things that tell one human being from another.
<!-- LS-08 -->

An entry often will have, for example, a full name, an address, a nationality, a passport, a tax identification or cedula number, a place of birth, a date of birth, former names, and aliases.
<!-- LS-08 ✓ VERBATIM (ofac.treasury.gov FAQ 5). This is the list that builds on screen, one item at a time — film bible §10. -->

And none of that is buried in prose. Treasury publishes it as data. The release consists of three linked files — the main sanctions list, a separate file of addresses, and a separate file of alternate names — so that a machine can read a nationality, a passport number or a date of birth as its own field.
<!-- LS-12 ✓ (ofac/ofac_sdn_dat_spec.txt — the SDN data release is three linked tables) · LS-08 -->

And OFAC tells you what to do with them. Its own procedure, published for anyone who screens names, runs in steps.
<!-- LS-06 -->

Step three. How much of the listed entry's name is matching against the name in your transaction? Is just one of two or more names matching — just the last name? If yes, you do not have a valid match.
<!-- LS-06 ✓ VERBATIM -->

Step four. Compare the complete sanctions list entry with all of the information you have on the matching name in your transaction. Are you missing a lot of this information? If yes, go back and get more information, and then compare your complete information against the entry.
<!-- LS-07 ✓ VERBATIM -->

OFAC knows what happens when you skip that. It has a term for a name so broad or generic that it generates a large volume of false hits when it is run through a computer-based screening system. It calls it a weak alias.
<!-- LS-09 ✓ VERBATIM -->

Its own search tool carries a warning that using it is not a substitute for undertaking appropriate due diligence. The tool works on approximate string matching. Its scoring runs on Jaro-Winkler, a string difference algorithm, and Soundex, a phonetic algorithm. It is built, in other words, to return things that are nearly right, so that a person can then check them.
<!-- LS-11 ✓ VERBATIM (three separate quotations, all located) -->

And OFAC has a page written for the ordinary person whose credit report has one of these alerts on it. It says the alert is merely a reminder to the person checking your credit that he or she should verify whether you are the individual on one of OFAC's sanctions lists, by comparing your information to the OFAC information. If you are not that individual, it says, the person checking your credit should disregard the alert.
<!-- LS-10 ✓ VERBATIM -->

Now. Beginning in 2002, TransUnion introduced an add-on product called OFAC Name Screen Alert.
<!-- LS-13 ✓ VERBATIM -->

Here is how it worked, in the Supreme Court's words. If the consumer's first and last name matched the first and last name of an individual on OFAC's list, then TransUnion would place an alert on the credit report indicating that the consumer's name was a potential match to a name on the OFAC list.
<!-- LS-14 ✓ VERBATIM (first half) -->

**TransUnion did not compare any data other than first and last names.**
<!-- LS-14 ✓ VERBATIM (second half). AE BEAT `ep67_kin_two_words` — FIRST NAME / LAST NAME / NOTHING ELSE, 3.2 s, lands on this line. -->

The software came from a vendor called Accuity. The Ninth Circuit describes what it did. Accuity's software conducted a name-only search, running a consumer's first and last name against the names on the OFAC list. A search would result in a match if the consumer's first and last name were either identical or similar to a name on the list. The court's own example is that Cortez would match with Cortes.
<!-- LS-16 ✓ VERBATIM (CA9 @16677) -->

Unsurprisingly, the Supreme Court says, the product generated many false positives. Thousands of law-abiding Americans happen to share a first and last name with one of the terrorists, drug traffickers or serious criminals on OFAC's list.
<!-- LS-15 ✓ VERBATIM -->

That is not the sentence that decides this case, though. This one is, and it is a footnote.
<!-- LS-17 -->

In collecting other types of data for use on consumer reports — such as tax liens or bankruptcy judgments — TransUnion used at least one additional identifier other than the consumer's name. An address. A date of birth. A social security number. OFAC information was the only consumer-report data that TransUnion collected using name alone.
<!-- LS-17 ✓ VERBATIM (CA9 footnote 2) -->

The company could do it. It did do it, everywhere else on the same page of the same report. For a tax lien, a name was not enough. For a terrorist list, it was.
<!-- LS-17. A restatement of the footnote's two halves. No claim about intent, motive or knowledge — ⛔-05. -->

There is a second footnote, and it is shorter. TransUnion presented no data showing that any of its name matches through the OFAC product were correct. In other words — and this is the court's own phrasing — TransUnion could not confirm that a single OFAC alert sold to its customers was accurate.
<!-- LS-19 ✓ VERBATIM (CA9 footnote 4) -->

When it first began offering the product, the company had determined that the alerts it was placing on consumer credit reports were exempt from the Fair Credit Reporting Act.
<!-- LS-20 ✓ VERBATIM ("When TransUnion first began offering the OFAC Advisor product, it determined that the OFAC alerts being placed on consumer credit reports were exempt from the FCRA") -->

That was the position. Whether it was right is the next act.
<!-- Transition. -->

---

## ACT_3 — THE WARNING, AND THE JURY

【R042–R053, R085–R089, R105–R112. Mixed era. AE beats `ep67_kin_cortez_dates` ≈13:05,
`ep67_kin_8185` ≈15:40, `ep67_kin_jury_award` ≈17:50. Motif state 3 at 16:20 — one card leaves the
drawer (R036).】

In 1970, Congress passed and President Nixon signed the Fair Credit Reporting Act.
<!-- MN-09 ✓ VERBATIM -->

Among other things, it requires a consumer reporting agency to follow reasonable procedures to assure maximum possible accuracy in the reports it prepares.
<!-- MN-09 ✓ VERBATIM ("follow reasonable procedures to assure maximum possible accuracy") -->

What "reasonable procedures" means, when the data is an OFAC alert, had been said out loud once already. In 2005, a consumer sued.
<!-- N9-01 · TH-04 ✓ VERBATIM ("In 2005, a consumer sued.") -->

Justice Thomas set out her case in his dissent in this one. TransUnion had sold an OFAC credit report about her to a car dealership. The report flagged her — Sandra Jean Cortez, born in May 1944 — as a match for a person on the OFAC list: Sandra Cortes Quintero, born in June 1971.
<!-- TH-04 ✓ VERBATIM. Attributed to Thomas out loud, as ⛔-06 requires. The Cortez opinion itself was not retrieved (○-03), so nothing further about her case is spoken. -->

There is one more thing in Justice Thomas's account of that case. When Sandra Cortez asked TransUnion for her own credit report, the alert was not in what they sent her. It stayed on the file, and it stayed there for years.
<!-- TH-04 ✓ (TransUnion withheld the alert from the report Cortez requested and kept it in place for years). Attributed to Thomas, ⛔-06. The rhyme with SR-05 is left for the audience to hear; the film does not point at it. -->

Twenty-seven years apart. A jury awarded her fifty thousand dollars in actual damages and seven hundred and fifty thousand in punitive damages. The district court cut the punitive award to a hundred thousand, and in August 2010 the Third Circuit affirmed that — stressing that TransUnion's failure to, at the very least, compare birth dates when they are available, was reprehensible.
<!-- TH-04 ✓ VERBATIM ("The jury awarded $50,000 in actual damages and $750,000 in punitive damages"). LEDGER ADDENDUM, located by exact string search in the cached sources on 2026-08-11 and NOT yet a ledger row: ✓ "The District Court reduced the punitive damages award to $100,000, which the Third Circuit affirmed on appeal" (TU @67378) and ✓ "at the very least, compar[e] birth dates when they are available" ... "reprehensible" (TU @67530); ✓ "The district court remitted the punitive damages to $100,000, but otherwise upheld the verdict" (CA9 @19720); ✓ "In August 2010, the Third Circuit flatly rejected th[at argument]" (CA9 @19999). AN EARLIER DRAFT OF THIS LINE SAID THE THIRD CIRCUIT AFFIRMED THE $750,000 — it did not, and this is the correction. Add these four rows to the ledger as TH-04b before the script is approved. AE BEAT `ep67_kin_cortez_dates` — BORN MAY 1944 / MATCHED TO / BORN JUNE 1971, 3.2 s, lands here. -->

The Ninth Circuit, years later, described what that decision had established, and what happened next.
<!-- N9-01 -->

Plaintiffs presented evidence that, despite being told in 2010 by another circuit court that OFAC alerts were covered by the Fair Credit Reporting Act and subject to the reasonable procedures requirement, TransUnion continued to use name-only searches to produce OFAC matches.
<!-- N9-01 ✓ VERBATIM -->

Most notably, the Ninth Circuit wrote, the Third Circuit specifically reprimanded TransUnion for failing to use an additional identifier such as date of birth to verify the accuracy of OFAC matches.
<!-- N9-02 ✓ VERBATIM -->

Despite this warning, TransUnion continued to use problematic matching technology, and to treat OFAC information as separate from other types of information on consumer reports. In doing so, the court held, it ran an unjustifiably high risk of error.
<!-- N9-03 ✓ VERBATIM. This is the outer limit of what this film says about the company's conduct; nothing about knowledge, intent or motive is added — ⛔-05. -->

That is what a court found, on evidence, and it is where this film's account of the company's conduct stops.
<!-- ⛔-05, stated on air. -->

Between the first of January and the twenty-sixth of July, 2011, the letters kept going out.
<!-- MN-01 ✓ VERBATIM (the class period) -->

TransUnion sent the same OFAC letter to eight thousand, one hundred and eighty-four other consumers who had also requested copies of their credit reports in that window.
<!-- SR-13 ✓ VERBATIM -->

In July 2011, TransUnion finally stopped sending the letters, and began including OFAC alerts directly on the credit reports it sent to consumers.
<!-- LS-21 ✓ VERBATIM -->

Ramirez sued in February 2012. In 2014 the district court certified a class. In 2016 it held that all of them had standing to be there.
<!-- ID-08 -->

The class the court certified was defined by a letter. All natural persons in the United States and its Territories to whom TransUnion sent a letter similar in form to the March 1st, 2011 OFAC Letter it sent to Ramirez, from January 1st, 2011 to July 26th, 2011.
<!-- MN-01 ✓ VERBATIM (CA9 @25411). The source's bracketed substitutions are read as the words they stand for; no detail is added to them. -->

Before trial, the two sides agreed on the numbers, so that no jury would have to find them.
<!-- MN-02 -->

The parties stipulated that the class contained eight thousand, one hundred and eighty-five members, including Ramirez.
<!-- MN-02 ✓ VERBATIM. AE BEAT `ep67_kin_8185` — 8,185 / PEOPLE, INCLUDING RAMIREZ, 2.4 s. -->

And they stipulated that only one thousand, eight hundred and fifty-three of them — Ramirez among them — had their credit reports disseminated by TransUnion to potential creditors during that same period.
<!-- MN-02 ✓ VERBATIM -->

Hold on to those two numbers. Everything left in this film is the distance between them.
<!-- MN-03 — states the arithmetic relationship without yet naming 6,332. -->

There were three claims, and all three were about willfulness, because statutory and punitive damages are available under the Act for willful violations and not for negligent ones.
<!-- MN-10 ✓ VERBATIM ("Ramirez and the class pursued only a willfulness theory for each of their three claims, presumably because statutory and punitive damages are available for willful, but not negligent, FCRA violations.") · MN-08 -->

One: a willful failure to follow reasonable procedures to assure accuracy. Two: a willful failure to disclose the whole file, because the copies sent to consumers left the alerts out. Three: a willful failure to provide the summary of rights with the second mailing.
<!-- MN-08 (CA9 @1220 — the three claims, with their statutory subsections) -->

The trial ran six days.
<!-- MN-04 ✓ VERBATIM ("After six days of trial") -->

Ramirez testified about what happened at the dealership. He did not present evidence about the experiences of other members of the class — and that absence will matter enormously in about ten minutes.
<!-- MN-04 · SR-15 ✓ VERBATIM ("At trial, Ramirez testified about his experience at the Nissan dealership. But Ramirez did not present evidence about the experiences of other members of the class.") -->

The jury returned a verdict for the plaintiffs, and it awarded the same amount to every one of them. Nine hundred and eighty-four dollars and twenty-two cents in statutory damages. Six thousand, three hundred and fifty-three dollars and eight cents in punitive damages. Each.
<!-- MN-04 ✓ VERBATIM. AE BEAT `ep67_kin_jury_award` — $984.22 STATUTORY / $6,353.08 PUNITIVE / TO EACH OF THEM, 3.2 s. -->

More than sixty million dollars.
<!-- MN-04 ✓ VERBATIM ("for a total award of more than $60 million") -->

TransUnion appealed, and it appealed to a court that mostly agreed with the jury. The Ninth Circuit affirmed the verdict and the judgment. It held that the punitive award was excessive under constitutional due process, and it reduced it — from six thousand, three hundred and fifty-three dollars and eight cents per class member to three thousand, nine hundred and thirty-six dollars and eighty-eight cents.
<!-- MN-06 ✓ VERBATIM (both quotations). THE REDUCTION IS THE NINTH CIRCUIT'S, in 2020, before the Supreme Court touched the case — ⛔-03. -->

On the willfulness question it was blunt. The jury's verdict, it said, is consistent with the law and supported by substantial evidence.
<!-- N9-03 ✓ VERBATIM -->

The opinion was filed on the twenty-seventh of February, 2020 — nine years to the day after the afternoon in Dublin.
<!-- ID-06 ✓ VERBATIM ("Filed February 27, 2020") · SR-01 ✓ VERBATIM ("On February 27, 2011"). The interval is calendar arithmetic on two verbatim dates and asserts nothing else. -->

It also set out, in a list, what separated Ramirez from everybody else in the class. His credit report with the false OFAC alert was sent to a third party. His alert said that he was a match, instead of a potential match. He was denied credit because of the alert. He cancelled a vacation because of the alert. And he spent significant time and energy trying to remove the alert, including hiring a lawyer.
<!-- SR-12 ✓ VERBATIM (CA9 @68241). Nothing is added to the five items and nothing is interpreted; ⛔-07 holds. -->

Three judges heard that appeal, and they did not agree with each other. Judge Murguia wrote the opinion. Judge McKeown concurred in part and dissented in part. She would have held that only the 1,853 had standing on the accuracy claim, and only Ramirez on the other two.
<!-- ID-06, ID-07 ✓ VERBATIM ("Opinion by Judge Murguia; Partial Concurrence and Partial Dissent by") · N9-06. Her separate opinion was not read line by line (○-01), so her result is given and her reasoning is not. -->

Nobody paid much attention to that at the time. It is, almost exactly, what the Supreme Court was about to say.
<!-- N9-06 — a comparison of two stated results, not a claim about influence. -->

---

## ACT_4 — NO CONCRETE HARM, NO STANDING

【TURN at 18:30: music out, 2.5 s of silence, then the first line below over R042 — the first time
the film leaves the counter for stone. R042–R053, R090–R091. AE beats `ep67_kin_five_four` ≈19:10,
`ep67_kin_1853_6332` ≈22:20. Motif state 4 at 21:00 — the drawer closes with the cards still in it
(R037, R038).】

To have Article III standing to sue in federal court, plaintiffs must demonstrate, among other things, that they suffered a concrete harm. No concrete harm, no standing.
<!-- HD-01 ✓ VERBATIM — the opening lines of the opinion. -->

That is the first thing the Supreme Court of the United States said about this case, on the twenty-fifth of June, 2021. Justice Kavanaugh delivered the opinion of the Court.
<!-- ID-01 ✓ · ID-02 ✓ VERBATIM -->

He was joined by the Chief Justice and by Justices Alito, Gorsuch and Barrett. Justice Thomas filed a dissent, joined by Justices Breyer, Sotomayor and Kagan. Justice Kagan filed a second dissent, joined by Breyer and Sotomayor.
<!-- ID-03 ✓ VERBATIM -->

Five to four.
<!-- ID-04 ✓. AE BEAT `ep67_kin_five_four` — 5–4 / FIVE JUSTICES. FOUR IN DISSENT., 2.4 s. This film does not say six to three, and the arithmetic is on screen so that nobody can — ⛔-01. -->

The holding is one sentence long. Only plaintiffs concretely harmed by a defendant's statutory violation have Article III standing to seek damages against that private defendant in federal court.
<!-- HD-02 ✓ VERBATIM -->

Congress can write a law that says a company owes you something. The company can break it. That, on its own, does not get you into a federal courtroom. Article III standing requires a concrete injury even in the context of a statutory violation.
<!-- HD-05 ✓ VERBATIM (quoting Spokeo) · HD-14 (the approved plain-English gloss, spoken in the film's own voice and never as the Court's words) -->

An injury in law is not an injury in fact.
<!-- HD-04 ✓ VERBATIM -->

So where is the line? The Court drew it in a place that has nothing to do with whether the alert was true.
<!-- HD-06 -->

The standing inquiry in this case, the Court wrote, distinguishes between credit files that consumer reporting agencies maintain internally, and the consumer credit reports that consumer reporting agencies disseminate to third-party creditors.
<!-- HD-06 ✓ VERBATIM -->

The mere presence of an inaccuracy in an internal credit file, if it is not disclosed to a third party, causes no concrete harm.
<!-- HD-07 ✓ VERBATIM -->

And then the Court chose an image for it.
<!-- HD-08 -->

The plaintiffs' harm, it said, is roughly the same, legally speaking, as if someone wrote a defamatory letter and then stored it in her desk drawer. A letter that is not sent does not harm anyone, no matter how insulting the letter is. So too here.
<!-- HD-08 ✓ VERBATIM. Motif state 4 lands on this line — the drawer closes with the cards inside. -->

What about the risk that it would be sent later? The Court held that risk — the risk of dissemination to third parties — was too speculative to support Article III standing in a suit for damages.
<!-- HD-09 ✓ VERBATIM · ND-05 (a material risk of future harm can satisfy concreteness in a claim for injunctive relief; this was a damages suit) -->

So the eight thousand, one hundred and eighty-five split in two.
<!-- HD-11 -->

One thousand, eight hundred and fifty-three class members, whose credit reports were provided to third-party businesses, suffered a concrete harm, and had standing on the accuracy claim. Six thousand, three hundred and thirty-two class members, whose credit reports were not provided to third-party businesses, did not suffer a concrete harm, and did not have standing on it.
<!-- HD-11 ✓ VERBATIM · MN-03 (8,185 − 1,853 = 6,332, and the opinion states all three numbers itself). AE BEAT `ep67_kin_1853_6332` — 1,853 COULD SUE / 6,332 COULD NOT / SAME FALSE FLAG, 3.2 s. -->

As for the two claims about the format of the mailings — the incomplete file and the missing summary of rights — none of the 8,185 other than Ramirez himself had suffered a concrete harm at all.
<!-- HD-11 ✓ VERBATIM -->

The judgment below was reversed, and the case was remanded for further proceedings. Not dismissed. Not decided against the class on the merits. Sent back.
<!-- HD-12 ✓ VERBATIM · ⛔-02 — the film says out loud that the case was not thrown out. -->

On remand, the Court said, the Ninth Circuit may consider in the first instance whether class certification is appropriate in light of our conclusion about standing.
<!-- HD-13 ✓ VERBATIM -->

Now. It would be very easy to make the majority sound stupid here, and it was not.
<!-- Transition into HD-10, per film bible §2 problem 2. -->

Here is the strongest thing in the opinion, and it is aimed straight at the 6,332. The plaintiffs did not present any evidence that those class members even knew that there were OFAC alerts in their internal TransUnion credit files.
<!-- HD-10 ✓ VERBATIM -->

If those plaintiffs prevailed in this case, the Court wrote, many of them would first learn that they were injured when they received a check compensating them for their supposed injury.
<!-- HD-10 ✓ VERBATIM -->

The Ninth Circuit had recorded the same absence from the other direction. Only a quarter of the other class members had their credit reports sent to a third party during the class period, it wrote, and there was no evidence regarding whether other class members had experiences similar to Ramirez's as a result of the alerts. That gap is not a gap in this film. It is a finding in the record, and the majority is standing on it.
<!-- SR-14 ✓ VERBATIM (CA9 @68593) · HD-10 · ○-06 — film bible §13 item 4: the absence is stated out loud because the majority relied on it. The same number returns in ACT_5 in Justice Kagan's phrasing (KG-06), read the other way. -->

【4 seconds. R091 — the empty kitchen at night. No music.】

That is a real problem, and a court is entitled to notice it. A person who never learned of an entry that never moved is going to have a hard time saying what it did to them.
<!-- HD-10 · ○-06 — the film states the majority's argument at its strongest before answering it. -->

Four justices had an answer.
<!-- Transition to ACT_5. -->

---

## ACT_5 — THE ANSWER, AND WHAT WAS NOT DECIDED

【R042–R053, R092–R094, R039. RECOGNITION at 27:10 on the Kagan line. Motif state 5 at 26:10 — the
drawer closed, and a single blank slip on the desk above it (R039).】

Justice Thomas wrote first, for himself and three colleagues, and he began with the facts rather than the doctrine. TransUnion, he wrote, generated credit reports that erroneously flagged many law-abiding people as potential terrorists and drug traffickers.
<!-- TH-01 ✓ VERBATIM. Attributed twice in one sentence, deliberately — ⛔-06. -->

Yet despite Congress's judgment that such misdeeds deserve redress, he went on, the majority decides that TransUnion's actions are so insignificant that the Constitution prohibits consumers from vindicating their rights in federal court. The Constitution does no such thing.
<!-- TH-02 ✓ VERBATIM -->

On the machine itself he was brief. The system TransUnion used to decide which individuals to flag, he wrote, was rather rudimentary. It compared only the consumer's first and last name with the names on the OFAC list. It did not compare birth dates, middle initials, social security numbers, or any other available identifier routinely used to collect and verify credit-report data.
<!-- TH-03 ✓ VERBATIM · LS-18 ✓ VERBATIM -->

And he answered the majority's best argument with one line from the trial record. Quoting the Ninth Circuit's footnote, he wrote that TransUnion could not confirm that a single OFAC alert sold to its customers was accurate.
<!-- TH-06 ✓ VERBATIM (TU @100922, quoting CA9 @24648) · LS-19 -->

Think about what that does to the desk-drawer letter. The question was whether an alert sitting in a file, unsent, had harmed anybody. The company that wrote it could not show that even one of the ones it *had* sent was correct.
<!-- LS-19 · HD-08. The inference is stated as a comparison of two record facts and is not attributed to any court. -->

One need only tap into common sense, Justice Thomas wrote, to know that receiving a letter identifying you as a potential drug trafficker or terrorist is harmful. All the more so when the information comes in the context of a credit report, the entire purpose of which is to demonstrate that a person can be trusted.
<!-- TH-05 ✓ VERBATIM -->

He also thought the decision might not do what TransUnion wanted. State courts are not bound by the limitations of a case or controversy, or other federal rules of justiciability, even when they address issues of federal law. If federal courts are closed to these plaintiffs, state courts are not — and a defendant cannot remove a case to a forum that has no jurisdiction over it. He called that a possible pyrrhic victory for TransUnion.
<!-- TH-08 ✓ VERBATIM (both quotations) -->

And then Justice Thomas ended by counting. Who could possibly think, he wrote, that a person is harmed when he requests and is sent an incomplete credit report, or is sent a suspicious notice informing him that he may be a designated drug trafficker or terrorist, or is not sent anything informing him of how to remove this inaccurate red flag?
<!-- TH-09 ✓ VERBATIM (TU @102152). Attributed twice, ⛔-06. -->

The answer, he wrote, is of course legion: Congress, the President, the jury, the District Court, the Ninth Circuit, and four Members of this Court.
<!-- TH-09 ✓ VERBATIM. Four. The dissent counts its own side, which is why this film can never say six to three — ID-03, ID-04, ⛔-01. -->

Justice Kagan wrote separately, and shorter. The Court here, she wrote, transforms standing law from a doctrine of judicial modesty into a tool of judicial aggrandizement. It holds, for the first time, that a specific class of plaintiffs whom Congress allowed to bring a lawsuit cannot do so under Article III.
<!-- KG-01 ✓ VERBATIM -->

To say, as the majority does, that the resulting injuries did not exist in the real world, she wrote, is to inhabit a world I don't know.
<!-- KG-03 ✓ VERBATIM -->

Congress, she said, is better suited than courts to determine when something causes a harm or a risk of harm in the real world.
<!-- KG-05 ✓ VERBATIM -->

And then she asked the question this film has been walking toward for twenty-seven minutes.
<!-- KG-04 — RECOGNITION. -->

But why is it so speculative that a company in the business of selling credit reports to third parties will in fact sell a credit report to a third party?
<!-- KG-04 ✓ VERBATIM. Motif state 5 lands here: the closed drawer, and one blank slip on the desk above it. -->

She noted, as Justice Thomas had, that nearly twenty-five per cent of the class already had these reports sent to potential creditors.
<!-- KG-06 ✓ VERBATIM ("nearly 25% of the class" / "sent to potential creditors"). The opinions' own phrase is used; the exact percentage is not substituted for it. -->

Now — what did the Supreme Court actually decide? Less than almost anyone remembers.
<!-- ND-01 through ND-06. -->

It did not decide whether TransUnion violated the Fair Credit Reporting Act. The 1,853 keep that claim, and Ramirez keeps all three of his.
<!-- ND-01 · HD-11 · ⛔-02 -->

It did not decide whether the violations were willful. The word appears exactly once in the majority opinion, inside a quotation of the statute, and never in its analysis. The jury's finding on willfulness, and the Ninth Circuit's affirmance of it, were simply not before the Court.
<!-- ND-02 · N9-04 (verified by exhaustive count over the majority span) -->

It did not decide whether the class was properly certified. It sent that question back.
<!-- ND-03 ✓ VERBATIM -->

It did not decide whether the 6,332 could sue in a state court. Justice Thomas raised it. The majority did not answer it.
<!-- ND-04 · TH-08 -->

It did not decide what would have happened in a suit for an injunction rather than damages. The Court's own reasoning reserves that: a material risk of future harm can satisfy concreteness in the context of a claim for injunctive relief to prevent the harm from occurring. This was a claim for money.
<!-- ND-05 ✓ VERBATIM -->

And it set no figure. It did not remit, recalculate or apportion anything. The Supreme Court removed people from claims and sent the case back. The only per-person numbers anyone ever wrote down are the jury's nine hundred and eighty-four dollars and twenty-two cents, its six thousand three hundred and fifty-three dollars and eight cents, and the Ninth Circuit's reduced three thousand nine hundred and thirty-six dollars and eighty-eight cents — all of them as awarded or as ordered reduced. None of them as received.
<!-- MN-11 · MN-04 · MN-06 · ⛔-03 · ⛔-04 -->

One more thing about what the case is not. It is about one add-on product at one company. It is not about credit scores, and it is not about Equifax or Experian, neither of which is mentioned anywhere in it.
<!-- ND-07 -->

---

## ENDING

【No new facts. R017 — the forecourt with one car gone. R041 — the drawer closed, the room dark,
one window bright. R095, R096. `BrandEndcard` runs 9.0 s after the last word.】

Two words. A first name and a last name. That was the whole comparison.
<!-- LS-14 ✓ VERBATIM — restated, not new. -->

The record this film is built on ends on the twenty-fifth of June, 2021, with the case on its way back to the Ninth Circuit. What happened after that — whether the 1,853 ever recovered anything, whether the class was certified again, whether it settled — is not in any document we were able to retrieve. So this film ends where the record ends.
<!-- ⛔-12 · ○-04 · ND-06. ⟨OQ-04 SLOT⟩ — film bible §7: if the docket is retrieved, THIS PARAGRAPH is the one that changes, and nothing else in the script does. -->

Eight thousand, one hundred and eighty-five people were told by a credit bureau that their names matched a Treasury list of terrorists and drug traffickers. One thousand, eight hundred and fifty-three of them had that sent to somebody else. Six thousand, three hundred and thirty-two of them were told, by the Supreme Court of the United States, that nothing had happened to them yet.
<!-- MN-02 ✓ · MN-03 ✓ · HD-11 ✓ — all three numbers, restated, no new claim. -->

Most of them, the majority pointed out, did not know.
<!-- HD-10 ✓ -->

Justice Kagan's question is still on the table, and it is a short one. Why is it so speculative that a company in the business of selling credit reports will in fact sell one?
<!-- KG-04 ✓ VERBATIM, shortened for the reprise; the full sentence was spoken in full at 27:10. -->

---

## WHAT I WANTED TO SAY AND COULD NOT

Recorded here so the next revision does not rediscover it.

1. **What happened on remand.** The single question every viewer will ask. CourtListener returned
   HTTP 429 on the research pass and the docket could not be checked (○-04). The ENDING is written
   to stand without it, and the paragraph that would change is marked.
2. **Judge McKeown's reasoning.** Her result is in the script; her reasoning is not, because her
   separate opinion was not read line by line (○-01). She is the most striking figure in the lower
   court and she gets two sentences.
3. **Sandra Jean Cortez's own case.** 617 F.3d 688 was not retrieved (○-03). Everything here comes
   from Justice Thomas summarising it, and it is attributed to him on air. Two dates and a
   reprimand; no scene.
4. **A false-positive rate for name-only screening.** No such figure exists in any document
   retrieved (○-07). "Many false positives" and "could not confirm that a single alert was accurate"
   are the only quantitative-sounding statements available, and neither is a rate. None was invented.
5. **How many of the 8,185 were refused something, like Ramirez was.** Expressly absent from the
   record — ✓ *"there was no evidence regarding whether other class members had experiences similar
   to Ramirez's"* (SR-14). The film does not imply thousands of refused car loans. The **absence** is
   said out loud, because the majority relied on it (HD-10).
6. **Anything about Sergio Ramirez as a person.** A car, a wife, a father-in-law, two letters, a
   lawyer, a cancelled trip and a day in court is the whole of him in the record (⛔-07, ○-05). This
   script adds nothing to it, including the interior life it would be easy to add.
